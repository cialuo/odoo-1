# -*- coding: utf-8 -*-
# © 2016 Vividlab (<http://www.vividlab.de>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Web Ascending Sequence",
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
        "views/web_widget_ascending_sequence.xml",
    ],
    'qweb': ['static/src/xml/*.xml'],
}
