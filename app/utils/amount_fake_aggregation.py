#-*- coding: utf-8 -*-                                                                                     
"""
算出所有图书
# TODO: 应该用聚合完成
"""
from app.models import BookInfo


def count_all():
    sum_list = []
    for each in BookInfo.objects:
        sum_list.append(len(each.owner))
    result = sum(sum_list)
    return result


