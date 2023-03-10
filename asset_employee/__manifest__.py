{
    'name': 'Asset For Employees',
    'version': '14.0.0',
    'summary': 'Asset for Employee',
    'sequence': 15,
    'description': "",
    'category': 'Tools',
    'depends': [
        'contacts',
        'account_asset'
    ],
    'data': [
        'views/form.xml',
        'views/extend.xml'
    ],
    # 'data': [
    #     'data/sales_extend.xml'
    # ],
    'installable': True,
    'application': True,
    'auto_install': False,
}