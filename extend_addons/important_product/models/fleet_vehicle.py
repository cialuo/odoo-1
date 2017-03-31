# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, exceptions
from odoo.tools.translate import _

class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    component_ids = fields.One2many('product.component', 'parent_vehicle', string='Component')

class VehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'

    """
    车型管理加入要件控制
    """

    control_import = fields.Boolean(string='Control', default=False)
    product_lines = fields.One2many('vehicle.model.product', 'model_id', string='Product Line')

    def _vehicle_update_component(self, vehicles, update=True):
        """

        :param vehicles: 操作的车辆
        :param update: 是更新还是第一次分离部件
        :return:
        """
        com_obj = self.env['product.component']
        if update:
            a = self.product_lines.filtered(lambda x: x.is_update == True)
        else:
            a = self.product_lines
        for l in a:
            if l.product_id not in vehicles[0].mapped('component_ids').mapped('product_id'):
                lines = l.qty
            else:
                added_qty = len(vehicles[0].mapped('component_ids').filtered(lambda x: x.product_id == l.product_id))
                lines = l.qty - added_qty
            # if abs(lines) > 5:
            # 作为预留方案：如果执行过慢，后期根据数量修改
            #     raise exceptions.ValidationError(_(''))
            if lines > 0:
                # 数量增加，则增加部件清单
                for v in vehicles:
                    for line in range(lines):
                        com_obj.create({
                            'product_id': l.product_id.id,
                            'parent_vehicle': v.id,
                        })
            else:
                # 数量减少，则所有车辆对应的部件减少相应的部件清单（最近更新的清单）
                for v in vehicles:
                    all_component = v.mapped('component_ids').filtered(lambda x: x.product_id == l.product_id)
                    all_component[:abs(lines)].unlink()


    @api.multi
    def update_product_list(self):
        """
        根据车型的要件清单更新车型下面的所有车辆的重要部件清单
        :return:
        """
        self.ensure_one()
        vehicles = self.env['fleet.vehicle'].search([('model_id', '=', self.id)])
        if vehicles:
            self._vehicle_update_component(vehicles)
            self.product_lines.write({'is_update': False})
        else:
            raise exceptions.ValidationError(_('Not have any vehicles!'))
class ModelProduct(models.Model):
    _name = 'vehicle.model.product'

    """
    车型中的要件列表
    """

    model_id = fields.Many2one('fleet.vehicle.model', string='Vehicle Model')
    product_id = fields.Many2one('product.product', string='Product')
    uom_id = fields.Many2one(related='product_id.uom_id', string='Uom')
    description = fields.Text(related='product_id.description', string='Description')
    note = fields.Char(string='Note')
    qty = fields.Integer(string='Qty', default=1)
    default_code = fields.Char(related='product_id.default_code')
    is_update = fields.Boolean(string='Is Update', default=True)

    @api.multi
    def write(self, vals):
        """
        若数量改变，更新状态改为否
        :param vals:
        :return:
        """
        if vals.get('qty'):
            vals['is_update'] = True
        return super(ModelProduct, self).write(vals)
