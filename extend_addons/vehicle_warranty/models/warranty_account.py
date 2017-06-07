# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime


class WarrantyAccount(models.Model): # 结算单

    _inherit = 'warranty_order'

    calculate_state = fields.Selection([('calculating', 'calculating'), ('calculated', 'calculated')],
                                        string="Calculate State", default='calculating')
    # 结算时间
    calculate_time = fields.Datetime("Calculate Time")

    total_work_time = fields.Float('Total Work Time(Hour)', digits=(10, 2))
    total_work_fee = fields.Float(digits=(10, 2))
    total_product_fee = fields.Float(digits=(10, 2))
    total_fee = fields.Float(digits=(10, 2))

    materials_product_ids = fields.One2many('warranty_account_material', 'order_id', string="Materials Product")


    company_id = fields.Many2one('res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get('warranty_order'),
        index=True, required=True)

    work_fee = fields.Float(related='company_id.work_fee', default=50)

    @api.multi
    def action_back(self):
        self.write({
            'calculate_state': 'calculating'
        })


    @api.multi
    def action_calcuate(self):
        '''
        1,先执行刷新功能
        2，如果刷新成功，更新状态
        :return:
        '''

        self._refresh_picking()
        self._refresh_jobs_products()

        self.write({
            'calculate_time': datetime.datetime.now(),
            'calculate_state': 'calculated'
        })

    @api.multi
    def action_refresh(self):
        '''
        1,先统计领退料单
        2，计算工时和物料费用
        :return:
        '''

        self._refresh_picking()
        self._refresh_jobs_products()

    def _refresh_jobs_products(self):
        for i in self:
            work_fee = i.company_id.work_fee
            for j in i.manhour_manage_ids:
                if j.real_work:
                    real_work_fee = j.real_work * work_fee
                    j.write({'real_work_fee': real_work_fee})

            for k in i.materials_product_ids:
                product_fee = k.list_price * k.usage_ct
                k.write({'product_fee': product_fee})

            total_work_time = sum(i.manhour_manage_ids.mapped('real_work'))
            total_work_fee = sum(i.manhour_manage_ids.mapped('real_work_fee'))
            total_product_fee = sum(i.materials_product_ids.mapped('product_fee'))
            total_fee = total_work_fee + total_product_fee

            i.write({
                "work_fee": work_fee,
                "total_work_time": total_work_time,
                "total_work_fee": total_work_fee,
                "total_product_fee": total_product_fee,
                "total_fee": total_fee
            })


    def _refresh_picking(self):
        '''
        1,先判断领退料单中是否存在未完成的订单（不用管交旧领新的状态）
        2,删除已经统计过的用领清单
        2,分别获取领料和退料的picking单据
        3,插入使用数量大于0的物料
        :return:
        '''
        for picking in self.picking_ids.filtered(lambda i:i.picking_type_id.name in [u'发料', u'领料', u'退料']):
            if not all(move.state in ['cancel', 'done'] for move in picking.move_lines):
                raise exceptions.UserError(_('There is unfinished picking'))
        for i in self.materials_product_ids:
            i.unlink()

        picking_get = self.picking_ids.filtered(lambda i: i.state in ['done'] and
                                                i.picking_type_id.name in [u'发料', u'领料'])
        picking_back = self.picking_ids.filtered(lambda i: i.state in ['done'] and
                                                           i.picking_type_id.name in [u'退料'])
        data = {}
        for i in picking_get:
            for j in i.move_lines:
                if data.has_key(j.product_id):
                    data[j.product_id] = data[j.product_id] + j.product_uom_qty
                else:
                    data[j.product_id] = j.product_uom_qty

        for i in picking_back:
            for j in i.move_lines:
                if data.has_key(j.product_id):
                    data[j.product_id] = data[j.product_id] - j.product_uom_qty
                else:
                    data[j.product_id] = - j.product_uom_qty
        count = 0
        product_data = []
        for product, usage_ct in data.items():
            if usage_ct <= 0:
                continue
            count += 1
            vals = {
                "order_id": self.id,
                "sequence": count,
                "product_id": product.id,
                "usage_ct": usage_ct
            }
            product_data.append((0, 0, vals))
        self.write({'materials_product_ids': product_data})


class WarrantyAccountMaterial(models.Model): # 结算单_物料

    _name = 'warranty_account_material'

    order_id = fields.Many2one('warranty_order', ondelte='cascade', string="Maintain Repair")

    sequence = fields.Integer("Sequence")
    product_id = fields.Many2one('product.product', string="Product Name")
    product_code = fields.Char("Product Code", related='product_id.default_code')
    categ_id = fields.Many2one('product.category', related='product_id.categ_id',
                               string='Product Category')
    list_price = fields.Float("Stock Price", related='product_id.list_price', store=True)

    usage_ct = fields.Float('Usage Count')
    product_fee = fields.Float('Product Fee')


