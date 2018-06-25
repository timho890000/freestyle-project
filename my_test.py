# from freestyle-project.expense-tracker import
import sys
import os
from expense_tracker import show_account
from expense_tracker import list_transactions




def test_show_account():
    result = show_account("https://www.buxfer.com/api/accounts?token=kq5uhi7qksv6k8uo7503hu3jh6")
    assert type(result) == dict

def test_list_transactions():
    result = list_transactions("https://www.buxfer.com/api/transactions?token=kq5uhi7qksv6k8uo7503hu3jh6&startDate=2018-05-01&endDate=2018-05-30")
    assert type(result) == list


if __name__ == "__main__": # "if this script is run from the command-line, then ..."
    test_show_account()
