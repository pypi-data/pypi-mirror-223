# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:47:57 2023

@author: Administrator
"""

from elias import usual as u
table_name = ''
hosts = u.all_hosts('bi_data_warehouse')
comment_dic = {
    'id':'订单宽表主键也是此表主键',
    'snd_date':'发货日期',
    'trade_no2':'原始单号',
    'trade_no':'JY单号',
    'sale_type':'业务类型编码',
    'sale_type_name':'业务类型',
    'shop_id':'店铺id',
    'shop_name':'店铺',
    'shop_type':'平台',
    'goods_no':'商品编码',
    'principal':'负责人',
    'venture_id':'经营体id',
    'venture_name':'经营体',
    'syb':'事业部',
    'g_brand':'品牌',
    'class_name':'品类',
    'goods_name':'商品名称',
    'spec_name':'规格',
    'sku':'SKU',
    'sales':'销售额',
    'platform_allowance':'平台补贴',
    'sales_allowance':'销售额+平台补贴',
    'sum_sales':'订单销售额',
    'sum_platform_allowance':'订单平台补贴',
    'sum_sales_allowance':'订单（销售额+平台补贴）',
    'sales_rate':'销售额+平台补贴占订单（销售额+平台补贴）比例',
    'min_sales':'订单中明细销售额最小值',
    'min_trade_date':'订单中明细最早交易日期',
    'old_min_account_date':'老版本该订单的销售额账单中最早入账日期',
    'old_amount':'老版本该订单的销售额账单中入账总金额',
    'old_sales_rate':'老版本销售额+平台补贴占订单（销售额+平台补贴）比例',
    'old_received_amount':'老版本回款金额',
    'old_delta_amount':'老版本差异金额',
    'old_receivable_amount':'老版本应收金额',
    'sales_journal_flag':'销售额账单标识0-无账单；1-有账单；2-特殊条件视为有账单',
    'min_account_date':'该订单的销售额账单中最早入账日期',
    'amount':'该订单的销售额账单中入账总金额',
    'received_sales_amount':'销售额回款',
    'sales_delta_amount':'销售额回款差异金额',
    'sales_receivable_amount':'销售额应收金额',
    'allowance_journal_flag':'平台补贴账单标识0-无账单；1-有账单；2-特殊条件视为有账单',
    'min_allowance_account_date':'该订单的平台补贴账单中最早入账日期',
    'allowance_amount':'该订单的平台补贴账单中入账总金额',
    'received_allowance_amount':'平台补贴回款',
    'allowance_delta_amount':'平台补贴回款差异金额',
    'allowance_receivable_amount':'平台补贴应收金额',
    'delta_amount':'回款差异金额',
    'receivable_amount':'应收金额',
    'special_rules':'特殊规则',
    'receivable_days':'应收天数',
    'receivable_boxes':'应收天数分箱(左开右闭]'
    }

for i in comment_dic:
    column_name = i
    column_comment = comment_dic[i]
    r = u.mysql_column_comment(table = table_name,column = column_name,comment = column_comment,hosts = hosts)
    print(r)





from elias import usual as u
table_name = ''
hosts = u.all_hosts('bi_data_warehouse')
comment_dic ={}

def mysql_alter_comment(table_name,hosts,comment_dic):
    success_list = []
    fail_list = []
    for i in comment_dic:
        column_name = i
        column_comment = comment_dic[i]
        try:
            r = u.mysql_column_comment(table = table_name,column = column_name,comment = column_comment,hosts = hosts)
            print(r)
            success_list.append(column_name)
        except Exception as e:
            print(e)
            fail_list.append(column_name)

    s_str = ','.join(success_list)
    f_str = ','.join(fail_list)
    print(f'success：{len(success_list)}\n\nfail：{len(fail_list)}\n\n')
    print(f'success：{s_str}\nfail：{f_str}\n')



