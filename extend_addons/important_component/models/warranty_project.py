# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class WarrantyProject(models.Model):
    _inherit = 'warranty_project'

    is_important_product = fields.Boolean(string='Is important product')
    important_product_id = fields.Many2one('product.product', string="Important Product", domain=[('is_important', '=', True)])


class WizardCreateWarrantyOrder(models.TransientModel):
    _inherit = 'wizard_create_warranty_order'

    @api.multi
    def create_warranty_order(self):
        sheetIds = self._context.get('active_ids')
        plan_sheets = self.env['warranty_plan_order'].browse(sheetIds)
        for plan_sheet in plan_sheets:
            plan = plan_sheet.parent_id
            maintain_sheets = self.env['warranty_order'].search([('plan_id', '=', plan.id)])
            maintain_sheets_count = len(maintain_sheets)
            maintain_sheet_val = {
                'name': plan.name + '_' + str(maintain_sheets_count + 1),  # +''+str(maintain_sheets_count)
                'vehicle_id': plan_sheet.vehicle_id.id,
                'vehicle_type': plan_sheet.vehicle_type.id,
                'license_plate': plan_sheet.license_plate,
                'fleet': plan_sheet.fleet,
                'operating_mileage': plan_sheet.operating_mileage,
                'warranty_category': plan_sheet.approval_warranty_category.id,
                'planned_date': plan_sheet.planned_date,
                'vin': plan_sheet.vin,
                'average_daily_kilometer': plan_sheet.average_daily_kilometer,
                'line': plan_sheet.line,
                'warranty_location': plan_sheet.warranty_location,
                'plan_id': plan.id
            }
            maintain_sheet = self.env['warranty_order'].create(maintain_sheet_val)

            category_id = maintain_sheet.warranty_category.id

            condition = '%/' + str(category_id) + '/%'

            sql_query = """
                        select id,idpath from warranty_category
                        where idpath like %s
                        order by idpath asc
                    """

            self.env.cr.execute(sql_query, (condition,))

            results = self.env.cr.dictfetchall()

            sheet_items = []
            available_products = []
            sheet_instructions = []
            for line in results:
                category = self.env['warranty_category'].search([('id', '=', line.get('id'))])
                project_ids = category.project_ids
                for project in project_ids:
                    order_project = {
                        'warranty_order_id': maintain_sheet.id,
                        'category_id': category.id,
                        'project_id': project.id,
                        'sequence': len(sheet_items) + 1,
                        'work_time': project.manhour,
                        'percentage_work': 100,
                        'component_ids':[(6,0,plan_sheet.vehicle_id.mapped('component_ids').filtered(lambda x: x.product_id in project.important_product_id).ids)]
                    }

                    sheet_items.append((0, 0, order_project))

                    sheet_instruction = {
                        'warranty_order_id': maintain_sheet.id,
                        'category_id': category.id,
                        'project_id': project.id,
                        'sequence': len(sheet_instructions) + 1,
                        'operational_manual': project.operational_manual
                    }
                    sheet_instructions.append((0, 0, sheet_instruction))

                    warranty_project = self.env['warranty_project'].search([('id', '=', project.id)])
                    boms = warranty_project.avail_ids
                    for bom in boms:
                        available_product = {
                            'sequence': len(available_products) + 1,
                            'warranty_order_id': maintain_sheet.id,
                            'category_id': category.id,
                            'project_id': project.id,
                            'product_id': bom.product_id.id,
                            'change_count': bom.change_count,
                            'max_count': bom.max_count,
                            'require_trans': bom.require_trans
                        }
                        available_products.append((0, 0, available_product))

            maintain_sheet.write({'project_ids': sheet_items, 'available_product_ids': available_products,
                                  'instruction_ids': sheet_instructions})
            plan_sheet.update({'maintain_sheet_id': maintain_sheet.id,
                               'state': 'executing'})  # 'maintain_sheet_no': maintain_sheet.name,


