# AGENTS.md

This document provides guidelines and commands for agents working on the odoo-ambassador-coupons project.

## Project Overview

Odoo custom module for tracking discount coupon usage by brand ambassadors. The module extends `res.partner` with ambassador status and links users to discount codes, providing a portal dashboard with usage statistics.

## Development Commands

### Testing

```bash
# Run all tests (from Odoo instance)
odoo-bin -d <database> --test-tags=/ambassador_coupons

# Run a single test class
odoo-bin -d <database> --test-tags ambassador_coupons.tests.test_ambassador_coupon

# Run a single test method
odoo-bin -d <database> --test-tags ambassador_coupons.tests.test_ambassador_coupon.TestAmbassadorCoupon.test_ambassador_status
```

### Module Installation

```bash
# Install/update module via Odoo shell
env['ir.module.module'].search([('name', '=', 'ambassador_coupons')]).button_install()
env['ir.module.module'].search([('name', '=', 'ambassador_coupons')]).button_upgrade()
```

## Code Style Guidelines

### General Principles

- Follow Odoo official development documentation and state-of-the-art practices
- Keep functions small and focused on a single responsibility
- Use descriptive names for all identifiers
- Add docstrings to all public classes, methods, and functions

### Imports

```python
# Standard library imports first
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Third-party imports
from odoo import models, fields, api
from odoo.http import request

# Local imports (use relative imports within module)
from . import ambassador
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Models | Snake_case, descriptive | `ambassador_coupon`, `res_partner` |
| Fields | Snake_case | `is_ambassador`, `usage_date` |
| Methods | Snake_case | `_get_usage_stats`, `button_install` |
| Variables | Snake_case | `discount_codes`, `usage_stats` |
| Constants | UPPER_SNAKE_CASE | `MAX_MONTHS = 12` |
| XML IDs | Snake_case with dots | `view_partner_form_ambassador` |
| Views | Descriptive with context | `portal_ambassador_coupons` |

### File Organization

```
odoo-ambassador-coupons/
├── __init__.py           # Module entry, import subpackages
├── __manifest__.py       # Module metadata, dependencies, data files
├── models/
│   ├── __init__.py       # Import all model files
│   └── ambassador.py     # Model definitions
├── controllers/
│   ├── __init__.py
│   └── ambassador_portal.py  # Portal controllers
├── views/
│   ├── ambassador_views.xml  # Backend views
│   └── templates.xml         # Portal templates
├── security/
│   └── ir.model.access.csv   # Access control
├── tests/
│   ├── __init__.py
│   └── test_ambassador_coupon.py
└── static/src/js/
    └── chart.js
```

### Field Definitions

```python
# Required fields
partner_id = fields.Many2one('res.partner', string='Partner', required=True)

# Boolean fields
is_ambassador = fields.Boolean(string='Is Ambassador', default=False)

# Selection fields
state = fields.Selection([
    ('draft', 'Draft'),
    ('abandoned', 'Abandoned Cart'),
    ('sale', 'Validated Order'),
], string='Status', default='draft')

# Relational fields
discount_code_ids = fields.Many2many('product.discount', string='Discount Codes')
```

### Odoo-Specific Patterns

```python
# Use api.model for decorators that don't need records
@api.model
def _default_company(self):
    return self.env.company

# Use api.depends for compute methods
@api.depends('field_a', 'field_b')
def _compute_field_c(self):
    for record in self:
        record.field_c = record.field_a + record.field_b

# Use @api.onchange for UI triggers
@api.onchange('is_ambassador')
def _onchange_ambassador_status(self):
    if not self.is_ambassador:
        self.ambassador_discount_code_ids = False
```

### Error Handling

```python
# Use proper exception handling with Odoo exceptions
from odoo.exceptions import ValidationError, UserError

@api.constrains('discount_code')
def _check_discount_code(self):
    for record in self:
        if not record.discount_code:
            raise ValidationError(_('Discount code is required'))

# Controller error handling
try:
    stats = self._get_usage_stats(partner_id)
except Exception as e:
    request.env.cr.rollback()
    return {'error': str(e)}
```

### Security

- Always use `sudo()` for elevated operations when appropriate
- Define proper ACLs in `security/ir.model.access.csv`
- Use `env.user` to check current user permissions
- Validate access in controllers before operations

### Portal Controllers

```python
@http.route('/my/ambassador/coupons', type='http', auth='user', website=True)
def ambassador_coupons(self, **kwargs):
    partner = request.env.user.partner_id
    if not partner.is_ambassador:
        return request.redirect('/my')
    # ... rest of implementation
```

### Views and Templates

- Use QWeb templates with proper inheritance patterns
- Include `t-call="portal.portal_layout"` for portal pages
- Use `website=True` for publicly accessible controllers
- Include CSRF tokens in forms (`<input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>`)

### Testing Guidelines

```python
class TestAmbassadorCoupon(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({...})

    def test_ambassador_status(self):
        self.assertTrue(self.partner.is_ambassador)
```

## Key Dependencies

- `base` - Core Odoo functionality
- `sale` - Sales module (for discount codes)
- `website` - Website framework
- `website_sale` - E-commerce features
- `portal` - Portal access for customers

## Important Notes

- Always update `__manifest__.py` when adding new views, models, or controllers
- Include translations in `i18n/` directory for multi-language support
- Use `env.cr.execute()` for raw SQL with proper parameterization
- Backup production databases before running tests
