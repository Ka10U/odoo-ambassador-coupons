# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, HttpCase


class TestAmbassadorPartner(TransactionCase):

    def setUp(self):
        super(TestAmbassadorPartner, self).setUp()
        self.partner_ambassador = self.env['res.partner'].create({
            'name': 'Test Ambassador',
            'email': 'ambassador@test.com',
            'is_ambassador': True,
        })
        self.partner_regular = self.env['res.partner'].create({
            'name': 'Regular User',
            'email': 'regular@test.com',
        })

    def test_ambassador_status_default(self):
        new_partner = self.env['res.partner'].create({
            'name': 'New Partner',
            'email': 'new@test.com',
        })
        self.assertFalse(new_partner.is_ambassador)

    def test_ambassador_status_true(self):
        self.assertTrue(self.partner_ambassador.is_ambassador)

    def test_ambassador_status_false(self):
        self.assertFalse(self.partner_regular.is_ambassador)

    def test_ambassador_onchange_removes_codes(self):
        self.partner_ambassador.write({'is_ambassador': False})
        self.partner_ambassador._onchange_ambassador_status()
        self.assertFalse(self.partner_ambassador.ambassador_discount_code_ids)


class TestAmbassadorCoupon(TransactionCase):

    def setUp(self):
        super(TestAmbassadorCoupon, self).setUp()
        self.partner_ambassador = self.env['res.partner'].create({
            'name': 'Test Ambassador',
            'email': 'ambassador@test.com',
            'is_ambassador': True,
        })

    def test_coupon_creation(self):
        coupon = self.env['ambassador.coupon'].create({
            'partner_id': self.partner_ambassador.id,
            'discount_code_id': self.env['product.discount'].search([], limit=1).id,
            'usage_date': '2024-01-15',
            'state': 'draft',
        })
        self.assertEqual(coupon.partner_id, self.partner_ambassador)
        self.assertEqual(coupon.state, 'draft')

    def test_coupon_default_state(self):
        coupon = self.env['ambassador.coupon'].create({
            'partner_id': self.partner_ambassador.id,
            'discount_code_id': self.env['product.discount'].search([], limit=1).id,
        })
        self.assertEqual(coupon.state, 'draft')


class TestAmbassadorPortal(HttpCase):

    def setUp(self):
        super(TestAmbassadorPortal, self).setUp()
        self.partner_ambassador = self.env['res.partner'].create({
            'name': 'Test Ambassador',
            'email': 'ambassador@test.com',
            'is_ambassador': True,
        })
        self.partner_regular = self.env['res.partner'].create({
            'name': 'Regular User',
            'email': 'regular@test.com',
        })

    def test_portal_access_ambassador(self):
        self.authenticate(self.partner_ambassador.email, self.partner_ambassador.email)
        response = self.url_open('/my/ambassador/coupons')
        self.assertEqual(response.status_code, 200)

    def test_portal_redirect_non_ambassador(self):
        self.authenticate(self.partner_regular.email, self.partner_regular.email)
        response = self.url_open('/my/ambassador/coupons')
        self.assertIn(response.url, '/my')
