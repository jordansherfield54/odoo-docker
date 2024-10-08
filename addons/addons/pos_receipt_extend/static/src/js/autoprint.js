odoo.define('pos_receipt_extend.CustomPrintReceipt', function(require) {
    "use strict";
    const rpc = require('web.rpc');
    const PosModel = require('point_of_sale.models'); // Import the model where _printReceipt is defined
    const Registries = require('point_of_sale.Registries');
    const OrderReceipt = require('point_of_sale.ReceiptScreen'); // Assuming it's defined in OrderReceipt

    const CustomOrderReceipt = OrderReceipt => class extends OrderReceipt {
        async _printReceipt() {
            console.log("Custom Print Receipt Logic");
            async function fetchAndProcessInvoiceData(receipt_number) {
                try {
                    const result = await rpc.query({
                        model: 'pos.order',
                        method: 'get_invoice',
                        args: [receipt_number]
                    });

                    // Destructure relevant data from result
                    const {
                        message,
                        qr_code,
                        invoice_name,
                        deviceid,
                        verification_code,
                        fiscalday,
                        usdbp,
                        zwlbp,
                        zwlvat
                    } = result;

                    // Check if the message contains 'Success'
                    if (message.includes('Success')) {
                        console.log('Success!');
                    } else {
                        console.error(message);
                        alert(message);
                        // resetPosValues(); // Reset POS values if the message is not 'Success'
                        return;
                    }

                    // Generate QR code SVG
                    const qr_code_svg = generateQRCode(qr_code);
                    // updatePosData({
                    //     message,
                    //     qr_code_svg,
                    //     invoice_name,
                    //     deviceid,
                    //     verification_code,
                    //     fiscalday,
                    //     usdbp,
                    //     zwlbp,
                    //     zwlvat
                    // });

                } catch (error) {
                    console.error("Error fetching invoice data:", error);
                    alert("Error occurred while processing the invoice.");
                    // resetPosValues(); // Reset POS values on any exception
                }
            }

            // Helper function to generate the QR code SVG
            function generateQRCode(address) {
                const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter();
                const qr_code_svg = new XMLSerializer().serializeToString(codeWriter.write(address, 150, 150));
                return "data:image/svg+xml;base64," + window.btoa(qr_code_svg);
            }

            // Helper function to update POS data
            function updatePosData({
                message,
                qr_code_svg,
                invoice_name,
                deviceid,
                verification_code,
                fiscalday,
                usdbp,
                zwlbp,
                zwlvat
            }) {
                const pos = this.env.pos;
                pos.message = message;
                pos.qr_image = qr_code_svg;
                pos.invoice = invoice_name;
                pos.deviceid = deviceid;
                pos.verification_code = verification_code;
                pos.fiscalday = fiscalday;
                pos.usdbp = usdbp;
                pos.zwlbp = zwlbp;
                pos.zwlvat = zwlvat;
            }

            // Helper function to reset POS values to null
            function resetPosValues() {
                const pos = this.env.pos;
                pos.message = null;
                pos.qr_image = null;
                pos.invoice = null;
                pos.deviceid = null;
                pos.verification_code = null;
                pos.fiscalday = null;
                pos.usdbp = null;
                pos.zwlbp = null;
                pos.zwlvat = null;
            }

            // Call the function
            const receipt_number = this.env.pos.selectedOrder.name;
            // debugger;
            await fetchAndProcessInvoiceData(receipt_number);


            if (this.env.proxy.printer) {
                const printResult = await this.env.proxy.printer.print_receipt(this.orderReceipt.el.innerHTML);
                if (printResult.successful) {
                    return true;
                } else {
                    const {
                        confirmed
                    } = await this.showPopup('ConfirmPopup', {
                        title: printResult.message.title,
                        body: 'Do you want to print using the web printer?',
                    });
                    if (confirmed) {
                        await nextFrame();
                        return await this._printWeb();
                    }
                    return false;
                }
            } else {
                return await this._printWeb();
            }
        }
    };

    Registries.Component.extend(OrderReceipt, CustomOrderReceipt);

    return OrderReceipt;
});