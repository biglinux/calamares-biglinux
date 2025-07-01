#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAC Translation Utils
Utilities for translation support using gettext
"""

import gettext

# Configure the translation domain/name
gettext.textdomain("calamares-biglinux")

# Export _ directly as the translation function
_ = gettext.gettext


def setup_i18n():
    """Setup internationalization (already configured above)
    
    Returns:
        The translation function
    """
    return _