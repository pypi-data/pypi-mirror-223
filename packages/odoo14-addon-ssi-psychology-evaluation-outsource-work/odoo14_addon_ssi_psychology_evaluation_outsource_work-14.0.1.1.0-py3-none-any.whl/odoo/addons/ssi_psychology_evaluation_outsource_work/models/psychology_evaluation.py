# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class PsychologyEvaluation(models.Model):
    _name = "psychology.evaluation"
    _inherit = [
        "psychology.evaluation",
        "mixin.outsource_work_object",
    ]
    _outsource_work_create_page = True
    _work_log_page_xpath = "//page[@name='evaluation']"
    _work_log_template_position = "after"

    case_id = fields.Many2one(
        string="# Case",
        comodel_name="psychology.case",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    initial_recommendation_outsource_work_id = fields.Many2one(
        string="# Initial Recommendation Outsource Work",
        comodel_name="outsource_work",
        readonly=True,
    )
    evaluation_outsource_work_id = fields.Many2one(
        string="# Evaluation Outsource Work",
        comodel_name="outsource_work",
        readonly=True,
    )
    review_outsource_work_id = fields.Many2one(
        string="# Review Outsource Work",
        comodel_name="outsource_work",
        readonly=True,
    )
    edit_outsource_work_id = fields.Many2one(
        string="# Evaluation Outsource Work",
        comodel_name="outsource_work",
        readonly=True,
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_case_id(self):
        self.case_id = False

    @ssi_decorator.post_done_action()
    def _create_outsource_work(self):
        self.ensure_one()
        self._create_initial_recommendation_outsource_work()
        self._create_evaluation_outsource_work()
        self._create_review_outsource_work()
        self._create_edit_outsource_work()

    def _create_common_outsource_work(
        self, outsource_work_field_name, role_field_name, outsource_work_type_field_name
    ):
        self.ensure_one()
        if getattr(self, outsource_work_field_name):
            return True

        if not getattr(self, role_field_name):
            return True

        OutsourceWork = self.env["outsource_work"]
        ctx = {"outsource_work_model": self._name}
        temp_record = OutsourceWork.with_context(ctx).new(
            self._prepare_create_outsource_work(outsource_work_type_field_name)
        )
        temp_record = self._compute_outsource_work_onchange(temp_record)
        values = temp_record._convert_to_write(temp_record._cache)
        work = OutsourceWork.create(values)
        self.write({outsource_work_field_name: work.id})

    def _create_initial_recommendation_outsource_work(self):
        self.ensure_one()
        outsource_work_field_name = "initial_recommendation_outsource_work_id"
        role_field_name = "initial_recommender_id"
        outsource_work_type_field_name = "initial_recommendation_outsource_work_type_id"
        self._create_common_outsource_work(
            outsource_work_field_name, role_field_name, outsource_work_type_field_name
        )

    def _create_evaluation_outsource_work(self):
        self.ensure_one()
        outsource_work_field_name = "evaluation_outsource_work_id"
        role_field_name = "psychologist_id"
        outsource_work_type_field_name = "evaluation_outsource_work_type_id"
        self._create_common_outsource_work(
            outsource_work_field_name, role_field_name, outsource_work_type_field_name
        )

    def _create_review_outsource_work(self):
        self.ensure_one()
        outsource_work_field_name = "review_outsource_work_id"
        role_field_name = "reviewer_id"
        outsource_work_type_field_name = "review_outsource_work_type_id"
        self._create_common_outsource_work(
            outsource_work_field_name, role_field_name, outsource_work_type_field_name
        )

    def _create_edit_outsource_work(self):
        self.ensure_one()
        outsource_work_field_name = "edit_outsource_work_id"
        role_field_name = "editor_id"
        outsource_work_type_field_name = "edit_outsource_work_type_id"
        self._create_common_outsource_work(
            outsource_work_field_name, role_field_name, outsource_work_type_field_name
        )

    @ssi_decorator.post_cancel_action()
    def _delete_outsource_work(self):
        if self.initial_recommendation_outsource_work_id:
            self.initial_recommendation_outsource_work_id.unlink()

        if self.evaluation_outsource_work_id:
            self.evaluation_outsource_work_id.unlink()

        if self.review_outsource_work_id:
            self.review_outsource_work_id.unlink()

        if self.edit_outsource_work_id:
            self.edit_outsource_work_id.unlink()

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
        if self.psychologist_id.partner_id.contact_id:
            result = self.psychologist_id.partner_id.contact_id
        return result

    def _prepare_create_outsource_work(self, outsource_work_type_field_name):
        if not getattr(self.type_id, outsource_work_type_field_name):
            err_msg = _("No work type defined")
            raise ValidationError(err_msg)
        outsource_work_type = getattr(self.type_id, outsource_work_type_field_name)
        return {
            "partner_id": self._get_partner().id,
            "date": fields.Date.today(),
            "model_id": self._get_outsource_work_model_id(),
            "type_id": outsource_work_type.id,
            "product_id": outsource_work_type.product_id.id,
            "analytic_account_id": self.case_id.analytic_account_id.id,
            "work_object_id": self.id,
        }
