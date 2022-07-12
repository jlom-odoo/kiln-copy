# -*- coding: utf-8 -*-

from . import models

from odoo import api, SUPERUSER_ID

def plant_code_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].action_set_plant_code()

def plant_code_reset_uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].action_reset_plant_code()