
odoo.define("sale_line_detail_widget.DetailWidget", function (require) {
    "use strict";

    const Widget = require("web.Widget");
    const widgetRegistry = require("web.widget_registry");

    const DetailWidget = Widget.extend({
        template: "sale_line_detail_widget.detail_icon",

        events: {
            "click .fa-info-circle": "_onClick",
        },

        init(parent, params) {
            this.data = params.data;
            this._super(parent);
        },

        updateState(state) {
            const candidate = state.data[this.getParent().currentRow];
            if (candidate) {
                this.data = candidate.data;
                this.renderElement();
            }
        },

        _onClick(ev) {
            ev.stopPropagation();

            const productId = this.data.product_id?.data?.id;
            if (!productId) {
                return;
            }

            this.do_action("report_search_extend.action_sale_line_detail_wizard", {
                additional_context: {
                    default_product_id: productId,
                },
            });
        }


    });

    widgetRegistry.add("sale_line_detail_widget", DetailWidget);
});
