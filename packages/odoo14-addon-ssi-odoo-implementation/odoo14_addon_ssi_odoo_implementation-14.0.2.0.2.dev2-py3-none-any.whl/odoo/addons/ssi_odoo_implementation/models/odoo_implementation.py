# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class OdooImplementation(models.Model):
    _name = "odoo_implementation"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_done",
    ]
    _description = "Odoo Implementation"
    _approval_from_state = "draft"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    _statusbar_visible_label = "draft,open,done"

    _policy_field_order = [
        "open_ok",
        "restart_approval_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_done",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_done",
    ]

    _create_sequence_state = "open"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self._default_date(),
    )
    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", True),
            ("parent_id", "=", False),
        ],
        ondelete="restrict",
    )
    domain = fields.Char(
        string="Domain",
        required=True,
    )
    version_id = fields.Many2one(
        string="Version",
        comodel_name="odoo_version",
        ondelete="restrict",
        required=True,
    )
    environment_id = fields.Many2one(
        string="Environment",
        comodel_name="odoo_environment",
        ondelete="restrict",
        required=True,
    )
    feature_implementation_ids = fields.One2many(
        string="Feature Implementations",
        comodel_name="odoo_feature_implementation",
        inverse_name="implementation_id",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Not Deployed"),
            ("open", "Running"),
            ("done", "Finish"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    @api.model
    def _default_date(self):
        return fields.Date.today()

    @api.model
    def _get_policy_field(self):
        res = super(OdooImplementation, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "done_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def name_get(self):
        result = []
        for record in self:
            if getattr(record, self._document_number_field) == "/":
                name = record.domain
            else:
                name = record.domain + " (" + record.name + ")"
            result.append((record.id, name))
        return result
