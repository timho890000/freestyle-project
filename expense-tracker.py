import csv
import os
import requests
import json

def show_account(url):
    account = requests.get(url)
    account_body = json.loads(account.text)
    data = (account_body["response"])
    account_info = data["accounts"][0]
    print("Your balance in "+account_info["name"]+" is "+ str(account_info["balance"]))
    return account_info

def list_transactions(url):
    transactions = requests.get(url)
    transactions_body = json.loads(transactions.text)
    transaction_data = (transactions_body["response"]["transactions"])
    #data_keys =['id', 'description', 'date', 'normalizedDate', 'type', 'transactionType', 'amount', 'expenseAmount', 'accountId', 'accountName', 'tags', 'tagNames', 'status', 'isFutureDated']
    for d in transaction_data:
        return transaction_data

def return_list(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        my_list = list(reader)
    return my_list[0]

#def group_transactions

#def matching_product(product_identifier,categories):
#    categories_list = [p for p in categories if p["id"] == product_identifier] #makes a list of p in categories that have product ID as ID. (will only have one item in this case)
#    return categories_list[0]

def run():
    username = "timho890000@yahoo.com"#input("Please enter your email address: ")
    password = "timmy2co"#input("Please enter your password: ")
    categories = return_list("db/categories.csv")
    base = "https://www.buxfer.com/api";
    login_url  = base + "/login?userid=" + username + "&password=" + password
    response = requests.get(login_url)
    response_body = json.loads(response.text)
    token = response_body["response"]["token"] # token is used to get information

    print("Welcome to the expense tracking app!")
    print("Here are the current categories of your expenses")
    for c in categories:
        print(c.title())
    print()
    account_url =  base + "/accounts?token=" + token #url to get account(s)
    account = show_account(account_url)
    print()
    print("Here is a list of your transactions:")
    transactions_url =  base + "/transactions?token=" + token #url to get transactions
    transactions = list_transactions(transactions_url) #a list of all the transactions
    print()
    listed_data = []
    for t in transactions:
        listed_data.append({"Date":t["normalizedDate"],"Description":t["description"],"Amount":-t["expenseAmount"]})
    for l in listed_data:
        print(l)


    food_payments = []
    expense_payments = []
    shopping_payments = []
    other_payments = []
    income = [] #list of all positive transactions



    food_key_words = return_list("db/food.csv")
    expense_key_words = return_list("db/expense.csv")
    shopping_key_words = return_list("db/shopping.csv")
    other_key_words = return_list("db/other.csv")
    food_total=0
    expense_total=0
    shopping_total=0
    other_total=0
    income_total=0


    for t in transactions:
        for f in food_key_words:
            if(f.upper() in t["description"].upper()):
                food_payments.append(t)
                food_total= food_total+t["amount"]
                #transactions.remove(t) this will screw it up. find a way to remove.
                break
    print("You spend a total of "+str(food_total)+" on food. Here is a list of the transactions")
    for i in food_payments:
        print("Date: "+i["normalizedDate"]+" Description: "+i["description"]+" Amount: "+str(i["amount"]))

    for t in transactions:
        for f in expense_key_words:
            if(f.upper() in t["description"].upper()):
                expense_payments.append(t)
                expense_total= expense_total+t["amount"]
                #transactions.remove(t) this will screw it up. find a way to remove.
                break
    print("You spend a total of "+str(expense_total)+" on expense. Here is a list of the transactions")
    for i in expense_payments:
        print("Date: "+i["normalizedDate"]+" Description: "+i["description"]+" Amount: "+str(i["amount"]))

    for t in transactions:
        for f in shopping_key_words:
            if(f.upper() in t["description"].upper()):
                shopping_payments.append(t)
                shopping_total= shopping_total+t["amount"]
                #transactions.remove(t) this will screw it up. find a way to remove.
                break
    print("You spend a total of "+str(shopping_total)+" on shopping. Here is a list of the transactions")
    for i in shopping_payments:
        print("Date: "+i["normalizedDate"]+" Description: "+i["description"]+" Amount: "+str(i["amount"]))

    for t in transactions:
        for f in other_key_words:
            if(f.upper() in t["description"].upper()):
                other_payments.append(t)
                other_total= other_total+t["amount"]
                #transactions.remove(t) this will screw it up. find a way to remove.
                break
    print("You spend a total of "+str(other_total)+" on other. Here is a list of the transactions")
    for i in other_payments:
        print("Date: "+i["normalizedDate"]+" Description: "+i["description"]+" Amount: "+str(i["amount"]))


    for t in transactions:
        if -t["expenseAmount"]>0:
            income.append(t)
            #transactions.remove(t)
    print("Your income/refund items are shown below")
    for i in income:
        print("Date: "+i["normalizedDate"]+" Description: "+i["description"]+" Amount: "+str(i["amount"]))



if __name__ == "__main__": ## this will run only when this program is invoked from the command line. So if we run the reset function, it wont run the whole thing
    run()
