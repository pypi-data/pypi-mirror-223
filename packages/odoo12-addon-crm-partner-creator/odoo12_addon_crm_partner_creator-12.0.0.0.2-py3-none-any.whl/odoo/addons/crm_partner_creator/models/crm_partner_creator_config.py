# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools.translate import _


class CrmPartnerCreatorConfig(models.Model):
    _name = "crm.partner.creator.config"

    name = fields.Char(string=_("Name"))
    config = fields.Text(string=_("Config"))
    crm_lead_ids = fields.One2many(
        "crm.lead",
        "partner_creator_config_id",
        string=_("Related leads")
    )
