# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class CreateInstance(models.Model):
    _name = "create.instance.wizard"
    _description = 'Request instance wizard'

    cpu = fields.Char(string="CPU")
    ram = fields.Char(string="RAM")
    disk = fields.Char(string="DISK")
    tl_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    limit_date = fields.Date(string="Limit date")
    url = fields.Char(string="URL")
    tl_id = fields.Many2one(comodel_name='hr.employee', string="Employee")

    def _default_purchase_order(self):
        return self.env['sale.order'].browse(self._context.get('active_ids'))

    purchase_ids = fields.Many2many(comodel_name="sale.order", string="Sale order", required=True,
                                    default=_default_purchase_order)

    def action_save(self):
        ids = []

        if int(self.cpu) <= 0 or int(self.ram) <= 0 or int(self.disk) <= 0:
            raise ValidationError(_("You can't request instances with zero performance!"))
        for x in self.purchase_ids:
            val = self.env['kzm.instance.request'].create({'cpu': self.cpu, 'ram': self.ram, 'disk': self.disk,
                                                           'tl_id': self.tl_id,
                                                           'limit_date': self.limit_date,
                                                           'url': self.url, 'partner_id': x.partner_id.id})
            ids.append(val.id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Instances',
            'res_model': 'kzm.instance.request',
            'domain': [('id', '=', ids)],
            'view_mode': 'tree',
            'target': 'current',
        }
