# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class security_check_item(models.Model):
    _name = 'security_manage.check_item'
    _sql_constraints = [('check_item_no_unique', 'unique (name)', u"检查项目编号已存在!"),
                        ('check_item_name_unique', 'unique (check_item_name)', u"检查项目名称已存在!")]

    name = fields.Char(string='check_id', required=True)

    check_info = fields.Char(default="检查信息")

    check_item_name = fields.Char(string='check_item_name')

    check_content = fields.Char(string='check_content')

    check_standards = fields.Char(string='check_standards')

    create_time = fields.Date(string='create_time', required=True, default=fields.Date.today())

    state = fields.Selection([('use', 'Use'),('archive', "Archive"),], default='use', string='security_check_item_state')

    active = fields.Boolean(string="MyActive", default=True)
    
    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if ('name' not in default) :
            default['name'] = _("%s (copy)") % self.name
        if 'check_item_name' not in default:
            default['check_item_name'] = _("%s (copy)") % self.check_item_name
        return super(security_check_item, self).copy(default)    

    @api.multi
    def action_to_default(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_archive(self):
        self.state = 'archive'
        self.active = False

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "%s / %s" % (record.name, record.check_item_name)
            result.append((record.id, name))
        return result