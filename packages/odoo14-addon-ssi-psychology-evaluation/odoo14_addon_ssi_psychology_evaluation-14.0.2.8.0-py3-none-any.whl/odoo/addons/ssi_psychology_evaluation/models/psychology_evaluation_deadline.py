# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyEvaluationDeadline(models.Model):
    _name = "psychology.evaluation_deadline"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Evaluation Deadline"

    name = fields.Char(
        string="Deadline",
    )

    initial_recommendation_auto_deadline = fields.Boolean(
        string="Automate Initial Recommendation Deadline Computation",
        default=False,
    )
    initial_recommendation_deadline_offset = fields.Integer(
        string="Initial Recommendation Deadline Offset",
    )
    evaluation_auto_deadline = fields.Boolean(
        string="Automate Evaluation Deadline Computation",
        default=False,
    )
    evaluation_deadline_offset = fields.Integer(
        string="Evaluation Deadline Offset",
    )
    review_auto_deadline = fields.Boolean(
        string="Automate Review Deadline Computation",
        default=False,
    )
    review_deadline_offset = fields.Integer(
        string="Evaluation Deadline Offset",
    )
    editing_auto_deadline = fields.Boolean(
        string="Automate Editing Deadline Computation",
        default=False,
    )
    editing_deadline_offset = fields.Integer(
        string="Editing Deadline Offset",
    )
    report_auto_deadline = fields.Boolean(
        string="Automate Report Deadline Computation",
        default=False,
    )
    report_deadline_offset = fields.Integer(
        string="Report Deadline Offset",
    )
