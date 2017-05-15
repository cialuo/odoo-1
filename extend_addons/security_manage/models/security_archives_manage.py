# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class archives_class_manage(models.Model):
    _name = 'security_manage.cls_manage'
    # _sql_constraints = [('item_id_unique', 'unique(item_id)', _('id  already exists'))]
    _sql_constraints = [
        ('item_id_unique',
         'UNIQUE(item_id)',
         "The id must be unique"),
    ]
    name = fields.Char(string='archives_class_manage_item_name', required=True)
    item_id = fields.Char(string='archives_class_manage_item_id', required=True)
    item_name = fields.Char(string='archives_class_manage_table', default=_('archives_class_manage_table'))
    class_name = fields.Char(string='archives_class_manage_class_name')
    # TODO 这是一个Many2one
    # class_type = fields.Char(string=_('archives_class_manage_class_type'))
    class_type = fields.Selection([
        ('big_class', 'Big class'),
        ('little_class', 'Little class')
    ], string='archives_class_manage_class_type')

    # TODO 这是一个Many2one
    # parent = fields.Char(string=_('archives_class_manage_parent'))
    parent = fields.Many2one('security_manage.cls_manage', string='archives_class_manage_parent',
                             ondelete='set null',
                             domain=[('class_type', '=', 'big_class')])

    # form_creator= fields.Char()
    form_creator = fields.Many2one('res.users', string='archives_class_manage_form_creator', required=True,
                                   default=lambda
                                       self: self.env.user)

    create_time = fields.Date(string='archives_class_manage_create_time')

    state = fields.Selection([
        ('use', 'Use'),
        ('archive', "Archive"),
    ], default='use', string='archives_class_manage_state')

    # 归档标志
    active = fields.Boolean(default=True)

    @api.multi
    def action_to_default(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_archive(self):
        self.state = 'archive'
        self.active = False

    @api.onchange
    def onTypeChange(self):
        pass

        # @api.constrains('item_id')
        # def _check_something(self):
        #     for record in self:
        #         if record.item_id == item_id:
        #             raise ValidationError("record should unique: %s" % record.item_id)
