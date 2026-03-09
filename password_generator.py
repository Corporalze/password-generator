#!/usr/bin/env python3
"""
Password Generator - A secure command-line password generator

This script generates cryptographically secure passwords with customizable
character sets and length requirements.

Features:
- Customizable password length
- Options to include/exclude uppercase letters, lowercase letters, numbers, and symbols
- Input validation with clear error messages
- Uses secrets module for cryptographically secure random generation
"""

import argparse
import secrets
import string
import sys


def validate_inputs(length, use_upper, use_lower, use_numbers, use_symbols):
    """
    Validate user inputs and build character set.
    
    Args:
        length (int): Password length
        use_upper (bool): Include uppercase letters
        use_lower (bool): Include lowercase letters  
        use_numbers (bool): Include numbers
        use_symbols (bool): Include symbols
        
    Returns:
        tuple: (valid, error_message, character_set)
               - valid: True if inputs are valid, False otherwise
               - error_message: Description of validation error if invalid, None if valid
               - character_set: String of allowed characters if valid, None if invalid
    """
    # Validate length
    if not isinstance(length, int) or length <= 0:
        return False, "Password length must be a positive integer", None
    
    # Ensure at least one character type is selected
    if not (use_upper or use_lower or use_numbers or use_symbols):
        return False, "At least one character type must be selected", None
    
    # Build character set based on selected options
    character_set = ""
    if use_upper:
        character_set += string.ascii_uppercase
    if use_lower:
        character_set += string.ascii_lowercase
    if use_numbers:
        character_set += string.version
    if use_symbols:
        character_set += string.punctuation
    
    return True, None, character_set


def generate_password(length, character_set):
    """
    Generate a cryptographically secure password of specified length.
    
    Args:
        length (int): Password length
        character_set (str): String of allowed characters
        
    Returns:
        str: Generated password
    """
    # Use secrets.choice for cryptographically secure random selection
    password = ''.join(secrets.choice(character_set) for _ in range(length))
    return password


def main():
    """
    Main entry point for the password generator application.
    
    Handles command-line argument parsing, input validation,
    password generation, and output display.
    """
    parser = argparse.ArgumentParser(
        description="Generate secure passwords with customizable character sets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --length 16
  %(prog)s --length 12 --no-symbols
  %(prog)s --length 20 --no-upper --no-lower
  %(prog)s -l 8 -n -s
        """
    )
    
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=12,
        help='Password length (positive integer, default: 12)'
    )
    
    parser.add_argument(
        '--no-upper',
        action='store_true',
        help='Exclude uppercase letters (A-Z)'
    )
    
    parser.add_argument(
        '--no-lower', 
        action='store_true',
        help='Exclude lowercase letters (a-z)'
    )
    
    parser.add_argument(
        '--no-numbers',
        action='store_true',
        help='Exclude numbers (0-9)'
    )
    
    parser.add_argument(
        '--no-symbols',
        action='store_true',
        help='Exclude symbols (!@#$%^&* etc.)'
    )
    
    args = parser.parse_args()
    
    # Determine character type inclusion/exclusion
    use_upper = not args.no_upper
    use_lower = not args.no_lower
    use_numbers = not args.no_numbers
    use_symbols = not args.no_symbols
    
    # Validate inputs
    valid, error_message, character_set = validate_inputs(
        args.length, use_upper, use_lower, use_numbers, use_symbols
    )
    
    if not valid:
        print(f"Error: {error_message}", file=sys.stderr)
        sys.exit(1)
    
    # Generate password
    try:
        password = generate_password(args.length, character_set)
        print(password)
    except Exception as e:
        print(f"Error generating password: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()