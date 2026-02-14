# CPU Scheduler Simulator

Python simulation of classic CPU scheduling algorithms. Built to make OS scheduling tangible — run algorithms side-by-side, compare metrics, and see exactly why algorithm choice matters.

---

## Algorithms Implemented

- FCFS — First Come, First Served
- SJF — Shortest Job First (non-preemptive)
- SRTF — Shortest Remaining Time First (preemptive)
- Round Robin — configurable time quantum
- Priority Scheduling

---

## Project Structure

| File | Responsibility |
|---|---|
| `Process.py` | Process model — holds PID, arrival, burst, priority, and computed stats (wait time, TAT) |
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

<!-- Paste a real sample of your console output here -->

---

## What I Learned

- **Preemption has real cost.** Implementing SRTF vs SJF made the complexity concrete — saving state, handling mid-burst arrivals, recalculating remaining times every tick.
- **Design separation pays off.** Isolating the process model from generation and scheduling logic meant adding a new algorithm only touched `Schedulers.py`.
- **"Best" scheduler depends on workload.** Measuring waiting time, turnaround time, and CPU utilization across algorithms demonstrated this more clearly than any textbook example.

---

## Notes

- Processes can be randomly generated (configurable seed for reproducibility) or defined manually
- Simulation runs on a discrete time-unit model with a single CPU
- Results are saved to `results/`
