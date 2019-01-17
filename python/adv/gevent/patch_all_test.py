import threading
import time
from gevent import monkey
monkey.patch_all()


def demo(*args):
    print("hello{}".format(args[0]))
    # time.sleep(1)


class Xiaorui(threading.Thread):
    def run(self):
        demo(self._args)
        print('finished working{}'.format(self._args[0]))


if __name__ == '__main__':
    worker = Xiaorui(args=(0,))
    worker1 = Xiaorui(args=(1,))
    worker2 = Xiaorui(args=(2,))
    worker.start()
    worker1.start()
    worker2.start()
    print('finished')