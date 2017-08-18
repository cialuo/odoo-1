# -*-coding:utf-8-*-
import threading;

mutex_lock = threading.RLock();  # 互斥锁的声明


class myThread(threading.Thread):  # 线程处理函数
    def __init__(self, name):
        threading.Thread.__init__(self);  # 线程类必须的初始化
        self.thread_name = name;  # 将传递过来的name构造到类中的name

    def run(self):
        # 声明在类中使用全局变量
        #global mutex_lock;


        mutex_lock.acquire();  # 临界区开始，互斥的开始

        print '111111'

            #mutex_lock.release();  # 临界区结束，互斥的结束
        mutex_lock.release();  # python在线程死亡的时候，不会清理已存在在线程函数的互斥锁，必须程序猿自己主动清理





thread1 = myThread("线程1");

# 开启线程
thread1.start();
