# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 17:17:20 2023

@author: nlsm
"""

import pandas as pd
from odps import ODPS
# pip install odps

# 配置MaxCompute连接信息
access_id = 'LTAI5tSnVoE2dHf5MakuEZ2z'
access_key = 'oZKfxkOiMfhB5xsCoEpDhIqmoibhbm'
project_name = 'prj_yingshou_20230629'
end_point = 'http://service.cn-shanghai.maxcompute.aliyun.com/api'

# 创建MaxCompute连接
odps = ODPS(access_id, access_key, project_name, endpoint=end_point)

# 执行查询并将结果转换为DataFrame
sql = 'SELECT * FROM trade_ods_order_wide_tab_d_f LIMIT 10'  # 根据您的需求修改查询语句
with odps.execute_sql(sql).open_reader() as reader:
    # 获取查询结果的字段信息
    columns = reader._schema.columns
    columns_list = []
    for i in range(len(columns)):
        column_str = str(columns[i])
        
        # 使用字符串处理方法提取目标部分
        start_index = column_str.index(" ") + 1
        end_index = column_str.index(",")
        column_name = column_str[start_index:end_index]
        print(column_name)
        columns_list.append(column_name)
    
    
    
    # 将查询结果逐行添加到DataFrame
    data = []
    for record in reader:
        data.append(record.values)

    # 创建DataFrame对象
    df = pd.DataFrame(data)

    # 设置列名
    df.columns = columns

# 打印DataFrame
print(df)







