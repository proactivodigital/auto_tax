from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # UVT Value field, related to the company's UVT value setting
    uvt_value_tax = fields.Float(string="UVT Value", related='company_id.uvt_value_tax', readonly=False)
