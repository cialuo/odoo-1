# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class maintainer_train(models.Model):
    _name = 'srp.maintainer_train'
    # 课程名
    name = fields.Char();
    course_name = fields.Char()
    course_id = fields.Char(string=_('编号'), required=True, index=True,
                            copy=False, default=' ', readonly=True)
    course_start_time = fields.Datetime()
    course_end_time = fields.Datetime()
    # 培训类型
    train_type = fields.Char()
    # 课程类型
    course_type = fields.Char()
    # 讲师
    teacher = fields.Char()
    # 上课地点
    course_place = fields.Char()
    # 学员说明
    student_desc = fields.Char()

    state = fields.Selection([
        ('start_course', _('Start course')),
        ('sign_in', _("Sign in")),
        ('exam', _("Exam")),
        ('done', _("Done")),
    ], default='start_course', string=_('workflow_state'))

    @api.multi
    def action_to_default(self):
        self.state = 'start_course'

    @api.multi
    def action_sign_in(self):
        self.state = 'sign_in'

    @api.multi
    def action_exam(self):
        self.state = 'exam'

    @api.multi
    def action_done(self):
        self.state = 'done'

        # @api.model
        # def create(self, vals):
        #     """
        #     维修单:
        #         自动生成订单号：前缀WXD+序号
        #     """
        #     if vals.get('archvies_id', ' ') == ' ':
        #         vals['archvies_id'] = self.env['ir.sequence'].next_by_code('srp.repair_quality') or '/'
        #     return super(maintainer_train, self).create(vals)
