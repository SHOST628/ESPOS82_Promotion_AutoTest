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
from util.readconfig import kp_method_id
from util.readconfig import gt_method_id
from util.readconfig import nc_method_id
from util.readconfig import base_json as bjson
from util.param_parser.param_parser import to_dict
from util.param_parser.param_parser import get_param_to_dict
from util.param_parser.param_parser import REQUEST
from json import dumps as json_dumps
from util.mylogger import logger
from util.readconfig import request_now
from datetime import datetime
import re


class Units:
    def __init__(self, test_cls, testcase):
        self.cls = test_cls
        self.testcase = testcase
        # to check the data if True
        self.flag = True
        for i, case in enumerate(self.testcase):
            if case['PROMLESSDETAIL'] is not None and case['PROMLESSDETAIL'].strip() != '':
                break
            else:
                if i == len(self.testcase) - 1:
                    self.flag = False

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
        if request_now.isdigit():
            request_now_ = int(request_now)
            if request_now_:
                now = datetime.now()
                cur_date = now.strftime('%Y-%m-%d')
                cur_time = now.strftime('%H%M')
                cur_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
                base_json_dict['salesData']['workingDate'] = cur_date
                base_json_dict['salesData']['workingTime'] = cur_time
                base_json_dict['repositoryDatetime'] = cur_datetime
        else:
            self.cls._testMethodDoc += "<br><font color='red' style='font-weight:bold'>confit.ini 中 " \
                                       "[JsonConfig]下的RequstNow 请正确配置，值只填0或1</font>"
            self.cls.skipTest('confit.ini 中 [JsonConfig]下的RequstNow 请正确配置，值只填0或1')
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
        if self.flag:
            if br_method_id == '':
                self.cls.skipTest('请补全config [PromParams] 下 BRMethodId 的信息')
            # base_json = self.param_xe(base_json)
            vipinfo = None
            promparam_brs = get_param_to_dict(self.cls, 'PROMPARAM_BR', self.testcase, REQUEST, 'bonus')
            promparam_br = None
            for pb in promparam_brs:
                if pb['request'] is not None:
                    promparam_br = pb
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
        else:
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
        if self.flag:
            if bl_method_id == '':
                self.cls.skipTest('请补全config [PromParams] 下 BLMethodId 的信息')
            promparam_bls = get_param_to_dict(self.cls, 'PROMPARAM_BL', self.testcase, REQUEST, 'promid', 'itemindex', 'useqty')
            promparam_bl = []
            for pb in promparam_bls:
                if pb['request'] is not None:
                    promparam_bl.append(pb)
            req_prom_quotas = {'reqPromQuota': []}
            req_prom_quota = {'promId': '', 'promMethodId': '', 'items': []}
            # solve the problem that quota multi items
            for i, bl in enumerate(promparam_bl):
                item = {'itemIndex': 0, 'useQty': 0}
                req_prom_quota['promId'] = bl['request']['promid']
                req_prom_quota['promMethodId'] = bl_method_id
                item['itemIndex'] = int(bl['request']['itemindex'])
                item['useQty'] = int(bl['request']['useqty'])
                if i == 0:
                    req_prom_quota['items'].append(item)
                    req_prom_quotas['reqPromQuota'].append(req_prom_quota)
                else:
                    if req_prom_quotas['reqPromQuota'] != []:
                        for prom_quota in req_prom_quotas['reqPromQuota']:
                            if req_prom_quota['promId'] == prom_quota['promId']:
                                # req_prom_quotas['reqPromQuota']['']
                                prom_quota['items'].append(item)
                                break
                            else:
                                req_prom_quota['items'].append(item)
                                req_prom_quotas['reqPromQuota'].append(req_prom_quota)
                                break
                    # req_prom_quota['items'].append(item)
                # req_prom_quotas['reqPromQuota'].append(req_prom_quota)
            base_json.update(req_prom_quotas)
            return base_json
        else:
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
        [TestCase] PROMPARAM_DIS : promId=PEOHQO200900006,lessItemIndex=0,useQty=1,pkgQty=1
        """
        # -DIS 参数的case，如果不传入对应需要的参数，促销服务器会奔溃
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
        promparam_diss = get_param_to_dict(self.cls, 'PROMPARAM_DIS', self.testcase, REQUEST, 'promid', 'lessitemindex', 'useqty', 'pkgqty')
        promparam_dis = None
        for pd in promparam_diss:
            if pd['request'] is not None:
                promparam_dis = pd
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
            self.cls._testMethodDoc += "<br><font color='red' style='font-weight:bold'> 请检查 itemcode: {} 是否正确 </font>".format(itemcode)
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

    def param_kp(self, base_json):
        """
        "reqPromKeys": [
        {
            "promId": "PEOHQO210200003",
            "promMethodId": "1",
            "keyCode": "HQ20210201"
        }]

        ==========================
        [TestCase]
        1.PROMPARAM_KDKP : promId=PEOHQO200900006,promMethodId=1,keyCode=HQ20210201
        2.PROMPARAM_KDKP : promKeyCode=HQ20210201  (salesitem)
        """
        if self.flag:
            if kp_method_id == '':
                self.cls.skipTest('请补全config [PromParams] 下 KPMethodId 的信息')
            promparam_kps = None
            testcase_desci = "<br><font color='red' style='font-weight:bold'>" \
                             "请补全testcase中PROMPARAM_KDKP下的 keycode或 promid和keycode的信息</font>"
            info = '请补全testcase中PROMPARAM_KDKP下的 keycode 或 promid和keycode的信息'
            Flag = False
            for i, case in enumerate(self.testcase):
                if case['PROMPARAM_KDKP'] is not None:
                    if len(re.findall(r'\bpromid\b|\bkeycode\b', case['PROMPARAM_KDKP'], re.IGNORECASE)) == 2:
                        Flag = True
                        promparam_kps = get_param_to_dict(self.cls, 'PROMPARAM_KDKP', self.testcase,
                                                          REQUEST, 'promid','keycode')
                        break
                    elif len(re.findall(r'\bpromkeycode\b', case['PROMPARAM_KDKP'], re.IGNORECASE)) == 1:
                        promparam_kps = get_param_to_dict(self.cls, 'PROMPARAM_KDKP', self.testcase,
                                                          REQUEST, 'promkeycode')
                        break
                    else:
                        if i == len(self.testcase) - 1:
                            self.cls._testMethodDoc += testcase_desci
                            self.cls.skipTest(info)
                else:
                    if i == len(self.testcase) - 1:
                        self.cls._testMethodDoc += testcase_desci
                        self.cls.skipTest(info)
            if Flag:
                req_promkeys = {'reqPromKeys': []}
                req_promkey = {'promId': '', 'promMethodId': '', 'keyCode': ''}
                for pb in promparam_kps:
                    if pb['request'] is not None:
                        req_promkey['promId'] = pb['request']['promid']
                        req_promkey['promMethodId'] = pb['request']['prommethodid']
                        req_promkey['keyCode'] = pb['request']['keycode']
                        req_promkeys['reqPromKeys'].append(req_promkey)
                    else:
                        pass
                base_json.update(req_promkeys)
                return base_json
            else:
                for i, pb in enumerate(promparam_kps):
                    if pb['request'] is not None:
                        keycode = {'promKeyCode': ''}
                        keycode['promKeyCode'] = pb['request']['promkeycode']
                        base_json['salesData']['salesItem'][i].update(keycode)
                    else:
                        pass
                return base_json
        else:
            return base_json

    def param_gt(self, base_json):
        """
            "reqGiftUserInput": [{
                "promId": "PEOHQO201100015",
                "promMethodId": "1"
            }]

        =====================================
        [TestCase] PROMPARAM_GT : promId=PEOHQO201100015
        """
        if self.flag:
            promid_dict = get_param_to_dict(self.cls, 'PROMPARAM_GT', self.testcase, REQUEST, 'promid')
            req_gift_user_input_dict = {'reqGiftUserInput':[]}
            req_gitf_user_inputs = []
            # to tag PROMPARAM_GT whether it is None
            PROMPARAM_GT_FLAG = True
            for promid_d in promid_dict:
                if promid_d['request'] is None:
                    pass
                else:
                    PROMPARAM_GT_FLAG = False
                    req_gitf_user_input = {}
                    requests = promid_d['request']
                    for req in requests:
                        req_gitf_user_input.update(req)
                        req_gitf_user_input['promMethodId'] = gt_method_id
                        req_gitf_user_inputs.append(req_gitf_user_input)
            # if no promid is including in PROMPARAM_GT, skip this testcase
            if PROMPARAM_GT_FLAG:
                for i, case in enumerate(self.testcase):
                    if case['PROMLESSDETAIL'] is None or case['PROMLESSDETAIL'].strip() == '':
                        pass
                    else:
                        self.cls._testMethodDoc += "<br><font color='red' style='font-weight:bold'> TESTCASE 下" \
                        "【PROMPARAM_GT】缺少promId数据</font>"
                        self.cls.skipTest('TESTCASE 下【PROMPARAM_GT】缺少promId数据')
            req_gift_user_input_dict['reqGiftUserInput'] = req_gitf_user_inputs
            base_json.update(req_gift_user_input_dict)
            return base_json
        else:
            return base_json

    def param_nc(self, base_json):
        """
            "reqPromCouponSettle": {
            "method": 3,
            "coupons": [{
                "batchNo": "HQ002",
                "cpNo": "0CF0B21002040100004239",
                "qty": 1,
                "batchDesci": "消费满500可得印花一枚，累计10个印花换礼品"
            }, {
                "batchNo": "HQ002",
                "cpNo": "0CF0B21002230100004375",
                "qty": 1,
                "batchDesci": "消费满500可得印花一枚，累计10个印花换礼品"
            }
            }]
        ================================
        PROMPARAM_NC : batchNo=HQ001,cpNo=0HQOO0001D710010000042,qty=1#batchNo=HQ001,cpNo=0HQOO0001D710010000145,qty=1;
        "#" 分隔符，如果 batchNo=HQ001,cpNo=0HQOO0001D710010000042,qty=1 有多个这样的组合，需要使用 '#' 分隔符分开，如果只有一个组合
        则不需要分隔符 #
        """
        if self.flag:
            if nc_method_id == '':
                self.cls.skipTest('请补全config [PromParams] 下 NCMethodId 的信息')
            promparam_ncs = None
            testcase_desci = "<br><font color='red' style='font-weight:bold'>" \
                             "请补全testcase中PROMPARAM_NC下的 batchNo、cpNo、qty的信息</font>"
            info = '请补全testcase中PROMPARAM_NC下的 batchNo、cpNo、qty的信息'
            Flag = False
            for i, case in enumerate(self.testcase):
                if case['PROMPARAM_NC'] is not None:
                    if len(re.findall(r'\bbatchno\b|\bcpno\b|\bqty\b', case['PROMPARAM_NC'], re.IGNORECASE)) >= 3:
                        promparam_ncs = get_param_to_dict(self.cls, 'PROMPARAM_NC', self.testcase,
                                                          REQUEST, 'batchno','cpno','qty')
                        break
                    else:
                        if i == len(self.testcase) - 1:
                            self.cls._testMethodDoc += testcase_desci
                            self.cls.skipTest(info)
                else:
                    if i == len(self.testcase) - 1:
                        self.cls._testMethodDoc += testcase_desci
                        self.cls.skipTest(info)
            for promparam_nc in promparam_ncs:
                if promparam_nc['request'] is None:
                    pass
                else:
                    Flag = True
                    req_prom_coupon_settle_dict = {'reqPromCouponSettle':{'method': nc_method_id, 'coupons': None}}
                    coupons = []
                    if type(promparam_nc['request']) is list:
                        for prom_param in promparam_nc['request']:
                            coupon = {'batchNo': None, 'cpNo': None, 'qty': None}
                            coupon['batchNo'] = prom_param['batchno']
                            coupon['cpNo'] = prom_param['cpno']
                            coupon['qty'] = prom_param['qty']
                            coupons.append(coupon)
                    elif type(promparam_nc['request']) is dict:
                        coupon = {'batchNo': None, 'cpNo': None, 'qty': None}
                        prom_param = promparam_nc['request']
                        coupon['batchNo'] = prom_param['batchno']
                        coupon['cpNo'] = prom_param['cpno']
                        coupon['qty'] = prom_param['qty']
                    req_prom_coupon_settle_dict['reqPromCouponSettle']['coupons'] = coupons
                    base_json.update(req_prom_coupon_settle_dict)
                    break
            if Flag:
                pass
            else:
                self.cls.skipTest(info)
            return base_json
        else:
            return base_json
    # todo to confirm request param
    def param_xc(self, base_json):
        """

        """
        return base_json

    def param_xg(self, base_json):
        """
        It's no need to add new param to request
        """
        return base_json

    def param_xp(self, base_json):
        """
        It's no need to add new param to request
        """
        return base_json

    # vip exists or not exists
    def param_bc_bx(self, base_json):
        salestotal_vip = produce_salestotal_vip(self.cls, self.testcase, 0)
        if salestotal_vip is None:
            return base_json
        else:
            base_json['salesData'].update(salestotal_vip)
            return base_json

    def param_bc(self, base_json):
        if self.flag:
            salestotal_vip = produce_salestotal_vip(self.cls, self.testcase, 1)
            base_json['salesData'].update(salestotal_vip)
        else:
            salestotal_vip = produce_salestotal_vip(self.cls, self.testcase, 0)
            if salestotal_vip is not None:
                base_json['salesData'].update(salestotal_vip)
        return base_json

class Assembler:
    def __init__(self, test_cls, testcase, common_params):
        self.unit = Units(test_cls, testcase)
        common_params = list(set(common_params))
        self.cls = test_cls
        self.common_params = ['param_{}'.format(param.lower()) for param in common_params]

    def assemble(self):
        """
        according to different params to find self method to control
        """
        self_json = self.unit.base()
        if 'param_bc' in self.common_params and 'param_bx' in self.common_params:
            self.common_params.remove('param_bx')
            self.common_params.remove('param_bc')
            self.common_params.append('param_bc_bx')
        elif 'param_bc' in self.common_params:
            pass
        elif 'param_bx' in self.common_params:
            self.common_params.remove('param_bx')
        for param in self.common_params:
            if hasattr(self.unit, param):
                func = getattr(self.unit, param)
                self_json = func(self_json)
            else:
                param = param.upper()
                param = param.replace('PARAM_', '-')
                self.cls._testMethodDoc += "<br><font color='red' style='font-weight:bold'>confit.ini 中 " \
                                           "本程序没有提供对该参数 {} 的处理</font>".format(param)
                self.cls.skipTest('本程序没有提供对该参数 {} 的处理'.format(param))
        if 'param_bc_bx' in self.common_params:
            self.common_params.remove('param_bc_bx')
        self_json = json_dumps(self_json, indent=4)
        logger.info('REQUEST:\n {}'.format(self_json))
        return self_json

