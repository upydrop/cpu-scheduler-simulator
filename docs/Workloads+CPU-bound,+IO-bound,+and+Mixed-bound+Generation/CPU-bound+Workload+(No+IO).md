# Workloads: CPU-Bound, IO-Bound, and Mixed-Bound Generation

In this section, we describe how the simulator generates **synthetic workloads** to evaluate scheduling algorithms. Each workload type targets different process behaviors: pure CPU processing, frequent I/O, or a mixture of both. Below, we focus on the **CPU-bound** workload, which models processes that never perform I/O and thus stress long CPU bursts.

## CPU-Bound Workload (No IO) 🖥️

The **CPU-bound workload** creates processes with substantial CPU bursts and **no I/O operations**. This workload highlights how schedulers handle long-running tasks without blocking for I/O.

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
            Process(
                pid=i+1,
                priority=priority,
                burst_time=burst_time,
                arrival_time=arrival_time,
                IO_start_time=None,
                IO_waiting_time=None
            )
        )
    return processes
```

The above function is defined in **ProcessGenerate.py** .

### Key Parameters

Each process in the CPU-bound workload is initialized with the following randomized fields:

| Parameter | Description |
| --- | --- |
| **arrival_time** | Integer between **0** and **300** ticks |
| **burst_time** | Integer between **80** and **120** ticks |
| **priority** | Integer between **1** (highest) and **5** |
| **IO_start_time** | Always **None** (no I/O phases) |
| **IO_waiting_time** | Always **None** (no I/O wait durations) |


### How It Stresses the Scheduler

- **Long CPU bursts** (80–120 ticks) keep processes in the **RUNNING** state until completion, revealing how schedulers manage CPU-intensive jobs.
- Absence of I/O means no process yields the CPU voluntarily, forcing schedulers to rely solely on their **preemptive logic** (e.g., time quanta or priorities).
- Varying **arrival times** (0–300) creates overlaps and idle intervals, testing responsiveness under different load patterns.
- Random **priorities** introduce preemptive decisions for algorithms like **Priority** and **MLFQ**.

### Integration in Simulation

In **main.py**, the CPU-bound workload is one of three generated before running simulations:

```python
from ProcessGenerate import generateCPU_bound, generateIO_bound, generateMixed_bound

def main():
    schedulers = [
        ("FCFS", FCFS()),
        ("SRTF", SRTF()),
        ("Round Robin (q=2)", RoundRobin(quantum=2)),
        ("Priority", Priority()),
        ("MLFQ (3q, base=2)", MLFQ(num_queues=3, quantum_base=2))
    ]
    workloads = {
        "CPU-bound":   generateCPU_bound(50),
        "IO-bound":    generateIO_bound(50),
        "Mixed-bound": generateMixed_bound(50)
    }
    …
```

Here, **50** processes are created for each workload type and passed to the discrete-time simulator .

---

**Note:** By isolating CPU work (no I/O), this workload reveals pure scheduling overhead and context-switch behavior under heavy computational demand.