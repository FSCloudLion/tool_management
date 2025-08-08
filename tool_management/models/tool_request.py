from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ToolRequest(models.Model):
    _name = 'tool.request'
    _description = 'Tool Request'
    _order = 'date_from desc'

    name = fields.Char(string="Request ID", required=True, copy=False, readonly=True, default="New")

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    tool_id = fields.Many2one('tool.tool', string="Tool", required=True)
    project_id = fields.Many2one('project.project', string="Project", required=False)

    date_from = fields.Date(string="From Date", required=True)
    date_to = fields.Date(string="To Date", required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('in_use', 'In Use'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tool.request') or 'New'
        return super().create(vals_list)

    @api.constrains('tool_id', 'date_from', 'date_to', 'state')
    def _check_overlap(self):
        for request in self:
            overlapping = self.search([
                ('id', '!=', request.id),
                ('tool_id', '=', request.tool_id.id),
                ('state', 'in', ['approved', 'in_use']),
                ('date_from', '<=', request.date_to),
                ('date_to', '>=', request.date_from),
            ])
            if overlapping:
                raise ValidationError(_('This tool is already booked during the selected period.'))

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for request in self:
            if request.date_from > request.date_to:
                raise ValidationError(_('Start date must be before or equal to end date.'))
            
    def action_approve(self):
        for request in self:
            if request.state != 'draft':
                raise ValidationError("Only draft requests can be approved.")
            request.state = 'approved'

    def action_reject(self):
        for request in self:
            if request.state != 'draft':
                raise ValidationError("Only draft requests can be rejected.")
            request.state = 'rejected'

    def action_mark_returned(self):
        for request in self:
            if request.state != 'in_use':
                raise ValidationError("Only in-use tools can be marked as returned.")
            request.state = 'returned'

    def action_set_in_use(self):
        for request in self:
            if request.state != 'approved':
                raise ValidationError("Only approved requests can be set to in use.")
            request.state = 'in_use'