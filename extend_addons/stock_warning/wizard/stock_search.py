# -*- coding: utf-8 -*-
from odoo import models, api, fields, _,exceptions
from odoo.tools.float_utils import float_round

class stock_search(models.TransientModel):

    _name = "stock_search_wizard"
    _description = "Stock Search"

    """
        仓库预警的搜索层
    """

    warehouse_id = fields.Many2one('stock.warehouse',string='Warehouse Id')

    @api.multi
    def action_search(self):
        """
            计算库存数据
        :return:
        """

        warehouse = self.env['stock.warehouse'].search([])
        if self.warehouse_id:
            warehouse = self.warehouse_id
        data = dict()
        data['data'] = self.get_data(warehouse)
        warning_data = self.env['stock.warning_data']
        warning_data.search([]).unlink()
        for c_data in data['data']:
            warning_data.create(c_data)
        action = self.env.ref('stock_warning.open_to_warning_data',False).read()[0]
        return action
    def get_data(self,warehouses):
        """
            计算预警信息
        :return:
        """
        data = list()
        #所有物资
        products = self.env['product.product'].search([])
        for warehouse in warehouses:
            res = products._compute_quantities_dict_by_warehouse_id(False, False, False, warehouse)
            data.extend(res)
        return data
class Product(models.Model):

    _inherit = 'product.product'

    @api.multi
    def _compute_quantities_dict_by_warehouse_id(self, lot_id, owner_id, package_id,warehouse, from_date=False, to_date=False):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self.with_context({'warehouse':warehouse.id})._get_domain_locations()
        domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
        dates_in_the_past = False
        if to_date and to_date < fields.Datetime.now():  # Only to_date as to_date will correspond to qty_available
            dates_in_the_past = True

        domain_move_in = [('product_id', 'in', self.ids)] + domain_move_in_loc
        domain_move_out = [('product_id', 'in', self.ids)] + domain_move_out_loc
        if lot_id:
            domain_quant += [('lot_id', '=', lot_id)]
        if owner_id:
            domain_quant += [('owner_id', '=', owner_id)]
            domain_move_in += [('restrict_partner_id', '=', owner_id)]
            domain_move_out += [('restrict_partner_id', '=', owner_id)]
        if package_id:
            domain_quant += [('package_id', '=', package_id)]
        if dates_in_the_past:
            domain_move_in_done = list(domain_move_in)
            domain_move_out_done = list(domain_move_out)
        if from_date:
            domain_move_in += [('date', '>=', from_date)]
            domain_move_out += [('date', '>=', from_date)]
        if to_date:
            domain_move_in += [('date', '<=', to_date)]
            domain_move_out += [('date', '<=', to_date)]

        Move = self.env['stock.move']
        Quant = self.env['stock.quant']
        domain_move_in_todo = [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_move_in
        domain_move_out_todo = [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_move_out
        moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in
                            Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id']))
        moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in
                             Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id']))
        quants_res = dict((item['product_id'][0], item['qty']) for item in
                          Quant.read_group(domain_quant, ['product_id', 'qty'], ['product_id']))
        if dates_in_the_past:
            # Calculate the moves that were done before now to calculate back in time (as most questions will be recent ones)
            domain_move_in_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_in_done
            domain_move_out_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_out_done
            moves_in_res_past = dict((item['product_id'][0], item['product_qty']) for item in
                                     Move.read_group(domain_move_in_done, ['product_id', 'product_qty'],
                                                     ['product_id']))
            moves_out_res_past = dict((item['product_id'][0], item['product_qty']) for item in
                                      Move.read_group(domain_move_out_done, ['product_id', 'product_qty'],
                                                      ['product_id']))

        data = list()
        for product in self.with_context(prefetch_fields=False):
            res = {}
            if dates_in_the_past:
                qty_available = quants_res.get(product.id, 0.0) - moves_in_res_past.get(product.id,
                                                                                        0.0) + moves_out_res_past.get(
                    product.id, 0.0)
            else:
                qty_available = quants_res.get(product.id, 0.0)

            res['product'] = product.id
            res['warehouse'] = warehouse.id
            res['qty_available'] = float_round(qty_available, precision_rounding=product.uom_id.rounding)
            res['incoming_qty'] = float_round(moves_in_res.get(product.id, 0.0),
                                                          precision_rounding=product.uom_id.rounding)
            res['outgoing_qty'] = float_round(moves_out_res.get(product.id, 0.0),
                                                          precision_rounding=product.uom_id.rounding)
            res['virtual_available'] = float_round(qty_available + res['incoming_qty'] - res['outgoing_qty'],
                precision_rounding=product.uom_id.rounding)

            #获取补货规则里的最小数量
            domain_orderpoint = [('product_id','=',product.id),('warehouse_id','=',warehouse.id)]
            orders = self.env['stock.warehouse.orderpoint'].search(domain_orderpoint)

            #补货规则存在则添加显示
            if orders:
                res['product_min_qty'] = min(orders.mapped('product_min_qty'))

                #最小数大于与与预测数
                if int(res['product_min_qty']) > int(res['virtual_available']):
                    data.append(res)
        return data