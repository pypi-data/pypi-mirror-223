# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyEvaluationPurpose(models.Model):
    _name = "psychology.evaluation_purpose"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Evaluation Purpose"

    name = fields.Char(
        string="Purpose",
    )
