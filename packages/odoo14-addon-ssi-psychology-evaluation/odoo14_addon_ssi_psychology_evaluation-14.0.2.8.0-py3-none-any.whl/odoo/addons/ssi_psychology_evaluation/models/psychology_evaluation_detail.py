# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PsychologyEvaluationDetail(models.Model):
    _name = "psychology.evaluation_detail"
    _description = "Psychology Evaluation Detail"
    _order = "evaluation_id, sequence, id"

    evaluation_id = fields.Many2one(
        string="# Evaluation",
        comodel_name="psychology.evaluation",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        string="Item",
        comodel_name="psychology.psychogram_item",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="item_id.sequence",
        store=True,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="psychology.psychogram_item_category",
        related="item_id.category_id",
        store=True,
    )

    @api.depends(
        "item_id",
    )
    def _compute_value_ids(self):
        for record in self:
            result = []
            if record.item_id:
                for value in record.item_id.set_id.detail_ids:
                    result.append(value.value_id.id)
            record.value_ids = result

    value_ids = fields.Many2many(
        string="Allowed Value(s)",
        comodel_name="psychology.psychogram_item_value",
        compute="_compute_value_ids",
        store=False,
    )
    value_id = fields.Many2one(
        string="Value",
        comodel_name="psychology.psychogram_item_value",
    )

    quantified_value = fields.Float(
        string="Quantified Value",
        required=True,
        default=0.0,
    )

    @api.onchange("item_id", "value_id")
    def onchange_quantified_value(self):
        self.quantified_value = 0.0
        obj_detail = self.env["psychology.psychogram_item_value_set_detail"]
        if self.item_id and self.value_id:
            value_set = self.item_id.set_id
            criteria = [
                ("set_id", "=", value_set.id),
                ("value_id", "=", self.value_id.id),
            ]
            values = obj_detail.search(criteria)
            if len(values) > 0:
                self.quantified_value = values[0].quantified_value
