# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PsychologyEvaluation(models.Model):
    _name = "psychology.evaluation"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _description = "Psychology Evaluation"
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    type_id = fields.Many2one(
        string="Type",
        copy=True,
        required=True,
        ondelete="restrict",
        comodel_name="psychology.evaluation_type",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    purpose_id = fields.Many2one(
        string="Purpose",
        comodel_name="psychology.evaluation_purpose",
        related=False,
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    report_type_ids = fields.Many2many(
        string="Allowed Report Types",
        comodel_name="psychology.evaluation_report_type",
        related="type_id.report_type_ids",
    )
    report_type_id = fields.Many2one(
        string="Report Type",
        comodel_name="psychology.evaluation_report_type",
        related=False,
        required=False,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    deadline_ids = fields.Many2many(
        string="Allowed Deadlines",
        comodel_name="psychology.evaluation_deadline",
        related="type_id.deadline_ids",
    )
    deadline_id = fields.Many2one(
        string="Deadline",
        comodel_name="psychology.evaluation_deadline",
        related=False,
        required=False,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    use_initial_recommendation = fields.Boolean(
        string="Use Initial Recommendation",
        related="type_id.use_initial_recommendation",
    )
    use_review = fields.Boolean(
        string="Use Review",
        default=False,
        related="type_id.use_review",
    )
    use_editing = fields.Boolean(
        string="Use Editing",
        default=False,
        related="type_id.use_editing",
    )
    psychogram_ids = fields.Many2many(
        string="Allowed Psychograms",
        comodel_name="psychology.psychogram",
        related="type_id.psychogram_ids",
    )
    psychogram_id = fields.Many2one(
        string="Psychogram",
        copy=True,
        required=True,
        ondelete="restrict",
        comodel_name="psychology.psychogram",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    psychologist_ids = fields.Many2many(
        string="Allowed Psychologist",
        comodel_name="res.users",
        related="type_id.psychologist_ids",
    )
    psychologist_id = fields.Many2one(
        string="Psychologist",
        copy=True,
        required=True,
        ondelete="restrict",
        comodel_name="res.users",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    initial_recommender_ids = fields.Many2many(
        string="Allowed Initial Recommenders",
        comodel_name="res.users",
        related="type_id.initial_recommender_ids",
    )
    initial_recommender_id = fields.Many2one(
        string="Initial Recommender",
        copy=True,
        required=False,
        ondelete="restrict",
        comodel_name="res.users",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    reviewer_ids = fields.Many2many(
        string="Allowed Reviewers",
        comodel_name="res.users",
        related="type_id.reviewer_ids",
    )
    reviewer_id = fields.Many2one(
        string="Reviewer",
        copy=True,
        required=False,
        ondelete="restrict",
        comodel_name="res.users",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    editor_ids = fields.Many2many(
        string="Allowed Editors",
        comodel_name="res.users",
        related="type_id.editor_ids",
    )
    editor_id = fields.Many2one(
        string="Editor",
        copy=True,
        required=False,
        ondelete="restrict",
        comodel_name="res.users",
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
    institution_id = fields.Many2one(
        string="Institution",
        copy=True,
        required=False,
        ondelete="restrict",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    batch_id = fields.Many2one(
        string="# Batch",
        copy=True,
        ondelete="restrict",
        comodel_name="psychology.evaluation_batch",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_report = fields.Date(
        string="Report Date",
        copy=True,
        index=True,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=fields.Date.context_today,
    )
    date_start = fields.Date(
        string="Start Date",
        copy=True,
        index=True,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=fields.Date.context_today,
    )
    initial_recommendation_deadline = fields.Date(
        string="Initial Recommendation Deadline",
        copy=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    evaluation_deadline = fields.Date(
        string="Evaluation Deadline",
        copy=True,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    review_deadline = fields.Date(
        string="Review Deadline",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    editing_deadline = fields.Date(
        string="Editing Deadline",
        copy=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    report_deadline = fields.Date(
        string="Report Deadline",
        copy=True,
        readonly=True,
        required=True,
        states={"draft": [("readonly", False)]},
    )
    initial_result_id = fields.Many2one(
        string="Initial Result",
        copy=False,
        required=False,
        ondelete="restrict",
        comodel_name="psychology.evaluation_result",
        readonly=True,
        states={"quick": [("readonly", False)]},
    )
    description = fields.Text(
        string="Description",
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    conclusion = fields.Text(
        string="Conclusion",
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    advise = fields.Text(
        string="Advise",
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    same_with_intial_result = fields.Boolean(
        string="Same With Initial Result",
        default=False,
        copy=False,
        readonly=True,
        states={"evaluation": [("readonly", False)]},
    )
    result_id = fields.Many2one(
        string="Result",
        copy=False,
        required=False,
        ondelete="restrict",
        comodel_name="psychology.evaluation_result",
        readonly=True,
        states={"evaluation": [("readonly", False)]},
    )
    same_with_result = fields.Boolean(
        string="Same With Initial Result",
        default=False,
        copy=False,
        readonly=True,
        states={"review": [("readonly", False)]},
    )
    final_result_id = fields.Many2one(
        string="Final Result",
        copy=False,
        required=False,
        ondelete="restrict",
        comodel_name="psychology.evaluation_result",
        readonly=True,
        states={"review": [("readonly", False)]},
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="psychology.evaluation_detail",
        inverse_name="evaluation_id",
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    quick_ok = fields.Boolean(
        string="Can Start Quick Recommendation",
        compute="_compute_policy",
    )
    evaluate_ok = fields.Boolean(
        string="Can Start Evaluation",
        compute="_compute_policy",
    )
    review_ok = fields.Boolean(
        string="Can Start Review",
        compute="_compute_policy",
    )
    editing_ok = fields.Boolean(
        string="Can Start Editing",
        compute="_compute_policy",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("quick", "Quick Recommendation"),
            ("evaluation", "Evaluation"),
            ("review", "Review"),
            ("editing", "Editing"),
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
        _super = super(PsychologyEvaluation, self)
        _super._compute_policy()

    def action_quick(self):
        for record in self.sudo():
            record._create_sequence()
            if not record.type_id.use_initial_recommendation:
                record.action_evaluate()
            else:
                record.write(record._prepare_quick_data())

    def action_evaluate(self):
        for record in self.sudo():
            record.sudo().write(record.sudo()._prepare_evaluate_data())

    def action_review(self):
        for record in self.sudo():
            if not record.type_id.use_review:
                record.action_editing()
            else:
                record.write(record._prepare_review_data())

    def action_editing(self):
        for record in self.sudo():
            if not record.type_id.use_editing:
                record.action_confirm()
            else:
                record.write(record._prepare_editing_data())

    def _prepare_quick_data(self):
        self.ensure_one()
        return {
            "state": "quick",
        }

    def _prepare_evaluate_data(self):
        self.ensure_one()
        return {
            "state": "evaluation",
        }

    def _prepare_review_data(self):
        self.ensure_one()
        return {
            "state": "review",
        }

    def _prepare_editing_data(self):
        self.ensure_one()
        return {
            "state": "editing",
        }

    @api.onchange(
        "initial_result_id",
        "same_with_intial_result",
    )
    def onchange_result_id(self):
        self.result_id = False
        if self.same_with_intial_result:
            self.result_id = self.initial_result_id

    @api.onchange(
        "result_id",
        "same_with_result",
    )
    def onchange_final_result_id(self):
        self.final_result_id = False
        if self.same_with_result:
            self.final_result_id = self.result_id

    @api.onchange(
        "type_id",
    )
    def onchange_psychogram_id(self):
        self.psychogram_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_report_type_id(self):
        self.report_type_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_deadline_id(self):
        self.deadline_id = False

    @api.onchange(
        "purpose_id",
    )
    def onchange_type_id(self):
        self.type_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_psychologist_id(self):
        self.psychologist_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.onchange(
        "institution_id",
    )
    def onchange_batch_id(self):
        self.batch_id = False

    @api.onchange(
        "batch_id",
    )
    def onchange_purpose_id(self):
        self.purpose_id = False
        if self.batch_id:
            self.purpose_id = self.batch_id.purpose_id

    @api.onchange(
        "batch_id",
    )
    def onchange_report_deadline(self):
        self.report_deadline = False
        if self.batch_id:
            self.report_deadline = self.batch_id.report_deadline

    @api.onchange(
        "deadline_id",
        "date_start",
        "initial_recommendation_deadline",
        "evaluation_deadline",
        "review_deadline",
        "editing_deadline",
        "type_id",
    )
    def onchange_deadline(self):
        if self.deadline_id and self.type_id:

            field_ref = self.date_start

            if (
                self.type_id.use_initial_recommendation
                and self.deadline_id.initial_recommendation_auto_deadline
            ):
                self.initial_recommendation_deadline = False
                if field_ref:
                    dt_ref = fields.Date.add(
                        field_ref,
                        days=self.deadline_id.initial_recommendation_deadline_offset,
                    )
                    self.initial_recommendation_deadline = fields.Date.to_string(dt_ref)
                    field_ref = self.initial_recommendation_deadline

            if self.deadline_id.evaluation_auto_deadline:
                self.evaluation_deadline = False
                if field_ref:
                    dt_ref = fields.Date.add(
                        field_ref, days=self.deadline_id.evaluation_deadline_offset
                    )
                    self.evaluation_deadline = fields.Date.to_string(dt_ref)
                    field_ref = self.evaluation_deadline

            if self.type_id.use_review and self.deadline_id.review_auto_deadline:
                self.review_deadline = False
                if field_ref:
                    dt_ref = fields.Date.add(
                        field_ref, days=self.deadline_id.review_deadline_offset
                    )
                    self.review_deadline = fields.Date.to_string(dt_ref)
                    field_ref = self.review_deadline

            if self.type_id.use_editing and self.deadline_id.editing_auto_deadline:
                self.editing_deadline = False
                if field_ref:
                    dt_ref = fields.Date.add(
                        field_ref, days=self.deadline_id.editing_deadline_offset
                    )
                    self.editing_deadline = fields.Date.to_string(dt_ref)
                    field_ref = self.editing_deadline

            if self.deadline_id.report_auto_deadline:
                self.report_deadline = False
                if field_ref:
                    dt_ref = fields.Date.add(
                        field_ref, days=self.deadline_id.report_deadline_offset
                    )
                    self.report_deadline = fields.Date.to_string(dt_ref)
                    field_ref = self.report_deadline

    def action_reload_detail(self):
        for record in self.sudo():
            record._reload_detail()

    def _reload_detail(self):
        self.ensure_one()
        if self.psychogram_id:
            self.detail_ids.unlink()
            self.write(self._prepare_evaluation_detail())

    def _prepare_evaluation_detail(self):
        self.ensure_one()
        result = []
        for detail in self.psychogram_id.detail_ids:
            result.append(detail._prepare_evaluation_detail())
        return {
            "detail_ids": result,
        }
