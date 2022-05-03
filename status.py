from time import time


def format_time(t, decimals=4):
    proper = ""
    if t >= 86400:
        proper += str(int(t / 86400)) + "d "
    if t >= 3600:
        proper += str(int((t % 86400) / 3600)) + "h "
    if t >= 60:
        proper += str(int((t % 3600) / 60)) + "m "
    proper += str(round(t % 60, decimals)) + "s"
    return proper


class StatusBar:
    def __init__(self, length, msg):
        self.rate = 0.25  # Estimate
        self.curr = 0
        self.length = length
        self.curr_rjust = len(str(self.length))
        self.msg = msg
        self.start_time = time()
        self.notify = ""
        self.print_status()

    def print_status(self):
        percent = self.curr / self.length
        print(f"\r{self.msg} | Completed {str(self.curr).rjust(self.curr_rjust)}/{self.length} |"
              + "█" * int(20 * percent)
              + "░" * (20 - int(20 * percent))
              + f"| {percent:>4.0%} | Remaining: {format_time((self.length - self.curr) * self.rate, decimals=1)} | {self.notify}\t",
              end="",
              flush=True)
        if self.curr == self.length:
            print()  # Prints new line upon completion

    def increment_status(self):
        self.curr += 1
        self.rate = (time() - self.start_time) / self.curr

    def increment_and_print(self):
        self.increment_status()
        self.print_status()

    def warn(self, warning):
        self.notify = warning
        self.print_status()
        self.notify = ""


class Timer:
    def __init__(self, names):
        self.names = names
        self.inc = [0] * len(names)
        self.times = [0] * len(names)
        self.last_time = -1
        self.recording = -1

    def swap_to(self, index):
        if self.last_time == -1:
            self.last_time = time()
            self.recording = index
        else:
            prev = self.last_time
            self.last_time = time()
            self.inc[self.recording] += 1
            self.times[self.recording] += self.last_time - prev
            self.recording = index

    def start(self, start_index=1):
        self.swap_to(start_index)

    def stop(self):
        self.swap_to(self.recording)
        self.inc[self.recording] -= 1

    def results(self):
        for i in range(len(self.names)):
            print(f"{self.names[i]}: {format_time(self.times[i])} ({format_time(self.times[i] / max(self.inc[i], 1))}/each)")
        print(f"Total time: {format_time(sum(self.times))}\n")
