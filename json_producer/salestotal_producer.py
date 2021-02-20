from param_parser.param_parser import to_dict
import re


def _salestotal_dict(test_cls, testcase):
    if testcase == []:
        test_cls.skipTest('找不到TestCase数据')
    info = 'TestCase 中的VIPINFO 缺少 customerCode, vipGradeCenter, vipBonusCenter 的相关信息'
    info1 = '请查看TestCase 中的VIPINFO 的 customerCode, vipGradeCenter, vipBonusCenter 的相关信息是否补全，' \
           '或者VIPINFO 的键值是否为：customerCode, vipGradeCenter, vipBonusCenter'
    testcase_desci = test_cls._testMethodDoc + \
                                          "<br><font color='red' style='font-weight:bold'>注意：【{}】</font>".format(info)
    for i, row in enumerate(testcase):
        if row['VIPINFO'] is None:
            if i == len(testcase) - 1:
                test_cls._testMethodDoc = testcase_desci
                test_cls.skipTest(info)
        elif row['VIPINFO'].strip() == '':
            if i == len(testcase) - 1:
                test_cls._testMethodDoc = testcase_desci
                test_cls.skipTest(info)
        # check TestCase 中 VIPINFO 是否缺漏信息
        elif 'customercode' in row['VIPINFO'].lower() and 'vipgradecenter' in row['VIPINFO'].lower() and 'vipbonuscenter' in row['VIPINFO'].lower():
            return to_dict(test_cls, 'VIPINFO', row['VIPINFO'])
        else:
            if i == len(testcase) - 1:
                test_cls._testMethodDoc = testcase_desci
                test_cls.skipTest(info1)


def produce_salestotal_vip(test_cls, testcase):
    """
    [TESTCASE] VIPINFO:  customerCode=NV02D0130120000006,vipGradeCenter=*,vipBonusCenter=*  (including these columns)
    :param test_cls:
    :param testcase:
    :return:

    【Demo salesTotal】
    salesTotal": {
        "customerCode": null,
        "bonusBalance": [
            "vipGradeCenter": "*",
            "vipBonusCenter": "*",
        ]
    },
    "vipGradeCenter": ["*"],
    "vipBonusCenter": "*"
    """
    vipinfo = _salestotal_dict(test_cls, testcase)
    sales_total = {'salesTotal': {}}
    sales_total['salesTotal']['customerCode'] = vipinfo['customercode']
    bonus_balance = {'bonusBalance': [{}]}
    bonus_balance['bonusBalance'][0]['vipGradeCenter'] = vipinfo['vipgradecenter']
    bonus_balance['bonusBalance'][0]['vipBonusCenter'] = vipinfo['vipbonuscenter']
    sales_total['salesTotal'].update(bonus_balance)
    vips = {'vipGradeCenter': [], 'vipBonusCenter': ''}
    vips['vipGradeCenter'].append(vipinfo['vipgradecenter'])
    vips['vipBonusCenter'] = vipinfo['vipbonuscenter']
    sales_total.update(vips)
    return sales_total
