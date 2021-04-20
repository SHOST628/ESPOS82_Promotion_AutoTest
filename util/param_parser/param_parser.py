from util.mylogger import logger
from util.oracle import oracle
from util.param_format_log import param_model
import re


REQUEST = 0
RESPONSE = 1


def param_extractor(prom_param, config_prom_param):
    """
    promotion param extrator
    :param config_prom_param: str,  from promotion parameter
    :param config_prom_param: str,  from config.ini
    :return: common promtion parameters list
    """
    if config_prom_param == '' or config_prom_param is None:
        return []
    prom_params = ['-'+ param.strip() for param in config_prom_param.split(',')]
    config_prom_param = ','.join(prom_params)
    config_prom_param = re.sub(r',', '|', config_prom_param)
    pattern = re.compile(r'{}'.format(config_prom_param))
    common_prom_params = pattern.findall(prom_param)
    common_prom_params = [param.replace('-', '') for param in common_prom_params]
    common_prom_params = list(set(common_prom_params))
    return common_prom_params


def param_extractors(promids, config_prom_param):
    """
    parse common promotion parameters
    :param promids: list
    :param config_prom_param: str
    :return: common promtion parameters list
    """
    prom_param = ''
    prom_param_list = []
    prom_param_sql = ''
    for promid in promids:
        prom_param_sql = "select xf_parameter0 from xf_promitem where xf_promid = '{}'".format(promid)
        prom_param += oracle.select(prom_param_sql)[0][0]
    prom_param_list = param_extractor(prom_param, config_prom_param)
    return prom_param_list


def to_dict(test_cls, key, value):
    """
    turn str into dict, just for testcase['VIPINFO'], testcase['PROMLESSDETAIL'] for example,
    1)str: promid=10001,vipgradecenter=*  --> dict: {'promid':'10001', 'vipgradecenter':'*'}

    for testcase['PROMLESSDETAIL']:
    2)str: PEOHQO200900015=100&50,PEOHQO201100031=130 --> {'PEOHQO200900015':['100', '50'], 'PEOHQO201100031':'30'}

    :param test_cls:
    :param key:  testcase key
    :param value:  testcase value
    :return:
    """
    if value is None:
        logger.debug('TESTCASE 中 【{}】的值为空 '.format(key))
        return
    elif value.strip() == '':
        logger.debug('TESTCASE 中 【{}】的值为空 '.format(key))
        return
    elif '=' in value:
        dic = {}
        count_equal = value.count('=')
        count_comma = value.count(',')
        if count_equal == count_comma + 1:
            kvs = value.split(',')
            for kv in kvs:
                k, v = kv.split('=')
                if k.strip() == '' or v.strip() == '':
                    test_cls._testMethodDoc += "<br><font color='red' style='font-weight:bold'> TESTCASE 下【{}】的值为:{} ,填写格式不正确 </font>".format(key, value)
                    test_cls._testMethodDoc += param_model(key)
                    test_cls.skipTest('TESTCASE 下【{}】的值为:{} ,填写格式不正确'.format(key, value))
                contain_num = re.search(r'\d+', k.strip())
                if contain_num is None:
                    k = k.lower().strip()
                    v = v.strip()
                else:
                    k = k.strip()
                    v = v.strip()
                    # just for testcase['PROMLESSDETAIL']
                    if '&' in v:
                        v = v.split('&')
                        v = [i.strip() for i in v]
                dic[k] = v
            return dic
        test_cls._testMethodDoc += "<br><font color='red' style='font-weight:bold'> TESTCASE 下【{}】的值为:{} ,填写格式不正确</font>".\
            format(key, value)
        test_cls._testMethodDoc += param_model(key)
        test_cls.skipTest('TESTCASE 下【{}】的值为:{} ,填写格式不正确'.format(key, value))
    test_cls._testMethodDoc += "<br><font color='red' style='font-weight:bold'> TESTCASE 下【{}】的值为:{} ,填写格式不正确 </font>".\
        format(key, value)
    test_cls._testMethodDoc += param_model(key)
    test_cls.skipTest('TESTCASE 下【{}】的值为:{} ,填写格式不正确'.format(key, value))


