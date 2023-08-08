from django.core.management import BaseCommand
import os
import xlrd
import datetime
from app01.models import *
import xlsxwriter
import pymysql


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.today = datetime.datetime.now()
        self.lastday = str(self.today-datetime.timedelta(days=1))[:10]
        self.department = "能良电器"
        path = 'report'
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)

        self.workbook = xlsxwriter.Workbook('./report/{}_{}.xlsx'.format(self.department,self.lastday))  # 创建新的excel


        self.summary()
        self.daily()

        self.workbook.close()


    def sgs(self,time,shop_name,spu):
        obj = OrderWideTab.objects.raw('''
                SELECT
                id,
	trade_no2,
	profit_after_inner_cost
FROM
	`operating-management`.`order_wide_tab` 
WHERE
	`snd_date` = '{}' 
	AND `shop_name` = '{}' 
	AND `goods_spu` = '{}' 
	and del_type = 1
	AND goods_count > 0
	and trade_no2 not like "%%调整列%%"
	

                '''.format(time,shop_name,spu))

        z_d = 0
        f_d = 0

        for i in obj:
            profit_after_inner_cost = i.profit_after_inner_cost
            if profit_after_inner_cost > 0:
                z_d += 1
            if profit_after_inner_cost  < 0:
                f_d += 1

        sum = z_d + f_d

        return  sum,f_d,z_d


    def summary(self):
        sheet = self.workbook.add_worksheet('SPU维度')  # 创建新的sheet
        headings = ['日期','经营体','部门','店铺','SPU','商品名称','总销售单量','亏损单量','盈利单量','亏损总金额','亏损占比','单均亏损',
                    '运营',]

        sheet.write_row(0, 0, headings)

        # sheet.set_column('A:A', 34)
        # sheet.set_column('B:B', 10)
        # sheet.set_column('C:D', 28)
        # sheet.set_column('E:E', 38)
        # sheet.set_column('F:F', 30)
        # sheet.set_column('G:G', 12)

        obj = OrderWideTab.objects.raw('''
        SELECT
        w.id,
        w.snd_date as snd_date,
	w.venture_name as venture_name,
	w.shop_name as shop_name,
	w.goods_name as goods_name,
	w.goods_spu as goods_spu,
	e.`name` as `name`,
	sum(profit_after_inner_cost) as money
FROM
	`operating-management`.`order_wide_tab` AS w
	JOIN om_org_employee AS e ON w.principal = e.id 
WHERE
	w.`snd_date` = '2023-03-26' 
	AND LEFT(W.venture_name,4) = "{}"
	AND w.del_type = 1 
	AND w.goods_count > 0 
	and w.trade_no2 not like "%%调整列%%"
	AND w.profit_after_inner_cost < 0 
GROUP BY
	w.venture_name,
	w.shop_name,
	w.goods_spu

        '''.format(self.department))

        row = 1
        for data in obj:
            snd_date = str(data.snd_date)
            venture_name= data.venture_name
            v_name = venture_name[:4]
            shop_name = data.shop_name
            goods_name = data.goods_name
            goods_spu  =data.goods_spu

            result = self.sgs(snd_date,shop_name,goods_spu)
            print(snd_date,shop_name,goods_spu)
            print("result",result)


            name = data.name
            money = data.money


            sheet.write(row,0,snd_date)
            sheet.write(row,1,venture_name)
            sheet.write(row,2,v_name)
            sheet.write(row, 3, shop_name)
            sheet.write(row, 4, goods_spu)
            sheet.write(row, 5, goods_name)
            sheet.write(row, 6,result[0] ) #总
            sheet.write(row, 7,result[1] ) #亏
            sheet.write(row, 8,result[2] ) #盈利
            sheet.write(row, 9,money )

            sheet.write(row, 10,format(( result[1]/ result[0]), '.2%' ) )#盈亏占比
            sheet.write(row, 11,money/ result[1])#单均亏损
            sheet.write(row, 12,name )

            row += 1





    def daily(self):

        worksheet = self.workbook.add_worksheet('订单详情')  # 创建新的sheet
        headings = ['日期','经营体名称','管家订单号','原始单号','平台','店铺名称',
                    '品牌','商品名称','商品sku','销量','销售额','进销毛利','占比',
                    '加平台补贴余额','占比2','减销售费用余额','占比3','减履约费用余额','占比4',
                    '减推广费用余额','占比5','减人工费用余额','占比6','减资金费用余额','占比7',
                    '减其他费用余额','占比8','部门毛利','占比9','其它办公费用','占比10',
                    '四级负责人','原因分析及对策','三级负责人','评论','二级负责人','评论2',
                    '商品成本','采购返利','价保','毛保','平台补贴','销售返现','赠品成本','平台费用','物流费用',
                    '售后成本','总推广费','部门其他成本',"shop_id","xs_shop_id",
"sale_type",
"trade_nl",
"goods_id",
"goods_spu",
"class_name",
"goods_weight",
"logistic_id",
"logistic_name",
"warehouse_id",
"warehouse_name",
"goods_len",
"goods_width",
"goods_height",
"bar_code",
"g_brand",
"trade_amount",
"used_integral",
"rebate_delivery",
"rebate_volume",
"rebate_marketing",
"rebate_marketing_promotion",
"rebate_marketing_activity",
"rebate_out",
"rebate_other",
"price_pledge_stock",
"price_pledge_delivery",
"price_pledge_other",
"platform_allowance_pdd",
"platform_allowance_xiaomi",
"salse_refund_inorder",
"salse_refund_outorder",
"salse_refund_outorder_amount",
"salse_refund_outorder_cost",
"gifts_drainage",
"gifts_drainage_entity",
"gifts_drainage_entity_goods",
"gifts_drainage_entity_card",
"gifts_drainage_virtual_card",
"gifts_drainage_other",
"gifts_deal",
"gifts_drainage_entity",
"gifts_drainage_entity_goods",
"gifts_drainage_entity_card",
"gifts_drainage_virtual_card",
"gifts_drainage_other",
"gifts_repurchase",
"gifts_drainage_entity",
"gifts_drainage_entity_goods",
"gifts_drainage_entity_card",
"gifts_drainage_virtual_card",
"gifts_drainage_other",
"gifts_referral",
"gifts_drainage_entity",
"gifts_drainage_entity_goods",
"gifts_drainage_entity_card",
"gifts_drainage_virtual_card",
"gifts_drainage_other",
"gifts_others",
"profit_salse_minus",
"profit_salse_add",
"give_integral",
"cost_pdd_performance",
"cost_pdd_commission",
"cost_pdd_fenqi",
"cost_pdd_service",
"cost_pdd_commission_ddjb",
"cost_pdd_groupon",
"cost_pdd_groupon_out",
"iphone",
"cost_jd_performance",
"cost_jd_commission",
"cost_jd_jingdou",
"cost_jd_jingtiaoke",
"cost_jd_insurance_pop",
"cost_jd_baitiao",
"cost_pdd_service",
"cost_tb_performance",
"cost_tb_commission_tmall",
"cost_tb_service_cuntao",
"cost_tb_rebate_integral",
"cost_tb_ryt",
"cost_tb_mlt",
"cost_tb_publicgood",
"cost_tb_cuntao",
"cost_tb_insurance_transportation",
"cost_tb_instalment_huabei",
"cost_tb_huabei",
"cost_tb_credit_card",
"cost_tb_yitao",
"cost_pdd_service",
"cost_other_performance",
"cost_other_commission",
"cost_platform_tax_wx",
"cost_base_operation",
"cost_warehousing",
"cost_warehousing_pickup",
"cost_warehousing_added",
"cost_warehousing_arrange",
"cost_warehouse",
"cost_warehouse_external",
"cost_warehouse_cainiao",
"cost_warehouse_oruite",
"cost_warehouse_jd",
"cost_warehouse_internal",
"cost_warehouse_shanghai",
"cost_warehouse_yiwu",
"cost_sorting",
"cost_packing",
"cost_packing_operation",
"cost_packing_operation_notape",
"cost_packing_operation_tape",
"cost_packing_supplies",
"cost_packing_outer",
"cost_packing_carton",
"cost_packing_inner",
"cost_packing_bubble_cloumn",
"cost_packing_gourd_film",
"cost_packing_other",
"cost_express",
"cost_express_sto",
"cost_express_sto_shanghai",
"cost_express_sto_yiwu",
"cost_express_yuantong",
"cost_express_zto",
"cost_express_yunda",
"cost_express_sf",
"cost_express_flash",
"cost_express_nl",
"cost_express_self",
"cost_express_other",
"cs_perfomance",
"cs_perfomance_bonus",
"cost_aftersales_deal",
"cost_aftersales_compensation_cash",
"cost_aftersales_repair",
"cost_aftersales_express",
"cost_aftersales_damage",
"cost_aftersales_other",
"promotion_pdd",
"promotion_pdd_recharge",
"promotion_pdd_materiel",
"cost_express_other",
"promotion_jd",
"promotion_jd_kc",
"promotion_jd_cd",
"promotion_jd_ht",
"promotion_jd_jzt",
"promotion_pdd_materiel",
"cost_express_other",
"promotion_tb",
"promotion_tb_ztc",
"promotion_tb_pxb",
"promotion_tb_jewel",
"promotion_tb_superrecommend",
"promotion_tb_new",
"promotion_tb_tbk",
"promotion_tb_back_card",
"promotion_tb_tools",
"promotion_pdd_materiel",
"promotion_tb_celebrity",
"cost_express_other",
"other_promotion",
"cost_human_resources_level_1",
"cost_human_resources_level_2",
"cost_human_resources_level_3",
"cost_human_resources_operating",
"cost_human_resources_cs",
"cs_base_wage",
"cs_social_insurance",
"cs_accumulation_fund",
"cs_welfare",
"cs_commuting_subsidy",
"cs_accommodation_subsidy",
"cs_communication_subsidy",
"cs_dinner_subsidy",
"cs_team_construction_subsidy",
"cs_insurance_supply",
"cs_physical_examination",
"cs_welfare_other",
"cost_human_resources_anchor",
"anchor_base_wage",
"anchor_perfomance",
"cs_social_insurance",
"cs_accumulation_fund",
"anchor_welfare",
"cs_commuting_subsidy",
"cs_accommodation_subsidy",
"cs_communication_subsidy",
"cs_dinner_subsidy",
"cs_team_construction_subsidy",
"cs_insurance_supply",
"cs_physical_examination",
"cs_welfare_other",
"anchor_equipment",
"anchor_microphone",
"anchor_lighting",
"anchor_camera",
"anchor_ktboard",
"anchor_equipment_other",
"cost_human_resources_aftersales",
"cost_human_resources_other",
"cost_human_resources_purchase_director",
"cs_company_subsidy",
"cost_fund_interest",
"cost_loan_interest",
"cost_service_charge",
"cost_fund_occupation",
"cost_interest_other",
"expense_department_entertainment",
"expense_travel",
"expense_entertainment",
"expense_gifts",
"expense_department_entertainment_other",
"expense_department_share",
"expense_travel_operating_share",
"expense_miscellaneous",
"expense_depreciation_facilities",
"expense_additional_tax",
"expense_insurance",
"cost_express_other",
"expense_storage_loss_share",
"loss_provision",
"damage_provision",
"overstocking_provision",
"expense_information_share",
"expense_computer_hardware",
"expense_computer_accessories",
"expense_software",
"expense_communication",
"expense_network_broadband",
"expense_cloud_services",
"cost_inner",
"cost_office_share",
"share_office_supplies",
"share_stationery_procurement",
"share_printing_equipment",
"share_printing_paper",
"share_ink",
"share_other_supplies",
"cost_site",
"share_rent",
"share_water",
"share_electricity",
"share_house_decoration",
"share_house_maintenance",
"share_daily_cleaning",
"share_garbage_disposal",
"share_air_conditioning_lighting_equipment_loss",
"share_other_energy",
"cost_working_dress",
"dress_frock",
"dress_work_license",
"dress_other",
"cost_other_consumables",
"share_tables_chairs",
"share_fan",
"share_drinking",
"share_snack",
"share_sanitary_products",
"share_first_aid_medicine",
"share_epidemic_prevention_supplies",
"share_other_consumables",
"cost_labor_share",
"share_staff_wage",
"share_staff_base_wage",
"share_staff_performance_wage",
"share_staff_bonus",
"share_staff_susidy",
"share_staff_social_insurance",
"share_staff_accumulation_fund",
"share_staff_welfare",
"cs_commuting_subsidy",
"cs_accommodation_subsidy",
"cs_communication_subsidy",
"cs_dinner_subsidy",
"cs_team_construction_subsidy",
"cs_insurance_supply",
"cs_physical_examination",
"cs_welfare_other",
"cost_labor_share_other",
"cost_other_inner_share",
"share_donation",
"share_sponsor",
"share_forfeit",
"share_confiscate",
"share_bad_debt",
"share_abnormal_loss",
"adjust_money_other",
"cost_platform_tax",
"cost_platform_tax_pdd",
"cost_tax",
"added_normal_tax",
"added_allowance_tax",
"cost_tax_income",
"cost_tax_added_value",
"profit_aftertax",
"del_type",
"is_scalper",
"state",
"per_id_level_top_name",
"ranking_category",
"performance_share_cost",
"per_id_level_top_name_info",
"per_id_level_middle_name_info",
"per_id_level_low_name",
'category',
'盈亏']   # 创建表头
        # 读取表头
        worksheet.write_row(0,0, headings)

        row = 1


        #old
