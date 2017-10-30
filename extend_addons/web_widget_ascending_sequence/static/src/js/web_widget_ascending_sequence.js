odoo.define('web_widget_ascendingSequence', function (require) {
    "use strict";

    var core = require('web.core');
    var formats = require('web.formats');
    var common = require('web.form_common');    

    var ascendingSequence = common.AbstractField.extend(common.ReinitializeFieldMixin, {
        is_field_number: true,        
        template: "ascendingSequence",
        internal_format: 'integer',
        widget_class: 'oe_form_field_sequence',
        events: {
            'change input': 'store_dom_value',
            'focus input': 'store_dom_value_2',
        },
        init: function (field_manager, node) {
            this._super(field_manager, node);
            
            this.internal_set_value(0);
        },
        initialize_content: function() {
            if(!this.get("effective_readonly")) {                    
                this.setupFocus(this.$('input'));
            }
        },
        is_syntax_valid: function() {
            if (!this.get("effective_readonly") && this.$("input").size() > 0) {
                try {
                    this.parse_value(this.$('input').val(),'');
                    return true;
                } catch(e) {
                    return false;
                }
            }
            return true;
        },
        is_false: function() {
            return this.get('value') === '' || this._super();
        },
        focus: function() {
            var input = this.$('input:first')[0];
            return input ? input.focus() : false;
        },
        set_dimensions: function (height, width) {
            this._super(height, width);
            this.$('input').css({
                height: height,
                width: width
            });
        },                        
        store_dom_value: function () {
            if (!this.get('effective_readonly')) {
                this.internal_set_value(
                    this.parse_value(
                        this.$('input').val(),''));
            }
        },
        store_dom_value_2: function () {
            if (!this.get('effective_readonly')) {
                this.internal_set_value(
                    this.parse_value(
                        this.$('input').val(),''));
            }
        },
        parse_value: function(val, def) {
            return formats.parse_value(val, {"widget": this.internal_format}, def);  
        },
        format_value: function(val, def) {
            return formats.format_value(val, {"widget": this.internal_format}, def);
        },
        render_value: function() {
            var self = this;
            var init_value = self.get('value');
            var show_value = init_value;
            if (!init_value){
                show_value = self.ascending_add();
            }

            if (!self.get("effective_readonly")) {
                self.$input = self.$el.find('input');
                self.$input.val(show_value);
            } else {
                self.$(".oe_form_time_content").text(show_value);
            }
        },
        ascending_add: function(){
            var self = this;
            var i_index = 'empty';
            var ascending_index = 1;
            _.each(self.$el.parent()[0].children, function(o_children, o_index){
                if (o_children == self.$el[0]){
                    i_index = o_index;
                    return false;
                }
            })

            console.log(i_index);

            if (i_index!="empty"){
                var tr_list = self.$el.parent().next().find("table tbody tr");
                _.each(tr_list, function(o_tr){
                    if (o_tr.getAttribute("data-id") && o_tr.getAttribute("data-id")!="false"){
                        var td_list = o_tr.children;
                        for (var i=0,l=td_list.length;i<l;i++){
                            if (i == i_index){
                                var o_td = td_list[i];
                                var td_v = o_td.textContent;
                                if (!isNaN(td_v) && parseInt(td_v)>=ascending_index){
                                    ascending_index = parseInt(td_v) + 1;
                                }
                            }
                        }
                    }
                })

                return ascending_index;
            }else{
                return ascending_index;
            }
        }
    });

    core.form_widget_registry.add('sequence', ascendingSequence);

    return {
        ascendingSequence: ascendingSequence,    
    };
});
