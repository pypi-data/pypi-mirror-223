# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PsychologyTestingClient(models.Model):
    _name = "psychology_testing.client"
    _description = "Psychology Testing Client"

    testing_id = fields.Many2one(
        string="# Testing",
        comodel_name="psychology_testing",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", False),
            ("parent_id", "=", False),
        ],
        required=True,
        ondelete="restrict",
    )
    case_id = fields.Many2one(
        string="# Case",
        comodel_name="psychology.case",
        required=False,
        ondelete="restrict",
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_case_id(self):
        self.case_id = False