#         obj_data = OrderWideTab.objects.raw('''
#         SELECT
#        w.*,
#        c.three_category
# FROM
#         order_wide_tab w
#         LEFT JOIN org_brand_info f ON LEFT ( w.goods_no, 16 ) = f.spu_code
#         LEFT JOIN org_brand_category c ON f.brand_category_id = c.id
# WHERE
#         w.snd_date = '{0}'
#         AND w.g_brand = '{1}'
#
#         AND w.del_type = 1
#         AND w.goods_count > 0
#         AND ( c.three_category = "手机" OR c.three_category IS NULL OR c.three_category = "" )
#
#         '''.format(self.lastday,'OPPO'))

        obj_data_3 = OrderWideTab.objects.raw('''
        SELECT
	* 
FROM
	`operating-management`.`order_wide_tab` 
WHERE
	`g_brand` = '荣耀（honor）' 
	AND `snd_date` = '{}' 
	AND `three_category` = '手机' 
	and del_type = 1
	and goods_count >0
        
                '''.format(self.lastday))

        obj_ceshi = OrderWideTab.objects.raw('''
       SELECT
	w.* ,
	e.`name`
FROM
	`operating-management`.`order_wide_tab` as w join om_org_employee as e on w.principal = e.id
WHERE
	 w.`snd_date` = '2023-03-26' 
	AND w.del_type = 1 
	AND LEFT(W.venture_name,4) = "{}"
	AND w.goods_count >0
	and w.trade_no2 not like "%%调整列%%"
	and w.profit_after_inner_cost < 0 
        
                '''.format(self.department))


        for obj in obj_ceshi:
            snd_date = str(obj.snd_date)
            venture_name = obj.venture_name
            trade_no = obj.trade_no  #管家订单号
            trade_no2 = obj.trade_no2 #原始单号
            shop_type = obj.shop_type
            shop_name = obj.shop_name  #店铺名称
            brand = obj.brand
            goods_name = obj.goods_name #商品名称
            goods_no = obj.goods_no  #商品sku
            goods_count = obj.goods_count
            sales = obj.sales
            # print('sales',sales)
            profit_purchase = obj.profit_purchase #进销毛利
            profit_add_allowance = obj.profit_add_allowance #加平台补贴余额
            profit_sales = obj.profit_sales #减销售费用余额
            profit_aftersales = obj.profit_aftersales #减履约费用余额
            profit_after_promotion = obj.profit_after_promotion #减推广费用余额
            profit_after_humanresources = obj.profit_after_humanresources #减人工费用余额
            profit_after_fund = obj.profit_after_fund #减资金费用余额
            profit_after_expense = obj.profit_after_expense #减其他费用余额
            profit_after_inner_cost = obj.profit_after_inner_cost #部门毛利
            cost_office_share_other = obj.cost_office_share_other #其他办公费用

            # 负责人
            level_4 = obj.name
            level_3 = obj.per_id_level_low_name_info
            level_2 = obj.per_id_level_middle_name_info

            cost_goods = obj.cost_goods #商品成本
            rebate = obj.rebate #采购返利
            price_pledge = obj.price_pledge #价保
            cost_protect = obj.cost_protect #毛保
            platform_allowance = obj.platform_allowance #平台补贴
            salse_refund = obj.salse_refund #销售返现
            cost_gifts = obj.cost_gifts # 赠品成本
            cost_platform = obj.cost_platform # 平台费用
            cost_logistics = obj.cost_logistics #物流费用
            cost_aftersales = obj.cost_aftersales # 售后成本
            cost_promotion = obj.cost_promotion # 总推广费
            cost_department = obj.cost_department# 部门其他成本

            #zhouyue
            shop_id = obj.shop_id  # 店铺id
            xs_shop_id = obj.xs_shop_id  # 醒市店铺id
            sale_type = obj.sale_type  # 销售类型
            trade_nl = obj.trade_nl  # 能良订单号
            goods_id = obj.goods_id  # 商品id
            goods_spu = obj.goods_spu  # 商品SPU
            class_name = obj.class_name  # 品类
            goods_weight = obj.goods_weight  # 货品重量
            logistic_id = obj.logistic_id  # 物流公司id
            logistic_name = obj.logistic_name  # 物流公司名称
            warehouse_id = obj.warehouse_id  # 仓库id
            warehouse_name = obj.warehouse_name  # 仓库名
            goods_len = obj.goods_len  # 长
            goods_width = obj.goods_width  # 宽
            goods_height = obj.goods_height  # 高
            bar_code = obj.bar_code  # 条码
            g_brand = obj.g_brand  # 修改后品牌
            trade_amount = obj.trade_amount  # 醒市交易金额
            used_integral = obj.used_integral  # 购物下单使用购物金
            rebate_delivery = obj.rebate_delivery  # 提货返
            rebate_volume = obj.rebate_volume  # 达量返
            rebate_marketing = obj.rebate_marketing  # 营销返利
            rebate_marketing_promotion = obj.rebate_marketing_promotion  # 促销返利
            rebate_marketing_activity = obj.rebate_marketing_activity  # 市场活动返利
            rebate_out = obj.rebate_out  # out返利
            rebate_other = obj.rebate_other  # 其它返利
            price_pledge_stock = obj.price_pledge_stock  # 库存价保
            price_pledge_delivery = obj.price_pledge_delivery  # 提货价保
            price_pledge_other = obj.price_pledge_other  # 其它价保
            platform_allowance_pdd = obj.platform_allowance_pdd  # 拼多多补贴
            platform_allowance_xiaomi = obj.platform_allowance_xiaomi  # 小米有品补贴
            salse_refund_inorder = obj.salse_refund_inorder  # 单内退款
            salse_refund_outorder = obj.salse_refund_outorder  # 单外退款
            salse_refund_outorder_amount = obj.salse_refund_outorder_amount  # 单外退款金额
            salse_refund_outorder_cost = obj.salse_refund_outorder_cost  # 单外退款成本
            gifts_drainage = obj.gifts_drainage  # 引流赠品
            gifts_drainage_entity = obj.gifts_drainage_entity  # 实物赠品
            gifts_drainage_entity_goods = obj.gifts_drainage_entity_goods  # 商品实物赠品
            gifts_drainage_entity_card = obj.gifts_drainage_entity_card  # 实体卡赠品
            gifts_drainage_virtual_card = obj.gifts_drainage_virtual_card  # 虚拟卡券赠品
            gifts_drainage_other = obj.gifts_drainage_other  # 其它赠品
            gifts_deal = obj.gifts_deal  # 成交赠品
            gifts_drainage_entity = obj.gifts_drainage_entity  # 实物赠品
            gifts_drainage_entity_goods = obj.gifts_drainage_entity_goods  # 商品实物赠品
            gifts_drainage_entity_card = obj.gifts_drainage_entity_card  # 实体卡赠品
            gifts_drainage_virtual_card = obj.gifts_drainage_virtual_card  # 虚拟卡券赠品
            gifts_drainage_other = obj.gifts_drainage_other  # 其它赠品
            gifts_repurchase = obj.gifts_repurchase  # 回头（复购）赠品
            gifts_drainage_entity = obj.gifts_drainage_entity  # 实物赠品
            gifts_drainage_entity_goods = obj.gifts_drainage_entity_goods  # 商品实物赠品
            gifts_drainage_entity_card = obj.gifts_drainage_entity_card  # 实体卡赠品
            gifts_drainage_virtual_card = obj.gifts_drainage_virtual_card  # 虚拟卡券赠品
            gifts_drainage_other = obj.gifts_drainage_other  # 其它赠品
            gifts_referral = obj.gifts_referral  # 转介绍赠品
            gifts_drainage_entity = obj.gifts_drainage_entity  # 实物赠品
            gifts_drainage_entity_goods = obj.gifts_drainage_entity_goods  # 商品实物赠品
            gifts_drainage_entity_card = obj.gifts_drainage_entity_card  # 实体卡赠品
            gifts_drainage_virtual_card = obj.gifts_drainage_virtual_card  # 虚拟卡券赠品
            gifts_drainage_other = obj.gifts_drainage_other  # 其它赠品
            gifts_others = obj.gifts_others  # 其它赠品分类
            profit_salse_minus = obj.profit_salse_minus  # 其它减项
            profit_salse_add = obj.profit_salse_add  # 其它加项
            give_integral = obj.give_integral  # 赠送购物金红包
            cost_pdd_performance = obj.cost_pdd_performance  # 拼多多履约
            cost_pdd_commission = obj.cost_pdd_commission  # 拼多多佣金
            cost_pdd_fenqi = obj.cost_pdd_fenqi  # 拼多多分期
            cost_pdd_service = obj.cost_pdd_service  # 服务费支出
            cost_pdd_commission_ddjb = obj.cost_pdd_commission_ddjb  # 多多进宝佣金
            cost_pdd_groupon = obj.cost_pdd_groupon  # 百亿补贴活动费收入
            cost_pdd_groupon_out = obj.cost_pdd_groupon_out  # pdd百亿补贴技术服务费
            iphone = obj.iphone  # iphone
            cost_jd_performance = obj.cost_jd_performance  # 京东履约
            cost_jd_commission = obj.cost_jd_commission  # 京东佣金
            cost_jd_jingdou = obj.cost_jd_jingdou  # 京豆
            cost_jd_jingtiaoke = obj.cost_jd_jingtiaoke  # 京挑客
            cost_jd_insurance_pop = obj.cost_jd_insurance_pop  # POP运费险
            cost_jd_baitiao = obj.cost_jd_baitiao  # 京东白条
            cost_pdd_service = obj.cost_pdd_service  # 服务费支出
            cost_tb_performance = obj.cost_tb_performance  # 淘宝履约
            cost_tb_commission_tmall = obj.cost_tb_commission_tmall  # 天猫佣金
            cost_tb_service_cuntao = obj.cost_tb_service_cuntao  # 村淘平台技术服务费
            cost_tb_rebate_integral = obj.cost_tb_rebate_integral  # 返点积分
            cost_tb_ryt = obj.cost_tb_ryt  # 淘宝客如意投
            cost_tb_mlt = obj.cost_tb_mlt  # 淘宝客魔力投
            cost_tb_publicgood = obj.cost_tb_publicgood  # 公益宝贝
            cost_tb_cuntao = obj.cost_tb_cuntao  # 村淘导购
            cost_tb_insurance_transportation = obj.cost_tb_insurance_transportation  # 运费险
            cost_tb_instalment_huabei = obj.cost_tb_instalment_huabei  # 花呗分期
            cost_tb_huabei = obj.cost_tb_huabei  # 花呗支付
            cost_tb_credit_card = obj.cost_tb_credit_card  # 信用卡支付
            cost_tb_yitao = obj.cost_tb_yitao  # 一淘营销服务
            cost_pdd_service = obj.cost_pdd_service  # 服务费支出
            cost_other_performance = obj.cost_other_performance  # 其它履约
            cost_other_commission = obj.cost_other_commission  # 其它佣金
            cost_platform_tax_wx = obj.cost_platform_tax_wx  # 微信平台佣金
            cost_base_operation = obj.cost_base_operation  # 基础操作费
            cost_warehousing = obj.cost_warehousing  # 入库
            cost_warehousing_pickup = obj.cost_warehousing_pickup  # 提货费
            cost_warehousing_added = obj.cost_warehousing_added  # 直接入库费
            cost_warehousing_arrange = obj.cost_warehousing_arrange  # 整理入库费
            cost_warehouse = obj.cost_warehouse  # 仓储
            cost_warehouse_external = obj.cost_warehouse_external  # 外仓
            cost_warehouse_cainiao = obj.cost_warehouse_cainiao  # 菜鸟XX市仓
            cost_warehouse_oruite = obj.cost_warehouse_oruite  # 欧瑞特XX市仓
            cost_warehouse_jd = obj.cost_warehouse_jd  # 京东XX市仓
            cost_warehouse_internal = obj.cost_warehouse_internal  # 内仓
            cost_warehouse_shanghai = obj.cost_warehouse_shanghai  # 上海仓
            cost_warehouse_yiwu = obj.cost_warehouse_yiwu  # 义乌仓
            cost_sorting = obj.cost_sorting  # 分拣
            cost_packing = obj.cost_packing  # 打包
            cost_packing_operation = obj.cost_packing_operation  # 操作费
            cost_packing_operation_notape = obj.cost_packing_operation_notape  # 无胶带成本
            cost_packing_operation_tape = obj.cost_packing_operation_tape  # 有胶带成本
            cost_packing_supplies = obj.cost_packing_supplies  # 物料费
            cost_packing_outer = obj.cost_packing_outer  # 外包装
            cost_packing_carton = obj.cost_packing_carton  # 外包装纸箱成本
            cost_packing_inner = obj.cost_packing_inner  # 内包装
            cost_packing_bubble_cloumn = obj.cost_packing_bubble_cloumn  # 内包装气泡柱
            cost_packing_gourd_film = obj.cost_packing_gourd_film  # 内包装葫芦膜
            cost_packing_other = obj.cost_packing_other  # 其它物料
            cost_express = obj.cost_express  # 快递
            cost_express_sto = obj.cost_express_sto  # 申通
            cost_express_sto_shanghai = obj.cost_express_sto_shanghai  # 上海
            cost_express_sto_yiwu = obj.cost_express_sto_yiwu  # 义乌
            cost_express_yuantong = obj.cost_express_yuantong  # 圆通
            cost_express_zto = obj.cost_express_zto  # 中通
            cost_express_yunda = obj.cost_express_yunda  # 韵达
            cost_express_sf = obj.cost_express_sf  # 顺丰
            cost_express_flash = obj.cost_express_flash  # XX闪送
            cost_express_nl = obj.cost_express_nl  # 能良自送
            cost_express_self = obj.cost_express_self  # 自提
            cost_express_other = obj.cost_express_other  # 其它
            cs_perfomance = obj.cs_perfomance  # 客服绩效
            cs_perfomance_bonus = obj.cs_perfomance_bonus  # 客服绩效奖金
            cost_aftersales_deal = obj.cost_aftersales_deal  # 售后处理成本
            cost_aftersales_compensation_cash = obj.cost_aftersales_compensation_cash  # 现金补偿
            cost_aftersales_repair = obj.cost_aftersales_repair  # 维修成本
            cost_aftersales_express = obj.cost_aftersales_express  # 快递成本
            cost_aftersales_damage = obj.cost_aftersales_damage  # 报损处理
            cost_aftersales_other = obj.cost_aftersales_other  # 其它售后费用成本
            promotion_pdd = obj.promotion_pdd  # 拼多多推广
            promotion_pdd_recharge = obj.promotion_pdd_recharge  # 拼多多充值推广
            promotion_pdd_materiel = obj.promotion_pdd_materiel  # 随单促销物料
            cost_express_other = obj.cost_express_other  # 其它
            promotion_jd = obj.promotion_jd  # 京东推广
            promotion_jd_kc = obj.promotion_jd_kc  # 京东推广快车
            promotion_jd_cd = obj.promotion_jd_cd  # 京东推广触点
            promotion_jd_ht = obj.promotion_jd_ht  # 京东推广海投
            promotion_jd_jzt = obj.promotion_jd_jzt  # 精准通
            promotion_pdd_materiel = obj.promotion_pdd_materiel  # 随单促销物料
            cost_express_other = obj.cost_express_other  # 其它
            promotion_tb = obj.promotion_tb  # 淘宝推广
            promotion_tb_ztc = obj.promotion_tb_ztc  # 天猫直通车
            promotion_tb_pxb = obj.promotion_tb_pxb  # 品销宝
            promotion_tb_jewel = obj.promotion_tb_jewel  # 钻石展位
            promotion_tb_superrecommend = obj.promotion_tb_superrecommend  # 超级推荐
            promotion_tb_new = obj.promotion_tb_new  # 品牌新享首单拉新计划
            promotion_tb_tbk = obj.promotion_tb_tbk  # 天猫淘宝客
            promotion_tb_back_card = obj.promotion_tb_back_card  # 天猫买返卡
            promotion_tb_tools = obj.promotion_tb_tools  # 其它商家工具
            promotion_pdd_materiel = obj.promotion_pdd_materiel  # 随单促销物料
            promotion_tb_celebrity = obj.promotion_tb_celebrity  # 网红推广
            cost_express_other = obj.cost_express_other  # 其它
            other_promotion = obj.other_promotion  # 其它平台推广费
            cost_human_resources_level_1 = obj.cost_human_resources_level_1  # 一级部门成本事业部总
            cost_human_resources_level_2 = obj.cost_human_resources_level_2  # 二级部门成本总监
            cost_human_resources_level_3 = obj.cost_human_resources_level_3  # 三级部门成本经理
            cost_human_resources_operating = obj.cost_human_resources_operating  # 运营成本
            cost_human_resources_cs = obj.cost_human_resources_cs  # 客服成本
            cs_base_wage = obj.cs_base_wage  # 客服基础工资
            cs_social_insurance = obj.cs_social_insurance  # 客服社保
            cs_accumulation_fund = obj.cs_accumulation_fund  # 客服公积金
            cs_welfare = obj.cs_welfare  # 客服福利
            cs_commuting_subsidy = obj.cs_commuting_subsidy  # 通勤补贴
            cs_accommodation_subsidy = obj.cs_accommodation_subsidy  # 住宿补贴
            cs_communication_subsidy = obj.cs_communication_subsidy  # 通讯补贴
            cs_dinner_subsidy = obj.cs_dinner_subsidy  # 活动聚餐
            cs_team_construction_subsidy = obj.cs_team_construction_subsidy  # 旅游团建
            cs_insurance_supply = obj.cs_insurance_supply  # 补充保险
            cs_physical_examination = obj.cs_physical_examination  # 体检
            cs_welfare_other = obj.cs_welfare_other  # 其它福利
            cost_human_resources_anchor = obj.cost_human_resources_anchor  # 主播成本
            anchor_base_wage = obj.anchor_base_wage  # 主播基础工资
            anchor_perfomance = obj.anchor_perfomance  # 主播业绩提成
            cs_social_insurance = obj.cs_social_insurance  # 客服社保
            cs_accumulation_fund = obj.cs_accumulation_fund  # 客服公积金
            anchor_welfare = obj.anchor_welfare  # 主播福利
            cs_commuting_subsidy = obj.cs_commuting_subsidy  # 通勤补贴
            cs_accommodation_subsidy = obj.cs_accommodation_subsidy  # 住宿补贴
            cs_communication_subsidy = obj.cs_communication_subsidy  # 通讯补贴
            cs_dinner_subsidy = obj.cs_dinner_subsidy  # 活动聚餐
            cs_team_construction_subsidy = obj.cs_team_construction_subsidy  # 旅游团建
            cs_insurance_supply = obj.cs_insurance_supply  # 补充保险
            cs_physical_examination = obj.cs_physical_examination  # 体检
            cs_welfare_other = obj.cs_welfare_other  # 其它福利
            anchor_equipment = obj.anchor_equipment  # 直播设备成本
            anchor_microphone = obj.anchor_microphone  # 话筒设备
            anchor_lighting = obj.anchor_lighting  # 灯具照明
            anchor_camera = obj.anchor_camera  # 摄像设备
            anchor_ktboard = obj.anchor_ktboard  # KT板
            anchor_equipment_other = obj.anchor_equipment_other  # 其它直播设备
            cost_human_resources_aftersales = obj.cost_human_resources_aftersales  # 售后人工成本
            cost_human_resources_other = obj.cost_human_resources_other  # 其他人工成本
            cost_human_resources_purchase_director = obj.cost_human_resources_purchase_director  # 采购总监
            cs_company_subsidy = obj.cs_company_subsidy  # 客服人工公司补贴
            cost_fund_interest = obj.cost_fund_interest  # 资金成本
            cost_loan_interest = obj.cost_loan_interest  # 贷款利息
            cost_service_charge = obj.cost_service_charge  # 手续费
            cost_fund_occupation = obj.cost_fund_occupation  # 资金占用费
            cost_interest_other = obj.cost_interest_other  # 其它资金利息成本
            expense_department_entertainment = obj.expense_department_entertainment  # 差旅招待
            expense_travel = obj.expense_travel  # 差旅费
            expense_entertainment = obj.expense_entertainment  # 招待费
            expense_gifts = obj.expense_gifts  # 礼品费
            expense_department_entertainment_other = obj.expense_department_entertainment_other  # 其它差旅招待成本
            expense_department_share = obj.expense_department_share  # 其它公共成本
            expense_travel_operating_share = obj.expense_travel_operating_share  # 营业费用分摊
            expense_miscellaneous = obj.expense_miscellaneous  # 运杂费
            expense_depreciation_facilities = obj.expense_depreciation_facilities  # 设施设备折旧费
            expense_additional_tax = obj.expense_additional_tax  # 附加税金
            expense_insurance = obj.expense_insurance  # 保险
            cost_express_other = obj.cost_express_other  # 其它
            expense_storage_loss_share = obj.expense_storage_loss_share  # 库损成本分摊
            loss_provision = obj.loss_provision  # 丢失计提
            damage_provision = obj.damage_provision  # 损坏计提
            overstocking_provision = obj.overstocking_provision  # 积压报废
            expense_information_share = obj.expense_information_share  # 信息费分摊
            expense_computer_hardware = obj.expense_computer_hardware  # 电脑硬件
            expense_computer_accessories = obj.expense_computer_accessories  # 键盘鼠标配件耗材
            expense_software = obj.expense_software  # 软件
            expense_communication = obj.expense_communication  # 通信
            expense_network_broadband = obj.expense_network_broadband  # 网络宽带
            expense_cloud_services = obj.expense_cloud_services  # 云服务
            cost_inner = obj.cost_inner  # 内部小计
            cost_office_share = obj.cost_office_share  # 内部办公费用分摊
            share_office_supplies = obj.share_office_supplies  # 办公用品
            share_stationery_procurement = obj.share_stationery_procurement  # 文具采购
            share_printing_equipment = obj.share_printing_equipment  # 打印设备
            share_printing_paper = obj.share_printing_paper  # 打印纸消耗
            share_ink = obj.share_ink  # 油墨消耗
            share_other_supplies = obj.share_other_supplies  # 其它用品消耗
            cost_site = obj.cost_site  # 水电煤房租
            share_rent = obj.share_rent  # 房租
            share_water = obj.share_water  # 水费
            share_electricity = obj.share_electricity  # 电费
            share_house_decoration = obj.share_house_decoration  # 房屋装修
            share_house_maintenance = obj.share_house_maintenance  # 房屋维修
            share_daily_cleaning = obj.share_daily_cleaning  # 日常清扫
            share_garbage_disposal = obj.share_garbage_disposal  # 垃圾处理
            share_air_conditioning_lighting_equipment_loss = obj.share_air_conditioning_lighting_equipment_loss  # 空调照明设备损耗
            share_other_energy = obj.share_other_energy  # 其它能源消耗
            cost_working_dress = obj.cost_working_dress  # 服装工牌
            dress_frock = obj.dress_frock  # 工装
            dress_work_license = obj.dress_work_license  # 工牌
            dress_other = obj.dress_other  # 其它服装用品
            cost_other_consumables = obj.cost_other_consumables  # 其它办公易耗品
            share_tables_chairs = obj.share_tables_chairs  # 桌椅板凳
            share_fan = obj.share_fan  # 风扇
            share_drinking = obj.share_drinking  # 饮水茶具
            share_snack = obj.share_snack  # 零食饮料供给
            share_sanitary_products = obj.share_sanitary_products  # 卫生用品
            share_first_aid_medicine = obj.share_first_aid_medicine  # 急救药品
            share_epidemic_prevention_supplies = obj.share_epidemic_prevention_supplies  # 防疫用品（含口罩）
            share_other_consumables = obj.share_other_consumables  # 其它易耗品
            cost_labor_share = obj.cost_labor_share  # 内部人力成本分摊
            share_staff_wage = obj.share_staff_wage  # 人员工资
            share_staff_base_wage = obj.share_staff_base_wage  # 固定工资
            share_staff_performance_wage = obj.share_staff_performance_wage  # 绩效工资
            share_staff_bonus = obj.share_staff_bonus  # 人员奖金
            share_staff_susidy = obj.share_staff_susidy  # 人员津贴
            share_staff_social_insurance = obj.share_staff_social_insurance  # 人员社保
            share_staff_accumulation_fund = obj.share_staff_accumulation_fund  # 人员公积金
            share_staff_welfare = obj.share_staff_welfare  # 福利费
            cs_commuting_subsidy = obj.cs_commuting_subsidy  # 通勤补贴
            cs_accommodation_subsidy = obj.cs_accommodation_subsidy  # 住宿补贴
            cs_communication_subsidy = obj.cs_communication_subsidy  # 通讯补贴
            cs_dinner_subsidy = obj.cs_dinner_subsidy  # 活动聚餐
            cs_team_construction_subsidy = obj.cs_team_construction_subsidy  # 旅游团建
            cs_insurance_supply = obj.cs_insurance_supply  # 补充保险
            cs_physical_examination = obj.cs_physical_examination  # 体检
            cs_welfare_other = obj.cs_welfare_other  # 其它福利
            cost_labor_share_other = obj.cost_labor_share_other  # 其它人力成本
            cost_other_inner_share = obj.cost_other_inner_share  # 部门其它成本
            share_donation = obj.share_donation  # 捐赠支出
            share_sponsor = obj.share_sponsor  # 赞助支出
            share_forfeit = obj.share_forfeit  # 罚款支出
            share_confiscate = obj.share_confiscate  # 没收支出
            share_bad_debt = obj.share_bad_debt  # 坏账损失
            share_abnormal_loss = obj.share_abnormal_loss  # 其它非常损失
            adjust_money_other = obj.adjust_money_other  # 其它绩效金额调整
            cost_platform_tax = obj.cost_platform_tax  # 平台扣税
            cost_platform_tax_pdd = obj.cost_platform_tax_pdd  # 拼多多税率
            cost_tax = obj.cost_tax  # 企业扣税
            added_normal_tax = obj.added_normal_tax  # 正常扣税
            added_allowance_tax = obj.added_allowance_tax  # 补贴扣税
            cost_tax_income = obj.cost_tax_income  # 企业所得税
            cost_tax_added_value = obj.cost_tax_added_value  # 企业增值税
            profit_aftertax = obj.profit_aftertax  # 税后毛利
            del_type = obj.del_type  # 明细类型
            is_scalper = obj.is_scalper  # 黄牛单标记
            state = obj.state  # 状态
            per_id_level_top_name = obj.per_id_level_top_name  # 一级负责人部门
            ranking_category = obj.ranking_category  # jd、天猫分类排行
            performance_share_cost = obj.performance_share_cost  # 绩效ABC分摊金额
            per_id_level_top_name_info = obj.per_id_level_top_name_info  # 一级部门负责人
            per_id_level_middle_name_info = obj.per_id_level_middle_name_info  # 二级部门负责人
            per_id_level_low_name = obj.per_id_level_low_name  # 三级部门负责人
            category = obj.three_category

            worksheet.write(row,0,snd_date)
            worksheet.write(row,1,venture_name)
            worksheet.write(row,2,trade_no)
            worksheet.write(row,3,trade_no2)
            worksheet.write(row,4,shop_type)
            worksheet.write(row,5,shop_name)
            worksheet.write(row,6,brand)
            worksheet.write(row,7,goods_name)
            worksheet.write(row,8,goods_no)
            worksheet.write(row,9,goods_count)
            worksheet.write(row,10,sales) #销售额
            worksheet.write(row,11,profit_purchase)

            if int(sales) != 0:
                worksheet.write(row,12,format(( profit_purchase/sales), '.2%')) #占比1
                worksheet.write(row,13,profit_add_allowance)
                worksheet.write(row,14,format((profit_add_allowance/sales), '.2%')) #占比2
                worksheet.write(row,15,profit_sales)
                worksheet.write(row,16,format((profit_sales/sales), '.2%')) #占比3
                worksheet.write(row,17,profit_aftersales)
                worksheet.write(row,18,format((profit_aftersales/sales), '.2%')) #占比4
                worksheet.write(row,19,profit_after_promotion)
                worksheet.write(row,20,format((profit_after_promotion/sales), '.2%')) #占比5
                worksheet.write(row,21,profit_after_humanresources)
                worksheet.write(row,22,format((profit_after_humanresources/sales), '.2%')) #占比6
                worksheet.write(row,23,profit_after_fund)
                worksheet.write(row,24,format((profit_after_fund/sales), '.2%')) #占比7
                worksheet.write(row,25,profit_after_expense)
                worksheet.write(row,26,format((profit_after_expense/sales), '.2%')) #占比8
                worksheet.write(row,27,profit_after_inner_cost)
                worksheet.write(row,28,format((profit_after_inner_cost/sales), '.2%')) #占比9
                worksheet.write(row,29,cost_office_share_other)
                worksheet.write(row,30,format((cost_office_share_other/sales), '.2%'))#占比10
            else:
                worksheet.write(row, 12,  '0.0%')  # 占比1
                worksheet.write(row, 13, profit_add_allowance)
                worksheet.write(row, 14, '0.0%')  # 占比2
                worksheet.write(row, 15, profit_sales)
                worksheet.write(row, 16, '0.0%')  # 占比3
                worksheet.write(row, 17, profit_aftersales)
                worksheet.write(row, 18, '0.0%')  # 占比4
                worksheet.write(row, 19, profit_after_promotion)
                worksheet.write(row, 20, '0.0%')  # 占比5
                worksheet.write(row, 21, profit_after_humanresources)
                worksheet.write(row, 22, '0.0%')  # 占比6
                worksheet.write(row, 23, profit_after_fund)
                worksheet.write(row, 24, '0.0%')  # 占比7
                worksheet.write(row, 25, profit_after_expense)
                worksheet.write(row, 26, '0.0%')  # 占比8
                worksheet.write(row, 27, profit_after_inner_cost)
                worksheet.write(row, 28, '0.0%')  # 占比9
                worksheet.write(row, 29, cost_office_share_other)
                worksheet.write(row, 30, '0.0%')  # 占比10

            worksheet.write(row,31,level_4) #四级负责人
            worksheet.write(row,32,'')
            worksheet.write(row,33,level_3)
            worksheet.write(row,34,'')
            worksheet.write(row,35,level_2)
            worksheet.write(row,36,'')

            worksheet.write(row, 37, cost_goods)
            worksheet.write(row, 38, rebate)
            worksheet.write(row, 39, price_pledge)
            worksheet.write(row, 40, cost_protect)
            worksheet.write(row, 41, platform_allowance)
            worksheet.write(row, 42, salse_refund)
            worksheet.write(row, 43, cost_gifts)
            worksheet.write(row, 44, cost_platform)
            worksheet.write(row, 45, cost_logistics)
            worksheet.write(row, 46, cost_aftersales)
            worksheet.write(row, 47, cost_promotion)
            worksheet.write(row, 48, cost_department)


            #zhouyue
            worksheet.write(row, 49, shop_id)
            worksheet.write(row, 50, xs_shop_id)
            worksheet.write(row, 51, sale_type)
            worksheet.write(row, 52, trade_nl)
            worksheet.write(row, 53, goods_id)
            worksheet.write(row, 54, goods_spu)
            worksheet.write(row, 55, class_name)
            worksheet.write(row, 56, goods_weight)
            worksheet.write(row, 57, logistic_id)
            worksheet.write(row, 58, logistic_name)
            worksheet.write(row, 59, warehouse_id)
            worksheet.write(row, 60, warehouse_name)
            worksheet.write(row, 61, goods_len)
            worksheet.write(row, 62, goods_width)
            worksheet.write(row, 63, goods_height)
            worksheet.write(row, 64, bar_code)
            worksheet.write(row, 65, g_brand)
            worksheet.write(row, 66, trade_amount)
            worksheet.write(row, 67, used_integral)
            worksheet.write(row, 68, rebate_delivery)
            worksheet.write(row, 69, rebate_volume)
            worksheet.write(row, 70, rebate_marketing)
            worksheet.write(row, 71, rebate_marketing_promotion)
            worksheet.write(row, 72, rebate_marketing_activity)
            worksheet.write(row, 73, rebate_out)
            worksheet.write(row, 74, rebate_other)
            worksheet.write(row, 75, price_pledge_stock)
            worksheet.write(row, 76, price_pledge_delivery)
            worksheet.write(row, 77, price_pledge_other)
            worksheet.write(row, 78, platform_allowance_pdd)
            worksheet.write(row, 79, platform_allowance_xiaomi)
            worksheet.write(row, 80, salse_refund_inorder)
            worksheet.write(row, 81, salse_refund_outorder)
            worksheet.write(row, 82, salse_refund_outorder_amount)
            worksheet.write(row, 83, salse_refund_outorder_cost)
            worksheet.write(row, 84, gifts_drainage)
            worksheet.write(row, 85, gifts_drainage_entity)
            worksheet.write(row, 86, gifts_drainage_entity_goods)
            worksheet.write(row, 87, gifts_drainage_entity_card)
            worksheet.write(row, 88, gifts_drainage_virtual_card)
            worksheet.write(row, 89, gifts_drainage_other)
            worksheet.write(row, 90, gifts_deal)
            worksheet.write(row, 91, gifts_drainage_entity)
            worksheet.write(row, 92, gifts_drainage_entity_goods)
            worksheet.write(row, 93, gifts_drainage_entity_card)
            worksheet.write(row, 94, gifts_drainage_virtual_card)
            worksheet.write(row, 95, gifts_drainage_other)
            worksheet.write(row, 96, gifts_repurchase)
            worksheet.write(row, 97, gifts_drainage_entity)
            worksheet.write(row, 98, gifts_drainage_entity_goods)
            worksheet.write(row, 99, gifts_drainage_entity_card)
            worksheet.write(row, 100, gifts_drainage_virtual_card)
            worksheet.write(row, 101, gifts_drainage_other)
            worksheet.write(row, 102, gifts_referral)
            worksheet.write(row, 103, gifts_drainage_entity)
            worksheet.write(row, 104, gifts_drainage_entity_goods)
            worksheet.write(row, 105, gifts_drainage_entity_card)
            worksheet.write(row, 106, gifts_drainage_virtual_card)
            worksheet.write(row, 107, gifts_drainage_other)
            worksheet.write(row, 108, gifts_others)
            worksheet.write(row, 109, profit_salse_minus)
            worksheet.write(row, 110, profit_salse_add)
            worksheet.write(row, 111, give_integral)
            worksheet.write(row, 112, cost_pdd_performance)
            worksheet.write(row, 113, cost_pdd_commission)
            worksheet.write(row, 114, cost_pdd_fenqi)
            worksheet.write(row, 115, cost_pdd_service)
            worksheet.write(row, 116, cost_pdd_commission_ddjb)
            worksheet.write(row, 117, cost_pdd_groupon)
            worksheet.write(row, 118, cost_pdd_groupon_out)
            worksheet.write(row, 119, iphone)
            worksheet.write(row, 120, cost_jd_performance)
            worksheet.write(row, 121, cost_jd_commission)
            worksheet.write(row, 122, cost_jd_jingdou)
            worksheet.write(row, 123, cost_jd_jingtiaoke)
            worksheet.write(row, 124, cost_jd_insurance_pop)
            worksheet.write(row, 125, cost_jd_baitiao)
            worksheet.write(row, 126, cost_pdd_service)
            worksheet.write(row, 127, cost_tb_performance)
            worksheet.write(row, 128, cost_tb_commission_tmall)
            worksheet.write(row, 129, cost_tb_service_cuntao)
            worksheet.write(row, 130, cost_tb_rebate_integral)
            worksheet.write(row, 131, cost_tb_ryt)
            worksheet.write(row, 132, cost_tb_mlt)
            worksheet.write(row, 133, cost_tb_publicgood)
            worksheet.write(row, 134, cost_tb_cuntao)
            worksheet.write(row, 135, cost_tb_insurance_transportation)
            worksheet.write(row, 136, cost_tb_instalment_huabei)
            worksheet.write(row, 137, cost_tb_huabei)
            worksheet.write(row, 138, cost_tb_credit_card)
            worksheet.write(row, 139, cost_tb_yitao)
            worksheet.write(row, 140, cost_pdd_service)
            worksheet.write(row, 141, cost_other_performance)
            worksheet.write(row, 142, cost_other_commission)
            worksheet.write(row, 143, cost_platform_tax_wx)
            worksheet.write(row, 144, cost_base_operation)
            worksheet.write(row, 145, cost_warehousing)
            worksheet.write(row, 146, cost_warehousing_pickup)
            worksheet.write(row, 147, cost_warehousing_added)
            worksheet.write(row, 148, cost_warehousing_arrange)
            worksheet.write(row, 149, cost_warehouse)
            worksheet.write(row, 150, cost_warehouse_external)
            worksheet.write(row, 151, cost_warehouse_cainiao)
            worksheet.write(row, 152, cost_warehouse_oruite)
            worksheet.write(row, 153, cost_warehouse_jd)
            worksheet.write(row, 154, cost_warehouse_internal)
            worksheet.write(row, 155, cost_warehouse_shanghai)
            worksheet.write(row, 156, cost_warehouse_yiwu)
            worksheet.write(row, 157, cost_sorting)
            worksheet.write(row, 158, cost_packing)
            worksheet.write(row, 159, cost_packing_operation)
            worksheet.write(row, 160, cost_packing_operation_notape)
            worksheet.write(row, 161, cost_packing_operation_tape)
            worksheet.write(row, 162, cost_packing_supplies)
            worksheet.write(row, 163, cost_packing_outer)
            worksheet.write(row, 164, cost_packing_carton)
            worksheet.write(row, 165, cost_packing_inner)
            worksheet.write(row, 166, cost_packing_bubble_cloumn)
            worksheet.write(row, 167, cost_packing_gourd_film)
            worksheet.write(row, 168, cost_packing_other)
            worksheet.write(row, 169, cost_express)
            worksheet.write(row, 170, cost_express_sto)
            worksheet.write(row, 171, cost_express_sto_shanghai)
            worksheet.write(row, 172, cost_express_sto_yiwu)
            worksheet.write(row, 173, cost_express_yuantong)
            worksheet.write(row, 174, cost_express_zto)
            worksheet.write(row, 175, cost_express_yunda)
            worksheet.write(row, 176, cost_express_sf)
            worksheet.write(row, 177, cost_express_flash)
            worksheet.write(row, 178, cost_express_nl)
            worksheet.write(row, 179, cost_express_self)
            worksheet.write(row, 180, cost_express_other)
            worksheet.write(row, 181, cs_perfomance)
            worksheet.write(row, 182, cs_perfomance_bonus)
            worksheet.write(row, 183, cost_aftersales_deal)
            worksheet.write(row, 184, cost_aftersales_compensation_cash)
            worksheet.write(row, 185, cost_aftersales_repair)
            worksheet.write(row, 186, cost_aftersales_express)
            worksheet.write(row, 187, cost_aftersales_damage)
            worksheet.write(row, 188, cost_aftersales_other)
            worksheet.write(row, 189, promotion_pdd)
            worksheet.write(row, 190, promotion_pdd_recharge)
            worksheet.write(row, 191, promotion_pdd_materiel)
            worksheet.write(row, 192, cost_express_other)
            worksheet.write(row, 193, promotion_jd)
            worksheet.write(row, 194, promotion_jd_kc)
            worksheet.write(row, 195, promotion_jd_cd)
            worksheet.write(row, 196, promotion_jd_ht)
            worksheet.write(row, 197, promotion_jd_jzt)
            worksheet.write(row, 198, promotion_pdd_materiel)
            worksheet.write(row, 199, cost_express_other)
            worksheet.write(row, 200, promotion_tb)
            worksheet.write(row, 201, promotion_tb_ztc)
            worksheet.write(row, 202, promotion_tb_pxb)
            worksheet.write(row, 203, promotion_tb_jewel)
            worksheet.write(row, 204, promotion_tb_superrecommend)
            worksheet.write(row, 205, promotion_tb_new)
            worksheet.write(row, 206, promotion_tb_tbk)
            worksheet.write(row, 207, promotion_tb_back_card)
            worksheet.write(row, 208, promotion_tb_tools)
            worksheet.write(row, 209, promotion_pdd_materiel)
            worksheet.write(row, 210, promotion_tb_celebrity)
            worksheet.write(row, 211, cost_express_other)
            worksheet.write(row, 212, other_promotion)
            worksheet.write(row, 213, cost_human_resources_level_1)
            worksheet.write(row, 214, cost_human_resources_level_2)
            worksheet.write(row, 215, cost_human_resources_level_3)
            worksheet.write(row, 216, cost_human_resources_operating)
            worksheet.write(row, 217, cost_human_resources_cs)
            worksheet.write(row, 218, cs_base_wage)
            worksheet.write(row, 219, cs_social_insurance)
            worksheet.write(row, 220, cs_accumulation_fund)
            worksheet.write(row, 221, cs_welfare)
            worksheet.write(row, 222, cs_commuting_subsidy)
            worksheet.write(row, 223, cs_accommodation_subsidy)
            worksheet.write(row, 224, cs_communication_subsidy)
            worksheet.write(row, 225, cs_dinner_subsidy)
            worksheet.write(row, 226, cs_team_construction_subsidy)
            worksheet.write(row, 227, cs_insurance_supply)
            worksheet.write(row, 228, cs_physical_examination)
            worksheet.write(row, 229, cs_welfare_other)
            worksheet.write(row, 230, cost_human_resources_anchor)
            worksheet.write(row, 231, anchor_base_wage)
            worksheet.write(row, 232, anchor_perfomance)
            worksheet.write(row, 233, cs_social_insurance)
            worksheet.write(row, 234, cs_accumulation_fund)
            worksheet.write(row, 235, anchor_welfare)
            worksheet.write(row, 236, cs_commuting_subsidy)
            worksheet.write(row, 237, cs_accommodation_subsidy)
            worksheet.write(row, 238, cs_communication_subsidy)
            worksheet.write(row, 239, cs_dinner_subsidy)
            worksheet.write(row, 240, cs_team_construction_subsidy)
            worksheet.write(row, 241, cs_insurance_supply)
            worksheet.write(row, 242, cs_physical_examination)
            worksheet.write(row, 243, cs_welfare_other)
            worksheet.write(row, 244, anchor_equipment)
            worksheet.write(row, 245, anchor_microphone)
            worksheet.write(row, 246, anchor_lighting)
            worksheet.write(row, 247, anchor_camera)
            worksheet.write(row, 248, anchor_ktboard)
            worksheet.write(row, 249, anchor_equipment_other)
            worksheet.write(row, 250, cost_human_resources_aftersales)
            worksheet.write(row, 251, cost_human_resources_other)
            worksheet.write(row, 252, cost_human_resources_purchase_director)
            worksheet.write(row, 253, cs_company_subsidy)
            worksheet.write(row, 254, cost_fund_interest)
            worksheet.write(row, 255, cost_loan_interest)
            worksheet.write(row, 256, cost_service_charge)
            worksheet.write(row, 257, cost_fund_occupation)
            worksheet.write(row, 258, cost_interest_other)
            worksheet.write(row, 259, expense_department_entertainment)
            worksheet.write(row, 260, expense_travel)
            worksheet.write(row, 261, expense_entertainment)
            worksheet.write(row, 262, expense_gifts)
            worksheet.write(row, 263, expense_department_entertainment_other)
            worksheet.write(row, 264, expense_department_share)
            worksheet.write(row, 265, expense_travel_operating_share)
            worksheet.write(row, 266, expense_miscellaneous)
            worksheet.write(row, 267, expense_depreciation_facilities)
            worksheet.write(row, 268, expense_additional_tax)
            worksheet.write(row, 269, expense_insurance)
            worksheet.write(row, 270, cost_express_other)
            worksheet.write(row, 271, expense_storage_loss_share)
            worksheet.write(row, 272, loss_provision)
            worksheet.write(row, 273, damage_provision)
            worksheet.write(row, 274, overstocking_provision)
            worksheet.write(row, 275, expense_information_share)
            worksheet.write(row, 276, expense_computer_hardware)
            worksheet.write(row, 277, expense_computer_accessories)
            worksheet.write(row, 278, expense_software)
            worksheet.write(row, 279, expense_communication)
            worksheet.write(row, 280, expense_network_broadband)
            worksheet.write(row, 281, expense_cloud_services)
            worksheet.write(row, 282, cost_inner)
            worksheet.write(row, 283, cost_office_share)
            worksheet.write(row, 284, share_office_supplies)
            worksheet.write(row, 285, share_stationery_procurement)
            worksheet.write(row, 286, share_printing_equipment)
            worksheet.write(row, 287, share_printing_paper)
            worksheet.write(row, 288, share_ink)
            worksheet.write(row, 289, share_other_supplies)
            worksheet.write(row, 290, cost_site)
            worksheet.write(row, 291, share_rent)
            worksheet.write(row, 292, share_water)
            worksheet.write(row, 293, share_electricity)
            worksheet.write(row, 294, share_house_decoration)
            worksheet.write(row, 295, share_house_maintenance)
            worksheet.write(row, 296, share_daily_cleaning)
            worksheet.write(row, 297, share_garbage_disposal)
            worksheet.write(row, 298, share_air_conditioning_lighting_equipment_loss)
            worksheet.write(row, 299, share_other_energy)
            worksheet.write(row, 300, cost_working_dress)
            worksheet.write(row, 301, dress_frock)
            worksheet.write(row, 302, dress_work_license)
            worksheet.write(row, 303, dress_other)
            worksheet.write(row, 304, cost_other_consumables)
            worksheet.write(row, 305, share_tables_chairs)
            worksheet.write(row, 306, share_fan)
            worksheet.write(row, 307, share_drinking)
            worksheet.write(row, 308, share_snack)
            worksheet.write(row, 309, share_sanitary_products)
            worksheet.write(row, 310, share_first_aid_medicine)
            worksheet.write(row, 311, share_epidemic_prevention_supplies)
            worksheet.write(row, 312, share_other_consumables)
            worksheet.write(row, 313, cost_labor_share)
            worksheet.write(row, 314, share_staff_wage)
            worksheet.write(row, 315, share_staff_base_wage)
            worksheet.write(row, 316, share_staff_performance_wage)
            worksheet.write(row, 317, share_staff_bonus)
            worksheet.write(row, 318, share_staff_susidy)
            worksheet.write(row, 319, share_staff_social_insurance)
            worksheet.write(row, 320, share_staff_accumulation_fund)
            worksheet.write(row, 321, share_staff_welfare)
            worksheet.write(row, 322, cs_commuting_subsidy)
            worksheet.write(row, 323, cs_accommodation_subsidy)
            worksheet.write(row, 324, cs_communication_subsidy)
            worksheet.write(row, 325, cs_dinner_subsidy)
            worksheet.write(row, 326, cs_team_construction_subsidy)
            worksheet.write(row, 327, cs_insurance_supply)
            worksheet.write(row, 328, cs_physical_examination)
            worksheet.write(row, 329, cs_welfare_other)
            worksheet.write(row, 330, cost_labor_share_other)
            worksheet.write(row, 331, cost_other_inner_share)
            worksheet.write(row, 332, share_donation)
            worksheet.write(row, 333, share_sponsor)
            worksheet.write(row, 334, share_forfeit)
            worksheet.write(row, 335, share_confiscate)
            worksheet.write(row, 336, share_bad_debt)
            worksheet.write(row, 337, share_abnormal_loss)
            worksheet.write(row, 338, adjust_money_other)
            worksheet.write(row, 339, cost_platform_tax)
            worksheet.write(row, 340, cost_platform_tax_pdd)
            worksheet.write(row, 341, cost_tax)
            worksheet.write(row, 342, added_normal_tax)
            worksheet.write(row, 343, added_allowance_tax)
            worksheet.write(row, 344, cost_tax_income)
            worksheet.write(row, 345, cost_tax_added_value)
            worksheet.write(row, 346, profit_aftertax)
            worksheet.write(row, 347, del_type)
            worksheet.write(row, 348, is_scalper)
            worksheet.write(row, 349, state)
            worksheet.write(row, 350, per_id_level_top_name)
            worksheet.write(row, 351, ranking_category)
            worksheet.write(row, 352, performance_share_cost)
            worksheet.write(row, 353, per_id_level_top_name_info)
            worksheet.write(row, 354, per_id_level_middle_name_info)
            worksheet.write(row, 355, per_id_level_low_name)
            worksheet.write(row, 356, category)
            if profit_after_inner_cost > 0:
                worksheet.write(row, 357, '盈利订单')
            else:
                worksheet.write(row, 357, '亏损订单')



            row += 1









