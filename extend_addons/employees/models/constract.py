# -*-encoding:utf-8-*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Constract(models.Model):
    _inherit = "hr.contract"

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,ondelete='restrict')

    @api.constrains('trial_date_start', 'trial_date_end')
    def _check_trial_dates(self):
        if self.filtered(lambda c: c.trial_date_end and c.trial_date_start > c.trial_date_end):
            raise ValidationError(_('trial start date must be less than contract end date.'))

    def searchRunningConstract(self):
        opendlist = self.search([('employee_id', '=', self.employee_id.id),('state', '=', 'open')])
        if len(opendlist) > 1:
            raise ValidationError('一个员工只能有一份执行状态的合同')

    @api.one
    @api.constrains('state')
    def _check_status(self):
        """
        现在一个员工合同 同一时间只有一个执行中的合同
        """
        if self.state == 'open':
            self.searchRunningConstract()

    @api.onchange('employee_id')
    def autoUpdateBaseSalary(self):
        """
        根据所选员工自动修改相应的员工所在岗位的基本工资
        :return:
        """
        if self.employee_id.workpost == False:
            return
        if self.employee_id.workpost.postlevel == False:
            return
        self.wage = self.employee_id.workpost.postlevel.basesalary

    # @api.onchange('state')
    # def changerelatedemployee(self):
    #     if self.state == "open":
    #         self.employee_id.bargain = self.id

    @api.multi
    def write(self, vals):
        res = super(Constract, self).write(vals)
        if self.state == "open":
            self.employee_id.bargain_id = self.id
        return res

class PostLevel(models.Model):

    _name = "employeepost.level"

    # 岗位基础薪资
    basesalary = fields.Float(string="post base salary", required=True)

    # 关联的岗位
    relatedpost = fields.One2many('employees.post', 'postlevel', string="related post salary")

    # 名称
    name = fields.Char(string="post level name", required=True)

    @api.one
    @api.constrains('basesalary')
    def _check_basesalary(self):
        if self.basesalary <=0 :
            raise ValidationError(_("base salary must bigger then 0"))


