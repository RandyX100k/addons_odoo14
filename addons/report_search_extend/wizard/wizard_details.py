from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderLineDetailWizard(models.TransientModel):
    _name = 'sale.order.line.detail.wizard'
    _description = 'Detalle de Producto'

    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        readonly=True
    )

    detail_html = fields.Html(
        string="Detalle",
        compute='_compute_detail_html',
        sanitize=False
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        product_id = self.env.context.get('default_product_id')
        if not product_id:
            raise UserError("No se pudo determinar el producto.")

        res['product_id'] = product_id
        return res

    @api.depends('product_id')
    def _compute_detail_html(self):
        Warehouse = self.env['stock.warehouse']
        Pricelist = self.env['product.pricelist']
        Quant = self.env['stock.quant']

        warehouses = Warehouse.search([])
        pricelists = Pricelist.search([])

        for wiz in self:
            if not wiz.product_id:
                wiz.detail_html = ""
                continue

            product = wiz.product_id

            html = """
            <div class="o_boxed">
                <h4>Precios por Lista</h4>
                <table class="table table-sm table-bordered">
                    <thead>
                        <tr>
                            <th>Lista de Precio</th>
                            <th>Precio</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            for pricelist in pricelists:
                price = pricelist.get_product_price(
                    product,
                    1.0,
                    self.env.user.partner_id
                )

                html += f"""
                    <tr>
                        <td>{pricelist.name}</td>
                        <td>{price:.2f}</td>
                    </tr>
                """

            html += """
                    </tbody>
                </table>

                <h4 class="mt-2">Stock por Almacén</h4>
                <table class="table table-sm table-bordered">
                    <thead>
                        <tr>
                            <th>Almacén</th>
                            <th>Stock</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            for wh in warehouses:
                location = wh.lot_stock_id
                qty = sum(
                    Quant.search([
                        ('product_id', '=', product.id),
                        ('location_id', 'child_of', location.id)
                    ]).mapped('quantity')
                )

                html += f"""
                    <tr>
                        <td>{wh.name}</td>
                        <td>{qty}</td>
                    </tr>
                """

            html += """
                    </tbody>
                </table>
            </div>
            """

            wiz.detail_html = html
