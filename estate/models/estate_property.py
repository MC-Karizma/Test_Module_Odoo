# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(string="Garden orientation",
                                          selection=[('North', 'North'), ('South', 'South'), ('East', 'East'),
                                                     ('West', 'West')],
                                          help="It is the garden orientation")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(string="State", selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('canceled', 'Canceled')], required=True, copy=False,
                             default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.uid)
    tag_ids = fields.Many2many('estate.property.tag', string="Property tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer")
    total_area = fields.Float(string="Total area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            price = record.offer_ids.mapped('price')
            if len(price) > 0:
                record.best_price = max(price)
            else:
                record.best_price = 0
