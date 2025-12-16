from odoo import models,fields,api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    display_detail_widget = fields.Boolean(
        string="Mostrar detalle",
        store=False
    )

    @api.onchange('product_id')
    def _onchange_display_detail_widget(self):
        for line in self:
            line.display_detail_widget = bool(line.product_id)
