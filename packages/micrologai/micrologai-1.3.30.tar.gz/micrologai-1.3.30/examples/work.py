#
# Microlog. Copyright (c) 2023 laffra, dcharbon. All rights reserved.
#

import microlog
import random
import time

def do_work_1():
    return [ [random.random() for col in range(1000)] for row in range(1000) ]

def do_work_2():
    return [ [random.random() for col in range(1000)] for row in range(1000) ]

def do_work_3():
    return [ [random.random() for col in range(1000)] for row in range(1000) ]

def do_sleep():
    time.sleep(0.2)


with microlog.enabled("work-work-work"):
    start = time.time()
    while time.time() - start < 3:
        print(f"Sleep {time.time() - start})")
        do_sleep()
    while time.time() - start < 6:
        print(f"Work 1: {time.time() - start})")
        do_work_1()
        print(f"Work 2: {time.time() - start})")
        do_work_2()
        print(f"Work 3: {time.time() - start})")
        do_work_3()