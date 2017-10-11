# -*- coding: utf-8 -*-
{
    'name': "Lottery",

    'summary': """
        Lottery Management Software""",

    'description': """
        This Lottery Management Module is used to sell lotteries and manage them all operation from one app.
    """,

    'author': "Ahmed Hassan",

    'website': "http://www.websoly.com",

    'category': 'Lottery',

    'application': True,
    'auto_install': False,
    'version': '0.1',
    'depends': ['inputmask_widget'],
    'data': [
        'views/views.xml',
    ],
    'qweb': ['static/src/xml/dashboard.xml'],
}
