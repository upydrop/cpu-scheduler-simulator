class Process:
    def __init__(self, pid, priority, burst_time, arrival_time, IO_start_time=None, IO_waiting_time=None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = self.burst_time
        self.priority = priority
        self.IO_start_time = IO_start_time
        self.IO_waiting_time = IO_waiting_time
        self.startTime = -1
        self.finishTime = -1
        self.state = "NEW"