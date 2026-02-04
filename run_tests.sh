#!/bin/bash
# Test runner script for Ambassador Coupons module on Odoo 18

# Usage:
#   ./run_tests.sh               # Run all tests
#   ./run_tests.sh Partner      # Run specific test class
#   ./run_tests.sh Partner.test_ambassador_status  # Run specific test

# Configuration - Update these values for your environment
ODOO_HOST="${ODOO_HOST:-localhost}"
ODOO_PORT="${ODOO_PORT:-8069}"
DATABASE="${DATABASE:-odoo}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"

TEST_CLASS="${1:-}"
TEST_METHOD="${2:-}"

# Build test tags
if [ -n "$TEST_METHOD" ]; then
    TEST_TAGS="ambassador_coupons.tests.test_ambassador_coupon.${TEST_CLASS}.${TEST_METHOD}"
elif [ -n "$TEST_CLASS" ]; then
    TEST_TAGS="ambassador_coupons.tests.test_ambassador_coupon.${TEST_CLASS}"
else
    TEST_TAGS="ambassador_coupons"
fi

echo "=========================================="
echo "Ambassador Coupons - Test Runner"
echo "=========================================="
echo "Host: $ODOO_HOST:$ODOO_PORT"
echo "Database: $DATABASE"
echo "Test Tags: $TEST_TAGS"
echo "=========================================="

# Check if odoo-bin is available
if command -v odoo-bin &> /dev/null; then
    ODOO_CMD="odoo-bin"
elif [ -f "/usr/bin/odoo" ]; then
    ODOO_CMD="/usr/bin/odoo"
elif [ -f "/opt/odoo/odoo-bin" ]; then
    ODOO_CMD="/opt/odoo/odoo-bin"
else
    echo "Error: odoo-bin not found. Please ensure Odoo is installed."
    exit 1
fi

echo "Using Odoo command: $ODOO_CMD"
echo ""
echo "Starting tests..."
echo ""

$ODOO_CMD \
    -d "$DATABASE" \
    --db_host "$ODOO_HOST" \
    --db_port "$ODOO_PORT" \
    --test-tags "/$TEST_TAGS" \
    --stop-after-init \
    --logfile /tmp/odoo_test.log 2>&1 | tee /tmp/odoo_test_output.log

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Tests completed successfully!"
else
    echo "✗ Tests failed with exit code: $EXIT_CODE"
    echo "Check logs at: /tmp/odoo_test.log"
fi
echo "=========================================="

exit $EXIT_CODE
