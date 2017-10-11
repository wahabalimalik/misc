odoo.define('lotto', function (require) {
"use strict";

var core = require('web.core');
var Widget = require('web.Widget');
var Model = require('web.Model');
var session = require('web.session');
var PlannerCommon = require('web.planner.common');
var framework = require('web.framework');
var webclient = require('web.web_client');
var PlannerDialog = PlannerCommon.PlannerDialog;

var QWeb = core.qweb;
var _t = core._t;

var Dashboard_Lotto = Widget.extend({
    template: 'DashboardMainLotto',

    init: function(parent, data){
        this.all_dashboards = ['apps_lotto'];
        return this._super.apply(this, arguments);
    },

    start: function(){
        return this.load(this.all_dashboards);
    },

    load: function(dashboards){
        var self = this;
        var loading_done = new $.Deferred();
        session.rpc("/web_settings_dashboard/data", {}).then(function (data) {
            // Load each dashboard
            var all_dashboards_defs = [];
            _.each(dashboards, function(dashboard) {
                var dashboard_def = self['load_' + dashboard](data);
                if (dashboard_def) {
                    all_dashboards_defs.push(dashboard_def);
                }
            });

            // Resolve loading_done when all dashboards defs are resolved
            $.when.apply($, all_dashboards_defs).then(function() {
                loading_done.resolve();
            });
        });
        return loading_done;
    },

    load_apps: function(data){
        return  new DashboardApps(this, data.apps).replace(this.$('.o_web_settings_dashboard_apps'));
    },

    load_share: function(data){
        return new DashboardShare(this, data.share).replace(this.$('.o_web_settings_dashboard_share'));
    },

    load_invitations: function(data){
        return new DashboardInvitations(this, data.users_info).replace(this.$('.o_web_settings_dashboard_invitations'));
    },

    load_planner: function(data){
        return  new DashboardPlanner(this, data.planner).replace(this.$('.o_web_settings_dashboard_planner'));
    },
});

core.action_registry.add('lotto.main', Dashboard);

return {
    Dashboard_Lotto: Dashboard_Lotto,
};

});
