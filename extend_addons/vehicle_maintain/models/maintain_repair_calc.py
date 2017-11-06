# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime


class MaintainRepairCalculate(models.Model):
    """
    车辆维修管理：结算单
    """

    _inherit = 'maintain.manage.repair'

    calculate_state = fields.Selection([('calculating', 'calculating'),
                                        ('calculated', 'calculated')],
                                        string="Calculate State", default='calculating')
    # 结算时间
    calculate_time = fields.Datetime("Calculate Time")

    total_work_time = fields.Float('Total Work Time(Hour)', digits=(10, 2))
    total_work_fee = fields.Float(digits=(10, 2))
    total_product_fee = fields.Float(digits=(10, 2))
    total_fee = fields.Float(digits=(10, 2))

    materials_product_ids = fields.One2many('maintain.manage.repair_materials', 'repair_id', string="Materials Product")

    company_id = fields.Many2one('res.company', 'Company',
                                default=lambda self: self.env['res.company']._company_default_get('maintain.manage.repair'),
                                index=True, required=True)

    work_fee = fields.Float(related='company_id.work_fee', default=50)

    end_job_ids = fields.One2many("maintain.manage.repair_end_jobs", 'repair_id', string='Maintain Repair Jobs'
                              )
    calculate_user_id = fields.Many2one('hr.employee', string="Calculate Name")

    @api.multi
    def action_back(self):
        '''
        刷新
        :return:
        '''
        self.write({'calculate_state': 'calculating'})

    @api.multi
    def action_calcuate(self):
        '''
        1,先执行刷新功能
        2，如果刷新成功，更新状态
        :return:
        '''

        self._new_refresh_picking()
        self._refresh_fee()

        self.write({
            'calculate_user_id': self._default_employee().id if self._default_employee() else '',
            'calculate_time': datetime.datetime.now(),
            'calculate_state': 'calculated'
        })

    @api.multi
    def action_refresh(self):
        '''
        1,统计领退料单
        2，计算工时和物料费用
        :return:
        '''

        self._new_refresh_picking()
        self._refresh_fee()

    def _refresh_jobs(self):
        '''
        检验通过后统计所有的工时管理
        :return:
        '''
        for i in self:
            end_job_datas = []
            sequence = 0
            i.end_job_ids.unlink()

            def _gen_dict(k, i, sequence):
                vals = {
                    'sequence': sequence,
                    "fault_category_id": k.fault_category_id.id,
                    "fault_appearance_id": k.fault_appearance_id.id or None,
                    "fault_reason_id": k.fault_reason_id.id,
                    "fault_method_id": k.fault_method_id.id,
                    "plan_start_time": k.plan_start_time,
                    "plan_end_time": k.plan_end_time,
                    'real_start_time': k.real_start_time,
                    'real_end_time': k.real_end_time,
                    "work_time": k.work_time,
                    "percentage_work": k.percentage_work,
                    "user_id": k.user_id.id,
                    'my_work': k.my_work,
                    'real_work': k.real_work,
                    'work_time_fee': k.work_time * i.work_fee * k.percentage_work / 100.0,
                }
                return vals

            for k in i.job_ids:
                sequence += 1
                vals = _gen_dict(k, i, sequence)
                vals.update({'is_need_calc': True,
                             "is_last_method": True
                             })
                end_job_datas.append((0, 0, vals))

            bak_repairs = i.search([('origin_repair_id', '=', i.id),
                                    ('state', '=', 'repair'),
                                    ('active', '=', False)])
            for m in bak_repairs:
                for k in m.job_ids:
                    sequence += 1
                    vals = _gen_dict(k, i, sequence)
                    end_job_datas.append((0, 0, vals))
            i.write({'end_job_ids': end_job_datas})

    def _refresh_fee(self):
        for i in self:
            work_fee = i.company_id.work_fee
            #工时费用不按实际工时计算，按额定工时计算

            for j in i.end_job_ids.filtered(lambda r: r.is_need_calc==True):
                work_time_fee = j.work_time * work_fee * j.percentage_work / 100.0
                j.write({'work_time_fee': work_time_fee})

            for k in i.materials_product_ids:
                product_fee = k.list_price * k.usage_ct
                k.write({'product_fee': product_fee})

            total_work_time = sum(i.end_job_ids.filtered(lambda r: r.is_need_calc==True).mapped('real_work'))
            #额定工时 核算 费用
            total_work_fee = sum(i.end_job_ids.filtered(lambda r: r.is_need_calc==True).mapped('work_time_fee'))
            total_product_fee = sum(i.materials_product_ids.mapped('product_fee'))
            total_fee = total_work_fee + total_product_fee

            i.write({
                "work_fee": work_fee,
                "total_work_time": total_work_time,
                "total_work_fee": total_work_fee,
                "total_product_fee": total_product_fee,
                "total_fee": total_fee
            })


    def _get_products(self, picking_get, picking_back):
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

        self.materials_product_ids.unlink()

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


class MaintainRepairEndJobs(models.Model):
    """
    车辆维修管理：维修单 所有的工时管理(包括修改维修方法的工时)
    """
    _name = 'maintain.manage.repair_end_jobs'
    name = fields.Char("Job Name", help="Job Name")
    sequence = fields.Integer("Sequence", help="Sequence")
    repair_id = fields.Many2one("maintain.manage.repair", ondelete='cascade',
                                string="Maintain Repair")
    fault_category_id = fields.Many2one("maintain.fault.category", ondelete='set null',
                                        string="Fault Category")
    fault_appearance_id = fields.Many2one("maintain.fault.appearance", ondelete='set null',
                                          string="Fault Appearance")
    fault_reason_id = fields.Many2one("maintain.fault.reason", ondelete='set null', string="Fault Reason")
    fault_method_id = fields.Many2one("maintain.fault.method", ondelete='set null', string="Fault Method")
    user_id = fields.Many2one('hr.employee', string="Repair Name", required=True)
    plan_start_time = fields.Datetime("Plan Start Time")
    plan_end_time = fields.Datetime("Plan End Time")
    real_start_time = fields.Datetime("Real Start Time")
    real_end_time = fields.Datetime("Real End Time")
    percentage_work = fields.Float('Percentage Work')
    work_time = fields.Float('Work Time(Hour)', digits=(10, 2))
    work_time_fee = fields.Float('Work Time Fee', digits=(10, 2))

    my_work = fields.Float('My Work(Hour)', digits=(10, 2), store=True)

    real_work = fields.Float('Real Work(Hour)', digits=(10, 2), store=True)
    real_work_fee = fields.Float('Real Work Fee', digits=(10, 2))
    is_need_calc = fields.Boolean("Is Need Calc", default=False)
    is_last_method = fields.Boolean("Is Last Method", default=False)

    calculate_state = fields.Selection(related='repair_id.calculate_state',string="Calculate State")

    @api.multi
    def job_not_calc(self):
        self.write({'is_need_calc':False})

    @api.multi
    def job_calc(self):
        self.write({'is_need_calc':True})