# TODO param_xx  格式不正确时，怎么处理？例如， 缺少 ；
def _param_to_dict(test_cls, key, value, request_response):
    """
    turn str into dict, for example,
    str: promid=10001,vipgradecenter=*;vipbonuscenter=*  --> dict: {'request':{'promid':'10001','vipgradecenter':'*'}, 'response':{'vipbonuscenter':'*'}}
    symbol priority:  ; >  #   >  : > , > =
    如：
    1)PROMPARAM_XE 中填写 ;PEOHQO201100036:bonusGive=1070  --> dict: {'response':{'PEOHQO201100036':{'bonusGive':1070}}}
    2)PROMPARAM_XE 中填写 ;PEOHQO201100036:bonusGive=1070&1080  --> dict: {'response':{'PEOHQO201100036':[{'bonusGive':1070},{'bonusGive':1080}]}}

    :param dict_str:
    :return: the key and value are string  for example, {'request': None, 'reponse': xxx}  {'request':xxx, 'response':{xxx:xxx}}
    """
    test_method_doc = "<br><font color='red' style='font-weight:bold'> TESTCASE 下" \
                      "【{}】的值为:{} ,填写格式不正确</font>"
    test_doc = 'TESTCASE 下【{}】的值为:{} ,填写格式不正确'
    # 用于转换TESTCASE中 PROMPARAM_XX 字段的数据
    if value is None:
        logger.debug('TESTCASE 中 【{}】的值为空 '.format(key))
        return
    elif value.strip() == '':
        logger.debug('TESTCASE 中 【{}】的值为空 '.format(key))
        return
    elif ';' in value:
        if value.count(';') >1:
            test_cls._testMethodDoc += "<br><font color='red' style='font-weight:bold'> TESTCASE 下" \
                                        "【{}】的值为:{} ,填写格式不正确,不能存在两个或以上的 ';'</font>".format(key, value)
            test_cls._testMethodDoc += param_model(key)
            test_cls.skipTest("【{}】的值为:{} ,填写格式不正确,不能存在两个或以上的 ';'".format(key, value))
        req, res = value.split(';')
        # deal with the promble that one item exists multi promid
        t_dict = {}
        if request_response:
            res = res.strip()
            prom_check_dict = {}
            # 处理 -XP case, 临时保存batchs的数据
            rep_tmp = None
            pattern = re.compile(r'\{.*?\}')
            rep_tmp = pattern.findall(res)
            res_replace = None
            if rep_tmp != []:
                sub_pattern = '|'.join(rep_tmp)
                # ;PEOHQO210400007:batchs={batchNo=HQ003,qty=1#batchNo=HQ004,qty=1},packCode=01 取代后
                # ;PEOHQO210400007:batchs=batchs,packCode=01
                res_replace = re.sub(r'{}'.format(sub_pattern), 'batchs', res)
            else:
                res_replace = res
            response_checks = res_replace.split('#')
            for check in response_checks:
                if check is None:
                    pass
                elif check.strip() == '':
                    pass
                else:
                    if ':' in check:
                        prom_check = check.split(':')
                        if prom_check[0] is None or prom_check[0].strip() == '':
                            test_cls._testMethodDoc += test_method_doc.format(key, value)
                            test_cls._testMethodDoc += param_model(key)
                            test_cls.skipTest(test_doc.format(key, value))
                        else:
                            if prom_check[1] is None or prom_check[1].strip() == '':
                                test_cls._testMethodDoc += test_method_doc.format(key, value)
                                test_cls._testMethodDoc += param_model(key)
                                test_cls.skipTest(test_doc.format(key, value))
                            else:
                                # prom_check_dict = {}
                                prom_check_key = prom_check[0]
                                prom_check_value = to_dict(test_cls, key, prom_check[1])
                                if prom_check_value is None:
                                    test_cls._testMethodDoc += test_method_doc.format(key, value)
                                    test_cls._testMethodDoc += param_model(key)
                                    test_cls.skipTest(test_doc.format(key, value))
                                else:
                                    prom_check_dict[prom_check_key] = prom_check_value
                                    t_dict['response'] = prom_check_dict
                    else:
                        test_cls._testMethodDoc += test_method_doc.format(key, value)
                        test_cls._testMethodDoc += param_model(key)
                        test_cls.skipTest(test_doc.format(key, value))
            if rep_tmp != []:
                # ;PEOHQO210400007:batchs={batchNo=HQ003,qty=1#batchNo=HQ004,qty=1},packCode=01
                # {'response': {'PEOHQO210400007':{'batchs':[{'batchNo':'HQ003','qty':1},{'batchNo':'HQ004','qty':1}],'packCode':'01'}}}
                i = 0
                res_assertion = t_dict['response']
                for k, v in res_assertion.items():
                    batchs = []
                    tmp_ = rep_tmp[i].lstrip('{')
                    tmp_ = tmp_.rstrip('}')
                    batch = tmp_.split('#')
                    for b in batch:
                        if b.strip() == '':
                            pass
                        else:
                            batch_dict = to_dict(test_cls, key, b.strip())
                            batchs.append(batch_dict)
                    res_assertion[k]['batchs'] = batchs
                    i += 1
                t_dict['response'] = res_assertion
                return t_dict
            else:
                return t_dict
        else:
            req = req.strip()
            if '#' in req:
                t_dict['request'] = []
                r_param_list = req.split('#')
                for param in r_param_list:
                    if param.strip() == '':
                        pass
                    else:
                        req_dict = to_dict(test_cls, key, param.strip())
                        t_dict['request'].append(req_dict)
            else:
                req_dict = to_dict(test_cls, key, req.strip())
                t_dict['request'] = req_dict
            return t_dict
    else:
        test_cls._testMethodDoc += test_method_doc.format(key, value)
        test_cls._testMethodDoc += param_model(key)
        test_cls.skipTest(test_doc.format(key, value))


