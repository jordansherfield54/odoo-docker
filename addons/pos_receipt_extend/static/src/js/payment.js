odoo.define('pos_receipt_extend.PaymentScreen', function(require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const {
        onMounted
    } = owl;

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            this.currentOrder.set_to_invoice(true);
        }
        async validateOrder(isForceValidate) {
            // debugger;
            const receipt_order = await super.validateOrder(...arguments);
            const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter();
            var receipt_number = this.env.pos.selectedOrder.name;
            var self = this;

            rpc.query({
                model: 'pos.order',
                method: 'get_invoice',
                args: [receipt_number]
            }).then(function(result) {
                self.env.pos.message = result.message
                try {
                    if (result.message.includes('Success')) {
                        // Perform a specific action
                        console.log('Success!');
                    } else {
                        console.error(result.message)
                        alert(result.message)
                    }
                    const address = result.qr_code
                    let qr_code_svg = new XMLSerializer().serializeToString(codeWriter.write(address, 150, 150));
                    self.env.pos.qr_image = "data:image/svg+xml;base64," + window.btoa(qr_code_svg);
                    self.env.pos.invoice = result.invoice_name
                    self.env.pos.deviceid = result.deviceid
                    self.env.pos.verification_code = result.verification_code
                    self.env.pos.fiscalday = result.fiscalday
                    self.env.pos.usdbp = result.usdbp
                    self.env.pos.zwlbp = result.zwlbp
                    self.env.pos.zwlvat = result.zwlvat
                } catch (error) {
                    console.error(result.message);
                    console.error(error);
                    alert(result.message);
                };

                return receipt_order
            });
        };
    };
    Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);

    return PaymentScreen;
});