odoo.define('scan_mrp_product.barcode', function(require){
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var FieldChar = require('web.basic_fields').FieldChar;
    var rpc = require('web.rpc');
    var KanbanView = require('web.KanbanView');
    var FormView = require('web.FormView');
	var session = require('web.session');
    var viewRegistry = require('web.view_registry');

    var KanbanBarcode = KanbanView.extend({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            this.loadBarcodeWizard();
        },
        loadBarcodeWizard: function (){
            console.log("======init=====yes called===========");
            setTimeout(function() { $('a[data-menu-xmlid="scan_mrp_product.menu_mrp_barcode_scan"]').click();}, 1000);
        }
    });
    var FormViewBarcode = FormView.extend({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
	    console.log("=======formView=======");
            this.loadFormBarcodeWizard();
        },
        loadFormBarcodeWizard: function (){
            console.log("======init=====yes called=====loadFormBarcodeWizard======");
            setTimeout(function() { $('button[name="scan_dev_wizard"]').click();}, 1500);
        }
    });

    var BarcodeSerial = FieldChar.extend({
        events: {
            'change': '_scanBarcode',
        },

        OpenMRPForm: function(e) {
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'mrp.production',
                res_id: e[0],
                views: [[false, 'form']],
                target: 'current'
            });
        },

        _scanBarcode: function (e) {
            self = this;
            var domain = [['name', '=', $(e.currentTarget).val()]];
			var bar = $(e.currentTarget).val();
            
            if ($(e.currentTarget).val()){
				//check for workorders
				rpc.query({
					model: 'mrp.production',
					method: 'search',
					args: [domain],
				})
				.then(function (result){
					console.log("mrp phase");
					console.log(result);
					console.log(result.length);
					if(result.length == 0){
						console.log("show error");
						return self.do_action({'type': 'ir.actions.client','tag': 'action_warn','name': 'Warning','params': {'title': 'Warning!','text': 'Barcode not found in system!',  'sticky': true}});
					}else{
						console.log('opening mrp form');
						self.OpenMRPForm(result);
						
					}
				});
					
            }
        },

    });

    var OperationWidget = FieldChar.extend({
        events: {
            'change': '_scanBarcode',
        },

        _scanBarcode: function (e) {
            self = this;
            var domain = [['name', '=', $(e.currentTarget).val()]];
            var bar = $(e.currentTarget).val();
            console.log("========OperationWidget======");
            if ($(e.currentTarget).val()){
                //check for workorders
                rpc.query({
                    model: 'wizard.mrp.scan.dev.serial',
                    method: 'scanwrk_serial',
                    args: [[], bar]
                })
                .then(function (result){
                    console.log("workorder array");
                    console.log(result);
                    if(result != false){
                        console.log('open view' + $(e.currentTarget).val());
                        return self.do_action(result);
                    }
                });
            }
        },

    });


	console.log(BarcodeSerial);
	
    fieldRegistry.add('BarcodeSerial', BarcodeSerial);
    fieldRegistry.add('OperationWidget', OperationWidget);
    viewRegistry.add('KanbanBarcodeScan', KanbanBarcode);
    viewRegistry.add('FormViewBarcode', FormViewBarcode);

});
