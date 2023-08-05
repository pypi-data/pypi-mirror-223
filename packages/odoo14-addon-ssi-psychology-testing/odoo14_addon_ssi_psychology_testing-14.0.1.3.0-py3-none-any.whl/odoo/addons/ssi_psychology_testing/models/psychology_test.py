# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyTest(models.Model):
    _name = "psychology_test"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Test"

    allowed_tester_ids = fields.Many2many(
        string="Allowed Testers",
        comodel_name="res.users",
        relation="rel_psychology_test_2_allowed_tester",
        column1="test_id",
        column2="user_id",
    )
    allowed_observer_ids = fields.Many2many(
        string="Allowed Observers",
        comodel_name="res.users",
        relation="rel_psychology_test_2_allowed_observer",
        column1="test_id",
        column2="user_id",
    )
