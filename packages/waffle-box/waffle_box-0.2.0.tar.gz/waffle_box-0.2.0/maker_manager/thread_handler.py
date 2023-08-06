import threading
from enum import Enum
from collections import deque

from waffle_box_exception.waffle_box_exception import ExceptionCode, WaffleBoxException


class ThreadStatus(Enum):
    CREATE = 1
    RUN = 2
    TERMINATE = 3
    EXCEPTION = 4


class ConvertThreadHandler:
    """onnx_convert의 ThreadHandler.

    전달받은 함수를 Thread로 실행시키고 관리하는 클래스.
    start와 join으로 Thread의 실행과 종료.

    status는 CREATE -> RUN(start시에) -> TERMINATE로 가며,
    에러 발생시 EXCEPTION으로 변합니다.

    전달받은 함수에 데코레이터를 적용하여,
    동작 후에 status가 TERMINATE로 변합니다.

    join은 status가 TERMIATE나, EXCEPTION에서만 가능하며,
    EXCEPTION시에는 raise로 에러를 발생 시킵니다.

    Attributes:
        __status (ThreadStatus): Thread의 상태를 관리.
        __exception (Exception): Thread드 작동 중 발생한 에러.
        convert_thread (Thread): 함수에 데코레이터를 적용한 Thread.
    """

    def __init__(self, func):
        self.__status = ThreadStatus.CREATE
        self.__exception = None
        self.func = func

        self.thread_queue = deque()
        self.finsh_queue = deque()

    def add_work(self, *args):
        #convert_threads에 작업을 추가
        convert_thread = threading.Thread(
            target=self.status_decorator(self.func),
            args = args,
        )
        convert_thread.setDaemon(True)
        self.thread_queue.append(convert_thread)

    def status_decorator(self, func):
        # func 작동 후, status를 TERMINATE로 설정하는 데코레이터.
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)

                if self.thread_queue:
                    thread = self.thread_queue.popleft()
                    self.finsh_queue.append(thread)
                    thread.start()
                else:
                    self.__status = ThreadStatus.TERMINATE

            except Exception as e:
                self.__exception = e
                self.__status = ThreadStatus.EXCEPTION
                raise WaffleBoxException(
                    "Thread convert exception",
                    ExceptionCode.MODEL_CONVERT_EXCEPTION
                )
            finally:
                args[0].exit_container_handler()
        return wrapper

    def start(self):
        # Thread의 상태를 RUN으로 하고 동작, 에러시 EXCEPTION으로 상태변경.
        if not self.thread_queue:
            raise WaffleBoxException(
                "Thread queue is empty!",
                ExceptionCode.MODEL_CONVERT_EXCEPTION
            )

        self.__status = ThreadStatus.RUN

        thread = self.thread_queue.popleft()
        thread.start()

    def join(self):
        # Thread가 종료 된 상태라면 동작, EXCEPTION이라면 Raise.
        while not (self.status == ThreadStatus.TERMINATE \
                or self.status == ThreadStatus.EXCEPTION):
            pass

        for thread in self.finsh_queue:
            thread.join()

            if self.status == ThreadStatus.EXCEPTION:
                raise self.__exception

    @property
    def status(self):
        return self.__status
