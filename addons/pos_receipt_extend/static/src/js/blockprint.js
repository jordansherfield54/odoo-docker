odoo.define('pos_receipt_extend.PrintReceiptRestriction', function (require) {
    'use strict';

    const AbstractReceiptScreen = require('point_of_sale.AbstractReceiptScreen');  // Import the correct base class
    const ReceiptScreen = require('point_of_sale.ReceiptScreen');  // Import the ReceiptScreen
    const Registries = require('point_of_sale.Registries');

    const CustomReceiptScreen = class extends ReceiptScreen {
        // Override the method that shows the "Print Receipt" button
        mounted() {
            super.mounted();
            console.log("PrintReceiptRestriction module is loaded");

            // Use RPC to check if the user belongs to the 'Point of Sale Administrator' group
            this.env.services.rpc({
                model: 'res.users',
                method: 'has_group',
                args: ['point_of_sale.group_pos_manager'],
            }).then(isPosAdmin => {
                if (!isPosAdmin) {
                    const printButton = this.el.querySelector('.actions');  // Adjust the selector to target your button
                    if (printButton) {
                        printButton.style.display = 'none';  // Hide the button
                    }
                }
            }).catch(err => {
                console.error('Error checking user group:', err);
            });
        }
    };

    // Register the CustomReceiptScreen in the POS Registries
    Registries.Component.extend(ReceiptScreen, CustomReceiptScreen);

    return CustomReceiptScreen;
});
