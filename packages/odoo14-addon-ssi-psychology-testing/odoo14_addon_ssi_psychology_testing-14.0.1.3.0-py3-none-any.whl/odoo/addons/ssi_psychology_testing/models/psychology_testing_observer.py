# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyTestingObserver(models.Model):
    _name = "psychology_testing.observer"
    _description = "Psychology Testing Observer"

    testing_id = fields.Many2one(
        string="# Testing",
        comodel_name="psychology_testing",
        required=True,
        ondelete="cascade",
    )
    observer_id = fields.Many2one(
        string="Observer",
        comodel_name="res.users",
        required=True,
        ondelete="restrict",
    )
