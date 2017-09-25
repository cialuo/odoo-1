# -*- coding:utf-8 -*-

class UpDateConstract():

    def __init__(self, model):
        self.model = model

    def getCurrentConstract(self, employee_id):
        constracts = self.model._env['hr.contract'].search([('employee_id', '=', employee_id),
                                                            ('state', '=', 'open')])
        if len(constracts) == 0:
            return None
        else:
            return constracts[0]

    def changeBaseSalary(self, salary, constract):
        constract.write({'wage':salary})