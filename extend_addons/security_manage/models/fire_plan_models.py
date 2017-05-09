# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class fire_plan(models.Model):
    _name = 'sfs.fire_plan'
    name = fields.Char(string='archive name')

    archives_class_big = fields.Many2one('security_manage.cls_manage', string='archive big class',
                                         ondelete='set null',
                                         domain=[('class_type', '=', 'big_class')])
    archives_class_little = fields.Many2one('security_manage.cls_manage', string='archive little class',
                                            ondelete='set null',
                                            domain=[('class_type', '=', 'little_class')])

    archvies_id = fields.Char(string=_('archive id'), required=True, index=True,
                              copy=False, default=' ', readonly=True)

    description = fields.Text()

    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    state = fields.Selection([
        ('use', _('Use')),
        ('archive', _("Archive")),
    ], default='use', string='archive workflow state')

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
            vals['archvies_id'] = self.env['ir.sequence'].next_by_code('sfs_fire_plan') or '/'
        return super(fire_plan, self).create(vals)
