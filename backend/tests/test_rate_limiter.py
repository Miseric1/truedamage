"""
Rate limiter tests use tiny capacities/periods so they run in well under a
second instead of actually waiting near-real-world Riot windows.
"""

import asyncio
import time

import pytest

from app.core.rate_limiter import RiotRateLimiter, TokenBucket


@pytest.mark.asyncio
async def test_token_bucket_allows_burst_up_to_capacity():
    bucket = TokenBucket(capacity=3, refill_period_seconds=10)

    start = time.monotonic()
    for _ in range(3):
        await bucket.acquire()
    elapsed = time.monotonic() - start

    # All 3 tokens were available immediately - no waiting required.
    assert elapsed < 0.05


@pytest.mark.asyncio
async def test_token_bucket_blocks_once_capacity_exhausted():
    bucket = TokenBucket(capacity=2, refill_period_seconds=0.2)

    await bucket.acquire()
    await bucket.acquire()

    start = time.monotonic()
    await bucket.acquire()  # must wait for a refill
    elapsed = time.monotonic() - start

    # Refill rate is 2 tokens / 0.2s -> ~0.1s per token.
    assert elapsed >= 0.08


@pytest.mark.asyncio
async def test_token_bucket_refills_over_time():
    bucket = TokenBucket(capacity=1, refill_period_seconds=0.1)

    await bucket.acquire()
    await asyncio.sleep(0.15)  # enough time for a full refill

    start = time.monotonic()
    await bucket.acquire()
    elapsed = time.monotonic() - start

    assert elapsed < 0.05


@pytest.mark.asyncio
async def test_riot_rate_limiter_respects_the_tighter_of_two_limits():
    # Short bucket allows plenty; long bucket only allows 1 per 0.15s -
    # the combined limiter should be gated by the long bucket.
    limiter = RiotRateLimiter(per_second_limit=100, per_two_min_limit=1)
    limiter.long_bucket = TokenBucket(capacity=1, refill_period_seconds=0.15)

    await limiter.acquire()

    start = time.monotonic()
    await limiter.acquire()
    elapsed = time.monotonic() - start

    assert elapsed >= 0.1
