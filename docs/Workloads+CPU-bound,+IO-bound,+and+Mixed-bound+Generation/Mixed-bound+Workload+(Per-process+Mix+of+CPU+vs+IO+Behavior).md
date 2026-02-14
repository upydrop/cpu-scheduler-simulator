# Workloads: Mixed-bound Generation (Per-Process CPU vs IO Mix)

A **mixed-bound workload** simulates processes that exhibit either CPU-intensive or IO-intensive behavior on a per-process basis. This approach creates a **hybrid workload**, combining traits from both pure CPU-bound and IO-bound workloads to stress test scheduling algorithms under varied scenarios.

## Purpose

- Evaluate scheduler performance with heterogeneous process behaviors
- Reflect real-world scenarios where some tasks are CPU-heavy and others IO-heavy
- Observe metric differences (waiting, response, turnaround, throughput) across schedulers

## generateMixed_bound() Function 🛠️

This key function in **ProcessGenerate.py** creates a list of `Process` instances with a 50/50 split of CPU-like and IO-like characteristics.

```python
def generateMixed_bound(count=25):
    processes = []
    for i in range(count):
        arrival_time = randint(0, 300)
        priority = randint(1, 5)
        process_type = choices(['cpu', 'io'], weights=[0.5, 0.5], k=1)[0]

        if process_type == 'cpu':
            burst_time = randint(80, 120)
            IO_start_time = None
            IO_waiting_time = None
        else:
            burst_time = randint(5, 20)
            io_count = choices([0, 1, 2], weights=[0.3, 0.5, 0.2], k=1)[0]
            if io_count > 0 and burst_time > 4:
                IO_start_time = sorted(
                    sample(range(2, burst_time - 1),
                           min(io_count, burst_time - 3))
                )
                IO_waiting_time = [randint(3, 5) for _ in range(len(IO_start_time))]
            else:
                IO_start_time = None
                IO_waiting_time = None

        processes.append(Process(
            i + 1,
            priority,
            burst_time,
            arrival_time,
            IO_start_time,
            IO_waiting_time
        ))
    return processes
```

### Key Responsibilities

- **Arrival Time**: Randomized in `[0, 300]`
- **Priority**: Randomized in `[1, 5]`
- **Process Type Selection**
- 50% chance **CPU-like** (`'cpu'`)
- 50% chance **IO-like** (`'io'`)

## Behavior Branches

### 1. CPU-like Branch

- `burst_time` drawn from `randint(80, 120)`
- **No IO events** (`IO_start_time = None`, `IO_waiting_time = None`)

### 2. IO-like Branch

- `burst_time` drawn from `randint(5, 20)`
- **IO event count** (`io_count`) chosen from `[0, 1, 2]` with weights **[0.3, 0.5, 0.2]**
- If `io_count > 0` and `burst_time > 4`
- **IO start times**: sample unique points in the CPU burst
- **IO waiting times**: list of `randint(3, 5)` delays per IO event
- Else, no IO events

## Comparison: IO-bound vs Mixed-bound Generators

| Aspect | IO-bound Generator | Mixed-bound Generator |
| --- | --- | --- |
| **CPU burst range** | 5–20 | 5–20 (for IO-like processes) |
| **CPU-only processes** | None (all processes may have IO) | 50% processes have 80–120 burst with no IO |
| **IO event count weights** | [0.2, 0.5, 0.3] for [0,1,2] events | [0.3, 0.5, 0.2] for [0,1,2] events |
| **IO waiting time range** | 1–10 | 3–5 |
| **Per-process randomness** | Uniform IO characteristics | Mixed CPU/IO characteristics per process |


## Integration into Simulator 🔄

- **Imported by** `main.py` to populate the `workloads` dictionary alongside `generateCPU_bound` and `generateIO_bound`
- **Passed to** `CPUSimulator`, which applies scheduling algorithms and collects performance metrics
- Works in concert with **Process**, **Schedulers**, and **CPUSimulator** components

```python
workloads = {
    "CPU-bound": generateCPU_bound(50),
    "IO-bound": generateIO_bound(50),
    "Mixed-bound": generateMixed_bound(50)
}
```

## Process Generation Flowchart

```mermaid
flowchart TD
  Start[Start Mixed-bound Generation]
  Start --> Init[Initialize empty list]
  Init --> Loop{i < count?}
  Loop -- Yes --> RandValues[Randomize arrival & priority]
  RandValues --> TypeDecide[Choose 'cpu' or 'io' (50/50)]
  TypeDecide -- cpu --> CPUBurst[burst_time ∈ [80,120]]
  CPUBurst --> NoIO[IO_start_time=None, IO_waiting_time=None]
  TypeDecide -- io --> IOBurst[burst_time ∈ [5,20]]
  IOBurst --> IOCount[Select io_count w/ weights [0.3,0.5,0.2]]
  IOCount -- >0 --> GenIOStart[Sample IO_start_time positions]
  GenIOStart --> GenIOWait[IO_waiting_time ∈ [3,5]]
  IOCount -- 0 --> NoIO2[No IO events]
  NoIO2 --> CreateP
  NoIO --> CreateP
  GenIOWait --> CreateP[Instantiate Process object]
  CreateP --> Append[Add to processes list]
  Append --> Loop
  Loop -- No --> End[Return process list]
```

---

```card
{
    "title": "Key Takeaway",
    "content": "Mixed-bound workloads reveal scheduler behavior under heterogeneous CPU/IO process mixes."
}
```