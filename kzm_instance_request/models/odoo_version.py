# -*- coding: utf-8 -*-


from odoo import models, fields, api


class OdooVersion(models.Model):
    _name = 'odoo.version'
    _description = 'Version of odoo'

    name = fields.Char("Version")


