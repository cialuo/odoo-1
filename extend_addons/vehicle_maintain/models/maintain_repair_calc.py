# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime


class MaintainRepairCalculate(models.Model):
    """
    车辆维修管理：结算单
    """

    _inherit = 'maintain.manage.repair'

    calculate_state = fields.Selection([('calculating', 'calculating'), ('calculated', 'calculated')],
                                        string="Calculate State", default='calculating')
    # 结算时间
    calculate_time = fields.Datetime("Calculate Time")

    total_work_time = fields.Float('Total Work Time(Hour)', digits=(10, 2))
    total_work_fee = fields.Float(digits=(10, 2))
    total_product_fee = fields.Float(digits=(10, 2))
    total_fee = fields.Float(digits=(10, 2))

    materials_product_ids = fields.One2many('maintain.manage.repair_materials', 'repair_id', string="Materials Product")

    # computewarning = fields.Char(string="compute warning data", compute="_computeWarning")
    #
    # @api.multi
    # @api.depends('picking_ids')
    # def _computeWarning(self):
    #
    #     for item in self:
    #         item.computewarning  = None
    #         if getattr(item, 'sortedWt', None) == None:
    #             item.sortedWt = sorted(item.picking_ids, key=lambda x: x.waiting_time, reverse=True)
    #         for x in item.picking_ids:
    #             if x.id == item.sortedWt[0].id and item.sortedWt[0].waiting_time > 0:
    #                 x.needwarning = 'yes'
    #             else:
    #                 x.needwarning = 'no'


    company_id = fields.Many2one('res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get('maintain.manage.repair'),
        index=True, required=True)

    work_fee = fields.Float(related='company_id.work_fee', default=50)



    @api.multi
    def action_back(self):
        '''
        刷新
        :return:
        '''
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

        self._new_refresh_picking()
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

        self._new_refresh_picking()
        self._refresh_jobs_products()

    def _refresh_jobs_products(self):
        for i in self:
            work_fee = i.company_id.work_fee
            #工时费用不按实际工时计算，按额定工时计算

            for j in i.job_ids:
                #if j.real_work:
                real_work_fee = j.work_time * work_fee
                j.write({'real_work_fee': real_work_fee})

            for k in i.materials_product_ids:
                product_fee = k.list_price * k.usage_ct
                k.write({'product_fee': product_fee})

            total_work_time = sum(i.job_ids.mapped('real_work'))
            #额定工时 核算 费用
            total_work_fee = i.work_time * work_fee
            # total_work_fee = sum(i.job_ids.mapped('real_work_fee'))
            total_product_fee = sum(i.materials_product_ids.mapped('product_fee'))
            total_fee = total_work_fee + total_product_fee

            i.write({
                "work_fee": work_fee,
                "total_work_time": total_work_time,
                "total_work_fee": total_work_fee,
                "total_product_fee": total_product_fee,
                "total_fee": total_fee
            })


    def _get_products(self,picking_get,picking_back):
        '''
            １,根据领料单和发料单进行统计
            ２,区分物资是否启动批次，分别取其价格
            ３,去除退料单内的物资数量
        :param pack_operation_product:
        :return:
        '''
        products = {}

        for picking in picking_get:

                for operation in picking.pack_operation_product_ids:
                    if operation.pack_lot_ids:
                        for lot in operation.pack_lot_ids:
                            product = {}
                            key = lot.lot_id
                            if products.has_key(key):
                                product['products_id'] = lot.product_id.id
                                product['price_unit'] = lot.lot_price_unit
                                product['product_uom_qty'] = products[key]['product_uom_qty'] + lot.qty
                                products[key] = product
                            else:
                                product['products_id'] = lot.product_id.id
                                product['price_unit'] = lot.lot_price_unit
                                product['product_uom_qty'] = lot.qty
                                products[key]=product
                    else:
                            product = {}
                            key = operation.product_id
                            if products.has_key(key):
                                product['products_id'] = operation.product_id.id
                                product['product_uom_qty'] = products[key]['product_uom_qty'] + operation.qty_done
                                product['price_unit'] = operation.product_id.standard_price
                                products[key] = product
                            else:
                                product['products_id'] = operation.product_id.id
                                product['product_uom_qty'] = operation.qty_done
                                product['price_unit'] = operation.product_id.standard_price
                                products[key] = product


        for picking in picking_back:

                for operation in picking.pack_operation_product_ids:

                    if operation.pack_lot_ids:
                        for lot in operation.pack_lot_ids:
                            product = {}
                            key = lot.lot_id
                            if products.has_key(key):
                                product = products[key]
                                product['product_uom_qty'] = product['product_uom_qty'] - lot.qty
                                products[key]=product
                            else:
                                product['products_id'] = lot.product_id.id
                                product['price_unit'] = lot.lot_price_unit
                                product['product_uom_qty'] = - lot.qty
                                products[key] = product
                    else:
                            product = {}
                            key = operation.product_id
                            if products.has_key(key):
                                product =  products[key]
                                product['product_uom_qty'] = product['product_uom_qty'] - operation.qty_done
                                products[key] = product
                            else:
                                product['products_id'] = operation.product_id.id
                                product['price_unit'] = operation.product_id.standard_price
                                product['product_uom_qty'] = - operation.qty_done
                                products[key] = product

        return products

    def _new_refresh_picking(self):
        '''
            1,先判断领退料单中是否存在未完成的订单（不用管交旧领新的状态）
            2,删除已经统计过的用领清单
            3,分别获取领料和退料的picking单据
            4,除去物资退了分量
            4,插入使用数量大于0的物料
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

        products = self._get_products(picking_get,picking_back)

        count = 0
        product_data = []
        for key in products.keys():
            if products[key]['product_uom_qty'] <= 0:
                continue
            count += 1
            vals = {
                "repair_id": self.id,
                "sequence": count,
                "product_id": products[key]['products_id'],
                "usage_ct": products[key]['product_uom_qty'],
                "list_price": products[key]['price_unit']
            }
            product_data.append((0, 0, vals))
        self.write({'materials_product_ids': product_data})


    def _refresh_picking(self):
        '''
        1,先判断领退料单中是否存在未完成的订单（不用管交旧领新的状态）
        2,删除已经统计过的用领清单
        2,分别获取领料和退料的picking单据
        3,插入使用数量大于0的物料 和　库存移动内的　price_unit
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
                product = {}
                if data.has_key(j.product_id):
                    product['product_uom_qty'] = data[j.product_id]['product_uom_qty'] + j.product_uom_qty
                    product['price_unit'] = j.price_unit
                    data[j.product_id] = product
                else:
                    product['product_uom_qty'] = j.product_uom_qty
                    product['price_unit'] = j.price_unit
                    data[j.product_id] = product


        for i in picking_back:
            for j in i.move_lines:
                product = {}
                if data.has_key(j.product_id):
                    product['product_uom_qty'] = data[j.product_id]['product_uom_qty'] - j.product_uom_qty
                    product['price_unit'] = j.price_unit
                    data[j.product_id] = product#data[j.product_id] - j.product_uom_qty
                else:
                    product['product_uom_qty'] = - j.product_uom_qty
                    product['price_unit'] = j.price_unit
                    data[j.product_id] = product #- j.product_uom_qty
        count = 0
        product_data = []
        #for product, usage_ct in data.items():
        for product in data.keys():
            #if usage_ct <= 0:
            if data[product]['product_uom_qty'] <= 0:
                continue
            count += 1
            vals = {
                "repair_id": self.id,
                "sequence": count,
                "product_id": product.id,
                "usage_ct": data[product]['product_uom_qty'],
                "list_price": data[product]['price_unit']
            }
            product_data.append((0, 0, vals))
        self.write({'materials_product_ids': product_data})


class MaintainRepairMaterials(models.Model):
    """
    车辆维修管理：使用物料
    """

    _name = 'maintain.manage.repair_materials'

    repair_id = fields.Many2one('maintain.manage.repair', ondelte='cascade', string="Maintain Repair")

    sequence = fields.Integer("Sequence")
    product_id = fields.Many2one('product.product', string="Product Name")
    product_code = fields.Char("Product Code", related='product_id.default_code')
    categ_id = fields.Many2one('product.category', related='product_id.categ_id',
                               string='Product Category')
    list_price = fields.Float("Stock Price")

    usage_ct = fields.Float('Usage Count')
    product_fee = fields.Float('Product Fee')


