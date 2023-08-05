# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyEvaluationType(models.Model):
    _name = "psychology.evaluation_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Evaluation Type"

    name = fields.Char(
        string="Type",
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        ondelete="restrict",
    )
    purpose_id = fields.Many2one(
        string="Purpose",
        comodel_name="psychology.evaluation_purpose",
        required=True,
    )
    psychogram_ids = fields.Many2many(
        string="Allowed Psychograms",
        comodel_name="psychology.psychogram",
        relation="psychology_rel_evaluation_type_2_psychogram",
        column1="type_id",
        column2="psychogram_id",
    )
    psychogram_ids = fields.Many2many(
        string="Allowed Psychograms",
        comodel_name="psychology.psychogram",
        relation="psychology_rel_evaluation_type_2_psychogram",
        column1="type_id",
        column2="psychogram_id",
    )
    report_type_ids = fields.Many2many(
        string="Allowed Report Types",
        comodel_name="psychology.evaluation_report_type",
        relation="psychology_rel_evaluation_type_2_report_type",
        column1="type_id",
        column2="report_type_id",
    )
    deadline_ids = fields.Many2many(
        string="Allowed Deadlines",
        comodel_name="psychology.evaluation_deadline",
        relation="psychology_rel_evaluation_type_2_deadline",
        column1="type_id",
        column2="deadline_id",
    )
    recommendation_ids = fields.Many2many(
        string="Allowed Recommendations",
        comodel_name="psychology.evaluation_recommendation",
        relation="psychology_rel_evaluation_type_2_recommendation",
        column1="type_id",
        column2="recommendation_id",
    )
    psychologist_ids = fields.Many2many(
        string="Allowed Psychologist",
        comodel_name="res.users",
        relation="psychology_rel_evaluation_type_2_psychologist",
        column1="type_id",
        column2="user_id",
    )
    initial_recommender_ids = fields.Many2many(
        string="Allowed Initial Recommenders",
        comodel_name="res.users",
        relation="psychology_rel_evaluation_type_2_initial_recomender",
        column1="type_id",
        column2="user_id",
    )
    reviewer_ids = fields.Many2many(
        string="Allowed Reviewers",
        comodel_name="res.users",
        relation="psychology_rel_evaluation_type_2_reviewer",
        column1="type_id",
        column2="user_id",
    )
    editor_ids = fields.Many2many(
        string="Allowed Editors",
        comodel_name="res.users",
        relation="psychology_rel_evaluation_type_2_editor",
        column1="type_id",
        column2="user_id",
    )
    use_initial_recommendation = fields.Boolean(
        string="Use Initial Recommendation",
        default=False,
    )
    use_review = fields.Boolean(
        string="Use Review",
        default=False,
    )
    use_editing = fields.Boolean(
        string="Use Editing",
        default=False,
    )
