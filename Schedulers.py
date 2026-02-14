class FCFS:
    def __init__(self):
        self.readyProcesses = []

    def addProcess(self, process):
        if process not in self.readyProcesses:
            self.readyProcesses.append(process)

    def removeProcess(self, process):
        if process in self.readyProcesses:
            self.readyProcesses.remove(process)

    def getNextProcess(self, running, time):
        if running is not None:
            return running
        ready = [x for x in self.readyProcesses if x.state == "READY"]
        if len(ready) > 0:
            process = ready[0]
            self.readyProcesses.remove(process)
            return process
        else:
            return None

    def onTickEnd(self, running, time):
        pass


class SRTF:
    """Shortest Remaining Time First - Preemptive"""

    def __init__(self):
        self.readyProcesses = []

    def addProcess(self, process):
        if process not in self.readyProcesses:
            self.readyProcesses.append(process)

    def removeProcess(self, process):
        if process in self.readyProcesses:
            self.readyProcesses.remove(process)

    def getNextProcess(self, running, time):
        ready = [x for x in self.readyProcesses if x.state == "READY"]

        if len(ready) == 0:
            return running if running and running.state == "RUNNING" else None

        ready.sort(key=lambda x: x.remaining_time)
        shortest = ready[0]

        if running is not None and running.state == "RUNNING":
            if shortest.remaining_time < running.remaining_time:
                if running not in self.readyProcesses:
                    running.state = "READY"
                    self.readyProcesses.append(running)
                self.readyProcesses.remove(shortest)
                return shortest
            else:
                return running
        else:
            self.readyProcesses.remove(shortest)
            return shortest

    def onTickEnd(self, running, time):
        pass


class RoundRobin:
    """Round Robin with configurable time quantum"""

    def __init__(self, quantum=2):
        self.readyProcesses = []
        self.quantum = quantum
        self.current_quantum = 0

    def onProcessWaiting(self):
        self.current_quantum = 0

    def addProcess(self, process):
        if process not in self.readyProcesses:
            self.readyProcesses.append(process)

    def removeProcess(self, process):
        if process in self.readyProcesses:
            self.readyProcesses.remove(process)
            self.current_quantum = 0

    def getNextProcess(self, running, time):
        if running is not None and running.state == "RUNNING":
            if self.current_quantum >= self.quantum:
                if running not in self.readyProcesses:
                    running.state = "READY"
                    self.readyProcesses.append(running)
                self.current_quantum = 0
            else:
                return running
        ready = [x for x in self.readyProcesses if x.state == "READY"]
        if len(ready) > 0:
            process = ready[0]
            self.readyProcesses.remove(process)
            self.current_quantum = 0
            return process
        else:
            return None

    def onTickEnd(self, running, time):
        if running is not None and running.state == "RUNNING":
            self.current_quantum += 1


class Priority:
    """Priority Scheduling - Lower number = Higher priority, Preemptive"""

    def __init__(self):
        self.readyProcesses = []

    def addProcess(self, process):
        if process not in self.readyProcesses:
            self.readyProcesses.append(process)

    def removeProcess(self, process):
        if process in self.readyProcesses:
            self.readyProcesses.remove(process)

    def getNextProcess(self, running, time):
        ready = [x for x in self.readyProcesses if x.state == "READY"]

        if len(ready) == 0:
            return running if running and running.state == "RUNNING" else None

        ready.sort(key=lambda x: x.priority)
        highest_priority = ready[0]

        if running is not None and running.state == "RUNNING":
            if highest_priority.priority < running.priority:
                if running not in self.readyProcesses:
                    running.state = "READY"
                    self.readyProcesses.append(running)
                self.readyProcesses.remove(highest_priority)
                return highest_priority
            else:
                return running
        else:
            self.readyProcesses.remove(highest_priority)
            return highest_priority

    def onTickEnd(self, running, time):
        pass


class MLFQ:
    """Multi-Level Feedback Queue"""
    def __init__(self, num_queues=3, quantum_base=2):
        self.num_queues = num_queues
        self.queues = [[] for _ in range(num_queues)]
        self.quantum_base = quantum_base
        self.current_quantum = 0
        self.process_queue_level = {}

    def addProcess(self, process):
        if process.pid not in self.process_queue_level:
            self.process_queue_level[process.pid] = 0

        queue_level = self.process_queue_level[process.pid]

        if process not in self.queues[queue_level]:
            self.queues[queue_level].append(process)

    def removeProcess(self, process):
        for queue in self.queues:
            if process in queue:
                queue.remove(process)

        if process.pid in self.process_queue_level:
            del self.process_queue_level[process.pid]

    def onProcessWaiting(self):
        self.current_quantum = 0

    def getNextProcess(self, running, time):
        if running is not None and running.state == "RUNNING":
            queue_level = self.process_queue_level[running.pid]
            quantum = self.quantum_base * (2 ** queue_level)

            if self.current_quantum >= quantum:
                new_level = min(queue_level + 1, self.num_queues - 1)
                self.process_queue_level[running.pid] = new_level

                if running in self.queues[queue_level]:
                    self.queues[queue_level].remove(running)

                if running not in self.queues[new_level]:
                    running.state = "READY"
                    self.queues[new_level].append(running)

                self.current_quantum = 0
            else:
                return running

        for level in range(self.num_queues):
            ready = [x for x in self.queues[level] if x.state == "READY"]
            if len(ready) > 0:
                process = ready[0]
                self.queues[level].remove(process)
                self.current_quantum = 0
                return process

        return None

    def onTickEnd(self, running, time):
        if running is not None and running.state == "RUNNING":
            self.current_quantum += 1