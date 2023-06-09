import tkinter as tk
import random


def draw_path(canvas, algorithm, movements, max_movement):
    canvas.delete("all")
    canvas.create_text(10, 10, anchor=tk.NW, text=algorithm, font=("Arial", 14))
    for i in range(len(movements) - 1):
        x1 = i * (canvas.winfo_width() / (len(movements) - 1))
        y1 = (1 - movements[i] / max_movement) * canvas.winfo_height()
        x2 = (i + 1) * (canvas.winfo_width() / (len(movements) - 1))
        y2 = (1 - movements[i + 1] / max_movement) * canvas.winfo_height()
        canvas.create_line(x1, y1, x2, y2, fill="blue")


def run_simulation():
    head_position = int(head_position_entry.get())
    requests = generate_requests()
    results = {
        "FCFS": fcfs(requests, head_position),
        "SSTF": sstf(requests, head_position),
        "SCAN": scan(requests, head_position),
        "C-SCAN": c_scan(requests, head_position),
    }
    result_text.delete(1.0, tk.END)
    for algorithm, movements in results.items():
        result_text.insert(tk.END, f"{algorithm}磁头移动道数: {calculate_sum(movements)}\n")

        # 画图
        movements = [head_position] + movements
        draw_path(canvas, algorithm, movements, max(requests))
        root.update()
        # 暂停两秒后再显示
        root.after(2000)


def generate_requests():
    requests = []
    for _ in range(188):
        m = random.randint(0, 499)
        requests.append(m)
        requests.append(m + 1)
        m = random.randint(0, 499)
        requests.append(m)
        requests.append(m + 1)
        m = random.randint(500, 999)
        requests.append(m)
        requests.append(m + 1)
        m = random.randint(1000, 1499)
        requests.append(m)
        requests.append(m + 1)
    return requests[:1500]


def fcfs(requests, head_position):
    movements = []
    total_movement = 0
    for request in requests:
        total_movement += abs(head_position - request)
        head_position = request
        movements.append(head_position)
    return movements


def sstf(requests, head_position):
    movements = []
    total_movement = 0
    remaining_requests = requests.copy()
    while remaining_requests:
        closest_request = min(remaining_requests, key=lambda x: abs(x - head_position))
        total_movement += abs(head_position - closest_request)
        head_position = closest_request
        movements.append(head_position)
        remaining_requests.remove(closest_request)
    return movements


def scan(requests, head_position):
    movements = []
    total_movement = 0
    sorted_requests = sorted(requests)
    current_requests = [r for r in sorted_requests if r >= head_position]
    remaining_requests = [r for r in sorted_requests if r < head_position]
    total_movement += abs(head_position - current_requests[0])
    head_position = current_requests[0]
    movements.append(head_position)
    for i in range(len(current_requests) - 1):
        total_movement += abs(current_requests[i] - current_requests[i + 1])
        movements.append(current_requests[i + 1])
    if remaining_requests:
        total_movement += abs(current_requests[-1] - remaining_requests[-1])
        movements.append(remaining_requests[-1])
        for i in range(len(remaining_requests) - 1):
            total_movement += abs(remaining_requests[i] - remaining_requests[i + 1])
            movements.append(remaining_requests[i + 1])
    return movements


def c_scan(requests, head_position):
    movements = []
    total_movement = 0
    sorted_requests = sorted(requests)
    current_requests = [r for r in sorted_requests if r >= head_position]
    remaining_requests = [r for r in sorted_requests if r < head_position]
    total_movement += abs(head_position - current_requests[0])
    head_position = current_requests[0]
    movements.append(head_position)
    for i in range(len(current_requests) - 1):
        total_movement += abs(current_requests[i] - current_requests[i + 1])
        movements.append(current_requests[i + 1])
    if remaining_requests:
        total_movement += abs(current_requests[-1] - remaining_requests[0])
        movements.append(remaining_requests[0])
        for i in range(len(remaining_requests) - 1):
            total_movement += abs(remaining_requests[i] - remaining_requests[i + 1])
            movements.append(remaining_requests[i + 1])
    return movements

#计算路径长度
def calculate_sum(lst):
    n = len(lst)
    total_sum = 0

    for i in range(1, n):
        total_sum += abs(lst[i] - lst[i - 1])

    return total_sum


root = tk.Tk()
root.title("磁盘调度模拟程序")

head_position_label = tk.Label(root, text="输入磁头初始位置:")
head_position_label.grid(row=0, column=0, padx=10, pady=10)
head_position_entry = tk.Entry(root)
head_position_entry.grid(row=0, column=1, padx=10, pady=10)

run_button = tk.Button(root, text="开始模拟", command=run_simulation)
run_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

result_text = tk.Text(root, height=10, width=30)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

canvas = tk.Canvas(root, width=400, height=200, bg="white")
canvas.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
