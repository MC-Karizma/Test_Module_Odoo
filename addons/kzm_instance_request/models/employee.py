# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Employee(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin', 'hr.employee']

    instance_ids = fields.One2many('kzm_instance_request', 'tl_id ', string="Instance", tracking=True)
    instance_count = fields.Integer(string='Instance count', compute='_compute_instance_count')

    def _compute_instance_count(self):
        for rec in self:
            rec.instance_count = len(rec.instance_ids)
