
from collections import defaultdict
from time import time_ns
import pandas as pd


class Timer:
    def __init__(self, active=True):
        self.data = defaultdict(lambda: defaultdict(float))
        self.current = []
        self.total_running_time = 0
        self.active = active
     
    def evaluate(self, filename = None):
        
        output = defaultdict(list)
        total = self.total_running_time*1e-9
        for task, data in self.data.items():
            data = dict(data)
            N = data["executions"]
            T = data["total time"]*1e-9
            T_sq = data["total time squared"]*1e-18
            output["Task"].append(task)
            output["Exections"].append(N)
            output["Total time"].append(T)
            output["Ratio time"].append(T/total)
            output["Average time"].append(T/N)
            output["Standard div time"].append((T_sq/N + T**2/N**2)**0.5)

        output = pd.DataFrame(output)
        if filename is not None: output.to_csv(filename.replace(".csv", "") + ("_unfinished_tasks" if len(self.current) else ""))
        return output, total
    def __repr__(self):
        return str(self.evaluate()[0])

    def activate(self): self.active = True
    def deactivate(self): self.active = False

    def start(self, task, stop_previous=True):
        if self.active:
            if stop_previous and len(self.current) > 0: self.stop()
            task = task if len(self.current) == 0 else f"{self.current[-1][0]}/{task}"
            self.current.append((task, time_ns()))
    
    def stop(self):
        if self.active:
            assert len(self.current) > 0, RuntimeError('Timer was stopped with no running tasks')
            stop = time_ns()
            task, start = self.current.pop(-1)
            if len(self.current) == 0:
                self.total_running_time += stop-start
            self.data[task]["total time"] += stop-start
            self.data[task]["total time squared"] += (stop-start)**2
            self.data[task]["executions"] += 1
    
    def __call__(self, label=None, stop_previous=True):
        if self.active:
            if label is None: self.stop()
            else: self.start(label, stop_previous)
    
    def __add__(self, other):
        assert isinstance(other, Timer), ValueError("Can only add timers together")
        for task, task_data in other.data.items():
            for key, value in task_data.items():
                self.data[task][key] += value
        self.total_running_time += other.total_running_time
        return self
