import asyncio
import time


class CircuitBreaker(object):
    state = ""   # CB state
    fault_timeout = 0   # a duration to consider a fault as a recent one
    threshold = 0  # CB threshold
    resent_errors_tss = []  # occurred error timestamps are logged here
    timeout = 0  # function performing timeout

    def __init__(self, p_fault_timeout, p_threshold, p_timeout):
        self.fault_timeout = p_fault_timeout
        self.threshold = p_threshold
        self.state = "CLOSED"
        self.timeout = p_timeout

    def _update_recent_errors(self):
        for error_ts in self.resent_errors_tss:
            if time.time() > error_ts + self.fault_timeout:
                self.resent_errors_tss.remove(error_ts)

    async def perform_func(self, p_func):
        if self.state == "CLOSED":
            try:
                await asyncio.wait_for(p_func(), timeout=self.timeout)
            except asyncio.TimeoutError:
                self.resent_errors_tss.append(time.time())
                print("Fault. \n")
                self._update_recent_errors()
                if len(self.resent_errors_tss) >= self.threshold:
                    self.state = "OPEN"
                    print("Switched to the OPEN state. \n")
        elif self.state == "OPEN":
            now = time.time()
            if now > max(self.resent_errors_tss) + self.fault_timeout:
                self.state = "HALF-OPEN"
                print("Switched to the HALF-OPEN state. \n")
            else:
                print("Service unavailable.")
        if self.state == "HALF-OPEN":
            try:
                await asyncio.wait_for(p_func(), timeout=self.timeout)
                self.resent_errors_tss.clear()
                self.state = "CLOSED"
                print("Switched to the CLOSED state. \n")
            except asyncio.TimeoutError:
                self.resent_errors_tss.append(time.time())
                print("Fault. \n")
                self._update_recent_errors()

                self.state = "OPEN"
                print("Switched to the OPEN state. \n")

