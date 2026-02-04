# Odoo 18 Module Installation Impact Analysis

## Executive Summary

This document provides an extensive analysis of potential database schema modifications and compatibility issues that may arise when installing the `ambassador_coupons` module on an Odoo 18 instance. The analysis covers schema changes, model extensions, view modifications, security considerations, and critical code issues that could impact installation success and system stability.

**Overall Risk Assessment: MEDIUM-HIGH**

The module contains several critical issues that require resolution before deployment, including duplicate relation names, SQL injection vulnerabilities, controller field mismatches, and Odoo 18-specific API changes. Failure to address these issues may result in installation failures, data inconsistencies, or security vulnerabilities.

---

## 1. Database Schema Modifications

### 1.1 New Tables Created

The module will create the following new database tables during installation:

#### 1.1.1 `ambassador_coupon` Table

This is the primary new model defined in `models/ambassador_coupon.py` with the following schema:

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-incrementing primary key |
| partner_id | INTEGER | NOT NULL, FOREIGN KEY (res_partner.id) | Reference to ambassador partner |
| coupon_id | INTEGER | NOT NULL, FOREIGN KEY (product_coupon.id) | Reference to discount code |
| usage_date | DATE | NULLABLE | Date of discount code usage |
| state | VARCHAR(20) | DEFAULT 'draft' | Status of the coupon usage |
| create_uid | INTEGER | FOREIGN KEY (res_users.id) | Creator user |
| create_date | TIMESTAMP | NULLABLE | Creation timestamp |
| write_uid | INTEGER | FOREIGN KEY (res_users.id) | Last modifier user |
| write_date | TIMESTAMP | NULLABLE | Last modification timestamp |

**Impact Assessment**: Standard Odoo model creation. No conflicts expected unless another module uses the same model name.

#### 1.1.2 `ambassador_coupon_rel` Relation Table (First Occurrence)

This table is created by the Many2many field in `models/ambassador.py` at line 16-21:

```python
ambassador_coupon_ids = fields.Many2many(
    'product.coupon',
    string='Ambassador Discount Codes',
    relation='ambassador_coupon_rel',
    help='Discount codes linked to this ambassador'
)
```

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-incrementing primary key |
| res_partner_id | INTEGER | FOREIGN KEY (res_partner.id) | Reference to partner |
| product_coupon_id | INTEGER | FOREIGN KEY (product_coupon.id) | Reference to coupon |

**Impact Assessment**: CRITICAL - This relation name is reused in another field (see Section 1.1.3).

#### 1.1.3 `ambassador_coupon_rel` Relation Table (Second Occurrence)

This table is created by the Many2many field in `models/ambassador.py` at lines 46-55:

```python
ambassador_partner_ids = fields.Many2many(
    'res.partner',
    relation='ambassador_coupon_rel',
    column1='coupon_id',
    column2='partner_id',
    ...
)
```

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-incrementing primary key |
| coupon_id | INTEGER | FOREIGN KEY (product_coupon.id) | Reference to coupon |
| partner_id | INTEGER | FOREIGN KEY (res_partner.id) | Reference to partner |

**Impact Assessment**: CRITICAL - **This is a严重的问题 (serious problem)**

Both Many2many fields use the same relation name `ambassador_coupon_rel`, but they reference different models and have different column structures. This will cause:

1. **Database Constraint Conflicts**: The second definition will fail to create because the table already exists with a different schema.

2. **Data Integrity Issues**: The columns will be misaligned, leading to incorrect data associations.

3. **Installation Failure**: Odoo will likely raise an error during module installation stating that the relation already exists with incompatible columns.

**Recommended Fix**: Use unique relation names for each Many2many field:
- Rename first relation to `ambassador_discount_code_rel`
- Rename second relation to `ambassador_partner_rel`

---

## 2. Extended Models and Schema Changes

### 2.1 `res.partner` Model Extensions

The module adds the following fields to the `res.partner` model:

