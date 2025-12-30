from odoo import models, api

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

        warehouse_id = self.env.context.get('warehouse_id')
        if not warehouse_id:
            return products.name_get()

        warehouse = self.env["stock.warehouse"].browse(warehouse_id)
        location = warehouse.lot_stock_id

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
            if product.default_code:
                display = f"[{product.default_code}] {product.name} ({qty:.2f} {product.uom_id.name})"
            else:
                display = f"{product.name} ({qty:.2f} uds)"
            result.append((product.id, display))

        return result



class ProductTemplate(models.Model):
    _inherit = "product.product"

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        search_native = self.env['ir.config_parameter'].sudo().get_param(
            'report_search_extend.search_native'
        )

        if not search_native or search_native == 'False':
            return super(ProductTemplate, self).name_search(
                name=name, args=args, operator=operator, limit=limit
            )

        domain = [
            '|',
            ('name', operator, name),
            ('default_code', operator, name),
        ] + args

        templates = self.search(domain, limit=limit)

        result = []
        for tmpl in templates:
            ref = f"[{tmpl.default_code}] " if tmpl.default_code else ""
            display = f"{ref}{tmpl.name}"
            
            result.append((tmpl.id, display))

        return result