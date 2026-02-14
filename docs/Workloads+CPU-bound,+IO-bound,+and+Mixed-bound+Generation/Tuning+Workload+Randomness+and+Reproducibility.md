# Workloads: CPU-bound, IO-bound, and Mixed-bound Generation

This section describes how synthetic workloads are generated for the CPU scheduling simulator. Three generator functions—`generateCPU_bound`, `generateIO_bound`, and `generateMixed_bound`—produce lists of `Process` instances with different characteristics. Tuning these functions lets you explore scheduler behavior under diverse arrival patterns, burst lengths, IO frequencies, and wait durations.

## generateCPU_bound(count)

Generates **CPU-bound** processes that perform long CPU bursts without IO.

```python
from random import randint
from Process import Process

def generateCPU_bound(count=25):
    processes = []
    for i in range(count):
        arrival_time = randint(0, 300)
        burst_time   = randint(80, 120)
        priority     = randint(1, 5)
        processes.append(
            Process(i+1, priority, burst_time, arrival_time, None, None)
        )
    return processes
```

| Parameter | Distribution | Range | Description |
| --- | --- | --- | --- |
| `arrival_time` | `randint(a, b)` | 0 – 300 | Uniform arrival over simulated time |
| `burst_time` | `randint(a, b)` | 80 – 120 | Long CPU bursts |
| `priority` | `randint(a, b)` | 1 – 5 | Scheduling priority (lower is higher) |
| `IO_start_time` | – | – | No IO phases (`None`) |
| `IO_waiting_time` | – | – | No IO waiting (`None`) |


---

## generateIO_bound(count)

Creates **IO-bound** processes with short CPU bursts interleaved by IO waits.

```python
from random import randint, choices, sample
from Process import Process

def generateIO_bound(count=25):
    processes = []
    for i in range(count):
        arrival_time = randint(0, 300)
        burst_time   = randint(5, 20)
        priority     = randint(1, 5)
        io_count     = choices([0, 1, 2], weights=[0.2, 0.5, 0.3], k=1)[0]

        if io_count > 0 and burst_time > 4:
            IO_start_time   = sorted(sample(range(2, burst_time-1), min(io_count, burst_time-3)))
            IO_waiting_time = [randint(1, 10) for _ in IO_start_time]
        else:
            IO_start_time, IO_waiting_time = None, None

        processes.append(
            Process(i+1, priority, burst_time, arrival_time,
                    IO_start_time, IO_waiting_time)
        )
    return processes
```

| Parameter | Distribution | Description |
| --- | --- | --- |
| `burst_time` | `randint(5, 20)` | Short CPU bursts |
| `io_count` | `choices([0,1,2], weights=[0.2,0.5,0.3])` | Number of IO phases |
| `IO_start_time` | `sample(range(2, burst_time-1), k)` | Points in CPU burst to switch to IO |
| `IO_waiting_time` | `[randint(1,10) for _ in IO_start_time]` | Duration of each IO wait |


---

## generateMixed_bound(count)

Produces a **mixed** workload: half CPU-bound and half IO-bound processes by default.

```python
from random import randint, choices, sample
from Process import Process

def generateMixed_bound(count=25):
    processes = []
    for i in range(count):
        arrival_time = randint(0, 300)
        priority     = randint(1, 5)
        process_type = choices(['cpu', 'io'], weights=[0.5, 0.5], k=1)[0]

        if process_type == 'cpu':
            burst_time, IO_start_time, IO_waiting_time = randint(80, 120), None, None
        else:
            burst_time = randint(5, 20)
            io_count   = choices([0,1,2], weights=[0.3,0.5,0.2], k=1)[0]
            if io_count > 0 and burst_time > 4:
                IO_start_time   = sorted(sample(range(2, burst_time-1),
                                                min(io_count, burst_time-3)))
                IO_waiting_time = [randint(3, 5) for _ in IO_start_time]
            else:
                IO_start_time, IO_waiting_time = None, None

        processes.append(
            Process(i+1, priority, burst_time, arrival_time,
                    IO_start_time, IO_waiting_time)
        )
    return processes
```

---

# Tuning Workload Randomness and Reproducibility 🎛️

You can tailor the workload generators to stress different scheduler behaviors. All tuning happens in **ProcessGenerate.py**  .

- **Arrival patterns**
- Modify `randint(0, 300)` to narrow or widen arrival window.
- **CPU burst lengths**
- Adjust `randint(80, 120)` (CPU-bound) or `randint(5, 20)` (IO phases).
- **Process priorities**
- Change `randint(1, 5)` range to simulate more priority levels.
- **IO frequency**
- Tweak `choices([...], weights=[…])` weights or support more phases.
- **IO wait durations**
- Update `randint(1, 10)` (IO-bound) or `randint(3, 5)` (mixed) ranges.

**Randomness is **** seeded** by default. To achieve deterministic runs, add:

```python
# At top of ProcessGenerate.py or before calling generators
import random
random.seed(42)   # any fixed integer
```

```card
{
    "title": "Reproducibility Tip",
    "content": "Seed the random module before workload generation for repeatable simulations."
}
```

---

By adjusting these parameters, you can generate diverse workloads—ranging from bursty IO patterns to long-running CPU tasks—and observe how each scheduling algorithm responds under controlled or highly variable conditions.