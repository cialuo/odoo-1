# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class BiddingDoc(models.Model):
    _name = 'bidding.doc'

    name = fields.Char(string='Doc name', required=True)
    code = fields.Char(string='Doc Code')
    attach_ids = fields.Many2many('ir.attachment', 'bidding_doc_attachment', id1='bidding_doc', id2='attach_id', string='Doc file')