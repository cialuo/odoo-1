# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class repair_site(models.Model):
    _name = 'srp.repair_site'
    name = fields.Char()

    archives_class_big = fields.Many2one('security_manage.cls_manage', ondelete='set null',
                                         domain=[('class_type', '=', 'big_class')])
    archives_class_little = fields.Many2one('security_manage.cls_manage', ondelete='set null',
                                            domain=[('class_type', '=', 'little_class')])

    archvies_id = fields.Char(string=_('档案编号'), required=True, index=True,
                              copy=False, default=' ', readonly=True)
    archives_creator = fields.Many2one('res.users', string=_('archives_creator'), required=True, default=lambda
        self: self.env.user)
    archives_creator_date = fields.Date()

    description = fields.Text()

    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

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

    @api.model
    def create(self, vals):
        """
        维修单:
            自动生成订单号：前缀WXD+序号
        """
        if vals.get('archvies_id', ' ') == ' ':
            vals['archvies_id'] = self.env['ir.sequence'].next_by_code('srp.repair_quality') or '/'
        return super(repair_site, self).create(vals)
