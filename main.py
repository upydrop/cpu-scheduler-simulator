from ProcessGenerate import generateCPU_bound, generateIO_bound, generateMixed_bound
from Schedulers import FCFS, SRTF, RoundRobin, Priority, MLFQ
from Process import Process
import copy


def CPUSimulator(scheduler, workload):
    time = 0
    all_processes = [p for p in workload]
    active_processes = [p for p in workload]

    running = None

    while len(active_processes) > 0:
        for p in active_processes:
            if p.arrival_time == time:
                p.state = "READY"
                scheduler.addProcess(p)

        for p in active_processes:
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
            cpu_burst_consumed = running.burst_time - running.remaining_time

            if running.IO_start_time is not None and len(running.IO_start_time) > 0:
                if cpu_burst_consumed == running.IO_start_time[0]:
                    running.state = "WAITING"
                    running = None

            if running is not None and running.remaining_time == 0:
                running.state = "TERMINATED"
                running.finishTime = time
                active_processes.remove(running)
                scheduler.removeProcess(running)
                running = None

        scheduler.onTickEnd(running, time)
        time += 1

    return time


def printResults(workload, scheduler_name, completion_time):
    print(f"\n{'=' * 80}")
    print(f"Scheduler: {scheduler_name}")
    print(f"{'=' * 80}")
    print(
        f"{'PID':<6} {'Arrival':<10} {'Burst':<10} {'Start':<10} {'Finish':<10} {'Response':<10} {'Waiting':<10} {'Turnaround':<12}")
    print(f"{'-' * 80}")

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

        print(
            f"{p.pid:<6} {p.arrival_time:<10} {p.burst_time:<10} {p.startTime:<10} {p.finishTime:<10} {response_time:<10} {waiting_time:<10} {turnaround_time:<12}")

    num_processes = len(workload)
    avg_response = total_response / num_processes
    avg_waiting = total_waiting / num_processes
    avg_turnaround = total_turnaround / num_processes
    throughput = num_processes / completion_time

    print(f"{'-' * 80}")
    print(f"{'Metric':<30} {'Value':<20}")
    print(f"{'-' * 80}")
    print(f"{'Average Response Time:':<30} {avg_response:<20.2f}")
    print(f"{'Average Waiting Time:':<30} {avg_waiting:<20.2f}")
    print(f"{'Average Turnaround Time:':<30} {avg_turnaround:<20.2f}")
    print(f"{'Throughput (processes/tick):':<30} {throughput:<20.4f}")
    print(f"{'Total Completion Time:':<30} {completion_time:<20}")
    print(f"{'=' * 80}\n")


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

    workloads = {"CPU-bound":generateCPU_bound(), "IO-bound":generateIO_bound(), "Mixed-bound":generateMixed_bound()}

    for workload_name, workload in workloads.items():
        print(f"\n{'#' * 60}")
        print(f"# {workload_name}")
        print(f"{'#' * 60}")

        for scheduler_name, scheduler in schedulers:
            workload_copy = copy.deepcopy(workload)
            completion_time = CPUSimulator(scheduler, workload_copy)
            printResults(workload_copy, scheduler_name, completion_time)


if __name__ == "__main__":
    main()