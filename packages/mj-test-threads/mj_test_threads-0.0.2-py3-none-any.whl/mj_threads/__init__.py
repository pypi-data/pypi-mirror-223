#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2023/8/3 17:51
@SoftWare: PyCharm
@Project: mj_tools
@File: __init__.py
"""
__all__ = ["Threads"]

import ctypes
import inspect
import os
import warnings
from multiprocessing import Queue
from threading import Thread, Lock


class Threads:
    def __init__(self, func, max_workers=None):
        self.__max_workers = self.__check_max_workers(max_workers)
        self.__queue = Queue()
        self.__lock = Lock()
        self.__func = func
        self.__workers = dict()
        self.__threads = dict()
        self.__while = True
        self.__thread_number = 1
        self.__start()

    def __start(self):
        self.__thread1 = Thread(target=self.__queue_init)
        self.__thread1.start()
        self.__thread2 = Thread(target=self.__check_status)
        self.__thread2.start()

    def send(self, thread_name=None, **kwargs):
        if not self.__check_while():
            return
        self.__lock.acquire()
        if thread_name and thread_name not in self.__workers.keys():
            new_name = thread_name
        else:
            new_name = f"thread_{self.__thread_number}"
            self.__thread_number += 1
            self.__warning(f"线程名 {thread_name} 未定义或已存在，已自动定义为 {new_name}")
        self.__lock.release()
        self.__workers.update({new_name: self.__Worker(self.__func, **kwargs)})
        self.__queue.put(new_name)

    def join(self):
        if not self.__check_while():
            return
        all_list = [1, 2, 3]
        while True:
            status_list = [worker.status for thread_name, worker in self.__workers.items()]
            difference = list(set(status_list) - set(all_list))
            if not difference:
                break

    def stop(self):
        if not self.__check_while():
            return
        self.__stop()

    def wait_stop(self):
        if not self.__check_while():
            return
        self.__queue.empty()

    def close(self):
        if not self.__check_while():
            return
        try:
            self.__while = False
            self.__queue.empty()
            self.__queue.close()
            self.__stop()
        except Exception as err:
            raise self.__ManagerError(f"管理器停止失败，失败原因：{err}")

    def done(self):
        all_list = [1, 2, 3]
        status_list = [worker.status for thread_name, worker in self.__workers.items()]
        difference = list(set(status_list) - set(all_list))
        return False if difference else True

    def get_qsize(self):
        if not self.__check_while():
            return
        return self.__queue.qsize()

    def get_status(self, thread_name):
        worker = self.__workers.get(thread_name)
        if worker is None:
            self.__warning(f"任务-{thread_name}- 未定义")
            return
        status_dict = {"0": "运行中", "1": "完成", "2": "失败", "3": "停止"}
        return status_dict.get(str(worker.status))

    def get_result(self, thread_name):
        worker = self.__workers.get(thread_name)
        if worker is None:
            self.__warning(f"任务-{thread_name}- 未定义")
            return
        return worker.result

    def get_all_result(self):
        result_dict = dict()
        for thread_name, worker in self.__workers.items():
            result_dict.update({thread_name: worker.result})
        return result_dict

    def get_failed(self):
        if self.done():
            return [thread_name for thread_name, worker in self.__workers.items() if worker.status == 2]
        return False

    def rerun_failed(self):
        if not self.__check_while():
            return
        for thread_name, worker in self.__workers.items():
            if worker.status == 2:
                self.__queue.put(thread_name)

    def set_max_workers(self, workers_number=None):
        if not self.__check_while():
            return
        self.__max_workers = self.__check_max_workers(workers_number)

    def __check_while(self):
        if not self.__while:
            self.__warning(
                "管理器已执行 .close() 停止，当前仅提供 .done()/.get_status()/.get_result()/.get_failed() 功能"
            )
        return True

    def __stop(self):
        try:
            for thread_name, thread in self.__threads.items():
                if thread.ident:
                    self.__async_raise(thread.ident, SystemExit)
                    self.__workers.get(thread_name).status = 3
                    self.__warning(
                        f"任务-{thread_name}- 已停止，状态变更：运行中 ==> 停止"
                    )
            self.__async_raise(self.__thread1.ident, SystemExit)
            self.__async_raise(self.__thread2.ident, SystemExit)
        except Exception as err:
            raise self.__ManagerError(f"停止失败，失败原因：{err}")

    @staticmethod
    def __warning(text):
        warnings.warn(text, UserWarning, stacklevel=99)

    @staticmethod
    def __check_max_workers(max_workers):
        if max_workers == 0:
            return 0
        if isinstance(max_workers, int) and max_workers > 0:
            return min(30, max_workers)
        else:
            return min(30, (os.cpu_count() or 1) + 4)

    def __queue_init(self):
        while self.__while:
            try:
                if len(self.__threads) < self.__max_workers:
                    event = self.__queue.get(block=True)
                    self.__consumer(event)
            except(Exception,):
                continue

    def __check_status(self):
        while True:
            try:
                for thread_name in self.__threads.keys():
                    worker = self.__workers.get(thread_name)
                    if worker.status in (1, 2):
                        self.__threads.pop(thread_name)
            except(Exception,):
                continue

    def __consumer(self, thread_name):
        worker = self.__workers.get(thread_name)
        worker.status = 0
        thread = Thread(target=worker.start)
        self.__threads.update({thread_name: thread})
        thread.start()

    @staticmethod
    def __async_raise(tid, exc_type):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exc_type):
            exc_type = type(exc_type)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        if res == 0:
            return ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            return SystemError("PyThreadState_SetAsyncExc failed")

    class __Worker:
        def __init__(self, mjtools_func, **kwargs):
            self.mjtools_func = mjtools_func
            self.kwargs = kwargs
            self.status = None
            self.result = None

        def start(self):
            try:
                self.result = self.mjtools_func(**self.kwargs)
                self.status = 1
            except Exception as err:
                self.result = err
                self.status = 2

    class __JoinError(Exception):
        pass

    class __ManagerError(Exception):
        pass
