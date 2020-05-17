#encoding:utf-8

import threading


def task_thread(task_data):
    print task_data
    return task_data



all_task=[]

all_task.append(1)
all_task.append(1)
all_task.append(1)
all_task.append(1)


task_index=0
all_res=[]
threadLock = threading.Lock()



def one_thread():
    global task_index
    global all_task
    taskCount=0
    threadName=threading.current_thread().name

    while True:
        threadLock.acquire()
        if (task_index + 1 >len(all_task)):
            print( threadName+" TaskDone:"+str(taskCount))
            threadLock.release()
            return

        task_data=all_task[task_index]
        task_index+=1
        threadLock.release()

        try:
             task_res=task_thread(task_data)
        except:
            print('errorTask:'+task_data)
            continue

        threadLock.acquire()
        if (task_res is not None):
            all_res.append(task_res)
            taskCount+=1
            print("task succ:"+str(task_index))
        threadLock.release()
       

thread_list = []
for i in range(16):
    t = threading.Thread(target=one_thread)
    thread_list.append(t)

for t in thread_list:
    t.setDaemon(True)
    t.start()

print('wait sub thead')
for t in thread_list:
    t.join()

print('sub thread done:'+str(len(all_res)))
print(all_res)
print('done')


