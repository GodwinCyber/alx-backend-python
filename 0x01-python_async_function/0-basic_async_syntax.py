#!/usr/bin/env python3
"""Module one"""

import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """Wait for a random delay"""
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
