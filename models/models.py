from odoo import  models , fields


class ResConfiSettings(models.TransientModel):
    _inherit = "res.config.settings"


    search_native = fields.Boolean(string="Búsqueda nativa?",
                                   config_parameter="report_search_extend.search_native")