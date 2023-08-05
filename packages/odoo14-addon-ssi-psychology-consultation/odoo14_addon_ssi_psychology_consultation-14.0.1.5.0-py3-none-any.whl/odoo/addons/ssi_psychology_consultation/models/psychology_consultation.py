# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PsychologyConsultation(models.Model):
    _name = "psychology_consultation"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _description = "Psychology Consultation"
    _approval_from_state = "open"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True

    _statusbar_visible_label = "draft,open,confirm,done"

    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    _create_sequence_state = "open"

    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", False),
            ("parent_id", "=", False),
        ],
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    case_id = fields.Many2one(
        string="# Case",
        comodel_name="psychology.case",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="psychology_consultation_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_psychologist_ids = fields.Many2many(
        string="Allowed Psychologists",
        related="type_id.allowed_psychologist_ids",
        store=False,
    )
    psychologist_id = fields.Many2one(
        string="Psychologist",
        comodel_name="res.users",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    result = fields.Html(
        string="Consultation Result",
        required=False,
        ondelete="restrict",
        readonly=True,
        states={"open": [("readonly", False), ("required", True)]},
    )
    date = fields.Date(
        string="Date Consultation",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("reject", "Reject"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    @api.model
    def _get_policy_field(self):
        res = super(PsychologyConsultation, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "open_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "partner_id",
    )
    def onchange_case_id(self):
        self.case_id = False
