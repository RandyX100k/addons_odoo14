from odoo import models,fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def view_details(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Detalle del Producto',
            'res_model': 'sale.order.line.detail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_template_id': self.product_template_id.id,
            }
        }


class SaleOrder(models.Model):
    _inherit = "sale.order"


    resumen_html = fields.Html()