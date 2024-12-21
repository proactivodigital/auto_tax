from odoo import models, fields

class AccountTax(models.Model):
    _inherit = 'account.tax'

    # Type of tax applied, can be either 'invoice' or 'product'
    tax_type = fields.Selection([
        ('invoice', 'Factura'),  # For invoice-related tax
        ('product', 'Producto')  # For product-related tax
    ], string='Tipo de Impuesto')

    # Amount in UVT (Unidad de Valor Tributario) for tax calculation
    uvt_amount = fields.Integer(string='Cantidad de UVT')
