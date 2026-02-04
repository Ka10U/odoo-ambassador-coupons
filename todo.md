# Ambassador Coupons - Todo List

## Completed Tasks

### Module Structure

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

### Models

- [x] Create `ambassador.py` - extend `res.partner` with ambassador fields
- [x] Add `is_ambassador` boolean field to partners
- [x] Add `ambassador_coupon_ids` Many2many field
- [x] Fix duplicate relation names (ambassador_discount_code_rel, ambassador_partner_rel)
- [x] Create `ambassador_coupon.py` - tracking model for usage stats
- [x] Implement `_get_usage_stats()` method with 12-month query
- [x] Add `@api.constrains` for validation
- [x] Add `@api.onchange` handlers
- [x] Add `action_view_orders()` method

### Controllers

- [x] Create `ambassador_portal.py` with `/my/ambassador/coupons` route
- [x] Add authentication check for ambassadors only
- [x] Fix field name references (ambassador_discount_code_ids → ambassador_coupon_ids)
- [x] Create JSON endpoint for chart data
- [x] Add error handling for non-ambassador access
- [x] Implement proper permission validation
- [x] Add CSV export endpoint

### Views

- [x] Create `ambassador_views.xml` backend views
- [x] Extend `res.partner` form with ambassador fields
- [x] Fix view ID (sale.product_coupon_form_view → sale.product_coupon_view_form)
- [x] Create `templates.xml` portal template
- [x] Add Chart.js integration
- [x] Refine dashboard layout and styling
- [x] Add proper XML IDs for inheritance
- [x] Add tree/form views for ambassador.coupon model
- [x] Add menu items and actions

### Security

- [x] Create `ir.model.access.csv` with basic ACLs
- [x] Fix record rules (model_res_partner → model_ambassador_coupon)
- [x] Add portal-specific access rights
- [x] Create `ambassador_security.xml` with record rules
- [x] Set perm_write to 0 for ambassador_partner_own rule

### Frontend

- [x] Create `chart.js` for usage visualization
- [x] Implement monthly bar chart for total usage
- [x] Implement monthly bar chart for validated orders
- [x] Add loading states
- [x] Implement responsive design
- [x] Add chart legend and tooltips
- [x] Create `portal.css` with responsive styling

### Testing

- [x] Create `test_ambassador_coupon.py`
- [x] Write `test_ambassador_status()` test
- [x] Write `test_ambassador_discount_code_linking()` test
- [x] Write controller access tests
- [ ] Write view rendering tests
- [ ] Run full test suite

### Documentation

- [x] Create `AGENTS.md` with development guidelines
- [x] Add inline code comments
- [x] Create README.md with installation instructions
- [x] Add module description for Odoo Apps
- [x] Create impacts-analysis.md with installation impact analysis
- [x] Create reliability-assessment.md with comprehensive reliability analysis

### Internationalization

- [x] Add translations in `i18n/` directory
- [x] Create `.pot` template file

### Validation

- [ ] Verify module loads without errors
- [ ] Test ambassador status toggle
- [ ] Test discount code linking
- [ ] Test portal access restrictions
- [ ] Verify chart rendering
- [ ] Test on different screen sizes

### Cleanup

- [x] Organize imports
- [x] Optimize SQL queries with `@ormcache`
- [x] Add proper error messages throughout
- [ ] Remove unused files

---

## Remaining Tasks (High Priority)

### Security Hardening

- [ ] Add input validation for `months` parameter in `_get_usage_stats()`
- [ ] Replace broad `except Exception` with specific exception handling
- [ ] Add logging to error handlers
- [ ] Add rate limiting to JSON API endpoint

### Performance Optimization

- [ ] Fix N+1 query pattern in portal controller (batch stats queries)
- [ ] Add cache invalidation strategy for `_get_usage_stats()`
- [ ] Add database indexes for frequently queried fields
- [ ] Implement pagination for portal listing with many codes

### Dependencies

- [ ] Declare Chart.js as module dependency or bundle locally
- [ ] Update i18n/ambassador_coupons.pot with correct version (18.0.1.0.0)
- [ ] Fix translation template field references

### Code Quality

- [ ] Define constants for magic numbers (DEFAULT_MONTHS = 12)
- [ ] Refactor duplicate stats calculation into helper method
- [ ] Add input validation to controller kwargs
- [ ] Implement proper loading states for portal page

---

## Remaining Tasks (Medium Priority)

### Testing

- [ ] Write view rendering tests
- [ ] Write record rule enforcement tests
- [ ] Write error handling tests
- [ ] Write CSV export functionality tests
- [ ] Write data consistency constraint tests
- [ ] Run full test suite

### Export Functionality

- [ ] Add server-side limits to export
- [ ] Consider background jobs for large exports
- [ ] Add pagination to export functionality
- [ ] Implement export progress indicator

### Advanced Features

- [ ] Add cron job for data cleanup
- [ ] Add data archival capability
- [ ] Implement soft delete for records
- [ ] Add audit logging for important actions
- [ ] Add rate limiting to API routes

### Documentation

- [ ] Update README.md with resolved issues
- [ ] Add troubleshooting section to documentation
- [ ] Document performance considerations
- [ ] Add deployment checklist to README

---

## Version History

### v18.0.1.0.0 (Current)
- Fixed duplicate relation names in ambassador.py
- Fixed controller field name references
- Fixed record rule model_id reference
- Updated mail.thread inheritance for Odoo 18
- Fixed view ID for product coupon form
- Created comprehensive analysis documents
- Updated for Odoo 18 compatibility

### v18.0.0.0.0 (Initial)
- Initial module structure
- Basic ambassador functionality
- Portal dashboard
- CSV export
