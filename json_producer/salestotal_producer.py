from util.param_parser.param_parser import to_dict


def _get_vipinfo(test_cls, testcase, if_get):
    """
    获取 testcase中 vipinfo 的数据
    promparam中如果只存在 -BC，则vipinfo 必须要有customerCode, vipGradeCenter, vipBonusCenter 的相关信息；
    如果同时存在 -BC，-BX，则vipinfo 可有可无
    :param test_cls:
    :param testcase:
    :param if_get: 1: vipinfo 必须有数据， 0:vipinfo 数据可有可无
    :return:
    """
    if testcase == []:
        test_cls.skipTest('找不到TestCase数据')
    if if_get == 1:
        info = 'TestCase 中的VIPINFO 缺少 customerCode, vipGradeCenter, vipBonusCenter 的相关信息'
        info1 = '请查看TestCase 中的VIPINFO 的 customerCode, vipGradeCenter, vipBonusCenter 的相关信息是否补全，' \
                '或者VIPINFO 的键值是否为：customerCode, vipGradeCenter, vipBonusCenter'
        testcase_desci = test_cls._testMethodDoc + \
                         "<br><font color='red' style='font-weight:bold'>【{}】</font>".format(info)
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
            elif 'customercode' in row['VIPINFO'].lower() and 'vipgradecenter' in row[
                'VIPINFO'].lower() and 'vipbonuscenter' in row['VIPINFO'].lower():
                return to_dict(test_cls, 'VIPINFO', row['VIPINFO'])
            else:
                if i == len(testcase) - 1:
                    test_cls._testMethodDoc = testcase_desci
                    test_cls.skipTest(info1)
    elif if_get == 0:
        info1 = '请查看TestCase 中的VIPINFO 的 customerCode, vipGradeCenter, vipBonusCenter 的相关信息是否补全，' \
                '或者VIPINFO 的键值是否为：customerCode, vipGradeCenter, vipBonusCenter'
        testcase_desci = test_cls._testMethodDoc + \
                         "<br><font color='red' style='font-weight:bold'>【{}】</font>".format(info1)
        for i, row in enumerate(testcase):
            if row['VIPINFO'] is None:
                if i == len(testcase) - 1:
                    pass
            elif row['VIPINFO'].strip() == '':
                if i == len(testcase) - 1:
                    pass
            # check TestCase 中 VIPINFO 是否缺漏信息
            elif 'customercode' in row['VIPINFO'].lower() and 'vipgradecenter' in row['VIPINFO'].lower() \
                    and 'vipbonuscenter' in row['VIPINFO'].lower():
                return to_dict(test_cls, 'VIPINFO', row['VIPINFO'])
            else:
                if i == len(testcase) - 1:
                    test_cls._testMethodDoc = testcase_desci
                    test_cls.skipTest(info1)
        return
    else:
        raise Exception('if_get值为{} ,只能输入 0 或 1'.format(if_get))


def produce_salestotal_vip(test_cls, testcase, if_get):
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
    vipinfo = _get_vipinfo(test_cls, testcase, if_get)
    if vipinfo is None:
        return
    else:
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
