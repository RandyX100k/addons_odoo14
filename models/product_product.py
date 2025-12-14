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

        domain = ['|',
                  ('name', operator, name),
                  ('default_code', operator, name)] + args

        products = self.search(domain, limit=limit)
        return products.name_get()