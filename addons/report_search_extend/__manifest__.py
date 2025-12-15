# -*- coding: utf-8 -*-
{
    'name': "report_search_extend",



    'author': "RutiversoTech",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base' , 'report_search','bitodoo_product_attr' ,'product' , 'stock'],

    'data': [
        'views/res_config_settings.xml',
        'views/product_product.xml',
        'views/sale_order.xml',
        'wizard/wizard_view.xml',
        'security/ir.model.access.csv',
    ],



}
