from util.oracle import oracle
from util.logger import logger
from util.readconfig import invt_type, price_mode, disc_mode, disc_value, itemlot_num
import re


def _items(test_cls, row_dict, row_no):
    # TODO 参数不配置时，不发送request
    if invt_type == '' or price_mode == '' or disc_mode == '' or disc_value == '' or itemlot_num == '':
        test_cls.skipTest('请检查config 配置中 [PromSalesItemDefault] 下的 invt_type, price_mode, disc_mode, dis_value 是否配置')
    item = {}
    # prom_id = row_dict['PROMID']
    item_code = row_dict['ITEMCODE']
    itemmas_sql = "select * from xf_itemmas where xf_style = '{}'".format(item_code)
    itemmas = oracle.dict_fetchall(itemmas_sql)
    if itemmas == []:
        test_cls.skipTest('【TESTCASE {}】 中查无此货品: {}'.format(row_dict['TESTCASEID'], item_code))
    itemmas = itemmas[0]
    item_std_price_sql = "select * from xf_itemstdprice where xf_style = '{}' order by XF_LASTMODTIME desc".format(item_code)
    item_std_price = oracle.dict_fetchall(item_std_price_sql)[0]
    column_group_list = []
    column_group_sql = "select COLUMN_NAME from user_tab_columns where TABLE_NAME='XF_ITEMMAS' and COLUMN_NAME LIKE 'XF_GROUP%'"
    column_groups = oracle.select(column_group_sql)
    for s in column_groups:
        column_group_list.append(s[0])
    column_group = ','.join(column_group_list)
    group_sql = "select {} from xf_itemmas where xf_style = '{}'".format(column_group, item_code)
    group_dict_ = oracle.dict_fetchall(group_sql)[0]
    group_dict = {}
    for k, v in group_dict_.items():
        k = re.sub(r'xf_', '', k.lower())
        group_dict[k] = v
    item['lineNumber'] = row_no + 1
    item['itemOrgId'] = itemmas['XF_ITEMORGID']
    item['itemCode'] = item_code
    item['itemLotNum'] = '*'  # TODO CONFIRM
    item['plu'] = itemmas['XF_STYLE']
    item['color'] = None  # TODO 后期加入color 和 size
    item['size'] = None  # TODO 后期加入color 和 size
    item['minPrice'] = item_std_price['XF_MINPRICE']
    item['maxPrice'] = item_std_price['XF_MAXPRICE']
    item['originalPrice'] = row_dict['ORIGINALPRICE']
    item['currSellingPrice'] = row_dict['CURRSELLINGPRICE']
    # item['currAltPrice'] = item_std_price['XF_ALTPRICE']
    # item['salesExclusive'] = None
    item.update(group_dict)
    item['invtType'] = int(invt_type)
    item['itemOption'] = itemmas['XF_ITEMOPTION']
    # salesMode deprecated
    # if prom_id is None or prom_id == '':
    #     item['salesMode'] = 3
    # else:
    #     prom_item_sql = "select xf_salesmode from xf_promitem where xf_promid = '{}'".format(prom_id)
    #     prom_item = oracle.dict_fetchall(prom_item_sql)
    #     if prom_item == []:
    #         item['salesMode'] = 3  #
    #     else:
    #         item['salesMode'] = prom_item['XF_SALESMODE']
    item['unitPrice'] = row_dict['UNITPRICE']
    item['qty'] = row_dict['QTY']
    item['amount'] = row_dict['UNITPRICE'] * row_dict['QTY']
    item['priceMode'] = price_mode
    item['discMode'] = disc_mode
    item['discValue'] = int(disc_value)
    return item


def produce_items(test_cls,testcase):
    """
    product item information list for
    {
    "validateOption": 0,
    "salesData":{
        "salesItem":[],
    },
    :param testcaseid:
    :return:
    """
    sales_item = []
    for i,item_row in enumerate(testcase):
        item = _items(test_cls, item_row, i)  # one row
        sales_item.append(item)
    return sales_item