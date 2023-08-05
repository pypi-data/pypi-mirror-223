# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyCaseType(models.Model):
    _name = "psychology.case_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Case Type"

    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        company_dependent=True,
    )
    usage_id = fields.Many2one(
        string="Default Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
    )
    pricelist_ids = fields.Many2many(
        string="Allowed Pricelist",
        comodel_name="product.pricelist",
        relation="resl_psychology_case_type_2_pricelist",
        column1="type_id",
        column2="pricelist_id",
    )
    analytic_group_id = fields.Many2one(
        string="Analytic Group",
        comodel_name="account.analytic.group",
    )
    auto_create_aa = fields.Boolean(
        string="Auto Create AA",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        relation="rel_psychology_case_type_2_product",
        column1="type_id",
        column2="product_id",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_psychology_case_type_2_product_categ",
        column1="type_id",
        column2="product_id",
    )
