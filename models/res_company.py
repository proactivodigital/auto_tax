from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    uvt_value_tax = fields.Float(string="UVT Value")