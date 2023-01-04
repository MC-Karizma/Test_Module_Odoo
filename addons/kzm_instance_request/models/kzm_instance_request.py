# -*- coding: utf-8 -*-

from datetime import timedelta, date, datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KzmInstanceRequest(models.Model):
    _name = 'kzm.instance.request'
    _description = 'Request for Proceedings'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string="Designation", tracking=True, default=lambda self: _('New'))
    # reference = fields.Char(string="Reference", tracking=True)
    address_ip = fields.Char(string="IP Address")
    active = fields.Boolean(string="Active", default=True)
    cpu = fields.Char(string="CPU")
    ram = fields.Char(string="RAM")
    disk = fields.Char(string="DISK")
    url = fields.Char(string="URL")
    state = fields.Selection(
        [('Draft', 'Draft'), ('Submitted', 'Submitted'), ('In process', 'In process'), ('Processed', 'Processed')],
        default='Draft', string="State", tracking=True)
    limit_date = fields.Date(string="Limit date", tracking=True)
    treat_date = fields.Datetime(string="Treat date")
    treat_duration = fields.Integer(string="Treat duration", compute='_compute_treat_duration', store=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string="Client")
    tl_id = fields.Many2one(comodel_name='hr.employee', string="Employee")
    tl_user_id = fields.Many2one(comodel_name='hr.employee', string="User on employee")
    odoo_id = fields.Many2one(comodel_name='odoo.version', string="Odoo version")
    perimeters_ids = fields.Many2many(comodel_name='perimeter', string="Perimeters")
    perimeters_count = fields.Integer(string='Perimeters count', compute='_compute_perimeters_count')
    address_id = fields.Many2one(related='tl_id.address_id', string='Address')

    def _compute_perimeters_count(self):
        for rec in self:
            rec.perimeters_count = len(rec.perimeters_ids)

    @api.depends('treat_date')
    def _compute_treat_duration(self):
        for rec in self:
            if rec.treat_date:
                treat = rec.treat_date.date()
                today = date.today()
                rec.treat_duration = (treat - today).days

    _sql_constraints = [
        ('unique_ip_address', 'UNIQUE (address_ip)', 'Ip Address must be unique')
    ]

    def action_draft(self):
        for x in self:
            x.state = "Draft"

    def action_submitted(self):
        for x in self:
            x.state = "Submitted"

    def action_in_process(self):
        for x in self:
            x.state = "In process"

    def action_processed(self):
        for x in self:
            self.state = "Processed"

    def submitted_cron(self):
        element = self.env['kzm.instance.request'].search([('limit_date', '<=', date.today() + timedelta(days=5))])
        for x in element:
            x.action_submitted()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('instance.increment') or _('New')
        res = super(KzmInstanceRequest, self).create(vals)
        return res

    def unlink(self):
        for x in self:
            if x.state != 'Draft':
                raise ValidationError(_("You can only delete an instance in \"Draft\" status !"))
            return super(KzmInstanceRequest, x).unlink()

    def write(self, vals):
        if vals.get('limit_date'):
            name = self.name
            deadline = vals.get('limit_date')
            date_time_obj = datetime.strptime(vals['limit_date'], '%Y-%m-%d')
            d = date_time_obj.date()
            print(self.limit_date)
            if d < date.today():
                raise ValidationError(_("You cannot set a deadline later than today!"))
            users = self.env.ref('kzm_instance_request.group_instance_manager').users
            for user in users:
                self.activity_schedule('kzm_instance_request.gmail_activity_instance', user_id=user.id,
                                       note=f'You have to Process {name}', date_deadline=deadline)
        return super(KzmInstanceRequest, self).write(vals)

    @api.onchange('state')
    def onchange_state(self):
        if self.state:
            if self.state == "Processed":
                self.treat_date = datetime.now()
