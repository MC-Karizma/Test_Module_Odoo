# -*- coding: utf-8 -*-
from collections import OrderedDict

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.osv.expression import AND, OR
from datetime import datetime
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


class InstanceCustomerPortal(CustomerPortal):

    def _get_portal_default_domain(self):
        my_user = request.env.user
        return [
            ('create_uid', '=', my_user.id),
        ]

    @http.route('/list', auth='public', website=True)
    def index(self, page=1, sortby=None, filterby=None, search=None, search_in='name', groupby='none', **kw):
        domain = self._get_portal_default_domain()
        searchbar_sortings = {
            'partner': {'label': _('Customer'), 'order': 'partner_id'},
            'name': {'label': _('Name'), 'order': 'name'},
            'odoo_version': {'label': _('Odoo version'), 'order': 'odoo_id'},
        }

        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in Name')},
            'odoo_id': {'input': 'odoo_id', 'label': _('Search in Odoo Version')},
            'limit_date': {'input': 'limit_date', 'label': _('Search in Limit Date')},
            'partner_id': {'input': 'partner_id', 'label': _('Search in Customer')},
        }

        """searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'state': {'input': 'state', 'label': _('State')},
        }"""

        """searchbar_filters = {
            'draft': {'label': _('Draft'), 'domain': [('state', '=', 'Draft')]},
            'submitted': {'label': _('Submitted'), 'domain': [('state', '=', 'Submitted')]},
            'in_process': {'label': _('In process'), 'domain': [('state', '=', 'In process')]},
            'processed': {'label': _('Processed'), 'domain': [('state', '=', 'Processed')]},
        }"""

        """if not filterby:
            filterby = 'draft'
        domain = AND([domain, searchbar_filters[filterby]['domain']])"""

        if not sortby:
            sortby = 'partner'
        order = searchbar_sortings[sortby]['order']

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'name':
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in == 'odoo_id':
                search_domain = OR([search_domain, [('odoo_id', 'ilike', search)]])
            if search_in == 'limit_date':
                if '-' in search:
                    search = search.replace("-", "/")
                search = datetime.strptime(search, '%d/%m/%Y')
                search = search.date()
                search_domain = OR([search_domain, [('limit_date', 'ilike', search)]])
            if search_in == 'partner_id':
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            domain = AND([domain, search_domain])

        instances = request.env['kzm.instance.request'].sudo().search(domain, order=order)

        instance_count = request.env['kzm.instance.request'].search_count(domain)
        pager = portal_pager(
            url="/list",
            url_args={'sortby': sortby, 'search_in': search_in,
                      'search': search},
            total=instance_count,
            page=page,
            step=self._items_per_page
        )

        # Group By
        """if groupby != 'none':
            grouped_instances = [request.env['kzm.instance.request'].concat(*g) for k, g in
                                 groupbyelem(instances, itemgetter(searchbar_groupby[groupby]['input']))]
        else:
            grouped_instance = [instances]"""

        return request.render('kzm_instance_creation_portal.list_instance_portal',
                              {'instances': instances, 'page_name': 'instance',
                               'searchbar_sortings': searchbar_sortings,
                               'sortby': sortby,
                               #'searchbar_groupby': searchbar_groupby,
                               #'groupby': groupby,
                               #'grouped_instance': grouped_instance,
                               'search_in': search_in,
                               'search': search,
                               'searchbar_inputs': searchbar_inputs,
                               'pager': pager,
                               # 'searchbar_filters': searchbar_filters,
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

    def _prepare_home_portal_values(self, counters):
        values = super(InstanceCustomerPortal, self)._prepare_home_portal_values(counters)
        create_id = http.request.env.context.get('uid')
        instances_count = request.env['kzm.instance.request'].sudo().search_count([('create_uid', '=', create_id)])
        values.update({'instances_count': instances_count, })
        return values


#class KzmInstanceCreationPortal(http.Controller):