# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class OutsourceWorkRate(models.Model):
    _name = "outsource_work_rate"
    _description = "Outsource Work Rate"
    _inherit = [
        "mixin.date_duration",
        "mixin.transaction_confirm",
        "mixin.transaction_ready",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _order = "partner_id, date_start, id"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "ready"
    _approval_state = "confirm"
    _after_approved_method = "action_ready"

    # Sequence attribute
    _create_sequence_state = "ready"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True

    _statusbar_visible_label = "draft,confirm,ready,open,done"
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_required = True
    _date_end_required = False
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "open_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_open",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_ready",
        "dom_open",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        domain=[("is_company", "=", False), ("parent_id", "=", False)],
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    detail_ids = fields.One2many(
        comodel_name="outsource_work_rate_detail",
        string="Details",
        inverse_name="rate_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("ready", "Ready to Start"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Reject"),
        ],
    )

    @api.model
    def _get_policy_field(self):
        res = super(OutsourceWorkRate, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "ready_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "open_ok",
            "cancel_ok",
            "restart_ok",
            "done_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res
