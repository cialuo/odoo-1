# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import time
import odoo


class SalaryCompute(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_worked_day_lines(self, contract_ids, date_from, date_to):
        """
        重载父类 get_worked_day_lines
        """
        res = []

        # fill only if the contract as a working schedule linked
        for contract in self.env['hr.contract'].browse(contract_ids).filtered(lambda contract: contract.working_hours):
            attendances = {
                'name': _("Normal Working Days paid at 100%"),
                'sequence': 1,
                'code': 'WORK100',
                'number_of_days': 0.0,
                'number_of_hours': 0.0,
                'contract_id': contract.id,
            }
            day_from = fields.Datetime.from_string(date_from)
            day_to = fields.Datetime.from_string(date_to)
            nb_of_days = (day_to - day_from).days + 1
            for day in range(0, nb_of_days):
                working_hours_on_day = contract.working_hours.working_hours_on_day(day_from + timedelta(days=day))
                if working_hours_on_day:
                    # the employee had to work
                    attendances['number_of_days'] += 1.0
                    attendances['number_of_hours'] += working_hours_on_day

            leaves = {}
            constrains = [
                ('state', '=', 'validate'),
                ('employee_id', '=', contract.employee_id.id),
                ('type', '=', 'remove'),
                ('date_from', '<=', date_to),
                ('date_to', '>=',date_from)
            ]
            leaveRecords = self.env['hr.holidays'].search(constrains)
            leaveTotalHour = 0
            for item in leaveRecords:
                leave_type = item.holiday_status_id.name
                leave_type_name = item.holiday_status_id.namestr
                if leave_type in leaves:
                    leaves[leave_type]['number_of_hours'] += item.length
                else:
                    leaves[leave_type] = {
                        'name': leave_type_name,
                        'sequence': 5,
                        'code': leave_type,
                        'number_of_days': 0.0,
                        'number_of_hours': item.length,
                        'contract_id': contract.id,
                    }
                leaveTotalHour += item.length
            leaves = [value for key, value in leaves.items()]
            attendances['number_of_hours'] -= leaveTotalHour
            res = [attendances] + leaves
        return res

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return

        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to

        monthAndYear = datetime.fromtimestamp(time.mktime(time.strptime(date_from, "%Y-%m-%d"))).strftime('%Y-%m-01')

        if date_from > date_to:
            raise ValidationError(_("Payslip 'Date From' must be before 'Date To'."))

        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(date_from, "%Y-%m-%d")))
        self.name = _('Salary Slip of %s for %s') % (employee.name, tools.ustr(ttyme.strftime('%Y-%m')))

        date_from_china = datetime.fromtimestamp(time.mktime(time.strptime(date_from, "%Y-%m-%d"))) - timedelta(hours=8)
        date_to_china = datetime.fromtimestamp(time.mktime(time.strptime(date_to, "%Y-%m-%d"))) - timedelta(hours=8)
        date_from = date_from_china.strftime(odoo.tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
        date_to = date_to_china.strftime(odoo.tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)

        self.company_id = employee.company_id

        if not self.env.context.get('contract') or not self.contract_id:
            contract_ids = self.get_contract(employee, date_from, date_to)
            if not contract_ids:
                return
            self.contract_id = self.env['hr.contract'].browse(contract_ids[0])

        if not self.contract_id.struct_id:
            return
        self.struct_id = self.contract_id.struct_id
        contractToUse = [self.contract_id.id]
        # computation of the salary input
        worked_days_line_ids = self.get_worked_day_lines(contractToUse, date_from, date_to)
        worked_days_lines = self.worked_days_line_ids.browse([])
        for r in worked_days_line_ids:
            worked_days_lines += worked_days_lines.new(r)
        self.worked_days_line_ids = worked_days_lines

        input_line_ids = self.get_inputs(contractToUse, date_from, date_to)
        input_lines = self.input_line_ids.browse([])
        absenceLines = self.getAbsenceData(monthAndYear, employee.id, self.contract_id.id)
        input_line_ids += [absenceLines]
        for r in input_line_ids:
            input_lines += input_lines.new(r)
        self.input_line_ids = input_lines
        return

    @api.model
    def getAbsenceData(self, date, employee_id, constract_id):
        constrains = [
            ('employee_id', '=', employee_id),
            ('month', '=', date),
        ]
        absence = self.env['employee.attencededucted'].search(constrains, limit=1)
        if absence:
            return {
                'name': _('absence record'),
                'code': 'KQKK',
                'amount': absence.deducted,
                'contract_id': constract_id,
            }
