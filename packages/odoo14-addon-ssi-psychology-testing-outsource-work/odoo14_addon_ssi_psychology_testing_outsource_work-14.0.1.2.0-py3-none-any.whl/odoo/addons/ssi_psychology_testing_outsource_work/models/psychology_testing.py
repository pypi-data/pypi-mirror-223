# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class PsychologyTesting(models.Model):
    _name = "psychology_testing"
    _inherit = [
        "psychology_testing",
        "mixin.outsource_work_object",
    ]
    _outsource_work_create_page = True
    _work_log_page_xpath = "//page[@name='note']"
    _work_log_template_position = "before"

    outsource_work_id = fields.Many2one(
        string="# Outsource Work",
        comodel_name="outsource_work",
        readonly=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )

    @ssi_decorator.post_done_action()
    def _create_outsource_work(self):
        self.ensure_one()
        if self.outsource_work_id:
            return True

        if not self.analytic_account_id:
            return True

        OutsourceWork = self.env["outsource_work"]
        ctx = {"outsource_work_model": self._name}
        temp_record = OutsourceWork.with_context(ctx).new(
            self._prepare_create_outsource_work()
        )

        temp_record = self._compute_outsource_work_onchange(temp_record)
        values = temp_record._convert_to_write(temp_record._cache)
        outsource_work = OutsourceWork.create(values)
        self.write({"outsource_work_id": outsource_work.id})

        for observer in self.observer_ids:
            observer._create_outsource_work()

    @ssi_decorator.post_cancel_action()
    def _delete_outsource_work(self):
        if not self.outsource_work_id:
            return True

        outsource_work = self.outsource_work_id
        self.write({"outsource_work_id": False})
        outsource_work.unlink()

        for observer in self.observer_ids:
            observer._delete_outsource_work()

    def _get_outsource_work_model_id(self):
        self.ensure_one()
        Model = self.env["ir.model"]
        criteria = [("model", "=", self._name)]
        return Model.search(criteria)[0].id

    def _compute_outsource_work_onchange(self, temp_record):
        temp_record.onchange_usage_id()
        temp_record.onchange_pricelist_id()
        temp_record.onchange_account_id()
        temp_record.onchange_uom_id()
        temp_record.onchange_pricelist_id()
        temp_record.onchange_price_unit()

        return temp_record

    def _get_partner(self):
        self.ensure_one()
        result = False
        # TODO: Raise exception when False
        if (
            self.tester_id.partner_id.id
            != self.tester_id.partner_id.commercial_partner_id.id
            and self.tester_id.partner_id.contact_id
        ):
            result = self.tester_id.partner_id.contact_id
        elif (
            self.tester_id.partner_id.id
            == self.tester_id.partner_id.commercial_partner_id.id
        ):
            result = self.tester_id.partner_id

        if not result:
            error_msg = _("No partner defined")
            raise UserError(error_msg)

        return result

    def _prepare_create_outsource_work(self):
        return {
            "partner_id": self._get_partner().id,
            "date": fields.Date.today(),
            "model_id": self._get_outsource_work_model_id(),
            "type_id": self.test_id.tester_outsource_work_type_id.id,
            "product_id": self.test_id.tester_outsource_work_type_id.product_id.id,
            "analytic_account_id": self.analytic_account_id.id,
            "work_object_id": self.id,
        }
