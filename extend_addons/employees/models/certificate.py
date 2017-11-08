# -*- coding:utf-8 -*-
from odoo import models, fields, api, _

class certificate(models.Model):
    """
    特种工证照
    """
    _name = 'employees.certificate'

    # 证件名称
    name = fields.Char('certificate name', required=True)
    # 过期日期
    expiredate = fields.Date('certificate expire date')

    # 图片
    image = fields.Many2many('ir.attachment', 'certificate_attachment', id1='check_pic',
                             id2='attach_id', string='certificate image')
    # 工号
    jobnumber = fields.Char(related='employee_id.jobnumber', readonly=True)
    # 用户名
    username = fields.Char(related='employee_id.name', readonly=True)
    # 岗位
    workpost = fields.Many2one(related='employee_id.workpost', readonly=True)
    # 员工状态
    employeestate = fields.Selection(related='employee_id.employeestate', readonly=True)

    # 用户图片
    userimage = fields.Binary(related='employee_id.image', readonly=True)

    # 关联员工
    employee_id = fields.Many2one('hr.employee', string='employee', default=None)
    # 部门
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    # 职称
    title = fields.Char(related='employee_id.title', readonly=True)
    # 电话
    mobile_phone = fields.Char(related='employee_id.mobile_phone', readonly=True)
    # 邮箱
    work_email = fields.Char(related='employee_id.work_email', readonly=True)

    # 培训记录
    trains = fields.One2many("certificate.trains", "certificate_id", string="certificate trains")

    # 审验记录
    validates = fields.Many2many('ir.attachment', 'certificate_validates_attachment', id1='check_pic',
                             id2='attach_id', string='certificate validate')

    # 体检记录
    perecords = fields.Many2many('ir.attachment', 'certificate_perecords_attachment', id1='check_pic',
                     id2='attach_id', string='certificate perecords')

class trains(models.Model):
    """
    证照培训经历
    """

    _name = 'certificate.trains'

    certificate_id = fields.Many2one('employees.certificate')

class validateRecord(models.Model):
    """
    审验记录
    """

    _name = "certificate.validate"

    certificate_id = fields.Many2one('employees.certificate')

class PErecords(models.Model):
    """
    体检记录
    """
    _name = "certificate.perecords"

    certificate_id = fields.Many2one('employees.certificate')
