# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyEvaluationReportType(models.Model):
    _name = "psychology.evaluation_report_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Evaluation Report Type"

    name = fields.Char(
        string="Report Type",
    )
