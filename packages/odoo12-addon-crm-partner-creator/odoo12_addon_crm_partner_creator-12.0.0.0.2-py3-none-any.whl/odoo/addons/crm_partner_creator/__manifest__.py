# -*- coding: utf-8 -*-
{
    'name': "crm_partner_creator",

    'summary': """
        Create new partner from crm lead metadata
    """,

    'author': "Coopdevs Treball SCCL",
    'website': "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/enhancements/enhancements-crm",

    'category': 'crm',
    'version': '12.0.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm_metadata', 'crm_sale_order_line'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead.xml',
        'views/crm_partner_creator_config.xml'
    ]
}
