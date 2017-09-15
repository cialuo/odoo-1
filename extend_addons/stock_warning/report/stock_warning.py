# -*- coding: utf-8 -*-
from odoo import api, models, fields, _,exceptions
import time
class StockWarning(models.AbstractModel):

    _name = 'report.stock_warning.warning_report'

    @api.multi
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('stock_warning.warning_report')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
            'data':data
        }
        return report_obj.render('stock_warning.warning_report', docargs)

class StockWarningData(models.Model):

    _name = 'stock.warning_data'
    _description = 'Stock Warning Data'

    warehouse = fields.Many2one('stock.warehouse')

    product = fields.Many2one('product.product')

    qty_available = fields.Float()

    virtual_available = fields.Float()

    product_min_qty = fields.Float()

    @api.multi
    def action_create_purchase_plan(self):
        '''
            创建采购计划
        :return:
        '''
        context = dict(self._context or {})
        ids = context['active_ids']
        if ids:
            warning_data = self.env['stock.warning_data'].search([('id','in',ids)])
            if warning_data:

                '''创建采购计划'''
                user = self.env.user
                purchase_plan_val = {
                    'user_id':user.employee_ids[0].id,
                    'month':time.strftime("%Y-%m")
                }
                plan = self.env['purchase.plan'].create(purchase_plan_val)

                '''创建采购计划详情'''
                for warning in warning_data:

                    #获取供应商
                    p_order = self.env['purchase.order.line'].search([('product_id', '=', warning.product.id)], limit=1,
                                                                     order='id desc')
                    p_supplierinfo = self.env['product.supplierinfo'].search([('name', '=', p_order.partner_id.id)],
                                                                             limit=1)
                    val = {
                        'plan_id':plan.id,
                        'product_id':warning.product.id,
                        'seller_id':p_supplierinfo.id,
                        'product_tmpl_id':warning.product.product_tmpl_id.id,
                        'price_unit':p_supplierinfo.price
                    }
                    self.env['purchase.plan.line'].create(val)

        return {
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.plan',
                'res_id': plan.id,
                'views': [[False, 'form']],
                }
