# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyPsychogramItemValueSetDetail(models.Model):
    _name = "psychology.psychogram_item_value_set_detail"
    _description = "Psychology Psychogram Item Value Set Detail"
    _order = "sequence, set_id, value_id"

    set_id = fields.Many2one(
        string="Set",
        comodel_name="psychology.psychogram_item_value_set",
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    value_id = fields.Many2one(
        string="Value",
        comodel_name="psychology.psychogram_item_value",
        ondelete="restrict",
        required=True,
    )
    quantified_value = fields.Float(
        string="Quantified Value",
        required=True,
    )
