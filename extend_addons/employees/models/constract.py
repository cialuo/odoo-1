from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Constract(models.Model):
    _inherit = "hr.contract"

    @api.constrains('trial_date_start', 'trial_date_end')
    def _check_trial_dates(self):
        if self.filtered(lambda c: c.trial_date_end and c.trial_date_start > c.trial_date_end):
            raise ValidationError(_('trial start date must be less than contract end date.'))