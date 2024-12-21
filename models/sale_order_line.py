import logging
from odoo import models, fields, api

# Setting up logging for this module
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Triggered when any of these fields change: product_id, product_uom_qty, or price_unit
    @api.onchange('product_id', 'product_uom_qty', 'price_unit')
    def product_id_change(self):
        # Retrieve the fiscal position of the sale order
        fiscal_position = self.order_id.fiscal_position_id
        # Get the UVT (Unidad de Valor Tributario) value from the company settings
        uvt_value = self.env.user.company_id.uvt_value_tax

        if fiscal_position:
            # Get the taxes associated with the fiscal position
            taxes = fiscal_position.tax_ids
            tax_applied = set()  # A set to track the taxes that are applied at the invoice level

            # Loop through the taxes to determine which ones to apply based on the fiscal position
            for tax in taxes:
                position_fiscal_tax = self.env['account.fiscal.position.tax'].browse(tax.id)
                tax_record = self.env['account.tax'].browse(position_fiscal_tax.tax_dest_id.id)
                total_price = self.order_id.amount_total  # Total price of the sale order

                # Skip if tax record is missing or doesn't have a UVT amount greater than 0
                if not tax_record or not hasattr(tax_record, 'uvt_amount') or tax_record.uvt_amount <= 0:
                    continue

                # Skip if the tax record doesn't have the 'tax_type' field
                if not hasattr(tax_record, 'tax_type'):
                    continue
                
                # Apply the tax if the tax type is 'invoice' and the total price in UVT meets the threshold
                if tax_record.tax_type == 'invoice':
                    if tax_record.id in tax_applied:
                        continue
                    
                    total_uvt = (total_price / uvt_value) if uvt_value > 0 else 0.0
                    total_uvt_int = int(total_uvt)  # Convert to integer to avoid decimal comparison
                    uvt_amount_int = int(tax_record.uvt_amount)  # Get the UVT amount as integer

                    # If the total UVT for the order is greater than or equal to the UVT amount of the tax, apply the tax
                    if total_uvt_int >= uvt_amount_int:
                        for line in self.order_id.order_line:
                            line.tax_id = [(4, tax_record.id)]  # Add the tax to the order line
                            break
                        tax_applied.add(tax_record.id)  # Mark this tax as applied

                # Apply the tax if the tax type is 'product' and the price of the product in UVT meets the threshold
                if tax_record.tax_type == 'product':
                    for line in self.order_id.order_line:
                        price_product = line.product_uom_qty * line.price_unit  # Price of the product in the order line
                        price_uvt = round(price_product / uvt_value, 1) if uvt_value > 0 else 0.0  # Price in UVT

                        # If the price in UVT is greater than or equal to the UVT amount of the tax, apply the tax
                        if price_uvt >= tax_record.uvt_amount:
                            line.tax_id = [(4, tax_record.id)]  # Add the tax to the order line
