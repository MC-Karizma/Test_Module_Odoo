# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Employee(models.Model):
    _inherit = 'hr.employee'

    instance_ids = fields.One2many(comodel_name='kzm.instance.request', inverse_name='tl_id', string="Instance",
                                   tracking=True)
    instance_count = fields.Integer(string='Instance count', compute='_compute_instance_count')

    @api.depends('instance_ids')
    def _compute_instance_count(self):
        for rec in self:
            rec.instance_count = len(rec.instance_ids)
