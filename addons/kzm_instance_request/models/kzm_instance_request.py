# -*- coding: utf-8 -*-

from datetime import timedelta, date
from odoo import models, fields, api


class KzmInstanceRequest(models.Model):
    _name = 'kzm.instance.request'
    _description = 'Request for Proceedings'

    name = fields.Char(string="Designation")
    address_ip = fields.Char(string="IP Address")
    active = fields.Boolean(string="Active", default=True)
    cpu = fields.Char(string="CPU")
    ram = fields.Char(string="RAM")
    disk = fields.Char(string="DISK")
    url = fields.Char(string="URL")
    state = fields.Selection(
        [('Draft', 'Draft'), ('Submitted', 'Submitted'), ('In process', 'In process'), ('Processed', 'Processed')],
        default='Draft', string="State")
    limit_date = fields.Date(string="Limit date")
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
