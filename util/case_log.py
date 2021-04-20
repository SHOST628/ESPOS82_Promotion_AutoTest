from util.param_parser.param_parser import to_dict


def _base_log(test_cls, testcase, response, log_type):
    """
        if testcase fail output some log
        log_type: 0,1
        log_type = 0 : just show actual promid and expected promid
        log_type = 1 : show actual and expected promid, promless
        :param testcase:
        :param response:
        :return:
        """
    res_sales_items = response['resSalesItems']
    b_log = ''
    promless = None
    itemcode = None
    actual_itemindexs = {}
    for i, case in enumerate(testcase):
        promless = case['PROMLESSDETAIL']
        itemcode = case['ITEMCODE']
        if i == 0:
            b_log += '【PromtionLess】'
            # 记录response中 列表的index和 itemindex 关系
            for j, sales_items in enumerate(res_sales_items):
                actual_itemindexs[sales_items['itemIndex']] = j
        b_log += '\n[ItemCode: {}]\n'.format(itemcode)
        expected_promids = []
        actual_promids = []
        promless = to_dict(test_cls, 'PROMLESSDETAIL', promless)
        if promless is not None:
            expected_promids = list(promless.keys())
            expected_promids.sort()
            for k, v in promless.items():
                if type(v) is list:
                    pass
                else:
                    promless[k] = []
                    promless[k].append(v)
        if i in actual_itemindexs:
            for item_consumes in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                actual_promids.append(item_consumes['promId'])
            actual_promids = list(set(actual_promids))
            actual_promids.sort()
            if log_type == 0:
                if promless is None:
                    b_log += '期望PromId: None, 实际PromId:{}\n'.format(','.join(actual_promids))
                else:
                    b_log += '期望PromId:{}, 实际PromId:{}\n'.format(','.join(expected_promids), ','.join(actual_promids))
            elif log_type == 1:
                # todo
                actual_promless_detail = {}
                for actual_promid in actual_promids:
                    actual_promless_detail[actual_promid] = []
                    for item_consume in res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']:
                        if actual_promid == item_consume['promId']:
                            actual_promless_detail[actual_promid].append(str(item_consume['lessAmount']))
                if promless is None:
                    for k,v in actual_promless_detail.items():
                        # b_log += 'PromId:{}, 期望结果:None, 实际结果:{}\n'.format(k, ' & '.join(v))
                        if len(v) == 1:
                            v = v[0]
                        b_log += 'PromId:{}, 期望结果:None, 实际结果:{}\n'.format(k, v)
                else:
                    if len(list(promless.keys())) >= len(list(actual_promless_detail.keys())):
                        for k, v in promless.items():
                            if k in actual_promless_detail:
                                # b_log += 'PromId:{}, 期望结果:{}, 实际结果:{}\n'.format(k, ' & '.join(v), ' & '.join(actual_promless_detail[k]))
                                if len(v) == 1:
                                    v = v[0]
                                if len(actual_promless_detail[k]) == 1:
                                    actual_promless_detail[k] = actual_promless_detail[k][0]
                                b_log += 'PromId:{}, 期望结果:{}, 实际结果:{}\n'.format(k, v, actual_promless_detail[k])
                            else:
                                # b_log += 'PromId:{}, 期望结果:{}, 实际结果:None\n'.format(k, ' & '.join(v))
                                if len(v) == 1:
                                    v = v[0]
                                b_log += 'PromId:{}, 期望结果:{}, 实际结果:None\n'.format(k, v)
                    else:
                        for k, v in actual_promless_detail.items():
                            if k in promless:
                                # b_log += 'PromId:{}, 期望结果:{}, 实际结果:{}\n'.format(k, ' & '.join(promless[k]), ' & '.join(v))
                                if len(v) == 1:
                                    v = v[0]
                                if len(promless[k]) == 1:
                                    promless[k] = promless[k][0]
                                b_log += 'PromId:{}, 期望结果:{}, 实际结果:{}\n'.format(k, promless[k], v)
                            else:
                                # b_log += 'PromId:{}, 期望结果:None, 实际结果:{}\n'.format(k, ' & '.join(v))
                                if len(v) == 1:
                                    v = v[0]
                                b_log += 'PromId:{}, 期望结果:None, 实际结果:{}\n'.format(k, v)
        else:
            if log_type == 0:
                if promless is None:
                    b_log += '期望结果: 不中促销, 实际结果: 不中促销\n'
                else:
                    b_log += '期望PromId:{}, 实际PromId: None\n'.format(','.join(expected_promids))
            elif log_type == 1:
                if promless is None:
                    b_log += '期望结果: 不中促销, 实际结果: 不中促销\n'
                else:
                    for k, v in promless.items():
                        # b_log += 'PromId:{}, 期望结果:{}, 实际结果:不中促销\n'.format(k, ' & '.join(v))
                        if len(v) == 1:
                            v = v[0]
                        b_log += 'PromId:{}, 期望结果:{}, 实际结果:不中促销\n'.format(k, v)
    return b_log


