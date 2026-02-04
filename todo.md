# Ambassador Coupons - Todo List

## Module Structure

- [x] Create `__init__.py` module entry point
- [x] Create `__manifest__.py` module metadata
- [x] Create `models/` directory with `__init__.py`
- [x] Create `controllers/` directory with `__init__.py`
- [x] Create `views/` directory
- [x] Create `security/` directory with `ir.model.access.csv`
- [x] Create `tests/` directory with `__init__.py`
- [x] Create `static/src/js/` directory with `chart.js`
- [x] Create `data/` directory
- [x] Create `static/src/css/` directory with portal styling

## Models

- [x] Create `ambassador.py` - extend `res.partner` with ambassador fields
- [x] Add `is_ambassador` boolean field to partners
- [x] Add `ambassador_discount_code_ids` Many2many field
- [x] Create `ambassador_coupon.py` - tracking model for usage stats
- [x] Implement `_get_usage_stats()` method with 12-month query
- [x] Add `@api.constrains` for validation
- [x] Add `@api.onchange` handlers
- [x] Add `action_view_orders()` method

## Controllers

- [x] Create `ambassador_portal.py` with `/my/ambassador/coupons` route
- [x] Add authentication check for ambassadors only
- [x] Create JSON endpoint for chart data
- [x] Add error handling for non-ambassador access
- [x] Implement proper permission validation
- [x] Add CSV export endpoint

## Views

- [x] Create `ambassador_views.xml` backend views
- [x] Extend `res.partner` form with ambassador fields
- [x] Create `templates.xml` portal template
- [x] Add Chart.js integration
- [x] Refine dashboard layout and styling
- [x] Add proper XML IDs for inheritance
- [x] Add tree/form views for ambassador.coupon model
- [x] Add menu items and actions

## Security

- [x] Create `ir.model.access.csv` with basic ACLs
- [x] Define proper record rules for ambassador data
- [x] Add portal-specific access rights
- [x] Create `ambassador_security.xml` with record rules

## Frontend

- [x] Create `chart.js` for usage visualization
- [x] Implement monthly bar chart for total usage
- [x] Implement monthly bar chart for validated orders
- [x] Add loading states
- [x] Implement responsive design
- [x] Add chart legend and tooltips
- [x] Create `portal.css` with responsive styling

## Testing

- [x] Create `test_ambassador_coupon.py`
- [x] Write `test_ambassador_status()` test
- [x] Write `test_ambassador_discount_code_linking()` test
- [x] Write controller access tests
- [ ] Write view rendering tests
- [ ] Run full test suite

## Documentation

- [x] Create `AGENTS.md` with development guidelines
- [x] Add inline code comments
- [x] Create README.md with installation instructions
- [x] Add module description for Odoo Apps

## Internationalization

- [x] Add translations in `i18n/` directory
- [x] Create `.pot` template file

## Validation

- [ ] Verify module loads without errors
- [ ] Test ambassador status toggle
- [ ] Test discount code linking
- [ ] Test portal access restrictions
- [ ] Verify chart rendering
- [ ] Test on different screen sizes

## Cleanup

- [x] Organize imports
- [x] Optimize SQL queries with `@ormcache`
- [x] Add proper error messages throughout
- [ ] Remove unused files
