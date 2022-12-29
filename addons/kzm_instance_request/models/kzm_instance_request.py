# -*- coding: utf-8 -*-

from datetime import timedelta, date
from odoo import models, fields, api


class KzmInstanceRequest(models.Model):
    _name = 'kzm.instance.request'
    _description = 'Request for Proceedings'

    name = fields.Char("Designation")
    address_ip = fields.Char("IP Address")
    active = fields.Boolean()
    cpu = fields.Char("CPU")
    ram = fields.Char("RAM")
    disk = fields.Char("DISK")
    url = fields.Char("URL")
    state = fields.Selection([('D', 'Draft'), ('S', 'Submitted'), ('I_P', 'In process'), ('P', 'Processed')],
                             default='B')
    limit_date = fields.Date()
    treat_date = fields.Datetime()
    treat_duration = fields.Float()

    def action_draft(self):
        self.state = "D"

    def action_submitted(self):
        self.state = "S"

    def action_in_process(self):
        self.state = "I_P"

    def action_processed(self):
        self.state = "P"

    def submitted_cron(self):
        element = self.env['kzm.instance.request'].search([('limit_date', '<=', date.today() + timedelta(days=5))])
        for x in element:
            x.state = 'S'
