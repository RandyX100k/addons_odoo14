# -*- coding: utf-8 -*-

from odoo import models, fields, api
from  odoo.exceptions import ValidationError


class Packing(models.Model):
    _name = "packing.product"
    _description = "Paquetes por producto"
    _rec_name = "packing_name"

    product_id = fields.Many2one(
        "product.template",
        string="Producto",
        required=True,
        ondelete="cascade"
    )

    packing_name = fields.Char(string="Paquete", required=True)

    min_qty = fields.Float(
        string="Cantidad mínima",
        required=True,
        default=1
    )

    price_packing = fields.Float(
        string="Precio del paquete",
        required=True
    )

    price_min_discount = fields.Many2one("product.pricelist",string="Precio minimo editable")


class ProductCustom(models.Model):
    _inherit = "product.template"

    packing_ids = fields.One2many(
        "packing.product",
        "product_id",
        string="Paquetes"
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    packing_enable = fields.Boolean(default=False)


    def _get_packing_values(self, product_tmpl, qty):

        if not product_tmpl or not qty:
            return {"packing_enable": False}

        for packing in product_tmpl.packing_ids:
            if qty >= packing.min_qty:
                return {
                    "price_unit": packing.price_packing,
                    "packing_enable": True,
                }

        return {"packing_enable": False}


    def _check_min_price(self):
        for line in self:
            if not line.packing_enable:
                continue

            for packing in line.product_template_id.packing_ids:
                for pricelist in packing.price_min_discount:
                    for item in pricelist.item_ids:
                        if (
                            item.product_tmpl_id == line.product_template_id
                            and line.price_unit < item.fixed_price
                        ):
                            raise ValidationError(
                                "El precio no puede ser menor al permitido"
                            )

    @api.model
    def create(self, vals):
        if vals.get("product_id") and vals.get("product_uom_qty"):
            product = self.env["product.product"].browse(vals["product_id"])
            vals.update(
                self._get_packing_values(
                    product.product_tmpl_id,
                    vals["product_uom_qty"],
                )
            )

        record = super().create(vals)
        record._check_min_price()
        return record

    def write(self, vals):

        res = super().write(vals)

        if any(f in vals for f in ["product_id", "product_uom_qty"]):
            for line in self:
                values = line._get_packing_values(
                    line.product_template_id,
                    line.product_uom_qty,
                )
                super(SaleOrderLine, line).write(values)

        self._check_min_price()
        return res