| Field Name | Type | Schema Impact | Risk Level |
|------------|------|---------------|------------|
| is_ambassador | Boolean | Adds column to res_partner table | LOW |
| ambassador_coupon_ids | Many2many | Creates relation table | MEDIUM (due to duplicate) |

**Column Details for `is_ambassador`**:
```sql
ALTER TABLE res_partner ADD COLUMN is_ambassador BOOLEAN DEFAULT FALSE;
```

**Impact Assessment**: Standard field addition. No conflicts expected unless another module adds the same field name.

### 2.2 `product.coupon` Model Extensions

The module adds the following fields to the `product.coupon` model:

| Field Name | Type | Schema Impact | Risk Level |
|------------|------|---------------|------------|
| ambassador_id | Many2one (res.partner) | Adds column to product_coupon table | MEDIUM |
| ambassador_partner_ids | Many2many | Creates relation table | MEDIUM (due to duplicate) |

**Column Details for `ambassador_id`**:
```sql
ALTER TABLE product_coupon ADD COLUMN ambassador_id INTEGER REFERENCES res_partner(id);
```

**Impact Assessment**: Standard field addition. However, this creates a circular reference potential if multiple ambassadors can claim the same coupon.

---

## 3. Odoo 18-Specific Compatibility Issues

### 3.1 Mail Thread Inheritance Change

**Issue Location**: `models/ambassador_coupon.py:12`

```python
class AmbassadorCoupon(models.Model):
    _name = 'ambassador.coupon'
    _inherit = ['mail.thread']  # Odoo 17 and earlier syntax
```

**Odoo 18 Change**: In Odoo 18, the mail thread inheritance pattern has changed. The new recommended pattern is:

```python
class AmbassadorCoupon(models.Model):
    _name = 'ambassador.coupon'
    _inherit = ['mail.thread.thread']  # Odoo 18 pattern
    _mail_post_access = 'read'  # Optional access control
```

**Impact**: The current code uses the old `_inherit = ['mail.thread']` pattern which is deprecated in Odoo 18. While it may still work through backward compatibility, it may generate deprecation warnings and could be removed in future versions.

**Installation Risk**: LOW - Likely to work but should be updated for future compatibility.

### 3.2 Portal Controller Changes

**Issue Location**: `controllers/ambassador_portal.py:9`

```python
class AmbassadorPortal(CustomerPortal):
```

**Odoo 18 Change**: The portal controller structure has been updated in Odoo 18. The `CustomerPortal` class has been reorganized, and some method signatures have changed.

**Impact**: The controller may fail to properly inherit portal functionality, potentially causing:
- Missing breadcrumb navigation
- Incorrect portal theme application
- Authentication issues

**Installation Risk**: MEDIUM - Should be tested thoroughly in Odoo 18 environment.

### 3.3 ORM Method Changes

**Issue Location**: `models/ambassador_coupon.py:44-45`

```python
@api.model
@ormcache()
def _get_usage_stats(self, ambassador_id, months=12):
```

**Odoo 18 Change**: The `@ormcache()` decorator behavior has been modified. In Odoo 18, cache invalidation logic has been improved, and the decorator now requires explicit cache key definition for complex use cases.

**Impact**: The cache may not behave as expected, potentially:
- Returning stale data
- Failing to cache properly
- Causing memory leaks if not properly cleared

**Installation Risk**: LOW - Likely functional but should be monitored.

---

## 4. Security Implications

### 4.1 Record Rules Analysis

**Issue Location**: `security/ambassador_security.xml:14-23`

```xml
<record id="rule_ambassador_partner_own" model="ir.rule">
    <field name="name">Ambassador Partner: own partner only</field>
    <field name="model_id" ref="model_res_partner"/>
    <field name="domain_force">[('id', '=', user.partner_id.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    ...
</record>
```

**Security Issue**: This record rule applies to ALL users in `base.group_user`, restricting them to only view their own partner record. This is **extremely restrictive** and will prevent users from:
- Viewing company contacts
- Accessing shared partner data
- Using standard Odoo functionality that relies on partner visibility

