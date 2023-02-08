# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string="Property", required=True)
