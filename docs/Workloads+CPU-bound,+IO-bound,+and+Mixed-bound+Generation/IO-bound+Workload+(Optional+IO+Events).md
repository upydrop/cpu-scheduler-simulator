# Workloads: CPU-bound, IO-bound, and Mixed-bound Generation

This section focuses on how the simulator generates an **IO-bound workload** with optional I/O events. We explain the `generateIO_bound()` function in `ProcessGenerate.py`, detail how it samples CPU bursts and I/O events, cover edge cases, and show how these events drive state transitions in the discrete‐time simulation loop.

---

## IO-bound Workload (Optional I/O Events)

IO-bound workloads simulate processes that frequently perform I/O, causing them to leave the CPU and wait. This models real-world scenarios like file reads or network operations.

### `generateIO_bound()` Function

This function creates a list of `Process` instances with:

- **Short CPU bursts**
- **Random count of I/O events**
- **I/O start times** and **waiting durations**

```python
def generateIO_bound(count=25):
    processes = []
    for i in range(count):
        arrival_time = randint(0, 300)
        burst_time = randint(5, 20)
        priority = randint(1, 5)
        io_count = choices([0, 1, 2],
                           weights=[0.2, 0.5, 0.3],
                           k=1)[0]
        if io_count > 0 and burst_time > 4:
            IO_start_time = sorted(
                sample(range(2, burst_time - 1),
                       min(io_count, burst_time - 3))
            )
            IO_waiting_time = [
                randint(1, 10) for _ in range(len(IO_start_time))
            ]
        else:
            IO_start_time = None
            IO_waiting_time = None

        processes.append(Process(
            i + 1, priority, burst_time, arrival_time,
            IO_start_time, IO_waiting_time
        ))
    return processes
```

### Key Steps in Process Generation

- **Arrival Time**: Uniform random between 0 and 300 ticks.
- **Burst Time**: Uniform random between 5 and 20 ticks (short CPU bursts).
- **Priority**: Random integer 1 (highest) to 5 (lowest).
- **I/O Count** (`io_count`): Sampled from {0,1,2} with weights {0.2, 0.5, 0.3}.

| IO Events | Weight |
| --- | --- |
| ----------: | -------: |
| 0 | 0.2 |
| 1 | 0.5 |
| 2 | 0.3 |


- **I/O Start Times** (`IO_start_time`):
- Sample `io_count` distinct CPU-offsets from [2, burst_time−2].
- Limit to at most `burst_time−3` offsets.
- Sort to enforce chronological order.
- **I/O Waiting Durations** (`IO_waiting_time`):
- For each start time, sample a random wait between 1 and 10 ticks.

### Edge Conditions

- If `io_count == 0` **or** `burst_time ≤ 4`, then **no I/O**:
- `IO_start_time = None`
- `IO_waiting_time = None`

This avoids generating invalid offsets when the CPU burst is too short.

---

## I/O‐Induced State Transitions

When a running process reaches an I/O start time, it moves to a **WAITING** state. After the I/O completes, it returns to the **READY** state and re‐enters the scheduler’s queue.

```python
# Inside CPUSimulator loop
if running.IO_start_time and len(running.IO_start_time) > 0:
    cpu_burst_consumed = running.burst_time - running.remaining_time
    if cpu_burst_consumed == running.IO_start_time[0]:
        running.state = "WAITING"
        if hasattr(scheduler, 'onProcessWaiting'):
            scheduler.onProcessWaiting()
        running = None
```

While waiting:

```python
# In each tick for waiting processes
if p.state == "WAITING" and p.IO_waiting_time:
    if p.IO_waiting_time[0] == 0:
        p.IO_waiting_time.pop(0)
        p.IO_start_time.pop(0)
        p.state = "READY"
        scheduler.addProcess(p)
    else:
        p.IO_waiting_time[0] -= 1
```

### State Transition Flowchart

```mermaid
flowchart LR
    Running[PROCESS RUNNING] -->|cpu_burst_consumed == IO_start_time| Waiting[PROCESS WAITING]
    Waiting -->|IO_waiting_time == 0| Ready[PROCESS READY]
    Ready -->|scheduler.addProcess| ReadyQueue[READY QUEUE]
```

---

## Interaction with Schedulers

I/O events influence scheduling in two main ways:

- **Preemption**: On hitting I/O, the running process yields the CPU immediately.
- **Quantum Reset**: Schedulers like Round Robin and MLFQ implement `onProcessWaiting()` to reset time quanta upon I/O:

```python
class RoundRobin:
    def onProcessWaiting(self):
        self.current_quantum = 0
```

This ensures the returning process receives a fresh time slice when it re‐enters the ready queue.

---

## Impact on Simulation Behavior

- **CPU Utilization** dips during I/O waits.
- **Average Waiting Time** may increase due to context switches.
- **Throughput** can improve if I/O overlaps allow CPU to run other processes.

```card
{
    "title": "Tip",
    "content": "Adjust I/O weights to simulate heavy I/O or almost CPU-bound workloads."
}
```

By tuning `io_count` weights and `IO_waiting_time` ranges, you can model a variety of IO-bound scenarios and study their impact across different scheduling algorithms.