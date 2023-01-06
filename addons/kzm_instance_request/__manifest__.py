# -*- coding: utf-8 -*-
{
    'name': "Instance",

    'summary': "Instance management",

    'description': "This module has been created to help in the request of instance",

    'author': "Mamady",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management',
    'version': '1.O.O',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'portal', 'contacts', 'sale_management', 'hr', 'sale'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/create_instance_wizard.xml',
        'data/activity.xml',
        'data/data_sequence.xml',
        'data/kzm_instance_request_mail_template.xml',
        'data/kzm_instance_request_mail_template2.xml',
        'views/kzm_instance_request_views.xml',
        'views/employee.xml',
        'views/devis.xml',
        'views/odoo_version_views.xml',
        'views/perimeter.xml',
        'data/data_odoo_version.xml',
        'data/data_perimeter.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': 'False',
    'sequence': -100,
}
