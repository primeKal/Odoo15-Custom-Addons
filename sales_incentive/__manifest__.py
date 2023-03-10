{
    'name': 'Sales Incentiive',
    'version': '14.0.0',
    'summary': 'Sales Incentive for Sales Team',
    'sequence': 15,
    'description': "",
    'category': 'Tools',
    'depends': [
        'sale_management',
        'crm'
    ],
    'data': [
        'views/form.xml',
        'security/ir.model.access.csv',
        'views/models.xml',
        'views/res_config_settings_views.xml'
    ],
    # 'data': [
    #     'data/sales_extend.xml'
    # ],
    'installable': True,
    'application': True,
    'auto_install': False,
}