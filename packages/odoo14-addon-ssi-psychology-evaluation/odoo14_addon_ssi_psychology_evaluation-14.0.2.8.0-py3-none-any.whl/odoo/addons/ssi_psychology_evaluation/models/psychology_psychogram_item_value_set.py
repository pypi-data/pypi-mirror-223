# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyPsychogramItemValueSet(models.Model):
    _name = "psychology.psychogram_item_value_set"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Psychogram Item Value Set"

    name = fields.Char(
        string="Item Value",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="psychology.psychogram_item_value_set_detail",
        inverse_name="set_id",
        copy=True,
    )
