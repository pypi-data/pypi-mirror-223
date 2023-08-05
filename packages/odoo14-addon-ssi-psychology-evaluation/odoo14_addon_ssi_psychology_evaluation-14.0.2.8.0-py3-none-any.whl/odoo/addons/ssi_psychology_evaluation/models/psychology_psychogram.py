# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyPsychogram(models.Model):
    _name = "psychology.psychogram"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Psychogram"

    name = fields.Char(
        string="Psychogram",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="psychology.psychogram_item",
        inverse_name="psychogram_id",
        copy=True,
    )
