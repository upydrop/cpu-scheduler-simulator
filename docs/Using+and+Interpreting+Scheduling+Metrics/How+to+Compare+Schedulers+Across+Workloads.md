# Using and Interpreting Scheduling Metrics – How to Compare Schedulers Across Workloads

This section guides you through reading and interpreting the output tables generated under `results/`. You will learn how to use **average waiting time**, **average response time**, **average turnaround time**, and **throughput** to compare different schedulers across **CPU-bound**, **IO-bound**, and **Mixed-bound** workloads.

## Scheduling Metrics Overview

Each report table contains the following metrics:

- **Avg Wait**

Time a process spends in the ready queue before its first execution.

- **Avg Resp**

Time from arrival to first execution (response latency).

- **Avg T-around**

Total time from arrival to completion (service time + waiting).

- **Throughput**

Number of processes completed per unit time.

These metrics help you balance between **fairness**, **latency**, and **overall system utilization**.

## Interpreting CPU-bound Workload Results

CPU-bound workloads consist of long-running, compute-intensive processes. Examine `results/CPU-bound.txt` for a baseline comparison:

```bash
cat results/CPU-bound.txt
```

```txt
+------------------+----------+----------+-------------+------------+
| Scheduler        | Avg Wait | Avg Resp | Avg T-around| Throughput |
+------------------+----------+----------+-------------+------------+
| FCFS             | 2335.86  | 2335.86  | 2435.32     | 0.0101     |
| SRTF             | 2120.94  | 2120.94  | 2220.40     | 0.0101     |
| Round Robin (q=2)| 4366.44  |   47.42  | 4465.90     | 0.0101     |
| Round Robin (q=4)| 4361.52  |   95.38  | 4460.98     | 0.0101     |
| Priority         | 2292.36  | 2268.62  | 2391.82     | 0.0101     |
| MLFQ (3q, base=2)| 4362.06  |    2.14  | 4461.52     | 0.0101     |
| MLFQ (4q, base=2)| 4349.32  |    2.14  | 4448.78     | 0.0101     |
+------------------+----------+----------+-------------+------------+
```

Key takeaways for **CPU-bound**:

- **SRTF** reduces both waiting and turnaround compared to FCFS.
- **Round Robin** (especially with small quantum) slashes response time but doubles wait and turnaround.
- **MLFQ** mimics aggressive Round Robin at the top level, yielding minimal response but very high waiting.

## Interpreting IO-bound Workload Results

IO-bound workloads contain short bursts of CPU work interleaved with I/O. Inspect `results/IO-bound.txt`:

```bash
cat results/IO-bound.txt
```

```txt
+------------------+----------+----------+-------------+------------+
| Scheduler        | Avg Wait | Avg Resp | Avg T-around| Throughput |
+------------------+----------+----------+-------------+------------+
| FCFS             |  275.98  |  110.20  |   289.22    | 0.0739     |
| SRTF             |  157.16  |  141.68  |   170.40    | 0.0725     |
| Round Robin (q=2)|  327.10  |   36.06  |   340.34    | 0.0736     |
| Round Robin (q=4)|  315.84  |   61.58  |   329.08    | 0.0731     |
| Priority         |  233.96  |  182.64  |   247.20    | 0.0730     |
| MLFQ (3q, base=2)|  341.34  |    2.00  |   354.58    | 0.0739     |
| MLFQ (4q, base=2)|  344.48  |    2.00  |   357.72    | 0.0739     |
+------------------+----------+----------+-------------+------------+
```

For **IO-bound**:

- **SRTF** minimizes waiting and turnaround by prioritizing short remaining bursts.
- **Round Robin** achieves the **best response time**, ideal for interactive tasks.
- **MLFQ** forces most processes into rapid preemption, giving near-zero response at the cost of increased waiting.

## Interpreting Mixed-bound Workload Results

Mixed workloads combine CPU-heavy and IO-heavy processes. See `results/Mixed-bound.txt`:

```bash
cat results/Mixed-bound.txt
```

```txt
+------------------+----------+----------+-------------+------------+
| Scheduler        | Avg Wait | Avg Resp | Avg T-around| Throughput |
+------------------+----------+----------+-------------+------------+
| FCFS             | 1528.04  | 1012.54  | 1580.30     | 0.0191     |
| SRTF             |  575.16  |  563.76  |  627.42     | 0.0191     |
| Round Robin (q=2)| 1209.48  |   42.66  | 1261.74     | 0.0191     |
| Round Robin (q=4)| 1220.34  |   81.02  | 1272.60     | 0.0191     |
| Priority         | 1284.88  | 1152.62  | 1337.14     | 0.0191     |
| MLFQ (3q, base=2)| 1229.82  |    2.56  | 1282.08     | 0.0191     |
| MLFQ (4q, base=2)| 1243.26  |    2.56  | 1295.52     | 0.0191     |
+------------------+----------+----------+-------------+------------+
```

In **Mixed-bound** scenarios:

- **SRTF** offers balanced improvements in waiting and turnaround.
- **Round Robin** still shines in response time but at moderate waiting cost.
- **Priority** biases toward high-priority tasks, possibly starving low-priority CPU-heavy processes.

## Comparing Schedulers Across Workloads

When choosing a scheduler, align your goals with workload characteristics:

- **Throughput**: CPU-bound and Mixed-bound see similar throughput across schedulers (fixed by total work).
- **Latency-sensitive tasks**:
- Use **Round Robin** or **MLFQ** to minimize response time for interactive or IO-heavy workloads.
- **Batch processing**:
- **SRTF** or **Priority** scheduling lowers average waiting/turnaround in CPU-heavy scenarios.
- **Fairness vs. starvation risk**:
- **FCFS** guarantees service order but yields high latency.
- **SRTF** and **Priority** may starve long or low-priority processes.

🎯 **Key Patterns to Look For**

- Round Robin typically **improves response time** but **increases waiting/turnaround** in CPU-heavy workloads.
- SRTF shows **consistent gains** in waiting and turnaround across all workloads.
- MLFQ targets interactivity: **ultra-low response** for short tasks, but **very high waiting** for long-running processes.
- Throughput remains roughly constant, so focus on response vs. turnaround trade-offs.

## Using Example Reports as Baseline

Use the provided reports under `results/` as starting points:

- Review `results/CPU-bound.txt`, `results/IO-bound.txt`, and `results/Mixed-bound.txt`.
- Compare your own runs by matching the **table structure** and **column order**.
- Adjust **time quantum**, **number of queues**, or **priority schemes**, then rerun to observe metric shifts.

By following these patterns and using the existing reports as a baseline, you can make informed decisions when tuning scheduler parameters for your specific workload.