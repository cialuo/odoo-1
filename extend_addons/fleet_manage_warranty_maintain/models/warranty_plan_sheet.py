# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyPlanSheet(models.Model): # 计划单
    _name = 'fleet_manage_warranty_maintain.warranty_plan_sheet'
    name = fields.Char()

    state = fields.Selection([ # 状态
        ('draft', "draft"),
        ('confirmed', "confirmed"),
        ('done', "done"),
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):

        values = {
            'vehicle_no': 'vehicle_no',
            'vehicle_type': 'vehicle_type',
            'plan_id': self.parent_id.id,
            'name': "auto sheet (%s)" % 'X8', # self.name
        }
        maintain_sheet=self.env['fleet_manage_warranty_maintain.warranty_maintain_sheet'].create(values)

        # params = (self.warranty_category.id,)

        category_id=self.warranty_category.id

        condition='%/' + str(category_id) + '/%'


        sql_query = """
            select t.id,t.path,t.idpath from (
                select t.* from (
                with recursive tmp_fleet_manage_warranty_category(id,path,idpath) as
                (
                select a.id,'/'||a.name as "path",'/'||a.id as "idpath" from fleet_manage_warranty_category as a  where a.parent_id is null
                union all
                select a.id,q.path||'/'||a.name as "path",q.idpath||'/'||a.id as "idpath" from fleet_manage_warranty_category as a inner join tmp_fleet_manage_warranty_category as q on (q.id = a.parent_id)

                )
                select a.id,a.path,a.idpath||'/' as idpath from tmp_fleet_manage_warranty_category as a
                ) t
                where idpath like %s
                order by idpath asc
            ) t
                                """

        self.env.cr.execute(sql_query,(condition,))

        results = self.env.cr.dictfetchall()
        # st_line = self.env['account.bank.statement.line']
        for line in results:
            category = self.env['fleet_manage_warranty.category'].search([('id', '=', line.get('id'))])
            items = category.items
            for item in items:
                sheet_item = self.env['fleet_manage_warranty_maintain.maintain_sheet.item'].create({
                    'maintenance_part': 'maintenance_part',
                    'maintainsheet_id': maintain_sheet.id,
                    'category_id': category.id,
                    'item_id': item.id
                })
            # st_line.browse(line.get('id')).write({'partner_id': line.get('partner_id')})


        # category = self.env['fleet_manage_warranty.category'].search([('id', '=', self.warranty_category.id)])
        # items=category.items
        # for item in items:
        #     sheet_item = self.env['fleet_manage_warranty_maintain.maintain_sheet.item'].create({
        #         'maintenance_part': 'maintenance_part',
        #         'maintainsheet_id': maintain_sheet.id,
        #         'category_id': category.id,
        #         'item_id': item.id
        #     })
        #
        # categorys = self.env['fleet_manage_warranty.category'].search([('parent_id', '=', self.warranty_category.id)])
        # for category in categorys:
        #     items=category.items
        #     for item in items:
        #         sheet_item = self.env['fleet_manage_warranty_maintain.maintain_sheet.item'].create({
        #             'maintenance_part': 'maintenance_part',
        #             'maintainsheet_id': maintain_sheet.id,
        #             'category_id': category.id,
        #             'item_id': item.id
        #         })



        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'


    # _rec_name = "product_id"
    #
    # def _get_default_product_uom_id(self):
    #     return self.env['product.uom'].search([], limit=1, order='id').id
    parent_id = fields.Many2one('fleet_manage_warranty_maintain.warranty_plan', 'parentId', required=True, ondelete='cascade')

    fleet_id = fields.Many2one('fleet.vehicle', 'Vehicle', required=True) # 车ID

    sequence = fields.Integer('Sequence', default=1)

    # bom_id = fields.Many2one(
    #     'mrp.bom', 'Parent BoM',
    #     index=True, ondelete='cascade', required=True)
    #
    #
    # product_qty = fields.Float(
    #     'Product Quantity', default=1.0,
    #     digits=dp.get_precision('Product Unit of Measure'), required=True)
    #
    # product_uom_id = fields.Many2one(
    #     'product.uom', 'Product Unit of Measure',
    #     default=_get_default_product_uom_id,
    #     oldname='product_uom', required=True,
    #     help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control")

    vehicle_no = fields.Char()  # 车号
    vehicle_type = fields.Char()  # 车型
    maintain_sheet_no = fields.Char()  # 保养单号

    warranty_category = fields.Many2one(
        'fleet_manage_warranty.category', 'WarrantyCategory',
        ondelete='cascade', required=True) # 生成保养类别

