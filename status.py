import time


def formattime(t, decimals=4):
    proper = ""
    if t >= 86400:
        proper += str(int(t / 86400)) + "d "
    if t >= 3600:
        proper += str(int((t % 86400) / 3600)) + "h "
    if t >= 60:
        proper += str(int((t % 3600) / 60)) + "m "
    proper += str(round(t % 60, decimals)) + "s"
    return proper


class statusbar:
    def printstatus(self):
        percent = self.curr / self.length
        print(f"\r{self.msg} | Completed {str(self.curr).rjust(self.currrjust)}/{self.length} |" + "█" * int(20 * percent) + "░" * (20 - int(20 * percent)) + f"| {percent:>4.0%} | Remaining: {formattime((self.length - self.curr) * self.rate, decimals=1)} | {self.notify}\t", end="", flush=True)
        if self.curr == self.length:
            print()  # Prints new line upon completion

    def incrementstatus(self):
        self.curr += 1
        self.rate = (time.time() - self.starttime) / self.curr

    def incrementandprint(self):
        self.incrementstatus()
        self.printstatus()

    def warn(self, warning):
        self.notify = warning
        self.printstatus()
        self.notify = ""

    def __init__(self, length, msg):
        self.rate = 0.25  # Estimate
        self.curr = 0
        self.length = length
        self.currrjust = len(str(self.length))
        self.msg = msg
        self.starttime = time.time()
        self.notify = ""
        self.printstatus()


class timer:
    def __init__(self, names):
        self.names = names
        self.inc = [0] * len(names)
        self.times = [0] * len(names)
        self.lasttime = -1
        self.recording = -1

    def swapto(self, index):
        if self.lasttime == -1:
            self.lasttime = time.time()
            self.recording = index
        else:
            prev = self.lasttime
            self.lasttime = time.time()
            self.inc[self.recording] += 1
            self.times[self.recording] += self.lasttime - prev
            self.recording = index

    def start(self, startindex=1):
        self.swapto(startindex)

    def stop(self):
        self.swapto(self.recording)
        self.inc[self.recording] -= 1

    def results(self):
        for i in range(len(self.names)):
            print(f"{self.names[i]}: {formattime(self.times[i])} ({formattime(self.times[i]/max(self.inc[i], 1))}/each)")
        print(f"Total time: {formattime(sum(self.times))}\n")
