# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import AccessError


class AmbassadorPortal(CustomerPortal):
    @http.route(['/my/ambassador/coupons'], type='http', auth='user', website=True, sitemap=False)
    def ambassador_coupons(self, **kwargs):
        partner = request.env.user.partner_id
        if not partner:
            return request.redirect('/web/login')

        if not partner.is_ambassador:
            return request.redirect('/my')

        try:
            discount_codes = partner.ambassador_discount_code_ids

            stats = []
            for code in discount_codes:
                usage_stats = request.env['ambassador.coupon']._get_usage_stats(partner.id)
                stats.append({
                    'code': code,
                    'usage_stats': usage_stats,
                })

            values = {
                'partner': partner,
                'discount_codes': discount_codes,
                'stats': stats,
            }
            return request.render('ambassador_coupons.portal_ambassador_coupons', values)

        except AccessError:
            request.env.cr.rollback()
            return request.redirect('/my')
        except Exception as e:
            request.env.cr.rollback()
            return request.render('ambassador_coupons.error_page', {'error': str(e)})

    @http.route(['/my/ambassador/coupons/json'], type='json', auth='user', website=True, sitemap=False)
    def ambassador_coupons_json(self, **kwargs):
        partner = request.env.user.partner_id
        if not partner or not partner.is_ambassador:
            return {'error': 'Access denied'}

        try:
            result = {}
            for code in partner.ambassador_discount_code_ids:
                stats = request.env['ambassador.coupon']._get_usage_stats(partner.id)
                result[code.id] = {
                    'code': code.name,
                    'code_id': code.id,
                    'stats': stats,
                }
            return result

        except AccessError:
            return {'error': 'Access denied'}
        except Exception as e:
            return {'error': str(e)}

    @http.route(['/my/ambassador/coupons/export'], type='http', auth='user', website=True, sitemap=False)
    def ambassador_coupons_export(self, **kwargs):
        partner = request.env.user.partner_id
        if not partner or not partner.is_ambassador:
            return request.redirect('/my')

        try:
            data = self.ambassador_coupons_json()
            if 'error' in data:
                return request.redirect('/my/ambassador/coupons')

            import csv
            import io

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Discount Code', 'Month', 'Total Usage', 'Validated Orders'])

            for code_id, code_data in data.items():
                for stat in code_data['stats']:
                    writer.writerow([
                        code_data['code'],
                        stat['month'],
                        stat['total_usage'],
                        stat['validated_orders']
                    ])

            output.seek(0)
            return request.make_response(
                output.getvalue(),
                headers=[
                    ('Content-Type', 'text/csv'),
                    ('Content-Disposition', 'attachment; filename="ambassador_coupons.csv"')
                ]
            )
        except Exception:
            request.env.cr.rollback()
            return request.redirect('/my/ambassador/coupons')
