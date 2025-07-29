from odoo import models, fields, api

class ToolTool(models.Model):
    _name = 'tool.tool'
    _description = 'Tool or Equipment'

    name = fields.Char(string="Tool Name", required=True)
    serial_number = fields.Char(string="Serial Number", required=True)

    is_available = fields.Boolean(
        string="Is Available",
        compute="_compute_is_available",
        store=True
    )

    current_request_id = fields.Many2one(
        'tool.request',
        string="Current Request",
        compute="_compute_current_request",
        store=True
    )

    request_ids = fields.One2many(
        'tool.request',
        'tool_id',
        string="Requests"
    )

    @api.depends('request_ids.state')
    def _compute_current_request(self):
        for tool in self:
            # Find any 'approved' or 'in_use' request for this tool
            active_request = tool.request_ids.filtered(
                lambda r: r.state in ['approved', 'in_use']
            )
            tool.current_request_id = active_request[0] if active_request else False

    @api.depends('current_request_id')
    def _compute_is_available(self):
        for tool in self:
            tool.is_available = not bool(tool.current_request_id)