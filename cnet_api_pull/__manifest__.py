{
    'name': 'Cnet Pull API',
    'version': '14.0.0',
    'summary': 'This is to pool sales data from Cnet ERP ',
    'sequence': 15,
    'description': "",
    'category': 'Tools',
    'depends': [
        "sale",
        "contacts",
        "hr"
    ],
    'data': [
        'views/extend.xml',
        'views/form.xml',
        'security/ir.model.access.csv'
    ],
    # 'data': [
    #     'data/sales_extend.xml'
    # ],
    'installable': True,
    
    'application': True,
    'auto_install': False,
}