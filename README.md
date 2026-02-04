# Ambassador Coupons

Odoo module for tracking discount coupon usage by brand ambassadors.

## Features

- Assign "Ambassador" status to portal users
- Link ambassadors to one or more discount codes
- Dashboard showing 12-month usage statistics (total usage + validated orders)
- Chart.js visualizations with monthly breakdowns
- CSV export of usage data
- Access control and record rules

## Installation

1. Copy the `ambassador_coupons` module to your Odoo addons path
2. Update the Odoo addons list (restart Odoo or update via Apps menu)
3. Install the module from Apps

## Configuration

1. Go to **Contacts** and select a partner
2. Check **Is Ambassador** to grant ambassador status
3. Select discount codes to link to the ambassador

## Usage

1. Ambassadors can access `/my/ambassador/coupons` from their portal
2. View usage statistics for each linked discount code
3. Export data to CSV for further analysis

## Requirements

- Odoo 18.0
- Sale module
- Website module
- Portal module

## Development

### Running Tests

```bash
odoo-bin -d <database> --test-tags=/ambassador_coupons
```

### Module Structure

```
ambassador_coupons/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── ambassador.py
│   └── ambassador_coupon.py
├── controllers/
│   ├── __init__.py
│   └── ambassador_portal.py
├── views/
│   ├── ambassador_views.xml
│   └── templates.xml
├── security/
│   ├── ir.model.access.csv
│   └── ambassador_security.xml
├── tests/
│   ├── __init__.py
│   └── test_ambassador_coupon.py
└── static/
    └── src/
        ├── js/
        │   └── chart.js
        └── css/
            └── portal.css
```

## License

LGPL-3
