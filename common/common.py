import pandas as pd
import os
import datetime
import common.common as common

# 定数定義
now = datetime.datetime.now()
LOG_FILE_PATH = f'./log/log_{now.strftime("%Y%m%d_%H%M%S")}.log'

## ログ機能用関数
def write_log(log_str):
    now_log = datetime.datetime.now()
    with open(LOG_FILE_PATH, mode='a+') as log_file:
        log_file.writelines(f"{str(now_log)}:{str(log_str)}\n")