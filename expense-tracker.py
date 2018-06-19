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


#def group_transactions

#def matching_product(product_identifier,categories):
#    categories_list = [p for p in categories if p["id"] == product_identifier] #makes a list of p in categories that have product ID as ID. (will only have one item in this case)
#    return categories_list[0]

def run():
    username = "timho890000@yahoo.com"#input("Please enter your email address: ")
    password = "timmy2co"#input("Please enter your password: ")
    categories = ["food","expenses","shopping","income","other"]
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
    food_key_words = ["cafe","market","joju","dumpling","qdoba","chipotle","pho"]
    expense_key_words = []
    shopping_key_words = []
    other_key_words = []

    for t in transactions:
        for f in food_key_words:
            if(f.upper() in t["description"].upper()):
                food_payments.append(t)
                #transactions.remove(t) this will screw it up. find a way to remove.
                break
    print("This is what you spent on food")
    for i in food_payments:
        print("Date: "+i["normalizedDate"]+" Description: "+i["description"]+" Amount: "+str(i["amount"]))


    for t in transactions:
        if -t["expenseAmount"]>0:
            income.append(t)
            #transactions.remove(t)
    print("Your income/refund items are shown below")
    for i in income:
        print("Date: "+i["normalizedDate"]+" Description: "+i["description"]+" Amount: "+str(i["amount"]))

    for t in transactions:
        print (t)


if __name__ == "__main__": ## this will run only when this program is invoked from the command line. So if we run the reset function, it wont run the whole thing
    run()
