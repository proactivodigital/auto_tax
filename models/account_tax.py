from odoo import models, fields

class AccountTax(models.Model):
    _inherit = 'account.tax'

    tax_type = fields.Selection([
        ('invoice', 'Factura'),
        ('product', 'Producto')],
        string='Tipo de Impuesto')

    uvt_amount = fields.Integer(string='Cantidad de UVT')