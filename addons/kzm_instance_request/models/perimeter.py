# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Perimeter(models.Model):
    _name = 'perimeter'
    _description = 'Perimeter'

    name = fields.Char(string="Name")


