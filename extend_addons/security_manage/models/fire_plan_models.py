# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class fire_plan(models.Model):
    _name = 'sfs.fire_plan'
    name = fields.Char(string='archive name',required=True)

    archives_class_big = fields.Many2one('security_manage.cls_manage', string='archive big class',
                                         ondelete='set null',required=True,
                                         domain=[('class_type', '=', 'big_class')])
    archives_class_little = fields.Many2one('security_manage.cls_manage', string='archive little class',
                                            ondelete='set null',
                                            domain=[('class_type', '=', 'little_class')])

    archvies_id = fields.Char(string='archive id', required=True, index=True,
                              copy=False, default=' ', readonly=True)

    description = fields.Text()

    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    # 归档标志
    active = fields.Boolean(default=True)

    state = fields.Selection([
        ('use', 'Use'),
        ('archive', "Archive"),
    ], default='use', string='archive workflow state')

    @api.multi
    def action_to_default(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_archive(self):
        self.state = 'archive'
        self.active = False

    @api.model
    def create(self, vals):
        """
        维修单:
            自动生成订单号：前缀WXD+序号
        """
        if vals.get('archvies_id', ' ') == ' ':
            vals['archvies_id'] = self.env['ir.sequence'].next_by_code('sfs_fire_plan') or '/'
        return super(fire_plan, self).create(vals)
