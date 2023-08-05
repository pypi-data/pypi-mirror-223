# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PsychologyServiceType(models.Model):
    _name = "psychology.service_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Service Type"
