#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Run tests for Plan.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from plan.testsuite import main


if __name__ == "__main__":
    main()
