import asyncio


class Retry(object):
    def __init__(self, p_timeout, p_attempts):
        self.timeout = p_timeout
        self.attempts = p_attempts

    async def perform_func(self, p_func):
        for i in range(self.attempts):
            try:
                print('Attempt ' + str(i + 1))
                await asyncio.wait_for(p_func(), timeout=self.timeout)
                return
            except asyncio.TimeoutError:
                print('Fault!')
        print('Attempt number exceeded!')
