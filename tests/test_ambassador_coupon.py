# -*- coding: utf-8 -*-
from odoo import tests


@tests.tagged('post_install', '-at_install')
class TestAmbassadorPartner(tests.TransactionCase):

    def setUp(self):
        super().setUp()
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


@tests.tagged('post_install', '-at_install')
class TestAmbassadorCoupon(tests.TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner_ambassador = self.env['res.partner'].create({
            'name': 'Test Ambassador',
            'email': 'ambassador@test.com',
            'is_ambassador': True,
        })

    def test_coupon_creation(self):
        coupon = self.env['ambassador.coupon'].create({
            'partner_id': self.partner_ambassador.id,
            'coupon_id': self.env['product.coupon'].search([], limit=1).id,
            'usage_date': '2024-01-15',
            'state': 'draft',
        })
        self.assertEqual(coupon.partner_id, self.partner_ambassador)
        self.assertEqual(coupon.state, 'draft')

    def test_coupon_default_state(self):
        coupon = self.env['ambassador.coupon'].create({
            'partner_id': self.partner_ambassador.id,
            'coupon_id': self.env['product.coupon'].search([], limit=1).id,
        })
        self.assertEqual(coupon.state, 'draft')

    def test_usage_stats_cached(self):
        stats = self.env['ambassador.coupon']._get_usage_stats(self.partner_ambassador.id)
        self.assertIsInstance(stats, list)
