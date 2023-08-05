# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyPsychogramItemValue(models.Model):
    _name = "psychology.psychogram_item_value"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Psychogram Item Value"

    name = fields.Char(
        string="Item Value",
    )
