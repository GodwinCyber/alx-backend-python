#!/usr/bin/env python3
"""Task Three module Three"""

import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Task wait random"""
    return asyncio.create_task(wait_random(max_delay))
