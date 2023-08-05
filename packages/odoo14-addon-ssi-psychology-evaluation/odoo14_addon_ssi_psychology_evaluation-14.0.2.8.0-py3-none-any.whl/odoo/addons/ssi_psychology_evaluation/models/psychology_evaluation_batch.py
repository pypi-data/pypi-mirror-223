# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PsychologyEvaluationBatch(models.Model):
    _name = "psychology.evaluation_batch"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _description = "Psychology Evaluation Batch"
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = "open"

    purpose_id = fields.Many2one(
        string="Purpose",
        comodel_name="psychology.evaluation_purpose",
        related=False,
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    user_id = fields.Many2one(
        string="Responsible",
        copy=True,
        required=True,
        ondelete="restrict",
        comodel_name="res.users",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    client_id = fields.Many2one(
        string="Client",
        copy=True,
        required=True,
        ondelete="restrict",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_start = fields.Date(
        string="Date Start",
        copy=True,
        readonly=True,
        required=True,
        states={"draft": [("readonly", False)]},
    )
    report_deadline = fields.Date(
        string="Report Deadline",
        copy=True,
        readonly=True,
        required=True,
        states={"draft": [("readonly", False)]},
    )
    evaluation_ids = fields.One2many(
        string="Evaluations",
        comodel_name="psychology.evaluation",
        inverse_name="batch_id",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.depends("policy_template_id")
    def _compute_policy(self):
        _super = super(PsychologyEvaluationBatch, self)
        _super._compute_policy()

    @api.onchange(
        "purpose_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id
