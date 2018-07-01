# from freestyle-project.expense-tracker import
import sys
import os
from dotenv import load_dotenv
from app import *

load_dotenv()

username = os.environ.get("BUXFER_USERNAME") or "OOPS. Please set an environment variable named 'BUXFER_USERNAME'."
if username == "OOPS. Please set an environment variable named 'BUXFER_USERNAME'.":
    print(username)
    exit()
password = os.environ.get("BUXFER_PASSWORD") or "OOPS. Please set an environment variable named 'BUXFER_PASSWORD'."
if password == "OOPS. Please set an environment variable named 'BUXFER_PASSWORD'.":
    print(password)
    exit()
username = username.replace('"', '') #removes the quotations from the environment variables
password = password.replace('"', '')
print(username)
print(password)

base = "https://www.buxfer.com/api";
login_url  = base + "/login?userid=" + username + "&password=" + password
response = requests.get(login_url)
response_body = json.loads(response.text)
token = response_body["response"]["token"] # token is used to get information

def test_show_account():
    result = show_account(base + "/accounts?token=" + token)
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
