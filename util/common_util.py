

def contain_list(list1, list2):
    """
    check if list1 contains list2
    """
    if len(list1) > len(list2):
        if list1 != [] and list2 != []:
            for l in list2:
                if l in list1:
                    pass
                else:
                    return False
            return True
        elif list1 != []:
            return False
        elif list2 != []:
            return False
        else:
            return True
    else:
        return False