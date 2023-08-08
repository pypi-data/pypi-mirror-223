# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 17:20:23 2023

@author: Administrator
"""


# =============================================================================
# 导入库
from elias import usual as u
from elias import wechat as w
from elias.Scripts import py_clickhouse as c

# =============================================================================
# 配置DB服务器
hosts=u.all_hosts('ch_bi_report')
origin_table_name = 'xxxxxxb'
vm_table_name = 
table_name = table_name.replace('_f','_i')
icri_table_name

today = u.date_add(u.today(),day=-2)
# robot
robot_key = w.robots(name='nl_bi_details')

# =============================================================================
# 1 代理表
# 1.1 删除代理表
def df_vm_drop():
    vm_drop_sql = '''
    DROP TABLE bi_report.XXXX ON CLUSTER default;
    '''
    df_vm_drop = c.clickhouse_ddl(vm_drop_sql,hosts)
    return df_vm_drop


# 1.2 创建代理表
def df_vm_create():
    vm_create_sql = f'''
    CREATE TABLE bi_report.{table_name}
    (
    	`id`                        Int64 COMMENT '订单宽表主键也是此表主键',
        updated                     String
    )
        ENGINE = MySQL('rm-uf698x9pde1ytqxe890130.mysql.rds.aliyuncs.com:3306', 'bi_data_warehouse',
                 '{table_name}', 'nl_bi', 'nenglianginfo_2023')
            COMMENT '应收明细表';
    '''
    
    
    df_vm_create = c.clickhouse_ddl(vm_create_sql,hosts)
    return df_vm_create



# =============================================================================
# 2 实体表
# 2.1 删除实体表
def df_drop():
    drop_sql = '''
    DROP TABLE bi_report.ch_{table_name} ON CLUSTER default;
    '''

    df_drop = c.clickhouse_ddl(drop_sql,hosts)
    return df_drop


# 2.2 创建实体表
def df_create():
    create_sql = '''
    CREATE TABLE bi_report.ch_{table_name}
    (
    	`id`                        Int64 COMMENT '订单宽表主键也是此表主键',
        updated                     String
    )
        ENGINE = ReplicatedReplacingMergeTree()
            PRIMARY KEY (id,snd_date, trade_no2, goods_no)
            ORDER BY (id,snd_date, trade_no2, goods_no)
            COMMENT '应收明细表';
    '''


    df_create = c.clickhouse_ddl(create_sql,hosts)
    return df_create

    
# 2.3 清空实体表
def df_truncate():
    truncate_sql = '''
    TRUNCATE table bi_report.ch_{table_name};
    '''
    df_truncate = c.clickhouse_ddl(truncate_sql,hosts)
    return df_truncate

    

# 2.4 插入实体表
def df_insert():
    insert_sql = '''
    INSERT INTO bi_report.ch_{table_name}
    SELECT
    *
    FROM bi_report.{table_name};
    '''
    df_insert = c.clickhouse_ddl(insert_sql,hosts)
    return df_insert
    
 
# =============================================================================   
# 3 增量分区表

# 3.1 删除增量表
def df_drop_i():
    drop_sql_i = '''
    DROP TABLE bi_report.ch_{table_name} ON CLUSTER default;
    '''
    
    df_drop_i = c.clickhouse_ddl(drop_sql_i,hosts)
    return df_drop_i

# 3.2 创建增量表
def df_create_i():
    create_sql_i = '''
    CREATE TABLE bi_report.ch_assets_dws_order_receivable_amount_d_i
    (
        `today` 					Date COMMENT '发货日期',
    	`id`                        Int64 COMMENT '订单宽表主键也是此表主键',
        `snd_date`                  String COMMENT '发货日期',
        `trade_no2`                 String COMMENT '原始单号',
        `trade_no`                  String COMMENT 'JY单号',
        `sale_type`                 String COMMENT '业务类型编码',
        `sale_type_name`            String COMMENT '业务类型',
        `shop_id`                   Float32 COMMENT '店铺id',
        `shop_name`                 String COMMENT '店铺',
        `shop_type`                 String COMMENT '平台',
        `goods_no`                  String COMMENT '商品编码',
        `principal`                 Float32 COMMENT '负责人',
        `venture_id`                Int32 COMMENT '经营体id',
        `venture_name`              String COMMENT '经营体',
        `syb`                       String COMMENT '事业部',
        `g_brand`                   String COMMENT '品牌',
        `class_name`                String COMMENT '品类',
        `goods_name`                String COMMENT '商品名称',
        `spec_name`                 String COMMENT '规格',
        `SKU`                       String COMMENT 'SKU',
        `sales`                     Float64 COMMENT '销售额',
        `platform_allowance`        Float64 COMMENT '平台补贴',
        sales_allowance             Float64 COMMENT '销售额+平台补贴',
        sum_sales                   Float64 COMMENT '订单销售额',
        sum_platform_allowance      Float64 COMMENT '订单平台补贴',
        sum_sales_allowance         Float64 COMMENT '订单（销售额+平台补贴）',
        sales_rate                  Float64 COMMENT '销售额+平台补贴占订单（销售额+平台补贴）比例',
        min_sales                   Float64 COMMENT '订单中明细销售额最小值',
        min_trade_date              String COMMENT '订单中明细最早交易日期',
        -- 原始账单
        old_min_account_date        String COMMENT '老版本 该订单的销售额账单中最早入账日期',
        old_amount                  Float64 comment '老版本 该订单的销售额账单中入账总金额',
        old_sales_rate              Float64 comment '老版本 销售额+平台补贴占订单（销售额+平台补贴）比例',
        old_received_amount         Float64 comment '老版本 回款金额',
        old_delta_amount            Float64 comment '老版本 差异金额',
        old_receivable_amount       Float64 comment '老版本 应收金额',
        -- 货款
        sales_journal_flag          Int32   COMMENT '销售额账单标识 0-无账单；1-有账单；2-特殊条件视为有账单',
        min_account_date            String comment '该订单的销售额账单中最早入账日期',
        amount                      Float64 comment '该订单的销售额账单中入账总金额',
        received_sales_amount       Float64 comment '销售额回款',
        sales_delta_amount          Float64 comment '销售额回款差异金额',
        sales_receivable_amount     Float64 comment '销售额应收金额',
        -- 补贴
        allowance_journal_flag      Int32   COMMENT '平台补贴账单标识 0-无账单；1-有账单；2-特殊条件视为有账单',
        min_allowance_account_date  String comment '该订单的平台补贴账单中最早入账日期',
        allowance_amount            Float64 comment '该订单的平台补贴账单中入账总金额',
        received_allowance_amount   Float64 comment '平台补贴回款',
        allowance_delta_amount      Float64 comment '平台补贴回款差异金额',
        allowance_receivable_amount Float64 comment '平台补贴应收金额',
        -- 总应收计算
        delta_amount                Float64 comment '回款差异金额',
        receivable_amount           Float64 comment '应收金额',
        -- 账期计算
        special_rules               String comment '特殊规则',
        receivable_days             Int32  COMMENT '应收天数',
        receivable_boxes            String COMMENT '应收天数分箱(左开右闭]',
        updated                     String,
        `current_sales_receivable_amount` Float64 COMMENT '历史当天的销售额应收金额',
        `current_allowance_receivable_amount` Float64 COMMENT '历史当天的平台补贴应收金额',
        `current_receivable_amount` Float64 COMMENT '历史当天的应收金额',
        `updatetime` String  COMMENT 'clickhouse中更新时间，历史数据计算更新日期'
    )
    ENGINE = ReplicatedReplacingMergeTree()
    PARTITION BY today
    PRIMARY KEY (today,id,snd_date,trade_no2,goods_no)
    ORDER BY (today,id,snd_date,trade_no2,goods_no)
    COMMENT '历史应收明细表（2023-01-01以后）';
    '''
    df_create_i = c.clickhouse_ddl(create_sql_i,hosts)
    return df_create_i
    

# 3.3 清空增量表
def df_truncate_i():
    truncate_sql_i = '''
    TRUNCATE table bi_report.ch_assets_dws_order_receivable_amount_d_i;
    '''

    df_truncate_i = c.clickhouse_ddl(truncate_sql_i,hosts)
    return df_truncate_i




# 3.4 删除增量表分区
def df_drop_partition_i(today):
    drop_partition_sql_i = f'''
    alter table bi_report.ch_assets_dws_order_receivable_amount_d_i drop partition '{today}';
    '''

    df_drop_partition_i = c.clickhouse_ddl(drop_partition_sql_i,hosts)
    return df_drop_partition_i

    
# 3.5 插入增量表
def df_insert_i(today):
    insert_sql_i = f'''
    INSERT INTO
    	bi_report.ch_assets_dws_order_receivable_amount_d_i
    SELECT
    	cast('{today}' as date) as `today`,
        `id`,
    	substring(`snd_date`,1,10) as `snd_date`,
    	`trade_no2`,
    	`trade_no`,
    	`sale_type`,
    	`sale_type_name`,
    	`shop_id`,
    	`shop_name`,
    	`shop_type`,
    	`goods_no`,
    	`principal`,
    	`venture_id`,
    	`venture_name`,
    	`syb`,
    	`g_brand`,
    	`class_name`,
    	`goods_name`,
    	`spec_name`,
    	`SKU`,
    	`sales`,
    	`platform_allowance`,
    	`sales_allowance`,
    	`sum_sales`,
    	`sum_platform_allowance`,
    	`sum_sales_allowance`,
    	`sales_rate`,
    	`min_sales`,
    	`min_trade_date`,
    	`old_min_account_date`,
    	`old_amount`,
    	`old_sales_rate`,
    	`old_received_amount`,
    	`old_delta_amount`,
    	`old_receivable_amount`,
    	`sales_journal_flag`,
    	`min_account_date`,
    	`amount`,
    	`received_sales_amount`,
    	`sales_delta_amount`,
    	`sales_receivable_amount`,
    	`allowance_journal_flag`,
    	`min_allowance_account_date`,
    	`allowance_amount`,
    	`received_allowance_amount`,
    	`allowance_delta_amount`,
    	`allowance_receivable_amount`,
    	`delta_amount`,
    	`receivable_amount`,
    	`special_rules`,
    	`receivable_days`,
    	`receivable_boxes`,
    	`updated` as updated,
        case when special_rules != '正常' THEN 0
                 when sales_journal_flag > 0 and substring(min_account_date,1,10) <= '{today}' then 0
        ELSE sales
        end as current_sales_receivable_amount,
        case when special_rules != '正常' THEN 0
                 when allowance_journal_flag > 0 and substring(min_allowance_account_date,1,10) <= '{today}' then 0
        ELSE platform_allowance
        end as current_allowance_receivable_amount,
        (
    	    case when special_rules != '正常' THEN 0
                 when sales_journal_flag > 0 and substring(min_account_date,1,10) <= '{today}' then 0
        	ELSE sales end 
        )+(
    	    case when special_rules != '正常' THEN 0
    	             when allowance_journal_flag > 0 and substring(min_allowance_account_date,1,10) <= '{today}' then 0
    	    ELSE platform_allowance end
        ) as current_receivable_amount,
    	cast(toDateTime(now(),'Asia/Shanghai') as String) as updatetime 
    FROM
    	bi_report.ch_assets_dws_order_receivable_amount_d_f as t
    	WHERE substring(t.snd_date,1,10)<='{today}'
    '''


    df_insert_i = c.clickhouse_ddl(insert_sql_i,hosts)
    return df_insert_i

# =============================================================================

if __name__ == '__main__':
    
    import time

    # --------------------------------------------------------------------------------------------
    start = time.time()

    print('\n【任务开始】当前时间：',u.Stamp_to_Datetime(start))
    
    # --------------------------------------------------------------------------------------------
    ee = ''
    try:
        df_truncate()
        print('truncate success')
    except Exception as e:
        print(e)
        ee = ee+f'实体表清空失败：{e}'+'\n'
    
    try:
        df_insert()
        print('insert success')
    except Exception as e:
        print(e)
        ee = ee+f'实体表插入失败：{e}'+'\n'
    
    try:
        df_drop_partition_i(today)
        print('partition drop success')
    except Exception as e:
        print(e)
        ee = ee+f'增量表当日分区删除失败：{e}'+'\n'
    
    try:
        df_insert_i(today)
        print('partition insert success')
    except Exception as e:
        print(e)
        ee = ee+f'增量表插入失败：{e}'+'\n'
    
    if ee=='':
        result = 'clickhouse 更新成功'
    else:
        result = ee
    
    # --------------------------------------------------------------------------------------------
    
    end = time.time()
    print('\n【任务结束】当前时间：',u.Stamp_to_Datetime(end))
    usetime = round(end-start, 2)
    print('usetime:', round(end-start, 2), 'seconds')
    
    # --------------------------------------------------------------------------------------------
    w.run_warning(title = f"clickhouse更新 - 资产分解（应收部分） - {usetime}",text = f'**`today`**：{today}' + '\n'+ result, user='刘益廷',key = robot_key)
    print('\n任务执行报告发送成功')



