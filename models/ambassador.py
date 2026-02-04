# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_ambassador = fields.Boolean(
        string='Is Ambassador',
        default=False,
        help='Check this box to grant ambassador status to this portal user'
    )
    ambassador_coupon_ids = fields.Many2many(
        'product.coupon',
        string='Ambassador Discount Codes',
        relation='ambassador_discount_code_rel',
        column1='partner_id',
        column2='coupon_id',
        help='Discount codes linked to this ambassador'
    )

    @api.constrains('is_ambassador', 'ambassador_coupon_ids')
    def _check_ambassador_codes(self):
        for partner in self:
            if partner.is_ambassador and not partner.ambassador_coupon_ids:
                raise ValidationError(
                    _('An ambassador must have at least one discount code assigned.')
                )

    @api.onchange('is_ambassador')
    def _onchange_ambassador_status(self):
        if not self.is_ambassador:
            self.ambassador_coupon_ids = [(5, 0, 0)]


class ProductCoupon(models.Model):
    _inherit = 'product.coupon'

    ambassador_id = fields.Many2one(
        'res.partner',
        string='Ambassador',
        domain=[('is_ambassador', '=', True)],
        help='Primary ambassador linked to this discount code'
    )
    ambassador_partner_ids = fields.Many2many(
        'res.partner',
        relation='ambassador_partner_rel',
        column1='coupon_id',
        column2='partner_id',
        string='Ambassador Partners',
        domain=[('is_ambassador', '=', True)],
        readonly=True,
        help='Partners who are ambassadors for this discount code'
    )

    @api.constrains('ambassador_id', 'ambassador_partner_ids')
    def _check_ambassador_consistency(self):
        for coupon in self:
            if coupon.ambassador_id and coupon.ambassador_id not in coupon.ambassador_partner_ids:
                coupon.ambassador_partner_ids |= coupon.ambassador_id
