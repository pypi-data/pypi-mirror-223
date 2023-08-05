# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyTest(models.Model):
    _name = "psychology_test"
    _inherit = [
        "psychology_test",
    ]
    _description = "Psychology Test"

    tester_outsource_work_type_id = fields.Many2one(
        string="Tester Outsource Work Type",
        comodel_name="outsource_work_type",
    )
    observer_outsource_work_type_id = fields.Many2one(
        string="Observer Outsource Work Type",
        comodel_name="outsource_work_type",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
