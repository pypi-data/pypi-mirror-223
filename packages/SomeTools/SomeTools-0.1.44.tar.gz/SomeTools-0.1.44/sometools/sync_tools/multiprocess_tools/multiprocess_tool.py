import os
import time
import multiprocessing
from sometools.sync_tools.base import Base
from multiprocessing import Pool


def work_func(i):
    # Pool不能始终使用未在导入的模块中定义的对象。所以必须将函数写入不同的文件并导入模块或者写到一个文件里
    time.sleep(0.5)
    print(os.getpid())
    print(i)


class MultiProcessMixIn(Base):

    def __init__(self, *args, **kwargs):
        super(MultiProcessMixIn, self).__init__(*args, **kwargs)

    @staticmethod
    def multi_run(pool_count=multiprocessing.cpu_count(), process_count=1) -> None:
        pool = Pool(processes=pool_count)
        for i in range(process_count):
            pool.apply_async(work_func, (i,))
        pool.close()
        pool.join()


if __name__ == "__main__":
    aaa = MultiProcessMixIn()
    aaa.multi_run(30, 50)
