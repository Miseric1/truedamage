"""
Token-bucket rate limiter for the Riot API.

Riot enforces two simultaneous limits on a dev key (e.g. 20 req/1s AND
100 req/2min). A single bucket can't model that - you need two independent
buckets and must acquire from both before a request is allowed through.

This is async-native (asyncio.Lock + asyncio.sleep) so it can be awaited
directly from route handlers/services without blocking the event loop.
"""

import asyncio
import time


class TokenBucket:
    """Continuous-refill token bucket: `capacity` tokens refill smoothly
    over `refill_period_seconds`, rather than resetting in a hard step at
    the end of the window (which would let a burst through right at the
    window boundary)."""

    def __init__(self, capacity: int, refill_period_seconds: float) -> None:
        self.capacity = float(capacity)
        self.refill_period_seconds = refill_period_seconds
        self.tokens = float(capacity)
        self._lock = asyncio.Lock()
        self._last_refill = time.monotonic()

    async def acquire(self) -> None:
        while True:
            async with self._lock:
                now = time.monotonic()
                elapsed = now - self._last_refill
                refill_rate = self.capacity / self.refill_period_seconds
                self.tokens = min(self.capacity, self.tokens + elapsed * refill_rate)
                self._last_refill = now

                if self.tokens >= 1:
                    self.tokens -= 1
                    return

                # Not enough tokens yet - compute exactly how long until we have one.
                deficit = 1 - self.tokens
                wait_seconds = deficit / refill_rate

            await asyncio.sleep(wait_seconds)


class RiotRateLimiter:
    """Wraps a short (per-second) and long (per-2-minutes) bucket. A caller
    must clear both before a request is allowed, since Riot enforces both
    limits simultaneously."""

    def __init__(self, per_second_limit: int, per_two_min_limit: int) -> None:
        self.short_bucket = TokenBucket(per_second_limit, refill_period_seconds=1.0)
        self.long_bucket = TokenBucket(per_two_min_limit, refill_period_seconds=120.0)

    async def acquire(self) -> None:
        # Acquire long bucket first: it's the scarcer resource, so if we're
        # going to have to wait, we want to wait on it rather than burn a
        # short-bucket token and then block anyway.
        await self.long_bucket.acquire()
        await self.short_bucket.acquire()
