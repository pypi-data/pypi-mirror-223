# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class OutsourceWorkRateDetail(models.Model):
    _name = "outsource_work_rate_detail"
    _description = "Outsource Work Rate Detail"

    rate_id = fields.Many2one(
        comodel_name="outsource_work_rate",
        string="Rate",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        ondelete="restrict",
    )
    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Price List",
        required=True,
        ondelete="restrict",
    )
