def param_model(key):
    """
    get standard testcase column format
    :param key: the testcase column which starts with PROMPARAM_ or the column VIPINFO or the column PROMLESSDETAIL
    :return:
    KD,KP,GT,DIS,XC,XP,XG,NC,BL,BR,XE
    """
    vipinfo = "<br><font color='red' style='font-weight:bold'>" \
                         "参考格式：&nbsp&nbsp;customerCode=02087651988,vipGradeCenter=*,vipBonusCenter=* </font>"
    promlessdetail = "<br><font color='red' style='font-weight:bold'>参考格式：&nbsp&nbsp;PEOHQO201100034=265</font>" \
                     "<br><font color='red' style='font-weight:bold'>或&nbsp&nbsp;PEOHQO201100034=265&270</font>" \
                     "<br><font color='red' style='font-weight:bold'>或&nbsp&nbsp;PEOHQO201100034=-265&-270</font>"
    # todo to confirm
    promparam_kd = "<br><font color='red' style='font-weight:bold'>" \
                         " </font>"
    promparam_kp = "<br><font color='red' style='font-weight:bold'>参考格式：&nbsp&nbsp;promId=PEOHQO210200003,keyCode=HQ20210201; </font>" \
                   "<br><font color='red' style='font-weight:bold'>或promKeyCode=HQ20210202;</font>"
    promparam_gt = "<br><font color='red' style='font-weight:bold'>" \
                         "参考格式：&nbsp&nbsp;promId=PEOHQO201100015; </font>"
    promparam_dis = "<br><font color='red' style='font-weight:bold'>" \
                         "参考格式：&nbsp&nbsp;promId=PEOHQO200900006,lessItemIndex=0,useQty=1,pkgQty=1; </font>"
    promparam_xc = "<br><font color='red' style='font-weight:bold'>" \
                    "参考格式：&nbsp&nbsp;;PEOHQO201100029:batchNo=HQ002,qty=1 </font>" \
                    "<br><font color='red' style='font-weight:bold'>" \
                    "或&nbsp&nbsp;;PEOHQO201100029:batchNo=HQ002,qty=1#PEOHQO201100030:batchNo=HQ003,qty=1 </font>"
    promparam_xp = "<br><font color='red' style='font-weight:bold'>" \
                     "参考格式：&nbsp&nbsp;;PEOHQO210400007:batchs={batchNo=HQ003,qty=1#batchNo=HQ004,qty=1},packCode=01 </font>" \
                     "<br><font color='red' style='font-weight:bold'>或&nbsp&nbsp;;PEOHQO210400007:" \
                     "batchs={batchNo=HQ003,qty=1#batchNo=HQ004,qty=1},packCode=01#" \
                     "PEOHQO210400008:batchs={batchNo=HQ005,qty=1#batchNo=HQ006,qty=1},packCode=01</font>"
    promparam_xg = "<br><font color='red' style='font-weight:bold'>参考格式：&nbsp&nbsp;;PEOHQO210400008:batchno=0HQ002,qty=1 </font>" \
                   "<br><font color='red' style='font-weight:bold'>或&nbsp&nbsp;;PEOHQO210400008:batchno=0HQ002,qty=1#" \
                   "PEOHQO210400008:batchno=0HQ002,qty=1</font>"
    promparam_nc = "<br><font color='red' style='font-weight:bold'>参考格式：&nbsp&nbsp;batchNo=HQ001,cpNo=0HQOO0001D710010000042,qty=1; </font>" \
                   "<br><font color='red' style='font-weight:bold'>或&nbsp&nbsp;batchNo=HQ001,cpNo=0HQOO0001D710010000042,qty=1" \
                   "#batchNo=HQ001,cpNo=0HQOO0001D710010000145,qty=1; </font>"
    promparam_bl = "<br><font color='red' style='font-weight:bold'>" \
                         "参考格式：&nbsp&nbsp;promId=PEOHQO201100034,itemIndex=0,useQty=1; </font>"
    promparam_br = "<br><font color='red' style='font-weight:bold'>" \
                         "参考格式：&nbsp&nbsp;bonus=1000; </font>"
    promparam_xe = "<br><font color='red' style='font-weight:bold'>" \
                         "参考格式：&nbsp&nbsp;;PEOHQO201100036:bonusGive=1070 </font>"
    format_dict = {
        'VIPINFO': vipinfo,
        'PROMLESSDETAIL': promlessdetail,
        'PROMPARAM_KD': promparam_kd,
        'PROMPARAM_KP': promparam_kp,
        'PROMPARAM_GT': promparam_gt,
        'PROMPARAM_DIS': promparam_dis,
        'PROMPARAM_XC': promparam_xc,
        'PROMPARAM_XP': promparam_xp,
        'PROMPARAM_XG': promparam_xg,
        'PROMPARAM_NC': promparam_nc,
        'PROMPARAM_BL': promparam_bl,
        'PROMPARAM_BR': promparam_br,
        'PROMPARAM_XE': promparam_xe,
    }
    return format_dict[key]