# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyCaseTax(models.Model):
    _name = "psychology.case_tax"
    _description = "Psychology Case Tax"

    case_id = fields.Many2one(
        string="# Case",
        comodel_name="psychology.case",
        required=True,
        ondelete="cascade",
    )
    tax_id = fields.Many2one(
        string="Tax",
        comodel_name="account.tax",
        required=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="case_id.currency_id",
    )
    base_amount = fields.Monetary(
        string="Base",
        currency_field="currency_id",
        required=True,
    )
    tax_amount = fields.Monetary(
        string="Tax",
        currency_field="currency_id",
        required=True,
    )
    manual = fields.Boolean(
        string="Manual",
        default=True,
    )
    account_move_line_id = fields.Many2one(
        string="Journal Item",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
    )

    def _create_aml(self):
        self.ensure_one()
        AML = self.env["account.move.line"]
        aml = AML.with_context(check_move_validity=False).create(
            self._prepare_aml_data()
        )
        self.write(
            {
                "account_move_line_id": aml.id,
            }
        )

    def _prepare_aml_data(self):
        self.ensure_one()
        case = self.case_id
        aa_id = case.analytic_account_id and case.analytic_account_id.id or False
        debit, credit, amount_currency = self._get_aml_amount(case.currency_id)
        return {
            "move_id": case.move_id.id,
            "name": self.tax_id.name,
            "partner_id": case.partner_id.id,
            "account_id": self.account_id.id,
            "debit": debit,
            "credit": credit,
            "currency_id": case.currency_id.id,
            "amount_currency": amount_currency,
            "analytic_account_id": aa_id,
        }

    def _get_aml_amount(self, currency):
        self.ensure_one()
        debit = credit = amount = amount_currency = 0.0
        case = self.case_id
        move_date = case.date

        amount_currency = self.tax_amount
        amount = currency.with_context(date=move_date).compute(
            amount_currency,
            case.currency_id,
        )

        if amount < 0.0:
            debit = abs(amount)
        else:
            credit = abs(amount)

        return debit, credit, amount_currency
