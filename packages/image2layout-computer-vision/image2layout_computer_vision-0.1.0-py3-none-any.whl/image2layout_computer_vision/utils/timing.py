# %%
import time
import json
import numpy as np
import pandas as pd

from typing import Union, Any, Dict, List, Tuple

# %%
class Timer:
    def __init__(self):
        
        self.time_start = None
        self.time_stop = None
        self.time_elapsed = None
        self.time_total_last_start = None
        self.time_total = 0.
        
        self.started = False
        self.stopped = False
        self.elapsed = False
        self.running = False
    
    def __repr__(self) -> str:
        if self.elapsed:
            return f'Timer({self.time_total:.2f}s)'
        if self.started:
            return f'Timer(started)'
        return f'Timer()'
    
    def __call__(self):
        return self.tick()
    
    def tick(self):
        if not self.started:
            return self.start()
        else:
            return self.stop()
        
    def start(self):
        self.started = True
        self.running = True
        self.time_start = time.perf_counter()
        # self.elapse()
        return self.running
    
    def stop(self):
        self.stopped = True
        self.running = False
        self.time_stop = time.perf_counter()
        self.elapse()
        return self.running
    
    def elapse(self):
        if self.started and self.stopped:
            _time_elapsed = self.time_stop - self.time_start
            
            # duplicate time_start
            if self.time_total_last_start == self.time_start:
                # self.time_total += _time_elapsed - self.time_elapsed
                pass
            else:
                self.time_total += _time_elapsed
                
            self.time_total_last_start = self.time_start
            self.time_elapsed = _time_elapsed
            self.elapsed = True
        return self.running


# %%
class Chrono(list):
    def __init__(self, name='main', parent=None):
        self.name = str(name)
        self.parent = parent
        self.timer = Timer()
        super().__init__()
    
    def _reprs(self) -> list:
        _timer_str = ''
        if self.timer.elapsed:
            _timer_str = f'[{self.timer.time_elapsed:.3f}s]'
        elif self.timer.started:
            _timer_str = f'[started]'
        return [
            f'Chrono[{self.name}]{_timer_str}'
        ] + [
            '  ' + f'{v}'
            for child in self
            for v in child._reprs()
        ]
    
    def __getitem__(self, index: Union[str, int, tuple], error_on_notfound=False):
        
        if isinstance(index, int):
            return super().__getitem__(index)
        
        if isinstance(index, str):
            for child in self:
                if child.name == index:
                    return child
        
        if isinstance(index, (tuple, list)):
            if len(index) == 0:
                return self
            child = self[index[0]]
            if len(index) == 1:
                return child
            return child[index[1:]]
        
        if error_on_notfound:
            raise ValueError(f'child not found, index[{index}] is invalid')
        
        return None
    
    @property
    def running(self):
        return self.timer.running
    
    @property
    def timers(self):
        _timers = {
            tuple(): self.timer,
        }
        for child in self:
            _timers.update({
                tuple([child.name, *k]): v
                for k, v in child.timers.items()
            })
        return _timers
    
    def __repr__(self) -> str:
        return '\n'.join(self._reprs())
    
    def watch(self, *names):
        '''add the child is needed, tick the timer, tick the neighbors, tick the parent's timer if needed
        '''
        _chrono = self.add(*names)
        _chrono.timer.tick()
        _parent = _chrono.parent
        if not _chrono.timer.running:
            # stops all children
            for child in _chrono:
                if child.running:
                    child.stop()
        if isinstance(_parent, Chrono):
            if _chrono.timer.running:
                # stops neighbors' timer
                for child in _parent:
                    if child is _chrono:
                        continue
                    if child.running:
                        child.stop()
                if not _parent.timer.running:
                    # _parent.timer.start()
                    _parent.start()
    
    def start(self):
        self.timer.start()
    
    def stop(self):
        self.timer.stop()
        for child in self:
            child.stop()
    
    def tick(self, *names):
        if len(names) == 0:
            self.timer.tick()
        else:
            child = self.add(*names)
            child.timer.tick()
    
    def add(self, *names):
        '''add a new (leaf) child or just get the existing child and return that child'''
        # skips on duplicate found, guarantees that there are no duplicates
        if len(names) == 0:
            return self
        if len(names) == 1:
            _name = names[0]
            assert isinstance(_name, str), f'invalid name type[{type(_name)}], must be string'
            assert len(_name) > 0, f'invalid name, must not be empty'
            child = self[_name]
            if child is None:
                child = Chrono(names[0], parent=self)
                self.append(child)
            return child
        else:
            child = self.add(names[0])
            return child.add(*names[1:])

# %%