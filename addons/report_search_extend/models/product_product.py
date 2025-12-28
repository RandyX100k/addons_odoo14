from  odoo import  models , api
class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        search_native = self.env['ir.config_parameter'].sudo().get_param(
            'report_search_extend.search_native'
        )

        if not search_native or search_native == 'False':
            return super().name_search(
                name=name,
                args=args,
                operator=operator,
                limit=limit
            )

        domain = [
                     '|',
                     ('name', operator, name),
                     ('default_code', operator, name),
                 ] + args

        products = self.search(domain, limit=limit)


        order_id = self.env.context.get('order_id')
        if not order_id:
            return products.name_get()

        order = self.env['sale.order'].browse(order_id)
        if not order.exists() or not order.warehouse_id:
            return products.name_get()

        location = order.warehouse_id.lot_stock_id

        quants = self.env['stock.quant'].read_group(
            domain=[
                ('product_id', 'in', products.ids),
                ('location_id', 'child_of', location.id),
            ],
            fields=['product_id', 'quantity:sum'],
            groupby=['product_id'],
        )

        qty_by_product = {
            q['product_id'][0]: q['quantity']
            for q in quants
        }

        result = []
        for product in products:
            qty = qty_by_product.get(product.id, 0.0)
            result.append(
                (product.id, f"{product.display_name} (Stock: {int(qty)})")
            )

        return result