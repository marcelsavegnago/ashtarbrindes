from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class WizardProductSerial(models.TransientModel):
	_name = 'wizard.product.scan.dev.serial'
	_description = 'Scan ProductSerial'

	serial = fields.Char(required=True, string='Barcode')
	mrp_id = fields.Many2one('mrp.production')
	text = fields.Char()
	
	@api.onchange('serial')
	def scanbarcode_serial(self):
		barcode = self.serial
		if barcode:
			#search for serial in stock.production.lot
			product = self.env['product.product'].search([('barcode', '=', barcode)])
			move_line = self.mrp_id.move_raw_ids.filtered(lambda r: r.product_id.id == product.id)
			
			if move_line:
				if not move_line[0].barcode_scan:
					self.env['stock.move.line'].create(move_line[0]._prepare_move_line_vals(quantity=move_line[0].product_uom_qty))
					move_line[0].write({
						'barcode_scan': True,
						'state': 'assigned',
					})
			# else:
			# 	raise UserError("Product doesn't exist")
				#return False
				
			all_scanned = self.mrp_id.move_raw_ids.filtered(lambda r: r.product_uom_qty <= r.reserved_availability)
			if len(all_scanned) == len(self.mrp_id.move_raw_ids):
				if self.mrp_id.state == 'confirmed' and self.mrp_id.routing_id:
					self.mrp_id.button_plan()
				elif self.mrp_id.state == 'confirmed':
					mrp_produce_obj = self.env['mrp.product.produce']
					produce_fields = mrp_produce_obj.fields_get()
					pro_def_val = mrp_produce_obj.with_context(active_id=self.mrp_id.id).default_get(produce_fields)
					new_val = pro_def_val.copy()
					_logger.info('>>>>>>>>>>>> %s', new_val)
					produce = self.env['mrp.product.produce'].create(new_val)
					produce._onchange_product_qty()
					#self.mrp_id.open_produce_product()
					self.mrp_id.write({
						'check_to_done': True,
					})
					produce.do_produce()
					self.write({
						'text': 'all products scanned!',
					})
					return {'type': 'ir.actions.act_window_close'}
			#referesh 
			self.serial = ''

	"""@api.multi
	def scanbarcode_serial(self, barcode):
		print("==========barcode======",barcode)
		if barcode:
			#search for serial in stock.production.lot
			product = self.env['product.product'].search([('barcode', '=', barcode)])
			
			move_line = self.mrp_id.move_raw_ids.filtered(lambda r: r.product_id.id == product.id)
			all_scanned = self.mrp_id.move_raw_ids.filtered(lambda r: r.barcode_scan == False)
			
			if not all_scanned:
				raise UserError("All Product Scanned")
			elif move_line:
				if not move_line[0].barcode_scan:
					self.env['stock.move.line'].create(move_line[0]._prepare_move_line_vals(quantity=move_line[0].product_uom_qty))
					move_line[0].write({
						'barcode_scan': True,
						'state': 'assigned',
					})
					return True
			else:
				raise UserError("Product doesn't exist")
			#referesh 
			self.serial = ''"""
			
class StockMove(models.Model):
	_inherit='stock.move'
	
	barcode_scan = fields.Boolean(default=False)