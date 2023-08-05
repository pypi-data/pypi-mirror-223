var _a;
import { Column as BkColumn, ColumnView as BkColumnView } from "@bokehjs/models/layouts/column";
import * as DOM from "@bokehjs/core/dom";
class ColumnView extends BkColumnView {
    connect_signals() {
        super.connect_signals();
        const { children, scroll_button_threshold } = this.model.properties;
        this.on_change(children, () => this.trigger_auto_scroll());
        this.on_change(scroll_button_threshold, () => this.toggle_scroll_button());
    }
    get distance_from_latest() {
        return this.el.scrollHeight - this.el.scrollTop - this.el.clientHeight;
    }
    scroll_to_latest() {
        // Waits for the child to be rendered before scrolling
        requestAnimationFrame(() => {
            this.el.scrollTop = this.el.scrollHeight;
        });
    }
    trigger_auto_scroll() {
        const limit = this.model.auto_scroll_limit;
        const within_limit = this.distance_from_latest <= limit;
        if (limit == 0 || !within_limit)
            return;
        this.scroll_to_latest();
    }
    toggle_scroll_button() {
        const threshold = this.model.scroll_button_threshold;
        const exceeds_threshold = this.distance_from_latest >= threshold;
        requestAnimationFrame(() => {
            this.scroll_down_button_el.classList.toggle("visible", threshold !== 0 && exceeds_threshold);
        });
    }
    render() {
        super.render();
        this.empty();
        this._update_stylesheets();
        this._update_css_classes();
        this._apply_styles();
        this._apply_visible();
        this.class_list.add(...this.css_classes());
        this.scroll_down_button_el = DOM.createElement('div', { class: 'scroll-button' });
        this.shadow_el.appendChild(this.scroll_down_button_el);
        this.el.addEventListener("scroll", () => {
            this.toggle_scroll_button();
        });
        this.scroll_down_button_el.addEventListener("click", () => {
            this.scroll_to_latest();
        });
        for (const child_view of this.child_views) {
            this.shadow_el.appendChild(child_view.el);
            child_view.render();
            child_view.after_render();
        }
    }
    after_render() {
        super.after_render();
        requestAnimationFrame(() => {
            if (this.model.view_latest) {
                this.scroll_to_latest();
            }
            this.toggle_scroll_button();
        });
    }
}
ColumnView.__name__ = "ColumnView";
export { ColumnView };
class Column extends BkColumn {
    constructor(attrs) {
        super(attrs);
    }
}
_a = Column;
Column.__name__ = "Column";
Column.__module__ = "panel.models.layout";
(() => {
    _a.prototype.default_view = ColumnView;
    _a.define(({ Int, Boolean }) => ({
        auto_scroll_limit: [Int, 0],
        scroll_button_threshold: [Int, 0],
        view_latest: [Boolean, false],
    }));
})();
export { Column };
//# sourceMappingURL=column.js.map