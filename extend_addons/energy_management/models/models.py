# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools
from odoo.modules.module import get_module_resource

class energy_station(models.Model):

     _name = 'energy.station'
     _inherit = ['mail.thread']
     _description = 'Energy Station'

     """
        能源站
     """

     @api.model
     def _default_lister(self):
        """获取当前用户名称
        """
        uid = self.env.uid
        res = self.env['res.users'].search([('id', '=', uid)])
        return  res

     # 能源桩ids
     pile_ids = fields.One2many('energy.pile','station_id',string='Pile Ids')

     # 使用记录
     usage_record_ids = fields.One2many('energy.usage_record','station_id',string='Usage Record Ids')

     # 巡检记录
     security_check_ids = fields.One2many('energy.security_check','station_id',string='Security Check Ids')

     # 库位记录
     location_ids = fields.One2many('stock.location','station_id',string='Location Ids')

     # 组织架构
     department_id = fields.Many2one('hr.department',string='Subordinate unit')

     # 能源站名字
     name = fields.Char(string='Station Name',required=True)

     # 能源站编号
     station_no = fields.Char(string='Station No',required=True)

     # 能源站地址
     station_address = fields.Char(string='Station address')

     # 安全检查项
     security_check = fields.Many2one('security_manage.security_check_table','security_check')

     # 能源站规模
     station_scale = fields.Char(string='Person scale')

     # 责任人
     station_person_liable = fields.Many2one('hr.employee',string='Person liable',required=True)

     # 制表人
     station_lister = fields.Many2one('res.users',string='Lister',default=_default_lister)

     # 制表日期
     station_tab_date = fields.Datetime(string='Tab date',default=fields.Datetime.now())

     # 备注
     station_remarks = fields.Char(string='Remarks')

     # 能源站类型
     station_type = fields.Selection([('gasolineStation', 'Gasoline Station'), ('fillingStation', 'Filling Station'), ('powerStation', 'Power Station'), ('otherStation', 'Other Station')])

     # 能源站状态
     state = fields.Selection([('normal', 'Normal'), ('stop', 'Stop')],default='normal')

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
         return super(energy_station, self).create(vals)

     @api.multi
     def write(self, vals):
         tools.image_resize_images(vals)
         return super(energy_station, self).write(vals)

     @api.multi
     def normal_to_stop(self):
         """
            把能源站的状态修改为：报停
                1.判断是否有正常运行的能源桩
                2.判断是否有正常运行的库位
         :return:
         """
         self.state = 'stop'

     @api.multi
     def stop_to_normal(self):
         self.state = 'normal'

class energy_pile(models.Model):

    _name = 'energy.pile'
    _inherit = ['mail.thread']
    _description = 'Energy Pile'

    """
       能源桩
    """

    @api.model
    def _default_lister(self):
        """获取当前用户名称
        """
        uid = self.env.uid
        res = self.env['res.users'].search([('id', '=', uid)])
        return res

    # 能源站
    station_id = fields.Many2one('energy.station',string='Station Id')

    # 所属库位
    location_id = fields.Many2one('stock.location',string='Location Id',domain="[('station_id', '=', station_id)]")

    # 单位
    companyc_id = fields.Many2one('product.uom',string='Companyc Id')

    # 使用记录
    usage_record_ids = fields.One2many('energy.usage_record','pile_id',string='Usage record ids')

    # 能源桩名称
    name = fields.Char(required=True)

    # 能源桩编号
    pile_no = fields.Char(string='Pile No',required=True)

    # 能源桩类型
    pile_type = fields.Selection([('gasolinePile','Gasoline Pile'),('fillingPile','Filling Pile'),('powerPile','Power Pile'),('otherPile','Other Pile')])

    # 能源类型
    energy_type = fields.Many2one('product.product',string='Energy Type',domain="[('important_type', '=', 'energy')]")

    # 备注
    remark = fields.Char(string='Remark')

    # 状态
    state = fields.Selection([('normal','Normal'),('stop','Stop')],default='normal')

    # 责任人
    station_person_liable = fields.Many2one('hr.employee', string='Person liable',required=True)

    # 制表人
    station_lister = fields.Many2one('res.users', string='Lister',default=_default_lister)

    # 制表日期
    station_tab_date = fields.Datetime(string='Tab date',default=fields.Datetime.now())

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
        return super(energy_pile, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(energy_pile, self).write(vals)

    @api.multi
    def normal_to_stop(self):
        self.state = 'stop'

    @api.multi
    def stop_to_normal(self):
        self.state = 'normal'