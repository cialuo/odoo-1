# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lty_dsp_server_config(models.Model):
    _name = 'lty.dsp.server.config'
    _inherit = 'res.config.settings'

    @api.model_cr
    def get_latest_config(self):
        self._cr.execute('select name,port ,access_key from lty_dsp_server_config where id = (select max(id)  from lty_dsp_server_config)')
        dates = self._cr.fetchone()                
        return dates
    def get_ip_address(self):
        if self.get_latest_config() :
            return self.get_latest_config()[0]
    def get_port(self):
        if self.get_latest_config():
            return self.get_latest_config()[1]
    def get_access_key(self):
        if self.get_latest_config() :
            return self.get_latest_config()[2]    


    name = fields.Char('IP Address', required=False, default = get_ip_address )
    port = fields.Char('Port', required=False, default = get_port)
    access_key = fields.Char('Access Key', required=False, default = get_access_key)