def get_param_to_dict(test_cls, key, testcase, request_response, *need_params):
    """
    to solve the problem that PROMPARAM_XX value whether exist in testcase
    :param test_cls:
    :param key: need to get testcase key
    :param testcase:
    :param request_response: 0 : request ,  1 : reponse
    :param need_params: to check whether the data is completed
    :return: if_request = 0, return list including dict ; if_request = 1, return list including dict
    """
    Flag = True
    # need_params_ = ['\b{}\b'.format(param) for param in need_params]
    need_params_ = ['{}'.format(param) for param in need_params]
    need_param = '|'.join(need_params_)
    results = []
    test_method_doc = "<br><font color='red' style='font-weight:bold'>TestCase中{}的数据需要包含:{}</font>"
    skip_test_info = "TestCase 中 {} 的数据需要包含: {}"
    for i, row in enumerate(testcase):
        if row[key] is None:
            if request_response == 0:
                results.append({'request': None})
            else:
                results.append({'response': None})
        elif row[key].strip() == '':
            if request_response == 0:
                results.append({'request': None})
            else:
                results.append({'response': None})
        elif len(list(set(re.findall(r'{}'.format(need_param), row[key], flags=re.IGNORECASE)))) == len(need_params):
            if re.findall(need_param, row[key], flags=re.IGNORECASE):
                # todo 判断PROMPARAM_XX 的value是否存在需要的促销参数
                promparam = _param_to_dict(test_cls, key, row[key], request_response)
                Flag = False
                if request_response == 0:
                    results.append(promparam)
                else:
                    results.append(promparam)
            else:
                test_cls._testMethodDoc += test_method_doc.format(key, ','.join(need_params))
                test_cls._testMethodDoc += param_model(key)
                test_cls.skipTest(skip_test_info.format(key, ','.join(need_params)))
        else:
            test_cls._testMethodDoc += test_method_doc.format(key, ','.join(need_params))
            test_cls._testMethodDoc += param_model(key)
            test_cls.skipTest(skip_test_info.format(key, ','.join(need_params)))
    if Flag:
        test_cls._testMethodDoc += test_method_doc.format(key, ','.join(need_params))
        test_cls._testMethodDoc += param_model(key)
        test_cls.skipTest(skip_test_info.format(key, ','.join(need_params)))
    return results


def exclude_case(test_cls, testcaseid, skip_caseids):
    """
    not to execute testcase in excluding cases
    :param test_cls:
    :param testcaseid:
    :param skip_caseids: str
    :return:
    """
    if skip_caseids.strip() == '':
        return
    skips_ = skip_caseids.split(',')
    skip_caseids_tmp = []
    skip_caseids_range = []
    for caseid in skips_:
        if '-' in caseid:
            range = caseid.split('-')
            min = range[0].strip()
            max = range[1].strip()
            if min != '' and max != '':
                if max < min:
                    min, max = max, min
                skip_caseids_range.append([min, max])
        skip_caseids_tmp.append(caseid)
    if testcaseid in skip_caseids_tmp:
        test_cls.skipTest('属于指定排除的TestCase')
    elif skip_caseids_range != []:
        for range in skip_caseids_range:
            min, max = range
            if testcaseid >= min and testcaseid <= max:
                test_cls.skipTest('跳过执行被指定排除的TestCase')


def exclude_param_case(test_cls, exclude_param, common_params):
    """
    exclude some testcase with some promparams
    :param test_cls:
    :param exclude_param: str
    :param common_params: list
    :return: list
    """
    if exclude_param == '':
        return
    else:
        exclude_params = exclude_param.split(',')
        exclude_params = [param.strip() for param in exclude_params if param.strip() != '']
        common = list(set(exclude_params) & set(common_params))
        if common != []:
            test_cls.skipTest('跳过执行该TestCase，包含需要被排除的参数: {}'.format(exclude_param))


# TODO 优化代码，提取only_test_caseids_tmp和only_test_caseids_range  公有部分
# TODO 将testcase中的该函数调用改为引用方式
def only_test_case(test_cls, testcaseid, only_test_caseids, desci=''):
    """
    only test some cases in only_test_caseids list
    :param test_cls:
    :param testcaseid:
    :param only_test_caseids: str
    :return:
    """
    if only_test_caseids.strip() == '':
        return
    skips_ = only_test_caseids.split(',')
    only_test_caseids_tmp = []
    only_test_caseids_range = []
    for caseid in skips_:
        if '-' in caseid:
            ranges = caseid.split('-')
            min = ranges[0].strip()
            max = ranges[1].strip()
            if min != '' and max != '':
                if max < min:
                    min, max = max, min
                only_test_caseids_range.append([min, max])
        else:
            only_test_caseids_tmp.append(caseid.strip())
    if testcaseid not in only_test_caseids_tmp:
        if only_test_caseids_range != []:
            for i,ranges in enumerate(only_test_caseids_range):
                min, max = ranges
                if testcaseid >= min and testcaseid <= max:
                    break
                else:
                    if i == len(only_test_caseids_range) -1:
                        test_cls._testMethodDoc = desci
                        test_cls.skipTest('没有在指定执行的TestCase列表中')
        else:
            test_cls._testMethodDoc = desci
            test_cls.skipTest('没有在指定执行的TestCase列表中')
