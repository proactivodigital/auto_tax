{
    'name': 'Account Tax Automatically',  # Name of the module
    'version': '1.0',  # Version of the module
    'category': 'Accounting',  # Category the module belongs to
    'summary': 'Add custom fields to account tax',  # A brief description of what the module does
    'description': 'This module adds custom fields to the account.tax model.',  # A more detailed description
    'author': 'Cristian Berrio',  # Author of the module
    'depends': ['base', 'account', 'sale'],  # List of modules that this module depends on
    'data': [
        'views/account_tax_views.xml',  # The view that will define the user interface for the custom fields
        
    ],
    'installable': True,  # Indicates that the module can be installed
    'application': False,  # Indicates that this is not a standalone application in Odoo's dashboard
    'license': 'LGPL-3',  # License type, in this case, LGPL-3 (open-source license)
}