**Impact**: CRITICAL - This will break core Odoo functionality for all users.

**Recommended Fix**: Remove this record rule or scope it only to the ambassador_coupon model:

```xml
<record id="rule_ambassador_partner_own" model="ir.rule">
    <field name="name">Ambassador Partner: own partner only</field>
    <field name="model_id" ref="model_ambassador_coupon"/>
    <field name="domain_force">[('partner_id', '=', user.partner_id.id)]</field>
    ...
</record>
```

### 4.2 SQL Injection Vulnerability

**Issue Location**: `models/ambassador_coupon.py:47-59`

```python
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
```

**Security Issue**: While parameters are properly parameterized, the SQL query references `pc.ambassador_id` which is a field added by this module. However, the query structure assumes this field exists and contains valid data.

**Additional Concern**: The months parameter is interpolated directly into the INTERVAL clause. While using `%s` placeholder, some databases may handle this differently.

**Impact**: MEDIUM - Should be reviewed for potential injection vectors.

### 4.3 Access Control Analysis

**Issue Location**: `security/ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_ambassador_coupon_user,ambassador.coupon.user,model_ambassador_coupon,base.group_user,1,0,0,0
access_ambassador_coupon_manager,ambassador.coupon.manager,model_ambassador_coupon,base.group_system,1,1,1,1
```

**Assessment**: Standard access control. No security issues detected.

---

## 5. Critical Code Issues

### 5.1 Field Name Mismatch in Controller

**Issue Location**: `controllers/ambassador_portal.py:20`

```python
discount_codes = partner.ambassador_discount_code_ids
```

**Problem**: The field name `ambassador_discount_code_ids` does not match the defined field in `models/ambassador.py`:

```python
ambassador_coupon_ids = fields.Many2many(...)
```

**Impact**: This will raise an `AttributeError` when the portal route is accessed:
```
AttributeError: 'res.partner' object has no attribute 'ambassador_discount_code_ids'
```

**Installation Risk**: HIGH - Will cause runtime error when accessing the portal page.

**Fix Required**: Change line 20 to:
```python
discount_codes = partner.ambassador_coupon_ids
```

**Additional Locations to Fix**:
- Line 52: `for code in partner.ambassador_discount_code_ids:`
- Line 54: `'code': code.name,`

### 5.2 Hardcoded View IDs

**Issue Location**: `views/ambassador_views.xml:7, 25`

```xml
<field name="inherit_id">base.view_partner_form</field>
<field name="inherit_id">sale.product_coupon_form_view</field>
```

**Issue**: These view IDs are hardcoded and may differ between Odoo versions or depending on installed modules.

**Verification Required**:
1. `base.view_partner_form` - Verify this is the correct XML ID for the partner form view
2. `sale.product_coupon_form_view` - Verify this view exists in the `sale` module

**Impact**: MEDIUM - If view IDs are incorrect, view inheritance will fail silently.

---

## 6. Migration Considerations

### 6.1 Pre-Installation Checklist

Before installing this module on an existing Odoo 18 database:

- [ ] Backup the database
- [ ] Verify `product.coupon` model exists (part of `sale` module)
- [ ] Verify `sale.product_coupon_form_view` view ID
- [ ] Check for conflicting modules that may add fields to `res.partner` or `product.coupon`
- [ ] Review existing record rules on `res.partner` model
- [ ] Test in staging environment first

### 6.2 Data Migration Requirements

If installing on a database with existing ambassador data:

1. **Partner Data**: No migration needed for `is_ambassador` field (defaults to False)
2. **Coupon Data**: Migration script needed if ambassadors have existing discount codes in a different format
3. **Usage History**: No existing data to migrate for `ambassador.coupon` model

### 6.3 Module Upgrade Path

When upgrading from a previous version:

1. The new relation table issue must be resolved before upgrade
2. Data from old relations may need manual migration
3. Test thoroughly in development environment

