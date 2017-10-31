# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class vehicle_plan_details(models.Model):
    _name = 'security.vehicle_plan_details'

    # 序号
    item_id = fields.Many2one('security_manage.check_item', ondelete='cascade', string='item_id', readonly=1)
    check_item_name = fields.Char(string='check_item_name', readonly=1)
    check_content = fields.Char(string='check_content', readonly=1)
    check_standards = fields.Char(string='check_standards', readonly=1)

    check_result = fields.Selection([("check_normal", "check_normal"),  # 正常
                                     ("check_abnormal", "check_abnormal"),  # 异常
                                     ], string='check_result')
    remark = fields.Text(string='remark')

    vehicle_front_check_id = fields.Many2one('security.vehicle_front_check', ondelete='set null')
    vehicle_everyday_check_id = fields.Many2one('security.vehicle_everyday_check', ondelete='set null')
    vehicle_special_check_id = fields.Many2one('security.vehicle_special_check', ondelete='set null')
    vehicle_abarbeitung_check_id = fields.Many2one('security.vehicle_abarbeitung_check', ondelete='set null')
    vehicle_detection_check_id = fields.Many2one('security.vehicle_detection_check', ondelete='set null')
    # 图片
    image_ids = fields.Many2many('ir.attachment', 'front_check_attachment', id1='check_pic',
                             id2='attach_id', string='checking image')

    def openeditform(self):
        self.ensure_one()

        form_view_ref = self.env.ref('security_vehicle_front_check_form_action', False)

        return {
            'name': _('action_dispatch'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'security.vehicle_plan_details',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_id': False,
            'views': [(form_view_ref and form_view_ref.id, 'form')],
        }

    def save_change(self):
        return True