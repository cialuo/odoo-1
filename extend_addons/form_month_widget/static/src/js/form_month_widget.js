/**
 * Created by yineng on 2016-7-20.
 */
odoo.define('form_month_widget', function (require) {
    "use strict";
    var core = require('web.core'),
        form_common = require('web.form_common');
    var QWeb = core.qweb;

    var FieldMonth_Form = form_common.AbstractField.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.set("value", "");
        },
        start: function () {
            this.on("change:effective_readonly", this, function () {
                this.display_field();
                this.render_value();
            });
            this.display_field();
            return this._super();
        },
        display_field: function () {
            var self = this;
            this.$el.html(QWeb.render("FormMonth", {widget: this}));
            if (!this.get("effective_readonly")){
                this.$("input").datetimepicker({
                    format: 'YYYY-MM',
                    autoclose: true,
                    pickTime: false,
                    startViewMode: 1,
                    minViewMode: 1,
                    forceParse: false,
                    language: 'zh-CN'
                }).change(function() {
                    self.internal_set_value(self.$("input").val());
                });
            }
        },
        render_value: function () {
            if (this.get("effective_readonly")) {
                this.$el.text(this.get("value"));
            }
            else {
                if(this.get("value") == false){
                    this.$("input").val(this.get(""));
                }else{
                    this.$("input").val(this.get("value"));
                }
            }
        },

    });
    core.form_widget_registry.add('form_month', FieldMonth_Form);
    return {
        FieldMonth_Form: FieldMonth_Form,
    }
});
