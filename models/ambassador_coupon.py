# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import ormcache
from odoo.tools.translate import _


class AmbassadorCoupon(models.Model):
    _name = 'ambassador.coupon'
    _description = 'Ambassador Coupon Tracking'
    _order = 'usage_date desc'
    _inherit = ['mail.thread']

    partner_id = fields.Many2one(
        'res.partner',
        string='Ambassador',
        required=True,
        domain=[('is_ambassador', '=', True)],
        tracking=True
    )
    coupon_id = fields.Many2one(
        'product.coupon',
        string='Discount Code',
        required=True,
        tracking=True
    )
    usage_date = fields.Date(
        string='Usage Date',
        help='Date when the discount code was used',
        tracking=True
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('abandoned', 'Abandoned Cart'),
            ('sale', 'Validated Order'),
        ],
        string='Status',
        default='draft',
        tracking=True
    )

    @api.model
    @ormcache()
    def _get_usage_stats(self, ambassador_id, months=12):
        try:
            self.env.cr.execute("""
                SELECT
                    TO_CHAR(pc.create_date, 'YYYY-MM') AS month,
                    COUNT(*) AS total_usage,
                    COUNT(CASE WHEN s.state IN ('sale', 'done') THEN 1 END) AS validated_orders
                FROM product_coupon pc
                LEFT JOIN sale_order_line sol ON sol.coupon_id = pc.id
                LEFT JOIN sale_order s ON s.id = sol.order_id
                WHERE pc.ambassador_id = %s
                AND pc.create_date >= CURRENT_DATE - INTERVAL '%s months'
                GROUP BY TO_CHAR(pc.create_date, 'YYYY-MM')
                ORDER BY month DESC
            """, (ambassador_id, months))
            return self.env.cr.dictfetchall()
        except Exception:
            self.env.cr.rollback()
            return []

    def action_view_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Discount Code Orders'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [
                ('order_line.coupon_id', '=', self.coupon_id.id)
            ],
            'context': {'create': False},
        }
