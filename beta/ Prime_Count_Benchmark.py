#!/usr/bin/env python3
"""
🧮 CPU Prime Benchmark
Remote-ready: curl ... | python3
"""

import time
import multiprocessing as mp


def boxed(msg: str) -> str:
    """Draw a box around msg."""
    b = f"+{'-'*len(msg)}+"
    return f"{b}\n|{msg}|\n{b}"


def is_prime(n: int) -> bool:
    """Naïve primality test."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


def count_primes(limit: int) -> int:
    """Count primes < limit."""
    return sum(1 for i in range(limit) if is_prime(i))


def main():
    print(boxed("🧮 CPU Prime Benchmark"))
    limits = [100_000, 200_000]

    # Single-threaded run
    for L in limits:
        t0 = time.time()
        cnt = count_primes(L)
        print(f"Single-thread: {cnt} primes < {L:,} in {time.time() - t0:.2f}s")

    # Multi-core run
    workers = mp.cpu_count()
    print(f"\nSpawning {workers} workers (each ⟨{limits[0]:,}⟩)…")
    t0 = time.time()
    with mp.Pool(workers) as pool:
        results = pool.map(count_primes, [limits[0]] * workers)
    total = sum(results)
    print(f"Multi-core: {total} primes ({workers}×{limits[0]:,}) in {time.time() - t0:.2f}s")


if __name__ == "__main__":
    # Make sure multiprocessing works when piping from stdin
    mp.freeze_support()      # no-op on macOS/Linux, needed for Windows spawn
    try:
        # switch to fork whenever it’s available
        mp.set_start_method("fork", force=True)
    except (RuntimeError, ValueError):
        pass
    main()
