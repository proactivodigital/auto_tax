{
    'name': 'Account Tax automatically',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Add custom fields to account tax',
    'description': 'This module adds custom fields to the account.tax model.',
    'author': 'Cristian Berrio',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'views/account_tax_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}