# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 18:04:26 2023

@author: nlsm
"""


#------------------------------------------------------------------------------
from elias import usual as u
from elias import wechat as w
import pandas as pd

sql = '''
select * FROM `default`.order_wide_tab o
WHERE o.trade_time is null and snd_date >='2023-07-01'
and del_type =1 and trade_no2 not like '%调整列%'
'''


fname = f"宽表trade_time缺失值查询_{u.Datetime_now(t=1)}"
# hosts_read= u.all_hosts(name = 'bi_report')
# key = w.robots('nl_file_output')

u.sql_send_file(sql
                ,hosts = u.all_hosts(name = 'default')
                ,server_type = 'clickhouse'
                ,fname = fname
                ,key = w.robots('BI监控')
                ,host_record = u.all_hosts(name = 'bi_report')
                )


#------------------------------------------------------------------------------
from elias import usual as u
from elias import wechat as w
import pandas as pd

sql = '''
with t1 as (
SELECT o.snd_date ,o.venture_id ,o.venture_name,d.dept_id_2  ,d.dept_name_2 as syb,d.dept_id_3 ,d.dept_name_3 as department_name,o.profit_after_inner_cost 
FROM order_wide_tab o
left join bi_report.dwd_om_org_department_d_f d on d.id = o.venture_id 
WHERE o.snd_date >='2023-07-10' 
and o.profit_after_inner_cost <0
)
SELECT t1.snd_date ,t1.venture_id ,t1.venture_name,t1.dept_id_2  ,t1.syb,t1.dept_id_3 ,t1.department_name,sum(t1.profit_after_inner_cost ) as profit_after_inner_cost
from t1 group by t1.snd_date ,t1.venture_id ,t1.venture_name,t1.dept_id_2  ,t1.syb as syb,t1.dept_id_3 ,t1.department_name
'''


fname = f"经营体亏损_{u.Datetime_now(t=1)}"
# hosts_read= u.all_hosts(name = 'bi_report')
# key = w.robots('nl_file_output')

u.sql_send_file(sql
                ,hosts = u.all_hosts(name = 'default')
                ,server_type = 'clickhouse'
                ,fname = fname
                ,key = w.robots('zenghuan')
                ,host_record = u.all_hosts(name = 'bi_report')
                )


#------------------------------------------------------------------------------
from elias import usual as u
from elias import wechat as w
import pandas as pd

sql = '''
SELECT  *
FROM bi_report.ch_004_assets_036_dws_order_account_receivable_amount_d_f oar
WHERE oar.platform  = '天猫超市'
'''


fname = f"天猫超市平台应收明细_{u.Datetime_now(t=1)}"
# hosts_read= u.all_hosts(name = 'bi_report')
# key = w.robots('nl_file_output')

u.sql_send_file(sql
                ,hosts = u.all_hosts(name = 'default')
                ,server_type = 'clickhouse'
                ,fname = fname
                ,key = w.robots('zenghuan')
                ,host_record = u.all_hosts(name = 'bi_report')
                )