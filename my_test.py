# from freestyle-project.expense-tracker import
import sys
import os
from app import *

def test_show_account():
    result = show_account("https://www.buxfer.com/api/accounts?token=kq5uhi7qksv6k8uo7503hu3jh6")
    assert type(result) == dict

def test_list_transactions():
    result = list_transactions("https://www.buxfer.com/api/transactions?token=kq5uhi7qksv6k8uo7503hu3jh6&startDate=2018-05-01&endDate=2018-05-30")
    assert type(result) == list

def test_include_category_key_words():
    result = include_category_key_words("categories")
    assert type(result) == list

def test_return_list():
    result = return_list("db/categories.csv")
    assert type(result) == list

#not sure how to test a function with inputs
#def test_set_budget():
#    result = set_budget(["food","drinks"],["100","100"])
#    assert type(result) == list
