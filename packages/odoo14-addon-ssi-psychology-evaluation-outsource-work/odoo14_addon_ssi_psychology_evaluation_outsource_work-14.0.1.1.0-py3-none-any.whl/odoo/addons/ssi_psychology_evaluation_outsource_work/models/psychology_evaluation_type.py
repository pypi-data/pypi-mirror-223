# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyEvaluationType(models.Model):
    _name = "psychology.evaluation_type"
    _inherit = [
        "psychology.evaluation_type",
    ]
    _description = "Psychology Consultation Type"

    initial_recommendation_outsource_work_type_id = fields.Many2one(
        string="Initial Recommendation Outsource Work Type",
        comodel_name="outsource_work_type",
    )
    evaluation_outsource_work_type_id = fields.Many2one(
        string="Evaluation Outsource Work Type",
        comodel_name="outsource_work_type",
    )
    review_outsource_work_type_id = fields.Many2one(
        string="Review Outsource Work Type",
        comodel_name="outsource_work_type",
    )
    edit_outsource_work_type_id = fields.Many2one(
        string="Edit Outsource Work Type",
        comodel_name="outsource_work_type",
    )
