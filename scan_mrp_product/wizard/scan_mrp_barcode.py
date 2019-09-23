from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class WizardMRPSerial(models.TransientModel):
	_name = 'wizard.mrp.scan.dev.serial'
	_inherit = 'barcodes.barcode_events_mixin'
	_description = 'Scan ProductSerial'

	serial = fields.Char(required=True, string='Barcode')
  
	def scanwrk_serial(self, barcode):
		#search mrp
		workcenter = False
		if barcode:
			s = barcode.split('-')
			_logger.info('================ %s ==========', s)
			if len(s) > 0:
				_logger.info('>>>>>>> workcenter id %s=========', s[0])
				workcenter = self.env['mrp.workorder'].search([('id', '=', s[0])])
				_logger.info('>>>>>>> workcenter %s >>>>>>>>>>>>', workcenter)
				# _logger.info('>>>>>>> workcenter2 %s >>>>>>>>>>>>', workcenter)
				if workcenter:
					if workcenter.state == 'ready':
						workcenter.button_start()
					elif workcenter.state == 'progress':
						workcenter.record_production()
					action = self.env.ref('mrp.action_mrp_workorder_production_specific').read()[0]
					action['views'] = [(self.env.ref('mrp.mrp_production_workorder_form_view_inherit').id, 'form')]
					action['res_id'] = workcenter.id
					action['domain'] = [('production_id', '=', workcenter.production_id.id)]
				else:
					action = False
			return action

	"""@api.multi
	def scanbarcode_serial(self, barcode):
	#search mrp
	# raise UserError("Events Received " + barcode)
	if barcode:
	  mrp = self.env['mrp.production'].search([('name', '=', barcode)])
	  if mrp:
		action_id = self.env.ref('mrp.mrp_production_action').read()[0]
		views = self.env.ref('mrp.mrp_production_form_view').id
		# action['res_id'] = mrp.ids[0]
		_logger.info('>>>>>>>>>>>>> %s', mrp)
		return mrp.id
		return {
			"type": "ir.actions.act_window",
			"res_model": "mrp.production",
			"views": [[False, "tree"], [False, "form"]],
			"res_id": mrp.id,
			"target": "new",
		}
	  else:
		action = {'type': 'ir.actions.act_window_close'}
		return action"""