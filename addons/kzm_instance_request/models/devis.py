# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Order(models.Model):
    _inherit = 'sale.order'

    version_odoo_id = fields.Many2one(comodel_name="odoo.version", string="Id odoo version")

    def open_wizard(self):
        action = self.env.ref('kzm_instance_request.purchase_order_action').read()[0]
        return action

