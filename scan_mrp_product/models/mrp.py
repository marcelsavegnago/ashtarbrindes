# -*- coding: utf-8 -*-
from odoo import api, fields, models,tools
from odoo.exceptions import UserError
from odoo.tools.translate import _

class MRPProduction(models.Model):   
	_inherit = "mrp.production"
	
	@api.multi
	def scan_dev_wizard(self):
		scan_dev_form_wiz = self.env.ref('scan_mrp_product.scan_product_form_dev_wizard', False)
		
		ctx = dict(
			default_mrp_id=self.id
		)
		return {
			'name': _('Scan Serials'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'wizard.product.scan.dev.serial',
			'views': [(scan_dev_form_wiz.id, 'form')],
			'view_id': scan_dev_form_wiz.id,
			'context': ctx,
			'target': 'new',
		}