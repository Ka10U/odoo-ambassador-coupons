# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_ambassador = fields.Boolean(
        string='Is Ambassador',
        default=False,
        help='Check this box to grant ambassador status to this portal user'
    )
    ambassador_discount_code_ids = fields.Many2many(
        'product.discount',
        string='Ambassador Discount Codes',
        relation='ambassador_discount_code_rel',
        help='Discount codes linked to this ambassador'
    )

    @api.constrains('is_ambassador', 'ambassador_discount_code_ids')
    def _check_ambassador_codes(self):
        for partner in self:
            if partner.is_ambassador and not partner.ambassador_discount_code_ids:
                raise ValidationError(
                    _('An ambassador must have at least one discount code assigned.')
                )

    @api.onchange('is_ambassador')
    def _onchange_ambassador_status(self):
        if not self.is_ambassador:
            self.ambassador_discount_code_ids = False


class ProductDiscount(models.Model):
    _inherit = 'product.discount'

    ambassador_id = fields.Many2one(
        'res.partner',
        string='Ambassador',
        domain=[('is_ambassador', '=', True)],
        help='Primary ambassador linked to this discount code'
    )
    ambassador_user_ids = fields.Many2many(
        'res.partner',
        relation='ambassador_discount_code_rel',
        column1='discount_id',
        column2='partner_id',
        string='Ambassador Users',
        domain=[('is_ambassador', '=', True)],
        readonly=True,
        help='Ambassadors who can use this discount code'
    )

    @api.constrains('ambassador_id', 'ambassador_user_ids')
    def _check_ambassador_consistency(self):
        for discount in self:
            if discount.ambassador_id:
                ambassador_in_users = discount.ambassador_id in discount.ambassador_user_ids
                should_be_in_users = discount.ambassador_id in self.mapped(
                    'ambassador_discount_code_ids.partner_id'
                )
                if not ambassador_in_users and should_be_in_users:
                    discount.ambassador_user_ids |= discount.ambassador_id
