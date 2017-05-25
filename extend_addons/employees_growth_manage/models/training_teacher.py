# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools

class training_teacher(models.Model):

     _name = 'employees_growth.training_teacher'
     _description = 'Training teacher'
     _inherit = ['mail.thread']

     """
          培训老师：
               名称、老师类型、编号、职称、岗位、组织、入职时间、性别
               年龄、电邮、地址、个人介绍
     """
     name = fields.Char(string='Name')

     teacher_type = fields.Selection([('inside','Inside'),('external','External')],string='Teacher type')

     teacher_no = fields.Char(string='Teacher no')

     teacher_title = fields.Char(string='Teacher title')

     teacher_post = fields.Char(string='Teacher post')

     teacher_organization = fields.Char(string='Teacher organization')

     induction_time = fields.Datetime(string='Induction time')

     teacher_gender = fields.Selection([('male','Male'),('female','Female')],string='Teacher gender')

     teacher_telephone = fields.Char(string='Teacher telephone')

     teacher_age = fields.Integer(string='Teacher age')

     teacher_email = fields.Char(string='Teacher email')

     teacher_marriage = fields.Selection([('married','Married'),
                                          ('unmarried','Unmarried'),('divorce','Divorce')],string='Teacher marriage')

     teacher_address = fields.Char(string='Teacher address')

     personal_introduction = fields.Text(string='Personal introduction')

     # image: all image fields are base64 encoded and PIL-supported
     image = fields.Binary("Photo", attachment=True,
                           help="This field holds the image used as photo for the employee, limited to 1024x1024px.")

     image_medium = fields.Binary("Medium-sized photo", attachment=True,
                                  help="Medium-sized photo of the employee. It is automatically "
                                       "resized as a 128x128px image, with aspect ratio preserved. "
                                       "Use this field in form views or some kanban views.")

     image_small = fields.Binary("Small-sized photo", attachment=True,
                                 help="Small-sized photo of the employee. It is automatically "
                                      "resized as a 64x64px image, with aspect ratio preserved. "
                                      "Use this field anywhere a small image is required.")
     @api.model
     def create(self, vals):
         tools.image_resize_images(vals)
         return super(training_teacher, self).create(vals)

     @api.multi
     def write(self, vals):
         tools.image_resize_images(vals)
         return super(training_teacher, self).write(vals)








