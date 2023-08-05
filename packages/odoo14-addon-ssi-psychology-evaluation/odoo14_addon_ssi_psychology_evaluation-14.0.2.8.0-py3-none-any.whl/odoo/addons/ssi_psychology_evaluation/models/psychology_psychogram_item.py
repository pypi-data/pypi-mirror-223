# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyPsychogramItem(models.Model):
    _name = "psychology.psychogram_item"
    _description = "Psychology Psychogram Item"
    _order = "category_id, sequence, psychogram_id"

    psychogram_id = fields.Many2one(
        string="Psychogram",
        comodel_name="psychology.psychogram",
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    category_id = fields.Many2one(
        string="Item Set",
        comodel_name="psychology.psychogram_item_category",
        required=True,
        ondelete="restrict",
    )
    name = fields.Char(
        string="Item",
        required=True,
    )
    set_id = fields.Many2one(
        string="Item Set",
        comodel_name="psychology.psychogram_item_value_set",
        ondelete="restrict",
        required=True,
    )

    def _prepare_evaluation_detail(self):
        self.ensure_one()
        return (
            0,
            0,
            {
                "item_id": self.id,
            },
        )
