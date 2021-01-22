import asyncio


class Timeout(object):
    def __init__(self, p_timeout):
        self.timeout = p_timeout

    async def perform_func(self, p_func):
        try:
            await asyncio.wait_for(p_func(), timeout=self.timeout)
        except asyncio.TimeoutError:
            print('Timeout! Nothing has been performed!')
