{
    'name': "uom_sale",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'data':[
        'views/views.xml',
        'security/ir.model.access.csv',
    ],

    'author': "RutiversoTech",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['stock', 'sale'],


}
