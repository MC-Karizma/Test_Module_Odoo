# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'

    name = fields.Char(string="Name", required=True)
