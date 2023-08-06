from concurrent.futures import ThreadPoolExecutor
import concurrent.futures as futures

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ThreadPool(ThreadPoolExecutor,metaclass=Singleton):
    '''单例'''
    def __init__(self,max_workers = 8) -> None:
        self.future_list=[]
        super().__init__(max_workers=max_workers)
        
    def set_max_workers(self, max_workers):
        self._max_workers = max_workers
        self._adjust_thread_count()

    def add_task(self,task,*args, **kwargs):
        self.future_list.append(self.submit(task,*args, **kwargs))

    def wait_finish(self):
        for future in futures.as_completed(self.future_list):
            pass
        self.future_list=[]
    def restart(self, wait: bool = ..., *, cancel_futures: bool = ...) -> None:
        super().shutdown(wait, cancel_futures=cancel_futures)
        self.future_list=[]
        super().__init__(max_workers=self._max_workers)
        return 

class ThreadPools(ThreadPoolExecutor):
    '''多例'''
    def __init__(self,max_workers = 8) -> None:
        super().__init__(max_workers=max_workers)