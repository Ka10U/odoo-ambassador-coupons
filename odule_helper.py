#!/usr/bin/env python3
"""
Odoo Module Helper Script
Loads configuration from .env and provides utilities for
installing, testing, and managing the Ambassador Coupons module.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def load_env(env_file: str = ".env") -> dict:
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent / env_file
    env_vars = {}

    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()

    return env_vars


def get_env(key: str, default: str = "") -> str:
    """Get environment variable, loading from .env if not set."""
    return os.environ.get(key, load_env().get(key, default))


def run_odoo_command(args: list):
    """Run an Odoo command with proper environment."""
    env = os.environ.copy()

    odoo_bin = get_env("ODOO_BIN", "odoo-bin")
    database = get_env("DATABASE", "odoo")
    db_host = get_env("ODOO_HOST", "localhost")
    db_port = get_env("ODOO_PORT", "8069")

    cmd = [
        odoo_bin,
        "-d", database,
        "--db_host", db_host,
        "--db_port", db_port,
    ] + args

    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)

    result = subprocess.run(cmd, env=env)

    return result.returncode


def install_module():
    """Install or upgrade the module."""
    module_name = get_env("MODULE_NAME", "ambassador_coupons")
    admin_password = get_env("ADMIN_PASSWORD", "admin")

    args = [
        "-u", module_name,
        "--stop-after-init",
    ]

    return run_odoo_command(args)


def run_tests(test_tags: str = ""):
    """Run module tests."""
    module_name = get_env("MODULE_NAME", "ambassador_coupons")

    if not test_tags:
        test_tags = f"/{module_name}"

    args = [
        "--test-tags", test_tags,
        "--stop-after-init",
    ]

    return run_odoo_command(args)


def update_apps_list():
    """Update the apps list."""
    args = [
        "--update-modules",
        "--stop-after-init",
    ]

    return run_odoo_command(args)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ambassador Coupons - Odoo Module Helper"
    )
    parser.add_argument(
        "action",
        choices=["install", "test", "update", "shell"],
        help="Action to perform"
    )
    parser.add_argument(
        "--test-tags",
        help="Test tags to run (for test action)"
    )
    parser.add_argument(
        "--db",
        help="Override database name"
    )
    parser.add_argument(
        "--host",
        help="Override Odoo host"
    )
    parser.add_argument(
        "--port",
        help="Override Odoo port"
    )

    args = parser.parse_args()

    # Apply overrides
    if args.db:
        os.environ["DATABASE"] = args.db
    if args.host:
        os.environ["ODOO_HOST"] = args.host
    if args.port:
        os.environ["ODOO_PORT"] = args.port

    print("=" * 50)
    print("  Ambassador Coupons - Module Helper")
    print("=" * 50)
    print(f"  Database: {get_env('DATABASE')}")
    print(f"  Host:     {get_env('ODOO_HOST')}:{get_env('ODOO_PORT')}")
    print(f"  Module:   {get_env('MODULE_NAME')}")
    print("=" * 50)
    print()

    if args.action == "install":
        sys.exit(install_module())
    elif args.action == "test":
        sys.exit(run_tests(args.test_tags))
    elif args.action == "update":
        sys.exit(update_apps_list())
    elif args.action == "shell":
        print("To access Odoo Shell, run:")
        print(f"  {get_env('ODOO_BIN', 'odoo-bin')} -d {get_env('DATABASE')}")


if __name__ == "__main__":
    main()
