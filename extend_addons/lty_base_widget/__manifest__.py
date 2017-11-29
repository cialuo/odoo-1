# -*- coding: utf-8 -*-
# © 2016 Vividlab (<http://www.vividlab.de>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "lty widget buckets",
    "version": "1.0",
    "author": "VividLab, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Web",
    "website": "http://www.vividlab.de",
    'installable': True,
    "depends": [
        "web",
    ],
    "data": [
        "views/lty_base_widget_tep.xml",
    ],
    'qweb': ['static/src/xml/*.xml'],
}
