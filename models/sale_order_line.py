import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty', 'price_unit')
    def product_id_change(self):
        # Obtener la posición fiscal del cliente
        fiscal_position = self.order_id.fiscal_position_id
        # Obtener el valor de UVT desde la compañía
        uvt_value = self.env.user.company_id.uvt_value

        if fiscal_position:
            # Obtener los impuestos asociados a la posición fiscal
            taxes = fiscal_position.tax_ids
            total_price = 0

            for tax in taxes:
                position_fiscal_tax = self.env['account.fiscal.position.tax'].browse(tax.id)
                tax_record = self.env['account.tax'].browse(position_fiscal_tax.tax_dest_id.id)

                # Verificar si tax_record no existe, uvt_amount no está, o uvt_amount es <= 0
                if not tax_record or not hasattr(tax_record, 'uvt_amount') or tax_record.uvt_amount <= 0:
                    continue

                # Verificar si tax_record no tiene el atributo tax_type
                if not hasattr(tax_record, 'tax_type'):
                    continue
                
                if tax_record.tax_type == 'invoice':
                    for line in self.order_id.order_line:
                        total_price += (line.product_uom_qty * line.price_unit)
                    
                    total_uvt = round(total_price / uvt_value, 1) if uvt_value > 0 else 0.0
                    if total_uvt >= tax_record.uvt_amount:
                        line.tax_id = [(4, tax_record.id)]

                elif tax_record.tax_type == 'product':
                    for line in self.order_id.order_line:
                        price_product = line.product_uom_qty * line.price_unit
                        price_uvt = round(price_product / uvt_value, 1) if uvt_value > 0 else 0.0

                        if price_uvt >= tax_record.uvt_amount:
                            line.tax_id = [(4, tax_record.id)]
