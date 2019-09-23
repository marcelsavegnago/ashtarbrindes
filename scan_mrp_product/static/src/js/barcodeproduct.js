odoo.define('scan_mrp_product.BarcodeProduct', function(require){
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var FieldChar = require('web.basic_fields').FieldChar;
    var rpc = require('web.rpc');
	var session = require('web.session');

	var BarcodeProductSerial = fieldChar.extend({
		/*events: {
            'change': '_scanProductBarcode',
        },*/
		
		_scanProductBarcode: function (e) {
            self = this;
			console.log($(e.currentTarget).val());
        },
	});
	
	console.log(BarcodeProductSerial);
	
    fieldRegistry.add('BarcodeProductSerial', BarcodeProductSerial);
});