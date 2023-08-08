# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 09:16:44 2023

@author: Administrator
"""


import logging

# logging.basicConfig(level=logging.DEBUG, 
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     filename='app.log',  # 指定日志文件路径
#                     filemode='a')       # 指定写入模式，'w'表示每次运行时覆盖文件，'a'表示追加到文件末尾

# logging.debug("这是一个调试信息")
# logging.info("这是一条普通信息")
# logging.warning("这是一个警告")
# logging.error("这是一个错误")
# logging.critical("这是一个严重错误")





def logger():
    # 创建日志记录器
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)
    
    # 创建日志输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # 检查日志记录器是否已经有处理器
    if not logger.hasHandlers():
        # 创建控制台日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
    
        # 创建文件日志处理器
        file_handler = logging.FileHandler('./logs/app.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
    
        # 将处理器添加到日志记录器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger



from elias import usual as u 

log_file = '../logs/app.log'
logger = u.logger(log_file) 
   
# 打印不同级别的日志信息
logger.debug("这是一个调试信息")
logger.info("这是一条普通信息")
logger.warning("这是一个警告")
logger.error("这是一个错误")
logger.critical("这是一个严重错误")




