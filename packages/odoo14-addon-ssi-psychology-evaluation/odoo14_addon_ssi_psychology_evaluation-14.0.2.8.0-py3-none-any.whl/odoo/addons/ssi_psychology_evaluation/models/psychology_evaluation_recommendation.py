# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyEvaluationRecommendation(models.Model):
    _name = "psychology.evaluation_recommendation"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Evaluation Recommendation"

    name = fields.Char(
        string="Recommendation",
    )
