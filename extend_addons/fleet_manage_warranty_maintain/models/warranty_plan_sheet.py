# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyPlanSheet(models.Model): # 计划单
    _name = 'fleet_warranty_plan_sheet'
    name = fields.Char(string="Plan Sheet", required=True, index=True, default='New')

    parent_id = fields.Many2one('fleet_warranty_plan', 'WarrantyPlan', required=True, ondelete='cascade') # 车辆保养计划ID

    sequence = fields.Integer('Sequence', default=1)

    vehicle_id = fields.Many2one('fleet.vehicle',string="VehicleNo", required=True,) # 车号
    vehicle_type = fields.Many2one("fleet.vehicle.model",related='vehicle_id.model_id', store=True, readonly=True) # 车型
    license_plate = fields.Char("License Plate", related='vehicle_id.license_plate', store=True, readonly=True) # 车牌

    fleet = fields.Char()  # 车队

    operating_mileage = fields.Float(digits=(6, 1), string="OM") # 运营里程

    warranty_category = fields.Many2one(
        'fleet_manage_warranty.category', 'WC',
        required=True, domain=[('level', '=', '1')]) # 生成保养类别

    @api.one
    @api.depends('warranty_category')
    def _compute_awc(self):
        self.approval_warranty_category = self.warranty_category

    approval_warranty_category = fields.Many2one(
        'fleet_manage_warranty.category', 'AWC',
        domain=[('level', '=', '1')], compute='_compute_awc') # 核准保养类别

    planned_date = fields.Date('PlannedDate', default=fields.Date.context_today) # 计划日期

    vin = fields.Char() # 车架号

    average_daily_kilometer = fields.Float(digits=(6, 1), string="ADK") # 平均日公里

    line = fields.Char() # 线路

    maintain_location = fields.Char() # 保养地点

    # maintain_sheet_no = fields.Char(string="SheetNo", readonly=True)  # 保养单号

    maintain_sheet_id = fields.Many2one('fleet_warranty_maintain_sheet', string="Warranty Maintain Sheet")  # 保养单号 , required=True,


    state = fields.Selection([ # 状态
        ('draft', "draft"), # 草稿
        ('commit', 'commit'), # 已提交
        ('wait', "wait"), # 等待执行
        ('executing', "executing"), # 正在执行
        ('done', "done"), # 执行完毕
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

    # @api.model
    # def create(self, vals):
    #     vals['approval_warranty_category']=vals.get('warranty_category')
    #     result = super(WarrantyPlanSheet, self).create(vals)
    #     return result



class WarrantyWizardCreate(models.TransientModel):
    _name = 'fleet_warranty_wizard_create'

    def _default_sheet(self):
        sheetIds=self._context.get('active_ids')
        # print sheetIds
        sheets = self.env['fleet_warranty_plan_sheet'].browse(sheetIds)
        return sheets

    plan_sheet_ids = fields.Many2many('fleet_warranty_plan_sheet', string='Plan Sheet Ids', required=True, default=_default_sheet)

    @api.multi
    def create_maintain_sheet(self):
        sheetIds = self._context.get('active_ids')
        plan_sheets = self.env['fleet_warranty_plan_sheet'].browse(sheetIds)
        for plan_sheet in plan_sheets:
            plan=plan_sheet.parent_id
            maintain_sheets = self.env['fleet_warranty_maintain_sheet'].search([('plan_id', '=', plan.id)])
            maintain_sheets_count=len(maintain_sheets)
            maintain_sheet_val = {
                'name': plan.name+'_'+str(maintain_sheets_count+1), # +''+str(maintain_sheets_count)
                'vehicle_id': plan_sheet.vehicle_id.id,
                'vehicle_type': plan_sheet.vehicle_type.id,
                'license_plate': plan_sheet.license_plate,
                'fleet': plan_sheet.fleet,
                'operating_mileage': plan_sheet.operating_mileage,
                'warranty_category': plan_sheet.approval_warranty_category.id,
                'planned_date': plan_sheet.planned_date,
                'vin': plan_sheet.vin,
                'average_daily_kilometer':plan_sheet.average_daily_kilometer,
                'line':plan_sheet.line,
                'maintain_location':plan_sheet.maintain_location,
                'plan_id':plan.id
            }
            maintain_sheet=self.env['fleet_warranty_maintain_sheet'].create(maintain_sheet_val)

            category_id = maintain_sheet.warranty_category.id

            condition = '%/' + str(category_id) + '/%'

            sql_query = """
                select id,idpath from fleet_manage_warranty_category
                where idpath like %s
                order by idpath asc
            """

            # sql_query = """
            #             select t.id,t.path,t.idpath from (
            #                 select t.* from (
            #                 with recursive tmp_fleet_manage_warranty_category(id,path,idpath) as
            #                 (
            #                 select a.id,'/'||a.name as "path",'/'||a.id as "idpath" from fleet_manage_warranty_category as a  where a.parent_id is null
            #                 union all
            #                 select a.id,q.path||'/'||a.name as "path",q.idpath||'/'||a.id as "idpath" from fleet_manage_warranty_category as a inner join tmp_fleet_manage_warranty_category as q on (q.id = a.parent_id)
            #
            #                 )
            #                 select a.id,a.path,a.idpath||'/' as idpath from tmp_fleet_manage_warranty_category as a
            #                 ) t
            #                 where idpath like %s
            #                 order by idpath asc
            #             ) t
            #                                 """

            self.env.cr.execute(sql_query, (condition,))

            results = self.env.cr.dictfetchall()

            sheet_items = []
            available_products = []
            sheet_instructions = []
            for line in results:
                category = self.env['fleet_manage_warranty.category'].search([('id', '=', line.get('id'))])
                items = category.items
                for item in items:
                    sheet_item = {
                        'maintainsheet_id': maintain_sheet.id,
                        'category_id': category.id,
                        'item_id': item.id,
                        'sequence': len(sheet_items) + 1,
                        'work_time':item.manhour,
                        'percentage_work':100,
                        'component_ids':[(6,0,plan_sheet.vehicle_id.mapped('component_ids').filtered(lambda x: x.product_id in item.important_product_id).ids)] #plan_sheet.vehicle_id.mapped('component_ids').filtered(lambda x: x.product_id in item.important_product_id).ids
                    }
                    # sheet_item.component_ids=plan_sheet.vehicle_id.mapped('component_ids').filtered(lambda x: x.product_id in item.important_product_id).ids
                    sheet_items.append((0, 0, sheet_item))

                    sheet_instruction = {
                        'maintainsheet_id': maintain_sheet.id,
                        'category_id': category.id,
                        'item_id': item.id,
                        'sequence': len(sheet_instructions) + 1,
                        'operational_manual':item.operational_manual
                    }
                    sheet_instructions.append((0, 0, sheet_instruction))


                    # warranty_item = self.env['fleet_manage_warranty.item'].search([('id', '=', item.id)])
                    # boms = warranty_item.bom_line_ids
                    # for bom in boms:
                    #     available_product = {
                    #         'maintainsheet_id': maintain_sheet.id,
                    #         'category_id': category.id,
                    #         'item_id': item.id,
                    #         'product_id': bom.product_id.id,
                    #         'max_available_count': bom.collar_cap,
                    #         'default_avail_count': bom.default_usage,
                    #         'sequence': len(available_products) + 1,
                    #         'vehicle_type': bom.vehicle_type.id
                    #     }
                    #     available_products.append((0, 0, available_product))

                    warranty_item = self.env['fleet_manage_warranty.item'].search([('id', '=', item.id)])
                    boms = warranty_item.avail_ids
                    for bom in boms:
                        available_product = {
                            'sequence': len(available_products) + 1,
                            'maintainsheet_id': maintain_sheet.id,
                            'category_id': category.id,
                            'item_id': item.id,
                            'product_id': bom.product_id.id,
                            'change_count': bom.change_count,
                            'max_count': bom.max_count,
                            'require_trans': bom.require_trans
                        }
                        available_products.append((0, 0, available_product))

            maintain_sheet.write({'item_ids': sheet_items, 'available_product_ids': available_products, 'instruction_ids': sheet_instructions})
            plan_sheet.update({'maintain_sheet_id': maintain_sheet.id, 'state': 'executing'}) # 'maintain_sheet_no': maintain_sheet.name,



