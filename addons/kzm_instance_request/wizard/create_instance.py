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
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer")
    odoo_id = fields.Many2one(comodel_name="odoo.version", string="Odoo version")
    tl = fields.Many2one(comodel_name="hr.employee", string="Employee")
    limit_date = fields.Date(string="Limit date", tracking=True)
    url = fields.Char(string="URL")

    def _default_purchase_order(self):
        return self.env['sale.order'].browse(self._context.get('active_ids'))

    purchase_order = fields.Many2many(comodel_name="sale.order", string="Purchase order", required=True,
                                      default=_default_purchase_order)

    def action_save(self):

        if int(self.cpu) < 0 or int(self.ram) < 0 or int(self.disk) < 0:
            raise ValidationError(_("You can't request instances with zero performance!"))
        for x in range(len(self.purchase_order)):
            self.env['kzm.instance.request'].create({'cpu': self.cpu, 'ram': self.ram, 'disk': self.disk,
                                                     'partner_id': self.partner_id.id, 'odoo_id': self.odoo_id.id,
                                                     'tl_id': self.tl.id, 'limit_date': self.limit_date,
                                                     'url': self.url})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Instances',
            'res_model': 'kzm.instance.request',
            'domain': [('tl_id', '=', self.tl.name)],
            'view_mode': 'tree',
            'target': 'current',
        }
