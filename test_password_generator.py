#!/usr/bin/env python3
"""
Tests for the Password Generator

Run with: python -m pytest test_password_generator.py
Or:       python test_password_generator.py
"""

import string
import subprocess
import sys

# Import the functions to test
from password_generator import validate_inputs, generate_password


def test_validate_inputs_valid():
    """Test validation with valid inputs (all character types)."""
    valid, error, charset = validate_inputs(16, True, True, True, True)
    assert valid is True
    assert error is None
    assert string.ascii_uppercase in charset
    assert string.ascii_lowercase in charset
    assert string.digits in charset
    assert string.punctuation in charset
    print("  ✓ test_validate_inputs_valid")


def test_validate_inputs_length_zero():
    """Test validation rejects zero length."""
    valid, error, charset = validate_inputs(0, True, True, True, True)
    assert valid is False
    assert "positive integer" in error
    assert charset is None
    print("  ✓ test_validate_inputs_length_zero")


def test_validate_inputs_negative_length():
    """Test validation rejects negative length."""
    valid, error, charset = validate_inputs(-5, True, True, True, True)
    assert valid is False
    assert "positive integer" in error
    print("  ✓ test_validate_inputs_negative_length")


def test_validate_inputs_no_char_types():
    """Test validation rejects when no character types are selected."""
    valid, error, charset = validate_inputs(16, False, False, False, False)
    assert valid is False
    assert "At least one character type" in error
    print("  ✓ test_validate_inputs_no_char_types")


def test_validate_inputs_uppercase_only():
    """Test validation with only uppercase letters."""
    valid, error, charset = validate_inputs(8, True, False, False, False)
    assert valid is True
    assert charset == string.ascii_uppercase
    print("  ✓ test_validate_inputs_uppercase_only")


def test_validate_inputs_numbers_and_symbols():
    """Test validation with numbers and symbols only."""
    valid, error, charset = validate_inputs(10, False, False, True, True)
    assert valid is True
    assert string.digits in charset
    assert string.punctuation in charset
    assert string.ascii_uppercase not in charset
    assert string.ascii_lowercase not in charset
    print("  ✓ test_validate_inputs_numbers_and_symbols")


def test_generate_password_length():
    """Test generated password has correct length."""
    charset = string.ascii_letters + string.digits
    password = generate_password(20, charset)
    assert len(password) == 20
    print("  ✓ test_generate_password_length")


def test_generate_password_characters():
    """Test generated password only contains characters from the set."""
    charset = string.ascii_letters + string.digits
    password = generate_password(50, charset)
    for char in password:
        assert char in charset, f"Character '{char}' not in character set"
    print("  ✓ test_generate_password_characters")


def test_generate_password_symbols_only():
    """Test password generation with only symbols."""
    charset = string.punctuation
    password = generate_password(15, charset)
    assert len(password) == 15
    for char in password:
        assert char in string.punctuation
    print("  ✓ test_generate_password_symbols_only")


def test_generate_password_uniqueness():
    """Test that two generated passwords are not identical (statistical check)."""
    charset = string.ascii_letters + string.digits + string.punctuation
    passwords = {generate_password(32, charset) for _ in range(10)}
    # With 32 chars from ~94 possibilities, collisions are astronomically unlikely
    assert len(passwords) == 10, "Generated passwords should be unique"
    print("  ✓ test_generate_password_uniqueness")


def test_cli_default():
    """Test CLI with default arguments."""
    result = subprocess.run(
        [sys.executable, "password_generator.py"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    password = result.stdout.strip()
    assert len(password) == 12, f"Expected length 12, got {len(password)}"
    print(f"  ✓ test_cli_default (password: {password})")


def test_cli_custom_length():
    """Test CLI with custom length."""
    result = subprocess.run(
        [sys.executable, "password_generator.py", "--length", "20"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    password = result.stdout.strip()
    assert len(password) == 20, f"Expected length 20, got {len(password)}"
    print(f"  ✓ test_cli_custom_length (password: {password})")


def test_cli_no_symbols():
    """Test CLI with --no-symbols flag."""
    result = subprocess.run(
        [sys.executable, "password_generator.py", "--no-symbols"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    password = result.stdout.strip()
    for char in password:
        assert char not in string.punctuation, f"Found symbol '{char}'"
    print(f"  ✓ test_cli_no_symbols (password: {password})")


def test_cli_numbers_only():
    """Test CLI with only numbers."""
    result = subprocess.run(
        [
            sys.executable, "password_generator.py",
            "--no-upper", "--no-lower", "--no-symbols"
        ],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    password = result.stdout.strip()
    for char in password:
        assert char in string.digits, f"Found non-digit '{char}'"
    print(f"  ✓ test_cli_numbers_only (password: {password})")


def test_cli_invalid_length():
    """Test CLI with invalid (zero) length."""
    result = subprocess.run(
        [sys.executable, "password_generator.py", "--length", "0"],
        capture_output=True, text=True
    )
    assert result.returncode == 1
    assert "positive integer" in result.stderr
    print("  ✓ test_cli_invalid_length")


def test_cli_help():
    """Test CLI help message."""
    result = subprocess.run(
        [sys.executable, "password_generator.py", "--help"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Password" in result.stdout
    assert "--length" in result.stdout
    assert "--no-symbols" in result.stdout
    print("  ✓ test_cli_help")


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Password Generator Test Suite")
    print("=" * 60)

    tests = [
        ("Unit Tests", [
            test_validate_inputs_valid,
            test_validate_inputs_length_zero,
            test_validate_inputs_negative_length,
            test_validate_inputs_no_char_types,
            test_validate_inputs_uppercase_only,
            test_validate_inputs_numbers_and_symbols,
            test_generate_password_length,
            test_generate_password_characters,
            test_generate_password_symbols_only,
            test_generate_password_uniqueness,
        ]),
        ("CLI Integration Tests", [
            test_cli_default,
            test_cli_custom_length,
            test_cli_no_symbols,
            test_cli_numbers_only,
            test_cli_invalid_length,
            test_cli_help,
        ]),
    ]

    passed = 0
    failed = 0

    for section, test_funcs in tests:
        print(f"\n--- {section} ---")
        for test_func in test_funcs:
            try:
                test_func()
                passed += 1
            except AssertionError as e:
                print(f"  ✗ {test_func.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"  ✗ {test_func.__name__}: Unexpected error: {e}")
                failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
