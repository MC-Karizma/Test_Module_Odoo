# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class OdooVersion(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin', 'odoo_version']

    instance_ids = fields.One2many('kzm_instance_request', 'odoo_id', string="Instance")
    instance_count = fields.Integer(string='Instance count', compute='_compute_instance_count')

    def _compute_instance_count(self):
        for rec in self:
            rec.instance_count = len(rec.instance_ids)
