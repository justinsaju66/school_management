
/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
var qweb = core.qweb;
var Dynamic = PublicWidget.Widget.extend({

selector: '.dynamic_snippet_blog',

willStart: async function() {

var self = this;

await rpc.query({

route: '/get_events',

}).then((data) => {

this.data = data;

});

},

start: function() {

var chunks = _.chunk(this.data, 4)

chunks[0].is_active = true

this.$el.find('#courosel').html(qweb.render('school_management.event_data', {chunks}))
},

PublicWidget.registry.dynamic_snippet_blog = Dynamic;
return Dynamic;
});
