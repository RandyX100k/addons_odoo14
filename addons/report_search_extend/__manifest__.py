# -*- coding: utf-8 -*-
{
    'name': "report_search_extend",



    'author': "RutiversoTech",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base' ,  'product' , 'sale_management','stock'],

    'data': [
        'views/res_config_settings.xml',
        'views/sale_order.xml',
        'views/assets.xml',
        'wizard/wizard_view.xml',
        'security/ir.model.access.csv'
        'views/product_product.xml',
    ],

    "qweb": ["static/src/xml/widget_order.xml"],



}
