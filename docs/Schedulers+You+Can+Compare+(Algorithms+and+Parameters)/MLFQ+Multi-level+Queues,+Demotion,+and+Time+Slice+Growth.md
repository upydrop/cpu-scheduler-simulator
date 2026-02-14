# Multi-Level Feedback Queue (MLFQ) Scheduler ⚙️

The **Multi-Level Feedback Queue (MLFQ)** scheduler dynamically adjusts a process’s time slice based on its observed CPU usage. By using multiple queues with exponentially increasing time quanta, MLFQ favors interactive (short-burst) processes while still servicing CPU-bound tasks fairly .

## Key Parameters

MLFQ exposes two configurable parameters at initialization:

- **num_queues**: Number of priority levels (queues).
- **quantum_base**: Base time quantum for the highest-priority queue.

These determine how many queues exist and how time slices grow at lower priorities.

## Time Slice Growth

Each queue level `L` has a time slice calculated as:

| Level (L) | Time Slice (quantum) |
| --- | --- |
| 0 | `quantum_base * 2^0` |
| 1 | `quantum_base * 2^1` |
| … | … |
| N-1 | `quantum_base * 2^(N-1)` |


This **exponential scaling** ensures processes that consume more CPU get progressively longer slices but are demoted in priority .

## Process Queue Level Management

MLFQ tracks each process’s current queue in the `process_queue_level` map. When a new process is added:

```python
def addProcess(self, process):
    if process.pid not in self.process_queue_level:
        self.process_queue_level[process.pid] = 0
    level = self.process_queue_level[process.pid]
    if process not in self.queues[level]:
        self.queues[level].append(process)
```

- New processes start at **level 0**.
- They remain at their level until they exhaust their quantum.

## Time Slice Demotion

When a running process uses up its allocated quantum, MLFQ **demotes** it to the next lower-priority queue:

```python
def getNextProcess(self, running, time):
    if running and running.state == "RUNNING":
        level = self.process_queue_level[running.pid]
        quantum = self.quantum_base * (2 ** level)
        if self.current_quantum >= quantum:
            new_level = min(level + 1, self.num_queues - 1)
            self.process_queue_level[running.pid] = new_level
            # Move to lower queue
            self.queues[level].remove(running)
            running.state = "READY"
            self.queues[new_level].append(running)
            self.current_quantum = 0
        else:
            return running
    # ... select next ready process ...
```

- **Demotion** occurs at `current_quantum >= quantum`.
- The process is re-queued at lower priority with its quantum reset .

## IO Blocking and Quantum Reset

Interactive or IO-bound processes that block for IO are **not penalized**. When a process enters the WAITING state, MLFQ resets its quantum:

```python
def onProcessWaiting(self):
    self.current_quantum = 0
```

- Called by the simulator when IO starts.
- Ensures the process returns at its current level with a fresh quantum .

## Selecting the Next Process

After handling demotion, MLFQ scans queues from highest to lowest:

```python
for level in range(self.num_queues):
    ready = [p for p in self.queues[level] if p.state == "READY"]
    if ready:
        proc = ready[0]
        self.queues[level].remove(proc)
        self.current_quantum = 0
        return proc
return None
```

- Always selects the **oldest READY** process at the highest nonempty level.
- Resets `current_quantum` to start counting for the new process .

## MLFQ Variants in `main.py`

Two common configurations are instantiated in **main.py** for comparison:

| Variant | num_queues | quantum_base | Label |
| --- | --- | --- | --- |
| MLFQ (3q, base = 2) | 3 | 2 | `"MLFQ (3q, base=2)"` |
| MLFQ (4q, base = 2) | 4 | 2 | `"MLFQ (4q, base=2)"` |


```python
schedulers = [
    # ...
    ("MLFQ (3q, base=2)", MLFQ(num_queues=3, quantum_base=2)),
    ("MLFQ (4q, base=2)", MLFQ(num_queues=4, quantum_base=2)),
]
```

These variants illustrate how adding more queues affects **response** and **turnaround** times .

## Comparison Highlights

- More queues → **finer-grained** priority demotion.
- Larger `quantum_base` → longer initial bursts favored.
- IO-bound tasks benefit from **quantum resets**, avoiding demotion.

```card
{
    "title": "Key Takeaway",
    "content": "MLFQ dynamically balances responsiveness and throughput by adjusting quanta and queue levels based on CPU usage."
}
```

By tuning **num_queues** and **quantum_base**, you can explore trade-offs between **fairness**, **latency**, and **CPU utilization** in your simulations.