# CPU Scheduler Simulator

Python simulation of classic CPU scheduling algorithms. Built to make OS scheduling tangible — run algorithms side-by-side, compare metrics, and see exactly why algorithm choice matters.

---

## Algorithms Implemented

- FCFS — First Come, First Served
- SRTF — Shortest Remaining Time First (preemptive)
- Round Robin — configurable time quantum
- Priority Scheduling
- MLFQ - Multi-Level Feedback Queue

---

## Project Structure

| File | Responsibility |
|---|---|
| `Process.py` | Process model — holds PID, arrival, burst, priority, and other |
| `ProcessGenerate.py` | Generates random or custom process sets for simulation |
| `Schedulers.py` | All scheduling algorithm implementations |
| `main.py` | Entry point — runs schedulers, prints results, writes to `results/` |
| `docs/` | Algorithm notes and design documentation |
| `results/` | Saved simulation outputs for comparison |

---

## Getting Started

**Requirements:** Python 3.8+

```bash
git clone https://github.com/upydrop/cpu-scheduler-simulator.git
cd cpu-scheduler-simulator
python main.py
```

Output example:

== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
WORKLOAD: CPU-bound(50 processes)
== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==

+------------------+----------+----------+-------------+------------+
| Scheduler        | Avg Wait | Avg Resp | Avg T-around| Throughput |
+------------------+----------+----------+-------------+------------+
| FCFS             | 2335.86  | 2335.86  | 2435.32     | 0.0101     |
+------------------+----------+----------+-------------+------------+
| SRTF             | 2120.94  | 2120.94  | 2220.40     | 0.0101     |
+------------------+----------+----------+-------------+------------+
| Round Robin (q=2) | 4366.44  | 47.42    | 4465.90     | 0.0101     |
+------------------+----------+----------+-------------+------------+
| Round Robin (q=4) | 4361.52  | 95.38    | 4460.98     | 0.0101     |
+------------------+----------+----------+-------------+------------+
| Priority         | 2292.36  | 2268.62  | 2391.82     | 0.0101     |
+------------------+----------+----------+-------------+------------+
| MLFQ (3q, base=2) | 4362.06  | 2.14     | 4461.52     | 0.0101     |
+------------------+----------+----------+-------------+------------+
| MLFQ (4q, base=2) | 4349.32  | 2.14     | 4448.78     | 0.0101     |
+------------------+----------+----------+-------------+------------+


---

## What I Learned

- **Preemption has real cost.** Implementing preemption algorithms made the complexity concrete — saving state, handling mid-burst arrivals, recalculating remaining times every tick.
- **Design separation pays off.** Isolating the process model from generation and scheduling logic meant adding a new algorithm only touched `Schedulers.py`.
- **"Best" scheduler depends on workload.** Measuring waiting time, turnaround time, and CPU utilization across algorithms demonstrated this more clearly than any textbook example.
- **Modern OS schedulers (Linux CFS, Windows multilevel queue) are hybrids** — they combine priority tiers, preemption, and time-sharing because no single algorithm handles all workload types well. The value of simulating them individually is understanding what each one optimizes for, not finding a winner.

---

### Overall Verdict

| Goal | Best Scheduler |
|------|---------------|
| Minimize wait & turnaround (any workload) | **SRTF** |
| Minimize response time / interactive feel | **MLFQ** |
| Simplicity, predictability | **FCFS** |
| Enforce process importance tiers | **Priority** |

**SRTF wins on efficiency across all three workloads.** Its weakness — requiring knowledge of remaining burst time — is the reason real OSes don't use it directly, estimating it instead via exponential averaging. MLFQ is the closest approximation to production schedulers: it sacrifices raw efficiency to guarantee fast response for every process regardless of burst length.

---

## Notes

- Processes can be randomly generated (configurable seed for reproducibility) or defined manually
- Simulation runs on a discrete time-unit model with a single CPU
- Such schedulers as RoundRobin and MLFQ can be modified(confiigurable quantum)
- Results are saved to `results/`
