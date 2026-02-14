# Schedulers You Can Compare (Algorithms and Parameters)

## Round Robin: How Quantum Changes Results 🔄

The **Round Robin** scheduler cycles through processes in fixed time slices (quanta). Adjusting the quantum directly impacts response and waiting times. Below we document the `RoundRobin` class in **Schedulers.py**, explain its mechanics, show how **main.py** runs two variants (q=2 and q=4), and illustrate the effect on common metrics.

---

## RoundRobin Class Overview

The `RoundRobin` class implements a preemptive, time-slice scheduler. It maintains a FIFO ready queue and tracks how long the current process has executed.

```python
class RoundRobin:
    """Round Robin with configurable time quantum"""
    def __init__(self, quantum=2):
        self.readyProcesses = []
        self.quantum = quantum       # time slice length
        self.current_quantum = 0     # ticks run so far
```

Every new process joins `readyProcesses`; `current_quantum` resets whenever a process blocks or is preempted .

---

## Core Attributes and Methods

| **Member** | **Purpose** |
| --- | --- |
| `quantum` | Maximum ticks a process may run before preemption |
| `current_quantum` | Counts ticks since last context switch or IO block |
| `addProcess(p)` | Enqueue `p` if not already ready |
| `removeProcess(p)` | Dequeue `p` and reset `current_quantum` |
| `onProcessWaiting()` | Called when `p` blocks for IO; resets `current_quantum` |
| `getNextProcess(r,t)` |


- Continues running if quantum remains
- Otherwise preempts and rotates to queue
- Then dequeues next ready process  |

| `onTickEnd(r,t)` | Increments `current_quantum` after each CPU tick |
| --- | --- |


---

## Algorithm Workflow

1. **Arrival/Ready**
2. On each tick, newly arrived or IO-returned processes call `addProcess`.
3. **Selection**
4. `getNextProcess` checks if the running process has exceeded its quantum.
5. If so, it is set to READY and re-enqueued.
6. Otherwise, it continues.
7. **Context Switch**
8. When quantum expires or a process blocks for IO (`onProcessWaiting`), `current_quantum` resets.
9. **Time Accounting**
10. After each tick, `onTickEnd` increments the quantum counter for the running process.

```python
def getNextProcess(self, running, time):
    if running and running.state == "RUNNING":
        if self.current_quantum >= self.quantum:
            running.state = "READY"
            self.readyProcesses.append(running)
            self.current_quantum = 0
        else:
            return running

    for p in self.readyProcesses:
        if p.state == "READY":
            self.readyProcesses.remove(p)
            self.current_quantum = 0
            return p
    return None
```

---

## Configuration in main.py

`main.py` instantiates two Round Robin variants:

```python
schedulers = [
    ("Round Robin (q=2)", RoundRobin(quantum=2)),
    ("Round Robin (q=4)", RoundRobin(quantum=4)),
    # … other schedulers …
]
```

This drives two separate simulations, producing separate metric lines for q=2 and q=4 .

---

## Adding More Variants

To experiment with other time slices, simply extend the `schedulers` list. For example:

```python
("Round Robin (q=8)", RoundRobin(quantum=8)),
("Round Robin (q=16)", RoundRobin(quantum=16)),
```

Each entry will appear as its own column in the results tables.

---

## Impact of Quantum on Metrics

Below is a sample from the **CPU-bound** workload (50 processes). Notice how **increasing quantum** roughly doubles average response time while slightly reducing waiting time :

| Scheduler | Avg Waiting | Avg Response | Avg Turnaround | Throughput |
| --- | --- | --- | --- | --- |
| ------------------- | ------------: | -------------: | ---------------: | -----------: |
| Round Robin (q=2) | 4366.44 | 47.42 | 4465.90 | 0.0101 |
| Round Robin (q=4) | 4361.52 | 95.38 | 4460.98 | 0.0101 |


**Observations**

- **Smaller quantum (q=2)**: faster response (lower `Avg Response`), but more context switches.
- **Larger quantum (q=4)**: higher response time, slightly lower waiting time.

Similar patterns appear in **IO-bound** and **Mixed-bound** workloads (see `results/IO-bound.txt` and `results/Mixed-bound.txt`) .