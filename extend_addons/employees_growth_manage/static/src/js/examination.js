odoo.define('roport.test', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var WebsocketTest = Widget.extend({
        template: 'RoportTest',
    });
core.action_registry.add('report.page', WebsocketTest);
return WebsocketTest;
});