# Schedulers You Can Compare (Algorithms and Parameters)

This section describes two baseline CPU scheduling algorithms—**FCFS** and **SRTF**—implemented in `Schedulers.py`. You can use these to observe how non-preemptive versus preemptive, shortest-job strategies impact metrics like waiting time, response time, turnaround time, and throughput in the simulator.

## FCFS (First-Come, First-Served)

FCFS processes tasks in the exact order they arrive, without interruption once they start. It serves as a **baseline non-preemptive** scheduler, illustrating fairness but often resulting in higher average waiting times for later jobs.

- **Data structure**: Maintains a simple FIFO list called `readyProcesses`.
- **Non-preemptive**: Once a process is running, it continues until completion.
- **Selection rule**: Always picks the earliest-arrived READY process.

### getNextProcess Logic

Retrieves the next process to run:

```python
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
```

- If a process is already running, it remains in place.
- Otherwise, selects `readyProcesses[0]` and removes it from the queue.
- Returns `None` if no READY processes exist.

## SRTF (Shortest Remaining Time First)

SRTF is a **preemptive** variant of shortest-job scheduling. It continuously compares the remaining CPU burst of the running process against newly arrived or ready tasks, ensuring the CPU always serves the process closest to completion.

- **Data structure**: Keeps an unsorted list `readyProcesses`, sorted on demand by `remaining_time`.
- **Preemption**: Running processes can be preempted if a shorter job arrives.
- **Selection rule**: Always picks the READY process with minimal `remaining_time`.

### getNextProcess Logic

Determines whether to continue running the current process or switch to a shorter one:

```python
def getNextProcess(self, running, time):
    ready = [x for x in self.readyProcesses if x.state == "READY"]
    if len(ready) == 0:
        return running if running and running.state == "RUNNING" else None

    # Identify the process with the smallest remaining_time
    ready.sort(key=lambda x: x.remaining_time)
    shortest = ready[0]

    if running is not None and running.state == "RUNNING":
        if shortest.remaining_time < running.remaining_time:
            # Preempt: demote current process back to READY
            if running not in self.readyProcesses:
                running.state = "READY"
                self.readyProcesses.append(running)
            self.readyProcesses.remove(shortest)
            return shortest
        else:
            return running
    else:
        # No running process: dispatch the shortest one
        self.readyProcesses.remove(shortest)
        return shortest
```

- If no READY processes, continues with the current RUNNING process (if any).
- Sorts READY processes by `remaining_time` and picks the shortest.
- Preempts the running process only if a shorter job exists, re-enqueuing it.

## Feature Comparison

| ⚙️ Feature | FCFS | SRTF |
| --- | --- | --- |
| **Preemptive** | No | Yes |
| **Selection criterion** | Arrival order (FIFO) | Smallest remaining burst |
| **Potential starvation** | No | High (long jobs may starve) |
| **Average waiting time** | Generally higher | Often lower |
| **Complexity per tick** | O(n) filtering | O(n log n) sorting |
| **Typical use case** | Fairness baseline | Minimizing latency |


```card
{
    "title": "Starvation Warning",
    "content": "SRTF may starve long-running processes if many shorter jobs arrive."
}
```

---

By comparing FCFS and SRTF, you’ll see how preemption and shortest-job prioritization can dramatically alter scheduling metrics in the simulator.