#!/bin/bash
# Test runner script for Ambassador Coupons module on Odoo 18
# Loads configuration from .env file

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment variables from .env file if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
else
    echo "Warning: .env file not found. Using default values."
fi

# Allow command-line overrides
ODOO_HOST="${1:-$ODOO_HOST}"
ODOO_PORT="${2:-$ODOO_PORT}"
DATABASE="${3:-$DATABASE}"
ADMIN_PASSWORD="${4:-$ADMIN_PASSWORD}"

# Defaults
ODOO_HOST="${ODOO_HOST:-localhost}"
ODOO_PORT="${ODOO_PORT:-8069}"
DATABASE="${DATABASE:-odoo}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"
MODULE_NAME="${MODULE_NAME:-ambassador_coupons}"
TEST_TAGS="${TEST_TAGS:-$MODULE_NAME}"
ODOO_BIN="${ODOO_BIN:-odoo-bin}"

# Test class/method from arguments
TEST_CLASS="${5:-}"
TEST_METHOD="${6:-}"

# Build test tags
if [ -n "$TEST_METHOD" ]; then
    FULL_TEST_TAGS="${MODULE_NAME}.tests.test_${MODULE_NAME}.${TEST_CLASS}.${TEST_METHOD}"
elif [ -n "$TEST_CLASS" ]; then
    FULL_TEST_TAGS="${MODULE_NAME}.tests.test_${MODULE_NAME}.${TEST_CLASS}"
else
    FULL_TEST_TAGS="/${TEST_TAGS}"
fi

echo "=========================================="
echo "  Ambassador Coupons - Test Runner"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  Host:        $ODOO_HOST:$ODOO_PORT"
echo "  Database:     $DATABASE"
echo "  Module:       $MODULE_NAME"
echo "  Test Tags:    $FULL_TEST_TAGS"
echo "  Odoo Binary:  $ODOO_BIN"
echo ""
echo "=========================================="

# Check if odoo-bin is available
if ! command -v "$ODOO_BIN" &> /dev/null; then
    echo "Error: '$ODOO_BIN' not found in PATH."
    echo ""
    echo "Please either:"
    echo "  1. Install Odoo and ensure it's in your PATH"
    echo "  2. Set ODOO_BIN in .env to the full path (e.g., /opt/odoo/odoo-bin)"
    echo "  3. Create a symlink: ln -s /path/to/odoo-bin /usr/local/bin/odoo-bin"
    exit 1
fi

echo "Using Odoo binary: $(which $ODOO_BIN)"
echo ""
echo "Starting tests..."
echo ""

# Run the tests
$ODOO_BIN \
    -d "$DATABASE" \
    --db_host "$ODOO_HOST" \
    --db_port "$ODOO_PORT" \
    --test-tags "$FULL_TEST_TAGS" \
    --stop-after-init \
    --logfile /tmp/odoo_test.log 2>&1 | tee /tmp/odoo_test_output.log

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "  ✓ Tests completed successfully!"
else
    echo "  ✗ Tests failed with exit code: $EXIT_CODE"
    echo ""
    echo "Check logs at: /tmp/odoo_test.log"
fi
echo "=========================================="

exit $EXIT_CODE
