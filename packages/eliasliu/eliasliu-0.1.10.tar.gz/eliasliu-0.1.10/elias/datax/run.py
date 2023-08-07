# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 19:18:54 2023

@author: Administrator
"""

from elias import usual as u
from elias import config
import os
# u.run_cmd("ipconfig")
run_path = os.path.join(config.datax_path,r"bin\datax.py")

u.run_cmd_os('chcp 65001')

# 建表
u.run_cmd_os(r"python D:\anaconda3\Lib\elias\datax\main.py -s financial_data -st rpa_ali_journal_data -t mc -tt test_all_journal7")

# 同步
u.run_cmd_os(rf"python {run_path} C:\Users\Administrator\Downloads\datax\job\【maxcompute】prj_yingshou_20230629.test_all_journal7.json")