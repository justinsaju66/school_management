/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

function chunkArray(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
        chunks.push(array.slice(i, i + size));
    }
    return chunks;
}

publicWidget.registry.get_property_tab = publicWidget.Widget.extend({
    selector : '.categories_section',
    async willStart() {
        const result = await rpc('/get_events', {});
        if(result && result.events){
            const chunks = chunkArray(result.events, 4);
            chunks[0].is_active = true
            const uniq = Date.now()
            this.$target.empty().html(renderToElement('school_management.event_data', {
                event_chunks: chunks,
                uniq : uniq,

            }));
        }
    },
});