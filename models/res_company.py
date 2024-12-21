from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    # UVT Value field for the company model
    uvt_value_tax = fields.Float(string="UVT Value")
