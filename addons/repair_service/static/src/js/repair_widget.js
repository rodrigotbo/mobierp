/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

/**
 * MobiERP Repair Service Widget
 * Custom widget for enhanced repair order functionality
 */
export class RepairServiceWidget extends Component {
    static template = "repair_service.RepairServiceWidget";

    setup() {
        super.setup();
        this.initializeWidget();
    }

    initializeWidget() {
        // Add custom initialization logic here
        console.log("MobiERP Repair Service Widget initialized");
    }

    /**
     * Quick action to mark repair as completed
     */
    async quickCompleteRepair() {
        const { model, resId } = this.props.record;
        if (model === 'repair.order' && resId) {
            await this.env.services.orm.call(
                'repair.order',
                'action_done',
                [[resId]]
            );
            this.env.services.notification.add(
                this.env._t("Repair marked as completed"),
                { type: 'success' }
            );
        }
    }

    /**
     * Quick print receipt
     */
    async quickPrintReceipt() {
        const { model, resId } = this.props.record;
        if (model === 'repair.order' && resId) {
            await this.env.services.orm.call(
                'repair.order',
                'action_print_receipt',
                [[resId]]
            );
        }
    }
}

// Register the widget
registry.category("view_widgets").add("repair_service_widget", RepairServiceWidget);