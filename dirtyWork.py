from multiprocessing import Pool
import os, time, random

def long_time_task(name="holle"):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


from multiprocessing import Process
if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    process_list=[]
    p = Pool(4)
    for i in range(5):
        p=Process(target=long_time_task)
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
    print('Waiting for all subprocesses done...')
    print('All subprocesses done.')