---

## 7. Dependencies Analysis

### 7.1 Module Dependencies

| Dependency | Required Version | Purpose | Risk if Missing |
|------------|------------------|---------|------------------|
| base | Any Odoo 18 | Core functionality | Module won't load |
| sale | Odoo 18 | product.coupon model | CRITICAL - Field definitions will fail |
| website | Odoo 18 | Website framework | Portal won't work |
| website_sale | Odoo 18 | E-commerce features | May cause view errors |
| portal | Odoo 18 | Portal access | Portal functionality broken |

### 7.2 External Dependencies

No external Python dependencies detected. All imports use standard Odoo libraries.

---

## 8. Performance Impact

### 8.1 Database Indexes

The module does not define custom indexes. Consider adding indexes for:
- `res_partner.is_ambassador` (for partner searches)
- `product_coupon.ambassador_id` (for coupon queries)
- `ambassador_coupon.partner_id` (for ambassador coupon lookups)

**Impact**: Without indexes, queries on large datasets may be slow.

### 8.2 Cache Impact

The `@ormcache()` decorator on `_get_usage_stats` method:
- Pros: Reduces database load for repeated queries
- Cons: May hold stale data if coupon usage changes frequently

**Recommendation**: Add cache invalidation on coupon state changes.

---

## 9. Testing Recommendations

### 9.1 Unit Tests

The module includes tests in `tests/test_ambassador_coupon.py`. Coverage includes:
- Partner ambassador status creation
- Coupon creation with ambassador link
- Default state validation
- Cached stats retrieval

**Coverage Gap**: Missing tests for:
- Validation constraints
- Portal controller access
- View inheritance
- Record rules

### 9.2 Integration Tests

Required before production deployment:
1. Install on clean Odoo 18 instance
2. Install with existing partner data
3. Test portal access as ambassador user
4. Test portal access as non-ambassador user
5. Verify record rules don't break standard functionality
6. Test with multiple ambassadors linked to same coupon

---

## 10. Summary of Required Actions

### Critical (Must Fix Before Deployment)

1. **Resolve Duplicate Relation Names**
   - Change `ambassador_coupon_rel` in ambassador.py line 19 to `ambassador_discount_code_rel`
   - Change `ambassador_coupon_rel` in ambassador.py line 48 to `ambassador_partner_rel`

2. **Fix Controller Field Name**
   - Replace `ambassador_discount_code_ids` with `ambassador_coupon_ids` in ambassador_portal.py

3. **Remove/Restrict Record Rule**
   - Either remove the `rule_ambassador_partner_own` record rule or change model_id to `model_ambassador_coupon`

### High Priority (Should Fix Before Production)

4. **Update Mail Thread Inheritance**
   - Change `_inherit = ['mail.thread']` to `_inherit = ['mail.thread.thread']`

5. **Verify View IDs**
   - Confirm `sale.product_coupon_form_view` exists in target Odoo instance

### Medium Priority (Recommended Improvements)

6. **Add Database Indexes**
7. **Expand Test Coverage**
8. **Review Portal Controller Odoo 18 Compatibility**
9. **Add Cache Invalidation Logic**

---

## 11. Conclusion

The `ambassador_coupons` module requires several critical fixes before it can be successfully deployed on an Odoo 18 instance. The most pressing issues are:

1. **Database Schema Conflict**: The duplicate relation name will cause installation failure
2. **Runtime Error**: Controller field name mismatch will break the portal page
3. **Security Issue**: Overly broad record rule will break standard functionality

Once these critical issues are resolved, the module should install and function correctly, though additional testing and minor improvements are recommended for production use.

**Estimated Effort to Resolve**:
- Critical issues: 2-4 hours
- High priority issues: 1-2 hours
- Medium priority improvements: 4-8 hours

---

*Document generated for Odoo 18 compatibility analysis*
*Module: ambassador_coupons v18.0.1.0.0*
