# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class PsychologyCase(models.Model):
    _name = "psychology.case"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_pricelist",
    ]
    _description = "Psychology Case"
    _approval_from_state = "open"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True

    _statusbar_visible_label = "open,draft,confirm,done"

    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    _create_sequence_state = "open"

    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", False),
            ("parent_id", "=", False),
        ],
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    institution_id = fields.Many2one(
        string="Institution",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", True),
            ("parent_id", "=", False),
        ],
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="psychology.case_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    usage_id = fields.Many2one(
        string="Default Usage",
        related="type_id.usage_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        related="type_id.allowed_product_ids",
        store=False,
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.allowed_product_categ_ids",
        store=False,
    )
    date = fields.Date(
        string="Date Visit",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_due = fields.Date(
        string="Date Due",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    service_ids = fields.One2many(
        string="Services",
        comodel_name="psychology.service",
        inverse_name="case_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        copy=True,
    )
    tax_ids = fields.One2many(
        string="Taxes",
        comodel_name="psychology.case_tax",
        inverse_name="case_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        copy=True,
    )

    @api.depends(
        "service_ids",
        "service_ids.price_subtotal",
        "service_ids.price_tax",
        "service_ids.price_total",
        "tax_ids",
        "tax_ids.tax_amount",
    )
    def _compute_total(self):
        for record in self:
            amount_untaxed = amount_tax = 0.0
            for service in record.service_ids:
                amount_untaxed += service.price_subtotal

            for tax in record.tax_ids:
                amount_tax += tax.tax_amount

            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_untaxed + amount_tax

    amount_untaxed = fields.Monetary(
        string="Untaxed",
        required=False,
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        required=False,
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
    )
    amount_total = fields.Monetary(
        string="Total",
        required=False,
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
    )

    # Accounting
    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    move_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.move",
        readonly=True,
        ondelete="set null",
    )
    receivable_move_line_id = fields.Many2one(
        string="Receivable Journal Item",
        comodel_name="account.move.line",
        readonly=True,
        ondelete="set null",
        copy=False,
    )

    @api.depends(
        "receivable_move_line_id",
        "receivable_move_line_id.matched_debit_ids",
        "receivable_move_line_id.matched_credit_ids",
    )
    def _compute_reconciled(self):
        for record in self:
            result = False
            if record.receivable_move_line_id.reconciled:
                result = True
            record.reconciled = result

    reconciled = fields.Boolean(
        string="Reconciled",
        compute="_compute_reconciled",
        store=True,
    )

    @api.depends(
        "amount_total",
        "state",
        "receivable_move_line_id",
        "receivable_move_line_id.reconciled",
        "receivable_move_line_id.amount_residual",
        "receivable_move_line_id.amount_residual_currency",
    )
    def _compute_residual(self):
        for document in self:
            realized = 0.0
            residual = document.amount_total
            currency = document.currency_id
            if document.receivable_move_line_id:
                move_line = document.receivable_move_line_id
                if not currency:
                    residual = move_line.amount_residual
                else:
                    residual = move_line.amount_residual_currency
                realized = document.amount_total - residual
            document.amount_realized = realized
            document.amount_residual = residual

    amount_realized = fields.Monetary(
        string="Paid",
        compute="_compute_residual",
        store=True,
        currency_field="currency_id",
    )
    amount_residual = fields.Monetary(
        string="Residual",
        compute="_compute_residual",
        store=True,
        currency_field="currency_id",
    )

    # Analytic
    auto_create_aa = fields.Boolean(
        string="Auto Create AA",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    analytic_group_id = fields.Many2one(
        string="Analytic Group",
        comodel_name="account.analytic.group",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    @api.model
    def _get_policy_field(self):
        res = super(PsychologyCase, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "open_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "type_id",
    )
    def onchange_receivable_journal_id(self):
        self.receivable_journal_id = False
        if self.type_id:
            self.receivable_journal_id = self.type_id.receivable_journal_id

    @api.onchange(
        "type_id",
    )
    def onchange_receivable_account_id(self):
        self.receivable_account_id = False
        if self.type_id:
            self.receivable_account_id = self.type_id.receivable_account_id

    @api.onchange(
        "type_id",
    )
    def onchange_auto_create_aa(self):
        self.auto_create_aa = self.type_id.auto_create_aa

    @api.onchange(
        "type_id",
    )
    def onchange_analytic_group_id(self):
        self.analytic_group_id = False
        if self.type_id:
            self.analytic_group_id = self.type_id.analytic_group_id

    @ssi_decorator.post_done_action()
    def _post_done_acion_10_create_invoice(self):
        self.ensure_one()
        if self.auto_create_aa and not self.analytic_account_id:
            self._create_analytic_account()
        elif self.auto_create_aa and self.analytic_account_id:
            self._update_analytic_account()

    def _create_analytic_account(self):
        self.ensure_one()
        AA = self.env["account.analytic.account"]
        aa = AA.create(self._prepare_create_analytic_account())
        self.write({"analytic_account_id": aa.id})

    def _update_analytic_account(self):
        self.ensure_one()
        self.analytic_account_id.write(self._prepare_update_analytic_account())

    def _prepare_create_analytic_account(self):
        self.ensure_one()
        return {
            "name": self.name,
            "partner_id": self.partner_id.id,
            "group_id": self.analytic_group_id and self.analytic_group_id.id or False,
        }

    def _prepare_update_analytic_account(self):
        self.ensure_one()
        return {
            "name": self.name,
            "partner_id": self.partner_id.id,
            "group_id": self.analytic_group_id and self.analytic_group_id.id or False,
        }

    @ssi_decorator.post_done_action()
    def _post_done_acion_20_create_aml(self):
        self.ensure_one()
        move = (
            self.env["account.move"]
            .with_context(check_move_validity=False)
            .create(self._prepare_account_move_data())
        )
        self.write(
            {
                "move_id": move.id,
            }
        )
        self._create_receivable_aml()
        self._create_service_aml()
        self._create_tax_aml()
        self.move_id.action_post()

    def _create_receivable_aml(self):
        self.ensure_one()
        AML = self.env["account.move.line"]
        aml = AML.with_context(check_move_validity=False).create(
            self._prepare_receivable_aml_data()
        )
        self.write(
            {
                "receivable_move_line_id": aml.id,
            }
        )

    def _prepare_receivable_aml_data(self):
        self.ensure_one()
        debit, credit, amount_currency = self._get_receivable_amount(self.currency_id)
        data = {
            "name": self.name,
            "move_id": self.move_id.id,
            "partner_id": self.partner_id.id,
            "account_id": self.receivable_account_id.id,
            "debit": debit,
            "credit": credit,
            "currency_id": self.currency_id.id,
            "amount_currency": amount_currency,
            "date_maturity": self.date_due,
        }
        return data

    def _get_receivable_amount(self, currency):
        self.ensure_one()
        debit = credit = amount = amount_currency = 0.0
        move_date = self.date

        amount_currency = self.amount_total
        amount = currency.with_context(date=move_date).compute(
            amount_currency,
            self.company_id.currency_id,
        )

        if amount > 0.0:
            debit = abs(amount)
        else:
            credit = abs(amount)

        return debit, credit, amount_currency

    def _create_service_aml(self):
        self.ensure_one()
        for service in self.service_ids:
            service._create_aml()

    def _create_tax_aml(self):
        self.ensure_one()
        for service in self.tax_ids:
            service._create_aml()

    def _disconnect_invoice(self):
        self.ensure_one()
        self.write(
            {
                "invoice_id": False,
            }
        )

    def _get_receivable_journal(self):
        self.ensure_one()
        return self.receivable_journal_id

    def _get_receivable_account(self):
        self.ensure_one()
        return self.receivable_account_id

    def _prepare_account_move_data(self):
        self.ensure_one()
        journal = self._get_receivable_journal()
        return {
            "date": self.date,
            "name": self.name,
            "journal_id": journal.id,
            "ref": self.name,
        }

    @ssi_decorator.post_cancel_action()
    def _post_delete_acion_10_delete_invoice(self):
        self.ensure_one()
        if self.move_id:
            invoice = self.move_id
            self.write(
                {
                    "move_id": False,
                }
            )
            invoice.with_context(force_delete=True).unlink()

    def action_compute_tax(self):
        for record in self:
            record._recompute_tax()

    def _recompute_tax(self):
        self.ensure_one()
        taxes_grouped = self.get_taxes_values()
        self.tax_ids.unlink()
        tax_lines = []
        for tax in taxes_grouped.values():
            tax_lines.append((0, 0, tax))
        self.write({"tax_ids": tax_lines})

    def get_taxes_values(self):
        tax_grouped = {}
        cur = self.currency_id
        round_curr = cur.round
        for service in self.service_ids:
            price_unit = service.price_unit
            taxes = service.tax_ids.compute_all(price_unit, cur, service.quantity)[
                "taxes"
            ]
            for tax in taxes:
                val = self._prepare_tax_line_vals(service, tax)
                key = self.get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                    tax_grouped[key]["base_amount"] = round_curr(val["base_amount"])
                else:
                    tax_grouped[key]["tax_amount"] += val["tax_amount"]
                    tax_grouped[key]["base_amount"] += round_curr(val["base_amount"])
        return tax_grouped

    def get_grouping_key(self, tax_line):
        self.ensure_one()
        return str(tax_line["tax_id"]) + "-" + str(tax_line["account_id"])

    def _prepare_tax_line_vals(self, line, tax):
        vals = {
            "case_id": self.id,
            "tax_id": tax["id"],
            "tax_amount": tax["amount"],
            "base_amount": tax["base"],
            "manual": False,
            "account_id": tax["account_id"],
        }
        return vals
