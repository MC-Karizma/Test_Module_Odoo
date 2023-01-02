# -*- coding: utf-8 -*-
{
    'name': "kzm_instance_request",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mamady",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management',
    'version': '1.O.O',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/activity.xml',
        'data/data_sequence.xml',
        'data/kzm_instance_request_mail_template.xml',
        'data/kzm_instance_request_mail_template2.xml',
        'views/kzm_instance_request_views.xml',
        'views/odoo_version_views.xml',
        'data/data_odoo_version.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': 'True',
    'sequence': -100,
}
