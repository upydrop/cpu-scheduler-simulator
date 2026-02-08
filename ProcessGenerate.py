from random import randint, choices
from Process import Process


def generateCPU_bound(count=None):
    if count is None:
        count = randint(50, 100)

    processes = []
    for i in range(count):
        arrival_time = randint(0, 50)
        burst_time = randint(80, 120)
        priority = randint(1, 5)
        processes.append(Process(i + 1, priority, burst_time, arrival_time, None, None))

    return processes


def generateIO_bound(count=None):
    if count is None:
        count = randint(50, 100)

    processes = []
    for i in range(count):
        arrival_time = randint(0, 50)
        burst_time = randint(5, 20)
        priority = randint(1, 5)

        io_count = choices([0, 1, 2], weights=[0.2, 0.5, 0.3], k=1)[0]

        if io_count > 0:
            IO_start_time = [randint(2, burst_time - 2) for _ in range(io_count)]
            IO_start_time.sort()
            IO_waiting_time = [randint(1, 10) for _ in range(io_count)]
        else:
            IO_start_time = None
            IO_waiting_time = None

        processes.append(Process(i + 1, priority, burst_time, arrival_time, IO_start_time, IO_waiting_time))

    return processes


def generateMixed_bound(count=None):
    if count is None:
        count = randint(50, 100)

    processes = []
    for i in range(count):
        arrival_time = randint(0, 50)
        priority = randint(1, 5)

        process_type = choices(['cpu', 'io'], weights=[0.5, 0.5], k=1)[0]

        if process_type == 'cpu':
            burst_time = randint(80, 120)
            IO_start_time = None
            IO_waiting_time = None
        else:
            burst_time = randint(5, 20)
            io_count = choices([0, 1, 2], weights=[0.3, 0.5, 0.2], k=1)[0]

            if io_count > 0:
                IO_start_time = [randint(2, burst_time - 2) for _ in range(io_count)]
                IO_start_time.sort()
                IO_waiting_time = [randint(3, 5) for _ in range(io_count)]
            else:
                IO_start_time = None
                IO_waiting_time = None

        processes.append(Process(i + 1, priority, burst_time, arrival_time, IO_start_time, IO_waiting_time))

    return processes