# -*- encoding: utf-8 -*-

import odoo
import odoo.modules.registry
import ast

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home


import base64
import datetime
import jinja2
import json
import logging
import os
import werkzeug.utils
import werkzeug.wrappers


import odoo
import odoo.modules.registry
from odoo.tools.misc import str2bool, xlwt
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, \
                      serialize_exception as _serialize_exception
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


#----------------------------------------------------------
# OpenERP Web web Controllers
#----------------------------------------------------------



path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
loader = jinja2.FileSystemLoader(path)

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps

db_monodb = http.db_monodb


class Home(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        cr = request.cr
        uid = odoo.SUPERUSER_ID
        param_obj = request.env['ir.config_parameter']
        request.params['disable_footer'] = ast.literal_eval(param_obj.get_param('login_form_disable_footer')) or False
        request.params['disable_database_manager'] = ast.literal_eval(param_obj.get_param('login_form_disable_database_manager')) or False

        request.params['banner_img_src'] = '/web_login/static/src/img/banner_img.png'
        request.params['background_img_src'] = '/web_login/static/src/img/background_img.jpg'
        request.params['login_img_src'] = '/web_login/static/src/img/login_img.png'
        # request.params['banner_img_offset_src'] = 'col-md-offset-0'
        # request.params['login_dialog_offset_src'] = 'col-md-offset-0'
        # request.params['font-size'] = '14px'
        request.params['header_height_src'] = '10%'
        request.params['footer_height_src'] = '15%'
        request.params['body_login_height_src'] = '75%'
        val=request.env['login_config_settings'].sudo().search([('state', '=', 'using')], limit=1, order="id desc")
        if val:
            # request.params['banner_img_src'] = val.banner_img_src
            if val.background_img_src:
                request.params['background_img_src'] = 'data:image/jpeg;base64,'+val.background_img_src
            if val.login_img_src:
                request.params['login_img_src'] = 'data:image/jpeg;base64,'+val.login_img_src
            # request.params['banner_img_offset_src'] = val.banner_img_offset_src
            # request.params['login_dialog_offset_src'] = val.login_dialog_offset_src
            request.params['header_height_src'] = str(val.header_height_src)+'%'
            request.params['footer_height_src'] = str(val.footer_height_src)+'%'
            request.params['body_login_height_src'] = str(val.body_login_height_src)+'%'

        return super(Home, self).web_login(redirect, **kw)


    def _render_template(self, **d):
        d.setdefault('manage',True)
        d['insecure'] = odoo.tools.config['admin_passwd'] == 'admin'
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        # databases list
        d['databases'] = []
        try:
            d['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            monodb = db_monodb()
            if monodb:
                d['databases'] = [monodb]
        return env.get_template("database_manager2.html").render(d)

    @http.route('/web/database/selector', type='http', auth="none")
    def selector(self, **kw):
        return self._render_template(manage=False)

    @http.route('/web/database/manager', type='http', auth="none")
    def manager(self, **kw):
        return self._render_template()

    @http.route('/web/database/create', type='http', auth="none", methods=['POST'], csrf=False)
    def create(self, master_pwd, name, lang, password, **post):
        try:
            # country code could be = "False" which is actually True in python
            country_code = post.get('country_code') or False
            dispatch_rpc('db', 'create_database', [master_pwd, name, bool(post.get('demo')), lang, password, post['login'], country_code])
            request.session.authenticate(name, post['login'], password)
            return http.local_redirect('/web/')
        except Exception, e:
            error = "Database creation error: %s" % e
        return self._render_template(error=error)

    @http.route('/web/database/duplicate', type='http', auth="none", methods=['POST'], csrf=False)
    def duplicate(self, master_pwd, name, new_name):
        try:
            dispatch_rpc('db', 'duplicate_database', [master_pwd, name, new_name])
            return http.local_redirect('/web/database/manager')
        except Exception, e:
            error = "Database duplication error: %s" % e
            return self._render_template(error=error)

    @http.route('/web/database/drop', type='http', auth="none", methods=['POST'], csrf=False)
    def drop(self, master_pwd, name):
        try:
            dispatch_rpc('db','drop', [master_pwd, name])
            request._cr = None  # dropping a database leads to an unusable cursor
            return http.local_redirect('/web/database/manager')
        except Exception, e:
            error = "Database deletion error: %s" % e
            return self._render_template(error=error)

    @http.route('/web/database/backup', type='http', auth="none", methods=['POST'], csrf=False)
    def backup(self, master_pwd, name, backup_format = 'zip'):
        try:
            odoo.service.db.check_super(master_pwd)
            ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            filename = "%s_%s.%s" % (name, ts, backup_format)
            headers = [
                ('Content-Type', 'application/octet-stream; charset=binary'),
                ('Content-Disposition', content_disposition(filename)),
            ]
            dump_stream = odoo.service.db.dump_db(name, None, backup_format)
            response = werkzeug.wrappers.Response(dump_stream, headers=headers, direct_passthrough=True)
            return response
        except Exception, e:
            _logger.exception('Database.backup')
            error = "Database backup error: %s" % e
            return self._render_template(error=error)

    @http.route('/web/database/restore', type='http', auth="none", methods=['POST'], csrf=False)
    def restore(self, master_pwd, backup_file, name, copy=False):
        try:
            data = base64.b64encode(backup_file.read())
            dispatch_rpc('db', 'restore', [master_pwd, name, data, str2bool(copy)])
            return http.local_redirect('/web/database/manager')
        except Exception, e:
            error = "Database restore error: %s" % e
            return self._render_template(error=error)

    @http.route('/web/database/change_password', type='http', auth="none", methods=['POST'], csrf=False)
    def change_password(self, master_pwd, master_pwd_new):
        try:
            dispatch_rpc('db', 'change_admin_password', [master_pwd, master_pwd_new])
            return http.local_redirect('/web/database/manager')
        except Exception, e:
            error = "Master password update error: %s" % e
            return self._render_template(error=error)

    @http.route('/web/database/list', type='json', auth='none')
    def list(self):
        """
        Used by Mobile application for listing database
        :return: List of databases
        :rtype: list
        """
        return http.db_list()

