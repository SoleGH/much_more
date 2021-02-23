from concurrent.futures import ThreadPoolExecutor
from time import sleep

"""
当任务执行很慢时，任务会全部积压在worker_queue中，等待已有线程释放
这种这种IO耗时比较多的任务，可以适当调大线程池数量
"""
def executor(thread_name):
    print("thread {} start...".format(thread_name))
    sleep(10)
    print("thread {} end...".format(thread_name))


def pool_monitor(pool):
    while 1:
        sleep(1)
        print("work_queue len:{},current thread num:{}".format(pool._work_queue.qsize(), len(pool._threads)))


pool = ThreadPoolExecutor(max_workers=2)
print("###work_queue len:{},current thread num:{}".format(pool._work_queue.qsize(), len(pool._threads)))
for i in range(10):
    pool.submit(executor, i)
pool_monitor(pool)




