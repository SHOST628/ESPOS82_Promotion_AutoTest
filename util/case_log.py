

def _res_salesitems(testcase, response):
    """
    if testcase fail output some log
    :param testcase:
    :param response:
    :return:
    """
    # TODO output salesitems log
    res_sales_items = response['resSalesItems']
    for i, salesitem in enumerate(res_sales_items):
        pass


def case_log(testcase, response):
    """
    if testcase fail output some log
    :param testcase: list
    :param response: dict
    :return:
    """
    _res_salesitems(testcase, response)


"""
【Assertion】
simple statement

【PromLess】
{ItemCode1:{PromId1:{Actual:xx, Expected:xx}}, ItemCode2:{PromId1:{Actual:xx, Expected:xx}}}

【PromParam_XX】
{Actual:{}, Expected:{}}    

"""