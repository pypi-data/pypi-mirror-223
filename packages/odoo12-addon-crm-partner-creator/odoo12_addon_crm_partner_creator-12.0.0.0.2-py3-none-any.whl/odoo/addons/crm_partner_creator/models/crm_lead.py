# -*- coding: utf-8 -*-

import json
from odoo import fields, models
from odoo.tools.translate import _
from odoo import exceptions


class CrmLead(models.Model):
    _inherit = "crm.lead"

    partner_creator_config_id = fields.Many2one(
        'crm.partner.creator.config',
        string=_("Partner creator config")
    )

    def create_partner_from_config_action(self):
        self._validate_partner_creation()
        config_json = json.loads(self.partner_creator_config_id.config)
        config_json_partner = config_json.get('partner', False)
        if config_json_partner:
            partner = False
            config_json_partner_search = config_json_partner.get(
                'search',
                False
            )
            if config_json_partner_search:
                partner = self._search_partner_from_config(
                    config_json_partner_search
                )
            if not partner:
                config_json_partner_create = config_json_partner.get(
                    'create',
                    False
                )
                if config_json_partner_create:
                    partner = self._create_partner_from_config(
                        config_json_partner_create
                    )
            if partner:
                self.write({
                    'partner_id': partner.id
                })

        # TODO: Move to a new module "crm_partner_creator_invoice_partner"
        config_json_invoice_partner = config_json.get('invoice_partner', False)
        if config_json_invoice_partner:
            partner = False
            config_json_invoice_partner_search = \
                config_json_invoice_partner.get(
                    'search',
                    False
                )
            if config_json_invoice_partner_search:
                partner = self._search_partner_from_config(
                    config_json_invoice_partner_search
                )
            if not partner:
                config_json_invoice_partner_create = \
                    config_json_invoice_partner.get(
                        'create',
                        False
                    )
                if config_json_invoice_partner_create:
                    partner = self._create_partner_from_config(
                        config_json_invoice_partner_create
                    )
            if partner:
                for order_line in self.crm_order_line_ids:
                    order_line.write({'invoice_partner_id': partner.id})

    def _validate_partner_creation(self):
        if not self.partner_creator_config_id:
            raise exceptions.ValidationError(
                _("Partner creator must be defined")
            )
        # TODO: Move to new module "crm_cooperator_partner_creator"
#         if self.subscription_request_id:
#             raise exceptions.ValidationError(
#                 _("Can't create partner on lead \
#                 with subcription request defined.")
#             )

    def _search_partner_from_config(self, config_json):
        if not self.partner_id:
            search_data = self._get_partner_search_data(
                config_json
            )
            if search_data:
                partner = self.env['res.partner'].search(search_data)
                if partner:
                    return partner[0]
                else:
                    return False
            else:
                raise exceptions.ValidationError(
                    _("Configuration incompatible with partner search")
                )
        else:
            return self.partner_id

    def _create_partner_from_config(self, config_json):
        if not self.partner_id:
            creation_data = self._get_partner_creation_data(
                config_json)
            if creation_data:
                return self.env['res.partner'].create(creation_data)
            else:
                raise exceptions.ValidationError(
                    _("Configuration incompatible with partner creation")
                )
        else:
            return self.partner_id

    def _get_partner_search_data(self, partner_config_json):
        search_data = []
        for metadata_key in partner_config_json.keys():
            metadata = self.metadata_line_ids.filtered(
                lambda md: md.key == metadata_key)
            if metadata:
                search_data.append(
                    (partner_config_json[metadata_key], '=', metadata[0].value)
                )
        return search_data

    def _get_partner_creation_data(self, partner_config_json):
        creation_data = {
            'type': 'contact'
        }
        for metadata_key in partner_config_json.keys():
            metadata = self.metadata_line_ids.filtered(
                lambda md: md.key == metadata_key)
            if metadata:
                creation_data[
                    partner_config_json[metadata_key]
                ] = metadata[0].value
        return creation_data
