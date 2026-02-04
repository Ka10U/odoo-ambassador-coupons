# Odoo 18 Compatibility Checklist

## Pre-Installation Checklist

- [ ] Module copied to Odoo addons path
- [ ] Dependencies installed: `sale`, `website`, `website_sale`, `portal`
- [ ] Developer mode enabled in Odoo
- [ ] Apps list updated (Apps → Update Apps List)
- [ ] No duplicate module names in addons path

## Installation Testing

- [ ] Module installs without errors
- [ ] No XML validation errors in logs
- [ ] `ambassador.coupon` model created
- [ ] `res.partner` form extended with ambassador fields
- [ ] Menu item appears under Sales → Configuration

## Functional Testing

### Partner/Ambassador Fields
- [ ] Can toggle "Is Ambassador" checkbox on partners
- [ ] Ambassador page appears when enabled
- [ ] Can select discount codes on ambassador partners
- [ ] Validation prevents ambassador without discount codes

### Portal Access
- [ ] Ambassador can access `/my/ambassador/coupons`
- [ ] Non-ambassador redirected to `/my`
- [ ] Charts render correctly
- [ ] CSV export works
- [ ] JSON endpoint returns data

### Backend Views
- [ ] Ambassador Coupons menu works
- [ ] Tree view displays records
- [ ] Form view allows record creation

## Manual Test Steps

```python
# In Odoo Shell
env = self.env

# Create test ambassador
partner = env['res.partner'].create({
    'name': 'Test Ambassador',
    'email': 'test@ambassador.com',
    'is_ambassador': True,
})
print(f"Created ambassador: {partner.is_ambassador}")

# Check model exists
model = env['ir.model'].search([('model', '=', 'ambassador.coupon')])
print(f"Model exists: {bool(model)}")

# Check views exist
views = env['ir.ui.view'].search([('name', 'ilike', 'ambassador')])
print(f"Views found: {len(views)}")
```

## Common Issues

### "product.discount" model not found
- In Odoo 18, the model is `product.coupon` not `product.discount`
- Updated all references in code

### @api.onchange deprecated
- Used `@api.onchanges` instead for Odoo 18 compatibility

### View inheritance errors
- Used `invisible` instead of `attrs` for Odoo 18
- Updated view IDs to match Odoo 18 patterns

## Test Commands

```bash
# Run all tests
odoo-bin -d <database> --test-tags /ambassador_coupons

# Run specific test class
odoo-bin -d <database> --test-tags ambassador_coupons.tests.test_ambassador_coupon.TestAmbassadorPartner

# Run single test
odoo-bin -d <database> --test-tags ambassador_coupons.tests.test_ambassador_coupon.TestAmbassadorPartner.test_ambassador_status
```

## Expected Results

- All tests pass (green)
- No errors in Odoo logs
- Module appears in Apps with correct version (18.0.1.0.0)
- Portal dashboard shows for ambassadors
