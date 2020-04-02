from multiprocessing import Process, Value, Manager, Pool
import subprocess
import os
import time
from functools import reduce

configs = []  # 配置生产
config_lock = True


# 配置暴力生产
def configs_gen():
    for index in range(4)
    configs.append({"-env": f"{index}"})


# 运行任务
def run_task(configs):
    run_config = ["python3", "iron_man你.py"]  # 基本配置
    for item in [[key, value] for key, value in configs.items()]:
        run_config.extend(item)
    p = subprocess.Popen(run_config,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # print(p.poll())     # 增加容错机制
    # print("p stdout", p.stdout.readlines())

 
if __name__ == "__main__":
    configs_gen()
    with Pool() as pool:
        pool.map(run_task, configs)
