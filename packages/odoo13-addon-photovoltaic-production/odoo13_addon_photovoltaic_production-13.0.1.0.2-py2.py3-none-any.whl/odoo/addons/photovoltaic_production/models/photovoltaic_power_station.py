from odoo import models, fields


class PhotovoltaicPowerStation(models.Model):
    _inherit = "photovoltaic.power.station"

    production_name = fields.Char()
    billing_error_margin = fields.Float(default='5', string='Billing error margin [%]')
