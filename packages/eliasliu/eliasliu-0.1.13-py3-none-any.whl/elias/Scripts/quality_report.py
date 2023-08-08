# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 13:02:58 2023

@author: nlsm
"""

from elias import usual as u
origin_database = 'responsibility_data'
origin_table = 'responsibility_task_commodity_rel'

goal_database = 'responsibility_data'
goal_table = 'responsibility_016_dwd_task_rel_d_f'


hosts_originl = u.all_hosts('om')
hosts_goal = u.all_hosts('om')
hosts_write = u.all_hosts('bi_report')

column_key = 'task_rel_id'
column_updated = 'updated'
column_target_1 = ''
column_target_2 = ''
column_target_3 = ''


origin_column_key = 'task_rel_id'
origin_column_target_1 = ''
origin_column_target_2 = ''
origin_column_target_3 = ''

time_rule = f'{u.today()} 09:30:00'

# 完备性sql - 总记录数
sql1 = 'count(*) as `记录数`'
# 唯一性sql
sql2 = f'count(distinct {column_key}) as `主键数`'
# 及时性sql
sql3 = f'max(`{column_updated}`) as `最近更新时间`'
# 有效性sql - 含null记录数

describe = f'''
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = '{goal_database}' AND TABLE_NAME = '{goal_table}';
'''
df_column = u.mysql_select(describe, hosts_goal)
sql_final = ''
for i in range(len(df_column)):
    column_i = df_column['COLUMN_NAME'][i]
    sql_i = f"if(`{column_i}` is null,1,0)"
    sql_ii = ''
    if i == len(df_column)-1:
        sql_ii = sql_i
    else:
        sql_ii = sql_i+'+'
    sql_final = sql_final+sql_ii
        
sql4 = f'sum(if(({sql_final})>0,1,0)) as `缺失记录数`'


# 一致性sql
if column_target_1 == '':
    sql_str_1 = '0'
else:
    sql_str_1 = f'sum({column_target_1})'


if column_target_2 == '':
    sql_str_2 = '0'
else:
    sql_str_2 = f'sum({column_target_2})'


if column_target_3 == '':
    sql_str_3 = '0'
else:
    sql_str_3 = f'sum({column_target_3})'


sql5 = f'''
{sql_str_1} as `核心指标1总和`,
{sql_str_2} as `核心指标2总和`,
{sql_str_3} as `核心指标3总和`
'''


sql_goal =f'''
select 
current_date() as today,
'{goal_table}' as table_name,
'{goal_database}' as db_name,
{sql1},
{sql2},
{sql3},
{sql4},
{sql5}
from `{goal_database}`.`{goal_table}`
'''
df_goal = u.mysql_select(sql_goal, hosts_goal)



osql_0 = f'count(distinct {origin_column_key}) as `源记录数`'
# 一致性sql
if origin_column_target_1 == '':
    osql_str_1 = '0'
else:
    osql_str_1 = f'sum({origin_column_target_1})'


if origin_column_target_2 == '':
    osql_str_2 = '0'
else:
    osql_str_2 = f'sum({origin_column_target_2})'


if origin_column_target_3 == '':
    osql_str_3 = '0'
else:
    osql_str_3 = f'sum({origin_column_target_3})'

osql_1= f'''
{osql_str_1} as `核心指标1源总和`,
{osql_str_2} as `核心指标2源总和`,
{osql_str_3} as `核心指标3源总和`
'''

sql_origin = f'''
select 
current_date() as today,
'{origin_table}' as origin_table_name,
'{origin_database}' as origin_db_name,
{osql_0},
{osql_1}
from `{origin_database}`.`{origin_table}`

'''
df_origin = u.mysql_select(sql_origin, hosts_originl)


import pandas as pd
df = pd.merge(df_goal, df_origin, how='inner', left_on='today', right_on='today')
df.info()

df['完整性'] = None # 记录完整比例
df['完备性'] = None # 1-缺失记录占比
df['唯一性'] = None # 是否有唯一主键
df['有效性'] = None # 满足特定规则的占比
df['及时性'] = None # 在特定时间前更新完成
df['一致性'] = None # 指标值计算与数据源相同的指标占比

# for i in range(len(df)):
df['完整性'][0] = df['记录数'][0]/df['源记录数'][0]
df['完备性'][0] = 1-df['缺失记录数'][0]/df['记录数'][0]
if df['主键数'][0]==df['记录数'][0]:
    df['唯一性'][0] = 1
else:
    df['唯一性'][0] = 0

df['有效性'][0] = 1

if df['最近更新时间'][0]<time_rule:
    df['及时性'][0] = 1
else:
    df['及时性'][0] = 0

if df['核心指标1总和'][0]==df['核心指标1源总和'][0]:
    a = 1
else:
    a = 0

if df['核心指标2总和'][0]==df['核心指标2源总和'][0]:
    b = 1
else:
    b = 0

if df['核心指标3总和'][0]==df['核心指标3源总和'][0]:
    c = 1
else:
    c = 0

n = a+b+c

df['一致性'] = n/3


u.mysql_write(df,'data_quality_count',host_dic=hosts_write)

