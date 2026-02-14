# Using and Interpreting Scheduling Metrics

This section explains how the simulator computes key scheduling metrics and how to interpret them. Each metric is derived from process fields such as `arrival_time`, `startTime`, `finishTime`, and `burst_time`. All values are in **simulation ticks** and averaged across the entire workload. The calculations take place in the `countMetrics()` function in **main.py** .

## Metrics Overview

The simulator reports four primary metrics:

- **Average Response Time**
- **Average Turnaround Time**
- **Average Waiting Time**
- **Throughput** 🎯

Below we define each metric, show its formula, and highlight the relevant code.

---

### Response Time

Average response time measures how long a process waits before its first execution.

- **Definition**: Time from process arrival to when it first gets the CPU.
- **Formula**:

```plaintext
  response_time = startTime - arrival_time
```

- **Interpretation**: Lower response time indicates quicker initial service.

```python
# In countMetrics()
response_time = p.startTime - p.arrival_time
```

---

### Turnaround Time

Average turnaround time shows the total time a process spends in the system.

- **Definition**: Time from arrival to completion.
- **Formula**:

```plaintext
  turnaround_time = finishTime - arrival_time
```

- **Interpretation**: Captures both waiting and execution durations.

```python
# In countMetrics()
turnaround_time = p.finishTime - p.arrival_time
```

---

### Waiting Time

Average waiting time is the total time a process spends ready but not running.

- **Definition**: Turnaround time minus actual CPU execution time.
- **Formula**:

```plaintext
  waiting_time = turnaround_time - burst_time
```

- **Interpretation**: Reflects pure queuing delays.

```python
# In countMetrics()
waiting_time = turnaround_time - p.burst_time
```

---

### Throughput 🎯

Throughput indicates the scheduler’s capacity in terms of completed processes per tick.

- **Definition**: Number of processes completed divided by total simulation time.
- **Formula**:

```plaintext
  throughput = num_processes / completion_time
```

- **Interpretation**: Higher throughput means more processes finished per tick.

```python
# In countMetrics()
metrics["throughput"] = num_processes / completion_time
```

---

## Summary Table

| Metric | Formula | Units |
| --- | --- | --- |
| **Response Time** | `startTime - arrival_time` | ticks |
| **Turnaround Time** | `finishTime - arrival_time` | ticks |
| **Waiting Time** | `turnaround_time - burst_time` | ticks |
| **Throughput** 🎯 | `num_processes / completion_time` | processes/tick |


---

```card
{
    "title": "Field Sources",
    "content": "Process fields `arrival_time`, `startTime`, `finishTime`, and `burst_time` are defined in Process.py."
}
```

Reference for process fields in **Process** class .

---

## Implementation in `countMetrics()`

The `countMetrics()` function aggregates per-process metrics and computes averages:

```python
def countMetrics(workload, completion_time):
    total_response = 0
    total_waiting  = 0
    total_turnaround = 0

    for p in workload:
        response_time   = p.startTime - p.arrival_time
        turnaround_time = p.finishTime - p.arrival_time
        waiting_time    = turnaround_time - p.burst_time

        total_response    += response_time
        total_waiting     += waiting_time
        total_turnaround  += turnaround_time

    num_processes = len(workload)
    metrics = {
        "avg_response":   total_response   / num_processes,
        "avg_waiting":    total_waiting    / num_processes,
        "avg_turnaround": total_turnaround / num_processes,
        "throughput":     num_processes    / completion_time,
        "completion_time": completion_time
    }
    return metrics, num_processes
```

- **Averages** are calculated by dividing cumulative totals by `num_processes`.
- **Completion time** is the total ticks taken for all processes to finish, as returned by `CPUSimulator()` .