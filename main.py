from ProcessGenerate import generateCPU_bound, generateIO_bound, generateMixed_bound
from Schedulers import FCFS, SRTF, RoundRobin, Priority, MLFQ
import copy


def CPUSimulator(scheduler, workload):
    time = 0
    active_processes = [p for p in workload]

    running = None

    while len(active_processes) > 0:
        for p in active_processes:
            if p.arrival_time == time:
                p.state = "READY"
                scheduler.addProcess(p)
            if p.state == "WAITING":
                if p.IO_waiting_time and len(p.IO_waiting_time) > 0:
                    if p.IO_waiting_time[0] == 0:
                        p.IO_waiting_time = p.IO_waiting_time[1:]
                        p.IO_start_time = p.IO_start_time[1:]
                        p.state = "READY"
                        scheduler.addProcess(p)
                    else:
                        p.IO_waiting_time[0] -= 1

        running = scheduler.getNextProcess(running, time)

        if running is not None:
            running.state = "RUNNING"
            if running.startTime == -1:
                running.startTime = time

            running.remaining_time -= 1

            if running.IO_start_time is not None and len(running.IO_start_time) > 0:
                cpu_burst_consumed = running.burst_time - running.remaining_time
                if cpu_burst_consumed == running.IO_start_time[0]:
                    running.state = "WAITING"
                    if hasattr(scheduler, 'onProcessWaiting'):
                        scheduler.onProcessWaiting()
                    running = None

            if running is not None and running.remaining_time == 0:
                running.state = "TERMINATED"
                running.finishTime = time + 1
                active_processes.remove(running)
                scheduler.removeProcess(running)
                running = None

        scheduler.onTickEnd(running, time)

        time += 1

    return time


def countMetrics(workload, completion_time):
    total_response = 0
    total_waiting = 0
    total_turnaround = 0

    for p in workload:
        response_time = p.startTime - p.arrival_time
        turnaround_time = p.finishTime - p.arrival_time
        waiting_time = turnaround_time - p.burst_time

        total_response += response_time
        total_waiting += waiting_time
        total_turnaround += turnaround_time

    num_processes = len(workload)
    metrics = {
        "avg_response": total_response / num_processes,
        "avg_waiting": total_waiting / num_processes,
        "avg_turnaround": total_turnaround / num_processes,
        "throughput": num_processes / completion_time,
        "completion_time": completion_time
    }

    return metrics, num_processes


def printSchedulerResults(scheduler_name, workload_name, metrics, num_processes, file_handle=None):
    def write(text):
        if file_handle:
            file_handle.write(text + '\n')
        else:
            print(text)

    if scheduler_name == 'FCFS':
        write("== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==")
        write(f"WORKLOAD: {workload_name}({num_processes} processes)")
        write("== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==\n")
        write("+------------------+----------+----------+-------------+------------+")
        write("| Scheduler        | Avg Wait | Avg Resp | Avg T-around| Throughput |")
        write("+------------------+----------+----------+-------------+------------+")

    line = f"| {scheduler_name:<16} | {metrics['avg_waiting']:<8.2f} | {metrics['avg_response']:<8.2f} | {metrics['avg_turnaround']:<11.2f} | {metrics['throughput']:<10.4f} |"
    write(line)
    write("+------------------+----------+----------+-------------+------------+")


def main():
    schedulers = [
        ("FCFS", FCFS()),
        ("SRTF", SRTF()),
        ("Round Robin (q=2)", RoundRobin(quantum=2)),
        ("Round Robin (q=4)", RoundRobin(quantum=4)),
        ("Priority", Priority()),
        ("MLFQ (3q, base=2)", MLFQ(num_queues=3, quantum_base=2)),
        ("MLFQ (4q, base=2)", MLFQ(num_queues=4, quantum_base=2))
    ]

    workloads = {"CPU-bound": generateCPU_bound(50), "IO-bound": generateIO_bound(50), "Mixed-bound": generateMixed_bound(50)}

    for workload_name, workload in workloads.items():

        for scheduler_name, scheduler in schedulers:
            workload_copy = copy.deepcopy(workload)
            completion_time = CPUSimulator(scheduler, workload_copy)
            metrics, num_processes = countMetrics(workload_copy, completion_time)
            with open(f'results/{workload_name}.txt', 'a') as f:
                printSchedulerResults(scheduler_name, workload_name, metrics, num_processes, f)


if __name__ == "__main__":
    main()