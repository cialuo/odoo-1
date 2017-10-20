odoo.define('nvd3_extend.GraphWidget', function (require) {
    "use strict";
    var config = require('web.config');
    var core = require('web.core');
    var Model = require('web.DataModel');
    var formats = require('web.formats');
    var Widget = require('web.Widget');
    var GraphWidget = require('web.GraphWidget');

    GraphWidget.include({
        display_pie1: function () {
            var data = [],
                all_negative = true,
                some_negative = false,
                all_zero = true;

            this.data.forEach(function (datapt) {
                all_negative = all_negative && (datapt.value < 0);
                some_negative = some_negative || (datapt.value < 0);
                all_zero = all_zero && (datapt.value === 0);
            });
            if (some_negative && !all_negative) {
                return this.$el.append(QWeb.render('GraphView.error', {
                    title: _t("Invalid data"),
                    description: _t("Pie chart cannot mix positive and negative numbers. " +
                        "Try to change your domain to only display positive results"),
                }));
            }
            if (all_zero) {
                return this.$el.append(QWeb.render('GraphView.error', {
                    title: _t("Invalid data"),
                    description: _t("Pie chart cannot display all zero numbers.. " +
                        "Try to change your domain to display positive results"),
                }));
            }
            if (this.groupbys.length) {
                data = this.data.map(function (datapt) {
                    return {x:datapt.labels.join("/"), y: datapt.value};
                });
            }
            var svg = d3.select(this.$el[0]).append('svg');
            svg.datum(data);

            svg.transition().duration(100);

            var legend_right = config.device.size_class > config.device.SIZES.XS;

            var chart = nv.models.pieChart();
            chart.options({
              delay: 250,
              pieLabelsOutside:true,
              donut: true,
              showLegend: legend_right || _.size(data) <= MAX_LEGEND_LENGTH,
              legendPosition: legend_right ? 'right' : 'top',
              transition: 100,
              color: d3.scale.category10().range(),
            });

            chart(svg);
            this.to_remove = chart.update;
            nv.utils.onWindowResize(chart.update);
        },
    })
});