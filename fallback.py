import asyncio


class Fallback(object):
    def __init__(self, p_timeout, p_fallback_func):
        self.timeout = p_timeout
        self.fallback_func = p_fallback_func

    async def perform_func(self, p_func):
        try:
            await asyncio.wait_for(p_func(), timeout=self.timeout)
        except asyncio.TimeoutError:
            self.fallback_func()
