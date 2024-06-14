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
        uvt_value = self.env.user.company_id.uvt_value_tax

        if fiscal_position:
            # Obtener los impuestos asociados a la posición fiscal
            taxes = fiscal_position.tax_ids
            tax_applied = set()  # Conjunto para rastrear los impuestos aplicados a nivel de factura

            for tax in taxes:
                position_fiscal_tax = self.env['account.fiscal.position.tax'].browse(tax.id)
                tax_record = self.env['account.tax'].browse(position_fiscal_tax.tax_dest_id.id)
                total_price = self.order_id.amount_total

                if not tax_record or not hasattr(tax_record, 'uvt_amount') or tax_record.uvt_amount <= 0:
                    continue

                if not hasattr(tax_record, 'tax_type'):
                    continue
                
                if tax_record.tax_type == 'invoice':
                    if tax_record.id in tax_applied:
                        continue
                    
                    total_uvt = (total_price / uvt_value) if uvt_value > 0 else 0.0
                    total_uvt_int = int(total_uvt)
                    uvt_amount_int = int(tax_record.uvt_amount)
                    if total_uvt_int >= uvt_amount_int:
                        for line in self.order_id.order_line:
                            line.tax_id = [(4, tax_record.id)]
                            break
                        tax_applied.add(tax_record.id) 

                if tax_record.tax_type == 'product':
                    for line in self.order_id.order_line:
                        price_product = line.product_uom_qty * line.price_unit
                        price_uvt = round(price_product / uvt_value, 1) if uvt_value > 0 else 0.0

                        if price_uvt >= tax_record.uvt_amount:
                            line.tax_id = [(4, tax_record.id)]
