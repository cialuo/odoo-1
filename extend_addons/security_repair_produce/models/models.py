# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class repair_quality(models.Model):
    _name = 'srp.repair_quality'
    name = fields.Char()
    description = fields.Text()

    state = fields.Selection([
        ('use', _('Use')),
        ('archive', _("Archive")),
    ], default='use', string=_('workflow_state'))

    @api.multi
    def action_to_default(self):
        self.state = 'use'

    @api.multi
    def action_archive(self):
        self.state = 'archive'
