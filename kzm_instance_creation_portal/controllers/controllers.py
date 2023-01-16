# -*- coding: utf-8 -*-
from collections import OrderedDict

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.osv.expression import AND


class InstanceCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(InstanceCustomerPortal, self)._prepare_home_portal_values(counters)
        create_id = http.request.env.context.get('uid')
        instances_count = request.env['kzm.instance.request'].sudo().search_count([('create_uid', '=', create_id)])
        values.update({'instances_count': instances_count, })
        return values


class KzmInstanceCreationPortal(http.Controller):
    def _get_portal_default_domain(self):
        my_user = request.env.user
        return [
            ('create_uid', '=', my_user.id),
        ]

    @http.route('/list', auth='public', website=True)
    def index(self, sortby=None, filterby=None, **kw):
        domain = self._get_portal_default_domain()
        searchbar_sortings = {
            'partner': {'label': _('Customer'), 'order': 'partner_id'},
            'name': {'label': _('Name'), 'order': 'name'},
            'odoo_version': {'label': _('Odoo version'), 'order': 'odoo_id'},
        }
        """ searchbar_filters = {
            'draft': {'label': _('Draft'), 'domain': [('state', '=', 'Draft')]},
            'submitted': {'label': _('Submitted'), 'domain': [('state', '=', 'Submitted')]},
            'in_process': {'label': _('In process'), 'domain': [('state', '=', 'In process')]},
            'processed': {'label': _('Processed'), 'domain': [('state', '=', 'Processed')]},
        } """

        """         if not filterby:
            filterby = 'draft'
        domain = AND([domain, searchbar_filters[filterby]['domain']]) """

        if not sortby:
            sortby = 'partner'
        order = searchbar_sortings[sortby]['order']

        instances = request.env['kzm.instance.request'].sudo().search(domain, order=order)
        return request.render('kzm_instance_creation_portal.list_instance_portal',
                              {'instances': instances, 'page_name': 'instance',
                               'searchbar_sortings': searchbar_sortings,
                               'sortby': sortby,
                               #'searchbar_filters': searchbar_filters,
                              # 'filterby': filterby
                               })

    @http.route('/form_create_instance', auth='public', website=True)
    def instance_form(self, **kw):
        return request.render('kzm_instance_creation_portal.form_instance_portal', {})

    @http.route('/create/instance', auth='public', website=True)
    def instance_created(self, **kw):
        kw['state'] = 'Submitted'
        request.env['kzm.instance.request'].sudo().create(kw)
        return request.render('kzm_instance_creation_portal.instance_created', {})
