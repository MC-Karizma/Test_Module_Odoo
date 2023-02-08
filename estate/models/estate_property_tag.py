# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'

    name = fields.Char(string="Name", required=True)
