# -*- coding:utf-8 -*-
"""
@Time : 2023/3/29
@Author : skyoceanchen
@TEL: 18916403796
@File : dict_operation.py 
@PRODUCT_NAME : PyCharm 
"""
from collections import Counter


# <editor-fold desc="字典类工具">
class DictOperation(object):
    @staticmethod
    def twodictadd(dict1, dict2):
        dict_new = dict(Counter(dict1) + Counter(dict2))
        return dict_new

    # <editor-fold desc="取出列表内所有字典的value值">
    @staticmethod
    def list_dict_value(lis):
        """
        :param lis:
        :return:
        """
        res = [item[key] for item in lis for key in item]
        return res

    # </editor-fold>
    # <editor-fold desc="取出列表内所有字典的keys值">
    @staticmethod
    def list_dict_keys(lis):
        """
        :param lis:
        :return:
        """
        res = [key for item in lis for key in item]
        return res

    # </editor-fold>
    # <editor-fold desc="字典组成的数组怎么进行去重">
    @staticmethod
    def dic_duplicate_remove(data):  # 适用一般情况
        # data = reduce(lambda x, y: x + [y] if y not in x else x, [[], ] + data)#
        data = [dict(t) for t in set([tuple(d.items()) for d in data])]
        return data

    @staticmethod
    def delete_duplicate_str(data):  # 适用这种情况如： data2 = [{"a": {"b": "c"}}, {"a": {"b": "c"}}]
        immutable_dict = set([str(item) for item in data])
        data = [eval(i) for i in immutable_dict]
        return data

    # </editor-fold>
    # <editor-fold desc="列表中的字典按某个字段排序">
    @staticmethod
    def list_order(data: list, fields=None):
        """
        :param data:
        :param value:list 传入 索引  字典传入keys
        :return: list
        """
        if fields:
            data: list = sorted(data, key=lambda k: k[fields])
        else:
            data.sort()
        return data
    # </editor-fold>

# </editor-fold>
