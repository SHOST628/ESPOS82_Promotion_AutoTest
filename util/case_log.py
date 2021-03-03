from util.param_parser.param_parser import to_dict
from decimal import Decimal


def _base_log(test_cls, testcase, response):
    """
    if testcase fail output some log
    :param testcase:
    :param response:
    :return:
    """
    # TODO output salesitems log
    res_sales_items = response['resSalesItems']
    b_log = ''
    promless = None
    itemcode = None
    # just think about a existing promid
    for i, case in enumerate(testcase):
        promless = case['PROMLESSDETAIL']
        itemcode = case['ITEMCODE']
        # b_log += '【PromtionLess】'
        b_log += '\n[ItemCode: {}]\n'.format(itemcode)
        # todo modify
        if res_sales_items == []:
            if promless is None:
                b_log += 'PromId:None, 实际结果:不中促销, 期望结果:None\n'
            else:
                promless = to_dict(test_cls, 'PROMLESSDETAIL', promless)
                for k, v in promless.items():
                    if type(v) is list:
                        for v_ in v:
                            b_log += 'PromId:{}, 实际结果:不中促销, 期望结果:{}\n'.format(k, v_)
                    else:
                        b_log += 'PromId:{}, 实际结果:不中促销, 期望结果:{}\n'.format(k, v)
        else:
            actual_itemindexs = {}
            for j, sales_items in enumerate(res_sales_items):
                # 记录列表中index和 itemindex 关系
                actual_itemindexs[sales_items['itemIndex']] = j
            promless = to_dict(test_cls, 'PROMLESSDETAIL', promless)
            expected_promids = []
            actual_promids = []
            if i in actual_itemindexs:
                if promless is None:
                    expected_promids = None
                else:
                    expected_promids = list(promless.keys())
                    expected_promids.sort()
                for item_consumes in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                    actual_promids.append(item_consumes['promId'])
                actual_promids.sort()
                if expected_promids is not None:
                    # 注意：response有可能会存在，同一个itemcode里面，同一个promid 会被分拆成多个dict展示
                    if len(expected_promids) <= len(actual_promids):
                        if list(set(actual_promids)) == expected_promids:
                            actual_promless_detail = {}
                            if expected_promids == actual_promids:
                                for item_consumes in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                                    promid = item_consumes['promId']
                                    actual_promless_detail[promid] = []
                                    actual_promless_detail[promid].append(item_consumes['lessAmount'])
                            else:
                                actual_promids = list(set(actual_promids))
                                for actual_promid in actual_promids:
                                    for item_consume in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                                        if actual_promid == item_consume['promId']:
                                            if actual_promid in list(actual_promless_detail.keys()):
                                                actual_promless_detail[actual_promid].append(item_consume['lessAmount'])
                                            else:
                                                actual_promless_detail[actual_promid] = []
                                                actual_promless_detail[actual_promid].append(item_consume['lessAmount'])
                            for k, v in promless.items():
                                if type(v) is list:
                                    if len(v) == len(actual_promless_detail[k]):
                                        for h, v_ in enumerate(v):
                                            b_log += 'PromId:{}, 实际结果:{}, 期望结果:{}\n'.format(k, actual_promless_detail[k][h], v_)
                                    else:
                                        if len(v) > len(actual_promless_detail[k]):
                                            for h, v_ in enumerate(v):
                                                if h == len(actual_promless_detail[k]) -1:
                                                    b_log += 'PromId:{}, 实际结果:None, 期望结果:{}\n'. \
                                                        format(k, v_)
                                                else:
                                                    b_log += 'PromId:{}, 实际结果:{}, 期望结果:{}\n'.\
                                                        format(k, actual_promless_detail[k][h], v_)
                                        if len(v) < len(actual_promless_detail[k]):
                                            for h, v_ in enumerate(actual_promless_detail[k]):
                                                if h == len(v) - 1:
                                                    b_log += 'PromId:{}, 实际结果:{}, 期望结果:None\n'. \
                                                        format(k, v_)
                                                else:
                                                    b_log += 'PromId:{}, 实际结果:{}, 期望结果:{}\n'. \
                                                        format(k, v_, v[h])
                                else:
                                    if len(actual_promless_detail[k]) > 1:
                                        for h, v_ in enumerate(actual_promless_detail[k]):
                                            if h == 0:
                                                b_log += 'PromId:{}, 实际结果:{}, 期望结果:None\n'. \
                                                    format(k, v_)
                                            else:
                                                b_log += 'PromId:{}, 实际结果:{}, 期望结果:{}\n'. \
                                                    format(k, v_, v)
                                    else:
                                        b_log += 'PromId:{}, 实际结果:{}, 期望结果:{}\n'.\
                                            format(k, actual_promless_detail[k][0], v)
                        else:
                            actual_promids = list(set(actual_promids))
                            actual_promids.sort()
                            b_log += '实际PromId:{}, 期望PromId:{}\n'.format(','.join(actual_promids),','.join(expected_promids))
                    else:
                        actual_promids = list(set(actual_promids))
                        actual_promids.sort()
                        b_log += '实际PromId:{}, 期望PromId:{}\n'.format(','.join(actual_promids),','.join(expected_promids))
                else:
                    actual_promless_detail = {}
                    actual_promids = list(set(actual_promids))
                    for actual_promid in actual_promids:
                        for item_consume in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                            if actual_promid == item_consume['promId']:
                                if actual_promid in list(actual_promless_detail.keys()):
                                    actual_promless_detail[actual_promid].append(item_consume['lessAmount'])
                                else:
                                    actual_promless_detail[actual_promid] = []
                                    actual_promless_detail[actual_promid].append(item_consume['lessAmount'])

                    for k, v in actual_promless_detail.items():
                        if type(v) is list:
                            for l in v:
                                b_log += 'PromId:{}, 实际结果:{}, 期望结果:None\n'.format(k, l)
                        else:
                            b_log += 'PromId:{}, 实际结果:{}, 期望结果:None\n'.format(k, v)
            else:
                if promless is None:
                    b_log += 'PromId:None, 实际结果:None, 期望结果:None\n'
                else:
                    for k, v in promless.items():
                        if type(v) is list:
                            for v_ in v:
                                b_log += 'PromId:{}, 实际结果:None, 期望结果:{}\n'.format(k, v_)
                        else:
                            b_log += 'PromId:{}, 实际结果:None, 期望结果:{}\n'.format(k, v)
    return b_log


def base_log(test_cls, testcase, response):
    """
    if testcase fail output some log
    :param testcase: list
    :param response: dict
    :return:
    """
    b_log = _base_log(test_cls, testcase, response)
    return b_log


class ParamLog:
    def param_xe_log(self,testcase, response):
        b_log = '【Param_XE】\n'

    def param_bl_log(self):
        pass

    def param_br_log(self):
        pass

    def param_dis_log(self):
        pass