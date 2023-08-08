# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 11:45:06 2023

@author: Administrator
"""


from elias import usual as u

def mysql_comment_get(table_name,hosts):
    
    dbtype = hosts['dbtype']
    
    if dbtype == 'mysql':
        
        des_sql = f'''
        SELECT TABLE_COMMENT  as comment
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = '{hosts['db']}' 
        AND TABLE_NAME = '{table_name}'
        '''
        
        df = u.mysql_select(des_sql, hosts)
        table_comment = df['comment'][0]
    
    elif dbtype == 'clickhouse':
        
        des_sql = f'''
            SELECT name, engine, comment
            FROM system.tables
            WHERE database = '{hosts['db']}'
            AND name = '{table_name}';
        '''
        
        df = u.clickhouse_select(des_sql, hosts)
        table_comment = df['comment'][0]
    
    elif dbtype == 'maxcompute':
        from odps import ODPS
        access_id = hosts['access_id']
        access_key = hosts['access_key']
        project_name = hosts['project_name']
        endpoint = hosts['end_point']
        connection = ODPS(access_id, access_key, project_name, endpoint)
        # connection = ODPS(access_id = hosts['access_id'],access_key = hosts['access_key'], project = hosts['project_name'], endpoint = hosts['end_point'])
        table_obj = connection.get_table(f"{project_name}.{table_name}")
        # 获取表级别的注释
        table_comment = table_obj.comment
        
    return table_comment




from elias import usual as u 

table_name = 'ch_om_t_shop'
table_name = 'ch_assets_dws_order_receivable_amount_d_f'
table_name = 'your_table_name'

hosts = u.all_hosts('bi_data_warehouse')
hosts = u.all_hosts('om')
hosts = u.all_hosts('ch_bi_report')
hosts = u.all_hosts('mc')



origin_table_name = 'om_t_shop'
origin_table_name = 'ch_assets_dws_order_receivable_amount_d_f'
origin_table_name = 'your_table_name'

target_table_name = 'om_t_shop'
target_table_name = 'ch_assets_dws_order_receivable_amount_d_f'
target_table_name = 'your_table_name'

origin_hosts = u.all_hosts('om')
origin_hosts = u.all_hosts('ch_bi_report')
origin_hosts = u.all_hosts('mc')

target_hosts = u.all_hosts('om')
target_hosts = u.all_hosts('ch_bi_report')
target_hosts = u.all_hosts('mc')

comment = mysql_comment_get(table_name,hosts)
print(comment)
