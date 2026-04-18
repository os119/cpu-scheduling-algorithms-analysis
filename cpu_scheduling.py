import matplotlib.pyplot as plt
from tabulate import tabulate


def fcfs(processes):
    time = 0
    schedule = []
    waiting = []
    turnaround = []

    for p in sorted(processes, key=lambda x: x["arrival"]):
        if time < p["arrival"]:
            time = p["arrival"]
        start = time
        end = start + p["burst"]
        waiting.append(start - p["arrival"])
        turnaround.append(end - p["arrival"])
        schedule.append({"name": p["name"], "start": start, "end": end})
        time = end

    avg_wait = sum(waiting) / len(waiting)
    avg_turn = sum(turnaround) / len(turnaround)
    return schedule, avg_wait, avg_turn


def sjf(processes):
    time = 0
    schedule = []
    waiting = []
    turnaround = []
    ready = []
    plist = sorted(processes, key=lambda x: x["arrival"])
    i = 0

    while i < len(plist) or ready:
        while i < len(plist) and plist[i]["arrival"] <= time:
            ready.append(plist[i])
            i += 1
        if ready:
            ready.sort(key=lambda x: x["burst"])  
            p = ready.pop(0)
            start = time
            end = start + p["burst"]
            waiting.append(start - p["arrival"])
            turnaround.append(end - p["arrival"])
            schedule.append({"name": p["name"], "start": start, "end": end})
            time = end
        else:
            time = plist[i]["arrival"]

    avg_wait = sum(waiting) / len(waiting)
    avg_turn = sum(turnaround) / len(turnaround)
    return schedule, avg_wait, avg_turn


def round_robin(processes, quantum=3):
    time = 0
    ready = []
    timeline = []
    waiting = {p["name"]: 0 for p in processes}
    remain = {p["name"]: p["burst"] for p in processes}
    arrive = {p["name"]: p["arrival"] for p in processes}
    plist = sorted(processes, key=lambda x: x["arrival"])
    i = 0

    while i < len(plist) or ready:
        while i < len(plist) and plist[i]["arrival"] <= time:
            ready.append(plist[i]["name"])
            i += 1
        if not ready:
            time = plist[i]["arrival"]
            ready.append(plist[i]["name"])
            i += 1

        current = ready.pop(0)
        run = min(quantum, remain[current])
        timeline.append({"name": current, "start": time, "end": time + run})
        time += run
        remain[current] -= run

        while i < len(plist) and plist[i]["arrival"] <= time:
            ready.append(plist[i]["name"])
            i += 1
        if remain[current] > 0:
            ready.append(current)
        else:
            waiting[current] = time - arrive[current] - processes[[p["name"] for p in processes].index(current)]["burst"]

    avg_wait = sum(waiting.values()) / len(waiting)
    turn = [processes[j]["burst"] + waiting[processes[j]["name"]] for j in range(len(processes))]
    avg_turn = sum(turn) / len(turn)
    return timeline, avg_wait, avg_turn


def draw_chart(schedule, title):
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']  
    for idx, s in enumerate(schedule):
        plt.barh(s["name"], s["end"] - s["start"], left=s["start"], color=colors[idx % len(colors)])
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Processes")
    plt.show()


def print_timeline(schedule, name):
    print(f"\n{name} Order:")
    print(" | ".join([f"{s['name']}({s['start']}→{s['end']})" for s in schedule]))


if __name__ == "__main__":
    
    processes = [
        {"name": "P1", "arrival": 0, "burst": 8},
        {"name": "P2", "arrival": 1, "burst": 4},
        {"name": "P3", "arrival": 2, "burst": 2}
    ]

    fcfs_s, fcfs_w, fcfs_t = fcfs(processes)
    sjf_s, sjf_w, sjf_t = sjf(processes)
    rr_s, rr_w, rr_t = round_robin(processes, quantum=3)

    table = [
        ["FCFS", fcfs_w, fcfs_t],
        ["SJF", sjf_w, sjf_t],
        ["RR", rr_w, rr_t]
    ]

    print(tabulate(table, headers=["Algorithm", "Avg Waiting", "Avg Turnaround"], tablefmt="grid"))

    print_timeline(fcfs_s, "FCFS")
    print_timeline(sjf_s, "SJF")
    print_timeline(rr_s, "Round Robin")

    draw_chart(fcfs_s, "FCFS Scheduling")
    draw_chart(sjf_s, "SJF Scheduling")
    draw_chart(rr_s, "Round Robin Scheduling")
