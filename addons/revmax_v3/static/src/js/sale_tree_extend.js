/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
const rpc = require('web.rpc')
var Dialog = require('web.Dialog');

export class SaleListController extends ListController {

   setup() {
       super.setup();
   }
   open_day() {
    
    rpc.query({
        model: 'revmax_v3.zreport',
        method: 'open_fiscal_day',
        args : [[]]
        }).then(data => {
            const obj = JSON.parse(data);
            console.log(data);
            Dialog.confirm(
                this, obj.Message
             );
        });

           
   
   }
   close_day() {
    console.log("close Day")
    rpc.query({
        model: 'revmax_v3.zreport',
        method: 'open_fiscal_day',
        args : [[]]
        }).then(data => {
            const obj = JSON.parse(data);
            console.log(data);
            Dialog.confirm(
                this, obj.Message
             );  
        });


   }
   get_card_details() {
    
    rpc.query({
        model: 'revmax_v3.zreport',
        method: 'get_card_details',
        args : [[]]
        }).then(data => {
            const obj = JSON.parse(data);
            console.log(JSON.stringify(obj, null, 2));
            Dialog.confirm(
                this, JSON.stringify(obj, null, 2)
             );
        });

           
   
   }
}
registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: SaleListController,
   buttonTemplate: "button_sale.ListView.Buttons",
});