def base_log(test_cls, testcase, response, log_type):
    """
    if testcase fail output some log
    :param testcase: list
    :param response: dict
    :return:
    """
    b_log = _base_log(test_cls, testcase, response, log_type)
    return b_log


class ParamLog:
    def param_xe_log(self,test_cls, testcase, response, bonusgive_ex):
        """
        :param test_cls:
        :param testcase:
        :param response:
        :param bonusgive_ex_ac: dict,  bonusGive expected detail including the info about promids and bonusGive
        :return:
        """
        # param_xe = get_param_to_dict(test_cls, 'PROMPARAM_XE', testcase, RESPONSE, 'bonusGive')
        res_sales_items = response['resSalesItems']
        b_log = '\n【Param_XE】\n'
        actual_itemindexs = {}
        for j, sales_items in enumerate(res_sales_items):
            # record the relationship about item index in testcase and itemindex in response
            actual_itemindexs[sales_items['itemIndex']] = j
        for i, case in enumerate(testcase):
            item_code = case['ITEMCODE']
            b_log += '[ItemCode: {}]\n'.format(item_code)
            # the itemIndex for the item hit a promotion
            if i in actual_itemindexs:
                # change actual bonusGive format into {'PEOHQO201100036':[1070,1080], 'PEOHQO201100037':[1070,1080]}
                bonus_give_d = {}
                res_salesitem_consumes = res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']
                for res_salesitem_consume in res_salesitem_consumes:
                    if res_salesitem_consume['bonusGive'] == 0:
                        pass
                    else:
                        promid = res_salesitem_consume['promId']
                        if promid in bonus_give_d:
                            bonus_give_d[promid].append(res_salesitem_consume['bonusGive'])
                        else:
                            bonus_give_d[promid] = []
                            bonus_give_d[promid].append(res_salesitem_consume['bonusGive'])
                if bonusgive_ex[i] is not None:
                    for k, v in bonusgive_ex[i].items():
                        if k in bonus_give_d:
                            if len(v) == 1:
                                v = v[0]
                            if len(bonus_give_d[k]) == 1:
                                bonus_give_d[k] = bonus_give_d[k][0]
                            b_log += 'PromId:{}, 期望bonusGive: {}, 实际bonusGive: {}\n'. \
                                format(k, v, bonus_give_d[k])
                        else:
                            if len(v) == 1:
                                v = v[0]
                            b_log += 'PromId:{}, 期望bonusGive: {}, 实际bonusGive: None\n'.format(k, v)
                    # promids not in expected list
                    not_in_exs = list(bonus_give_d.keys() - bonusgive_ex[i].keys())
                    for p in not_in_exs:
                        if len(bonus_give_d[p]) == 1:
                            bonus_give_d[p] = bonus_give_d[p][0]
                        b_log += 'PromId:{}, 期望bonusGive: None, 实际bonusGive: {}\n'. \
                            format(p, bonus_give_d[p])
                else:
                    if bonus_give_d == {}:
                        b_log += '期望bonusGive: None, 实际bonusGive: None\n'
                    else:
                        for k, v in bonus_give_d.items():
                            if len(v) == 1:
                                v = v[0]
                            b_log += 'PromId:{}, 期望bonusGive: None, 实际bonusGive: {}\n'. \
                                format(k, v)
            # the itemIndex for item does not hit a promotion
            else:
                if bonusgive_ex[i] is not None:
                    for k, v in bonusgive_ex[i].items():
                        if len(v) == 1:
                            v = v[0]
                        b_log += 'PromId:{}, 期望bonusGive: {}, 实际bonusGive: None\n'. \
                            format(k, v)
                else:
                    b_log += '期望bonusGive: None, 实际bonusGive: None\n'
        return b_log

    def param_br_log(self, test_cls, testcase, response):
        # bonus_redeem = get_param_to_dict(test_cls, 'PROMPARAM_BR', testcase, RESPONSE, 'bonusRedeem')
        # res_sales_items = response['resSalesItems']
        # b_log = '\n【Param_BR】\n'
        # actual_itemindexs = {}
        # for j, sales_items in enumerate(res_sales_items):
        #     # record the relationship about item index in testcase and itemindex in response
        #     actual_itemindexs[sales_items['itemIndex']] = j
        # for i, case in enumerate(testcase):
        #     item_code = case['ITEMCODE']
        #     if i == 0:
        #         b_log += '[ItemCode: {}]\n'.format(item_code)
        #     else:
        #         b_log += '\n[ItemCode: {}]\n'.format(item_code)
        #     if i in actual_itemindexs:
        #         res_salesitem_consumes = res_sales_items[actual_itemindexs[i]]['resSalesItemConsumes']
        #         actual_bonus_redeem = 0
        #         for salesitem_consume in res_salesitem_consumes:
        #             actual_bonus_redeem += salesitem_consume['bonusRedeem']
        #         if bonus_redeem[i]['response'] is not None:
        #             b_log += '期望bonusRedeem: {}, 实际bonusRedeem: {}\n'. \
        #                 format(bonus_redeem[i]['response']['bonusredeem'], actual_bonus_redeem)
        #         else:
        #             b_log += '期望bonusRedeem: None, 实际bonusRedeem: {}\n'. \
        #                 format(actual_bonus_redeem)
        #     else:
        #         if bonus_redeem[i]['response'] is not None:
        #             b_log += '期望bonusRedeem: {}, 实际bonusRedeem: None\n'. \
        #                 format(bonus_redeem[i]['response']['bonusredeem'])
        #         else:
        #             b_log += '期望bonusRedeem: None, 实际bonusRedeem: None\n'
        return ''

    def param_xc_log(self, test_cls, testcase, *ex_ac):
        """
        :param test_cls:
        :param testcase:
        :param ex_ac: expected assertion dict and actual assertion dict
        :return:
        """
        ex_param_xc, res_relyon_consume = ex_ac
        common_promid_set = ex_param_xc.keys() & res_relyon_consume.keys()
        res_promid_other_set = res_relyon_consume.keys() - common_promid_set
        res_promid_others = list(res_promid_other_set)
        res_promid_others.sort()
        b_log = '\n【Param_XC】\n'
        # 期望结果对比实际结果
        for k, v in ex_param_xc.items():
            if k in res_relyon_consume:
                b_log += 'PromId:{}, 期望结果:[batchNo:{}, qty:{}], 实际结果:[batchNo:{}, qty:{}]\n'. \
                    format(k, v['batchno'], v['qty'], res_relyon_consume[k]['batchno'], res_relyon_consume[k]['qty'])
            else:
                b_log += 'PromId:{}, 期望结果:[batchNo:{}, qty:{}], 实际结果:None\n'. \
                    format(k, v['batchno'], v['qty'])
        # 公共部分之外的实际结果
        for k in res_promid_others:
            b_log += 'PromId:{}, 期望结果:None, 实际结果:[batchNo:{}, qty:{}]\n'. \
                format(k, res_relyon_consume[k]['batchno'], res_relyon_consume[k]['qty'])
        return b_log

    def param_xg_log(self, test_cls, testcase, *ex_ac):
        """
        :param test_cls:
        :param testcase:
        :param ex_ac: expected assertion dict and actual assertion dict
        :return:
        """
        ex_param_xg, res_relyon_consume = ex_ac
        common_promid_set = ex_param_xg.keys()&res_relyon_consume.keys()
        res_promid_other_set = res_relyon_consume.keys() - common_promid_set
        res_promid_others = list(res_promid_other_set)
        res_promid_others.sort()
        b_log = '\n【Param_XG】\n'
        # 期望结果对比实际结果
        for k, v in ex_param_xg.items():
            if k in res_relyon_consume:
                b_log += 'PromId:{}, 期望结果:[batchNo:{}, qty:{}], 实际结果:[batchNo:{}, qty:{}]\n'.\
                    format(k,v['batchno'], v['qty'], res_relyon_consume[k]['batchno'], res_relyon_consume[k]['qty'])
            else:
                b_log += 'PromId:{}, 期望结果:[batchNo:{}, qty:{}], 实际结果:None\n'. \
                    format(k, v['batchno'], v['qty'])
        # 公共部分之外的实际结果
        for k in res_promid_others:
            b_log += 'PromId:{}, 期望结果:None, 实际结果:[batchNo:{}, qty:{}]\n'. \
                format(k, res_relyon_consume[k]['batchno'], res_relyon_consume[k]['qty'])
        return b_log

    def param_xp_log(self, test_cls, testcase, *ex_ac):
        ex_param_xp, res_relyon_consume = ex_ac
        common_promid_set = ex_param_xp.keys() & res_relyon_consume.keys()
        res_promid_other_set = res_relyon_consume.keys() - common_promid_set
        res_promid_others = list(res_promid_other_set)
        res_promid_others.sort()
        b_log = '\n【Param_XP】\n'
        # {'PEOHQO210400007':{'batchs':[{'batchNo':'HQ003','qty':1},{'batchNo':'HQ004','qty':1}],'packCode':'01'}}
        # 期望结果对比实际结果
        for k, v in ex_param_xp.items():
            if k in res_relyon_consume:
                b_log += '[PromId:{}]\n期望结果: batchs: {}, packCode: {}\n实际结果: batchs: {}, packCode: {}\n'\
                         .format(k, v['batchs'], v['packcode'], res_relyon_consume[k]['batchs'],
                                 res_relyon_consume[k]['packcode'])
            else:
                b_log += '[PromId:{}]\n期望结果: batchs: {}, packCode: {}\n实际结果: None\n' \
                         .format(k, v['batchs'], v['pachcode'])
        # 公共部分之外的实际结果
        for k in res_promid_others:
            b_log += '[PromId:{}]\n期望结果: None\n实际结果: batchs: {}, packCode: {}\n' \
                     .format(k, res_relyon_consume[k]['batchs'], res_relyon_consume[k]['packcode'])
        return b_log