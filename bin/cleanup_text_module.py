#!/usr/bin/env python3

"""
Unicode Text Cleaner Module

This module provides the core Unicode cleaning functionality for the UnicodeFix web interface.
It's extracted from the command-line cleanup-text.py script for easier importing.
"""

import os
import re


def clean_text(text: str) -> str:
    """
    Normalize problematic or invisible Unicode characters to safe ASCII equivalents.

    This function performs multiple operations:
    1. Converts typographic characters (quotes, dashes) to their ASCII equivalents
    2. Removes zero-width and invisible Unicode characters
    3. Normalizes line endings for cross-platform compatibility
    4. Removes trailing whitespace

    Args:
        text (str): The input text containing Unicode characters

    Returns:
        str: The cleaned text with normalized ASCII characters

    Example:
        >>> clean_text('"Hello" — World')
        '"Hello" - World'
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    if not text:
        return text
    
    replacements = {
        '\u2018': "'", '\u2019': "'",  # Smart single quotes
        '\u201C': '"', '\u201D': '"',  # Smart double quotes
        '\u2013': '-', '\u2014': '-',  # En and em dashes
        '\u2026': '...',  # Ellipsis
        '\u00A0': ' ',    # Non-breaking space
    }
    
    # Apply character replacements
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)

    # Remove zero-width characters and other invisible characters
    text = re.sub(r'[\u200B\u200C\u200D\uFEFF\u00AD]', '', text)

    # Normalize line endings (convert all to \n, then to platform-specific)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove trailing whitespace on every line
    text = re.sub(r'[ \t]+\n', '\n', text)
    
    # Convert back to platform-specific line endings if needed
    if os.name == 'nt':  # Windows
        text = text.replace('\n', '\r\n')

    return text


def get_unicode_info(text: str) -> dict:
    """
    Get information about Unicode characters in the text.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: Dictionary with Unicode character statistics
    """
    if not text:
        return {
            'total_chars': 0,
            'ascii_chars': 0,
            'unicode_chars': 0,
            'problematic_chars': 0,
            'invisible_chars': 0
        }
    
    total_chars = len(text)
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    unicode_chars = total_chars - ascii_chars
    
    # Count problematic characters that would be replaced
    problematic_patterns = [
        '\u2018', '\u2019',  # Smart single quotes
        '\u201C', '\u201D',  # Smart double quotes
        '\u2013', '\u2014',  # En and em dashes
        '\u2026',           # Ellipsis
        '\u00A0',           # Non-breaking space
    ]
    
    problematic_chars = sum(text.count(char) for char in problematic_patterns)
    
    # Count invisible characters
    invisible_pattern = r'[\u200B\u200C\u200D\uFEFF\u00AD]'
    invisible_chars = len(re.findall(invisible_pattern, text))
    
    return {
        'total_chars': total_chars,
        'ascii_chars': ascii_chars,
        'unicode_chars': unicode_chars,
        'problematic_chars': problematic_chars,
        'invisible_chars': invisible_chars
    } 