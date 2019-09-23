odoo.define('scan_mrp_product.barcode', function(require){
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var FieldChar = require('web.basic_fields').FieldChar;
    var rpc = require('web.rpc');
	var session = require('web.session');

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
                rpc.query({
					model: 'wizard.product.scan.dev.serial',
					method: 'scanbarcode_serial',
					args: [[], bar]
                    
                })
                .then(function (result){
					console.log(result);
					console.log('after array');
					if(!Array.isArray(result) || !result.length){
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
							}else{
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
						});
					}else{
						return self.do_action(result);
					}
                });
            }
        },

    });


	console.log(BarcodeSerial);
	
    fieldRegistry.add('BarcodeSerial', BarcodeSerial);
});