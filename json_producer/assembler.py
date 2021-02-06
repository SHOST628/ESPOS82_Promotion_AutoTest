from util.oracle import oracle
from json_producer.salesitem_producer import produce_items
from json_producer.base_json_compare import compare_json_key
from json_producer.base_json_compare import model_base_json_path
from json_producer.salestotal_producer import produce_salestotal_vip
from util.readconfig import br_method_id
from util.readconfig import bl_method_id
from util.readconfig import dis_method_id
from util.readconfig import apply_serail
from util.readconfig import is_checked
from util.readconfig import base_json as bjson
from param_parser.param_parser import to_dict
from param_parser.param_parser import get_param_to_dict
from param_parser.param_parser import REQUEST
from json import dumps as json_dumps
from util.mylogger import logger


class Units:
    def __init__(self, test_cls, testcase):
        self.cls = test_cls
        self.testcase = testcase

    def base(self):
        """
        to produce a base request json
        :return dict base_json
        """
        # TODO 普通促销需要加上 VIP 信息
        if self.testcase == []:
            self.cls.skipTest('没有找到测试用例')
        # TODO 加入异常处理
        # bjson = readconfig.config.get('JsonModel', 'BaseJson')
        base_json_dict = compare_json_key(self.cls, bjson, model_base_json_path)
        sales_item = produce_items(self.cls, self.testcase)
        base_json_dict['salesData']['salesItem'] = sales_item
        # base_request_json = json_dumps(base_request_json, indent=4)
        logger.debug('generate base json: \n {} '.format(base_json_dict))
        return base_json_dict

    def param_xe(self, base_json):
        """
        promoid: PEOHQO201100036
        【request】
            "salesTotal": {
                "customerCode": "NV02D0130120000007",
                "bonusBalance": [
                    {
                        "vipGradeCenter": "*",
                        "vipBonusCenter": "*"
                    }
                ]
            }

        salesData 下：
        "vipGradeCenter": [
            "*"
        ],
        "vipBonusCenter": "*"
        =================================
        [TESTCASE] VIPINFO:  customerCode=NV02D0130120000006,vipGradeCenter=*,vipBonusCenter=*  (including these columns)
        """
        salestotal_vip = produce_salestotal_vip(self.cls, self.testcase)
        base_json['salesData'].update(salestotal_vip)
        return base_json

    def param_br(self, base_json):
        """
            是否加入XE 参数
            promid: PEOHQO201100039
            【request】
            "reqPromBonusRedeem": {
                "method": 2,
                "details": [
                    {
                        "gradeCenter": "*",
                        "bonusCenter": "*",
                        "bonus": 90160
                    }
                ]
            }
        =====================================
        [TestCase] PROMPARAM_BR:  bonus=90160
        """
        if br_method_id == '':
            self.cls.skipTest('请补全config [PromParams] 下 BRMethodId 的信息')
        base_json = self.param_xe(base_json)
        vipinfo = None
        promparam_br = get_param_to_dict(self.cls, 'PROMPARAM_BR', self.testcase, REQUEST, 'bonus')
        for row in self.testcase:
            if row['VIPINFO'] is not None:
                vipinfo = to_dict(self.cls, 'VIPINFO', row['VIPINFO'])
                break
        bonus_redeem_value = {'method': 0, 'details': []}
        req_prombonus_redeem = {'reqPromBonusRedeem': {}}
        bonus_redeem_value['method'] = br_method_id
        detail = {'gradeCenter': '', 'bonusCenter': '', 'bonus': 0}
        detail['gradeCenter'] = vipinfo['vipgradecenter']
        detail['bonusCenter'] = vipinfo['vipbonuscenter']
        detail['bonus'] = int(promparam_br['request']['bonus'])
        bonus_redeem_value['details'].append(detail)
        req_prombonus_redeem['reqPromBonusRedeem'] = bonus_redeem_value
        base_json.update(req_prombonus_redeem)
        return base_json

    def param_bl(self, base_json):
        # TODO 确认 items 是否会有多个货品信息 ？？？
        """
            promid: PEOHQO201100039 ???
            promid: Quota
            加入XE参数
            【request】
            "reqPromQuota": [
                {
                    "promId": "PEOHQO201100034",
                    "promMethodId": "1",
                    "items": [
                        {
                            "itemIndex": 0,
                            "useQty": 1
                        }
                    ]
                }
            ]
        ==========================================
        [TestCase] PROMPARAM_BL : promId=PEOHQO201100034,itemIndex=0,useQty=1
        """
        if bl_method_id == '':
            self.cls.skipTest('请补全config [PromParams] 下 BLMethodId 的信息')
        base_json = self.param_xe(base_json)
        promparam_bl = get_param_to_dict(self.cls, 'PROMPARAM_BL', self.testcase, REQUEST, 'promid', 'itemindex', 'useqty')
        req_prom_quotas = {'reqPromQuota':[]}
        req_prom_quota = {'promId': '', 'promMethodId': '', 'items': []}
        item = {'itemIndex': 0, 'useQty': 0}
        item['itemIndex'] = int(promparam_bl['request']['itemindex'])
        item['useQty'] = int(promparam_bl['request']['useqty'])
        req_prom_quota['items'].append(item)
        req_prom_quota['promId'] = promparam_bl['request']['promid']
        req_prom_quota['promMethodId'] = bl_method_id
        req_prom_quotas['reqPromQuota'].append(req_prom_quota)
        base_json.update(req_prom_quotas)
        return base_json

    # TODO 确认 pkgItems 是否有多个
    def param_dis(self, base_json):
        """
            【Demo request salesTotal】
            "reqDiscOneItemUserSelect": [
                {
                    "promId": "PEOHQO200900006",
                    "promMethodId": "1",
                    "selectedPromPackages": [
                        {
                            "applySerail": 1,
                            "pkgItems": [
                                {
                                    "itemCode": "DS016",
                                    "itemOrgId": "000000",
                                    "lessItemIndexs": [
                                        {
                                            "lessItemIndex": 0,
                                            "useQty": 1
                                        }
                                    ],
                                    "pkgQty": 1,
                                    "isChecked": true
                                }
                            ]
                        }
                    ]
                }
            ]
        =====================================
        [TestCase] PROMPARAM_DIS : promId=PEOHQO200900006,lessItemIndex=DS016,useQty=1,pkgQty=1
        """
        if dis_method_id == '':
            self.cls.skipTest('请补全config [PromParams] 下 DISMethodId 的信息')
        elif apply_serail == '':
            self.cls.skipTest('请补全config [reqDiscOneItemUserSelectDefault] 下 applySerail 的信息')
        elif is_checked == '':
            self.cls.skipTest('请补全config [reqDiscOneItemUserSelectDefault] 下 isChecked 的信息')
        _apply_serail = int(apply_serail)
        _is_checked = bool(is_checked)
        if self.testcase == []:
            self.cls.skipTest('找不到TestCase数据')
        promparam_dis = get_param_to_dict(self.cls, 'PROMPARAM_DIS', self.testcase, REQUEST, 'promid', 'lessitemindex', 'useqty', 'pkgqty')
        req_disc_one_item_user_select = {'reqDiscOneItemUserSelect': []}
        req_disc_one_item = {'promId': '', 'promMethodId': '', 'selectedPromPackages': []}
        req_disc_one_item['promId'] = promparam_dis['request']['promid']
        req_disc_one_item['promMethodId'] = dis_method_id
        selectedPromPackage = {'applySerail': 0, 'pkgItems': []}
        selectedPromPackage['applySerail'] = _apply_serail
        pkgItem = {'itemCode': '', 'itemOrgId': '', 'lessItemIndexs': [], 'pkgQty':0, 'isChecked': True}
        less_item_index = int(promparam_dis['request']['lessitemindex'])
        itemcode = self.testcase[less_item_index]['ITEMCODE']
        item_orgid = oracle.select("select xf_itemorgid from xf_itemmas where xf_style = '{}'".format(itemcode))
        if item_orgid == []:
            self.cls.skipTest('请检查 itemcode: {} 是否正确'.format(itemcode))
        else:
            item_orgid = item_orgid[0][0]
        pkgItem['itemCode'] = itemcode
        pkgItem['itemOrgId'] = item_orgid
        pkgItem['pkgQty'] = int(promparam_dis['request']['pkgqty'])
        pkgItem['isChecked'] = _is_checked
        lessItemIndex = {'lessItemIndex': 0, 'useQty': 0}
        lessItemIndex['lessItemIndex'] = less_item_index
        lessItemIndex['useQty'] = int(promparam_dis['request']['useqty'])
        pkgItem['lessItemIndexs'].append(lessItemIndex)
        selectedPromPackage['pkgItems'].append(pkgItem)
        req_disc_one_item['selectedPromPackages'].append(selectedPromPackage)
        req_disc_one_item_user_select['reqDiscOneItemUserSelect'].append(req_disc_one_item)
        base_json.update(req_disc_one_item_user_select)
        return base_json


class Assembler:
    def __init__(self, test_cls, testcase, common_params):
        self.unit = Units(test_cls, testcase)
        self.common_params = ['param_{}'.format(param.lower()) for param in common_params]

    def assemble(self):
        """
        according to different params to find self method to control
        """
        self_json = self.unit.base()
        for param in self.common_params:
            func = getattr(self.unit, param)
            self_json = func(self_json)
        self_json = json_dumps(self_json, indent=4)
        logger.info('Generate request json: \n {}'.format(self_json))
        return self_json

