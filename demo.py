import asyncio
import time

import circuit_breaker
import retry
import timeout
import fallback


NORMAL_EXEC_TIME = 1
SLOW_EXEC_TIME = 5


def fallback_func():
    print('Fallback func has been performed!')


async def normal_performance():
    await asyncio.sleep(NORMAL_EXEC_TIME)
    print('normal_func has been performed!')


async def slow_performance():
    await asyncio.sleep(SLOW_EXEC_TIME)
    print('slow_func has been performed!')


async def sleep_ten_sec():
    await asyncio.sleep(11)


def simulates_temporarily_unavailable_service(pattern):
    # service operates normally
    asyncio.run(pattern.perform_func(normal_performance))
    asyncio.run(pattern.perform_func(normal_performance))

    # service operates too slowly (considered as unavailable)
    asyncio.run(pattern.perform_func(slow_performance))
    asyncio.run(pattern.perform_func(slow_performance))
    asyncio.run(pattern.perform_func(slow_performance))
    asyncio.run(pattern.perform_func(slow_performance))
    asyncio.run(pattern.perform_func(normal_performance))
    asyncio.run(pattern.perform_func(slow_performance))

    print('Wait for 10 secs...')
    asyncio.run(sleep_ten_sec())

    # service operates normally again
    asyncio.run(pattern.perform_func(normal_performance))
    asyncio.run(pattern.perform_func(normal_performance))
    asyncio.run(pattern.perform_func(normal_performance))
    asyncio.run(pattern.perform_func(normal_performance))

    print('Wait for 10 secs...')
    asyncio.run(sleep_ten_sec())

    asyncio.run(pattern.perform_func(normal_performance))
    asyncio.run(pattern.perform_func(normal_performance))
    asyncio.run(pattern.perform_func(normal_performance))
    asyncio.run(pattern.perform_func(normal_performance))


TIMEOUT = 2
THRESHOLD = 3
FAULT_TIMEOUT = 20


def main():
    to = timeout.Timeout(TIMEOUT)
    fb = fallback.Fallback(TIMEOUT, fallback_func)
    rt = retry.Retry(TIMEOUT, THRESHOLD)
    cb = circuit_breaker.CircuitBreaker(FAULT_TIMEOUT, THRESHOLD, TIMEOUT)

    print('Timeout Pattern deals with temporarily unavailable service:\n')
    simulates_temporarily_unavailable_service(to)
    print('Fallback Pattern deals with temporarily unavailable service:\n')
    simulates_temporarily_unavailable_service(fb)
    print('Retry Pattern deals with temporarily unavailable service:\n')
    simulates_temporarily_unavailable_service(rt)
    print('Circuit Breaker Pattern deals with temporarily unavailable service:\n')
    simulates_temporarily_unavailable_service(cb)


main()
