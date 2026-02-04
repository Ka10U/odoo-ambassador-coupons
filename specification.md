# DESCRIPTION

odoo-ambassador-coupon is an Odoo custom module which aims at providing information to brand ambassadors about the use of their discount coupons.

Ambassadors are frontends users, like any other user with portal access (user who created an account on the Odoo ecommerce platform or an Odoo contact to whom portal access has been granted).

This module should allow Odoo users to apply "Ambassador" status to portal users.

The "Ambassador" status should allow users to have an additional link in their account page on the ecommerce platform that allows them to check the number of carts that used their nominative discount code.

This information is already available as "discounts" associated with each discount code.

Each ambassador should be "linked" with one (or several) discount codes.

When an ambassador connects to the ecommerce odoo platform and goes to his account page, he should have a link/card element that brings him to a new page where the platform reads database information about his discount code usage and presents data as two graphs:

- Total number of code usage every month (in the past 12 months, including abandonned carts)
- Number of code usage in actual validated orders (in the past 12 months)

This information should incentivize ambassadors to promote the brand as they can receive a commission for each order placed using their discount code.

# GENERAL INSTRUCTIONS

Respect state of the art rules for Odoo modules development.

Write and run tests whenever relevant.

If the next step is obvious move forward with it.
