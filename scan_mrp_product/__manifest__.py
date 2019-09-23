{
    "name": "MRP Barcode Scan",
    "version": "11.0.1.0.0",
    "category": "Generic Modules",
    "author": "",
    "description": "",
    "website": "",
    "depends": [
        "mrp", "stock","barcodes"
    ],
    "data": [
		"security/ir.model.access.csv",
		"wizard/scan_mrp_barcode_view.xml",
		"wizard/scan_mrp_product.xml",
		"views/mrp_view.xml",
        "views/template.xml"
    ],
    "installable": True,
}