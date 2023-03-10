{
    'name': 'Dynamic Check Printing',
    'version': '14.0.0',
    'summary': 'Used to create a non standard foam',
    'sequence': 15,
    'description': "",
    'category': 'Tools',
    'depends': [
        'account_accountant'
    ],
    'data': [
        'views/form.xml',
        'security/ir.model.access.csv',
        'reports/report.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    #     'assets': {
    #     'web.assets_backend': [
    #        'dynamic_check_print/static/src/js/cordinate.js',
    #        'dynamic_check_print/static/src/xml/check_template.xml'
    #     ],
    #         'web.assets_qweb': [
    #     'dynamic_check_print/static/src/xml/check_template.xml',
    # ],
    # }
}