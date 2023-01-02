# -*- coding: utf-8 -*-

from datetime import timedelta, date, datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KzmInstanceRequest(models.Model):
    _name = 'kzm.instance.request'
    _description = 'Request for Proceedings'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string="Designation", tracking=True)
    reference = fields.Char(string="Reference", tracking=True, default=lambda self: _('New'))
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
    treat_duration = fields.Float(string="Treat duration")

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
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('instance.increment') or _('New')
        res = super(KzmInstanceRequest, self).create(vals)
        return res

    def unlink(self):
        for x in self:
            if x.state != 'Draft':
                raise ValidationError(_("You can only delete an instance in \"Draft\" status !"))
            return super(KzmInstanceRequest, x).unlink()

    def write(self, vals):
        if vals.get('limit_date'):
            date_time_obj = datetime.strptime(vals['limit_date'], '%Y-%m-%d')
            d = date_time_obj.date()
            if d < date.today():
                raise ValidationError(_("You cannot set a deadline later than today!"))
        return super(KzmInstanceRequest, self).write(vals)
