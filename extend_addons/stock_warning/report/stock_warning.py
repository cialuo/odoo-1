
from odoo import api, models

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


