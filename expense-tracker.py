import csv
import os
import requests
import json

def show_account(url):
    account = requests.get(url)
    account_body = json.loads(account.text)
    data = (account_body["response"])
    account_info = data["accounts"][0]
    print("Here is a summary of your spending in the account: "+account_info["name"])
    return account_info

def list_transactions(url):
    transactions = requests.get(url)
    transactions_body = json.loads(transactions.text)
    transaction_data = (transactions_body["response"]["transactions"])
    #data_keys =['id', 'description', 'date', 'normalizedDate', 'type', 'transactionType', 'amount', 'expenseAmount', 'accountId', 'accountName', 'tags', 'tagNames', 'status', 'isFutureDated']
    for d in transaction_data:
        return transaction_data

def include_category_key_words(category):
    included = return_list("db/"+category+".csv")
    return included

def return_list(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        my_list = list(reader)
    return my_list[0]

def include_transactions(transactions,key_words):
    included_transactions = []

    for t in transactions:
        if key_words==["positive"] and -t["expenseAmount"]>0:
            included_transactions.append(t)
        elif key_words != ["other"]:
            for f in key_words:
                if(f.upper() in t["description"].upper()):
                    included_transactions.append(t)
    return included_transactions
#def group_transactions

#def matching_product(product_identifier,categories):
#    categories_list = [p for p in categories if p["id"] == product_identifier] #makes a list of p in categories that have product ID as ID. (will only have one item in this case)
#    return categories_list[0]

def run():
    #enter login information
    username = "timho890000@yahoo.com"#input("Please enter your email address: ")
    password = "timmy2co"#input("Please enter your password: ")

    #read the available categories (this is a list)
    categories = return_list("db/categories.csv")
    #retrieve the token for your account's data
    base = "https://www.buxfer.com/api";
    login_url  = base + "/login?userid=" + username + "&password=" + password
    response = requests.get(login_url)
    response_body = json.loads(response.text)
    token = response_body["response"]["token"] # token is used to get information
    print("--------------------------------------------------")
    print("Welcome to the expense tracking app!")
    print("--------------------------------------------------")
    print("Here are the current categories of your expenses, along with key words that identify transactions to be in that category")
    print("--------------------------------------------------")
    for c in categories:
        print(c.title()+":")
        print(return_list("db/"+c+".csv"))
    print("--------------------------------------------------")
    print()
    account_url =  base + "/accounts?token=" + token #url to get account(s)
    account = show_account(account_url)
    transactions_url =  base + "/transactions?token=" + token #url to get transactions
    transactions = list_transactions(transactions_url) #a list of all the transactions
    listed_data = [] #this is a list of all the transactions (which are each a dictionary)
    for t in transactions:
        listed_data.append({"Date":t["normalizedDate"],"Description":t["description"],"Amount":-t["expenseAmount"]})
    while True:
        print(f"""
        Please select from the following:
            Operation | Description
            --------- | ------------------
            Category  | Adds a category to sort your expenses by
            Key Word  | Adds a key word to a specific category
            ?Budget   | Sets a budget for a category
            Summarize | Summarizes your expenses
            """)
        action = input("Please select an operation: ").title()
        if(action == "Summarize"):
            summarize(categories,transactions)


def summarize(categories, transactions):
    #this creates a list of lists of key words for each category.
    #category_key_words[0] would be key words for the first category and so on so forth.
    category_key_words = []
    for c in categories:
        category_key_words.append(include_category_key_words(c))

    #this creates the list of list of dictionary transactions for each category
    category_payments = []
    for c in categories:
        category_payments.append(include_transactions(transactions,category_key_words[categories.index(c)])) #cycles through key words for that category

    # for everything else, the transactions is grouped to "other"
    for t in transactions:
        add_other = True
        for c in category_payments:
            if(t in c):
                add_other = False
        if(add_other):
            category_payments[1].append(t)

    count = -1
    for c in reversed(category_payments):
        print("---------")
        print(categories[count].title()+":")
        print("---------")
        sum=0
        for i in c:
            sum = sum-i["expenseAmount"]
            print(i["normalizedDate"]+": "+i["description"]+": "+"(${0:.2f})".format(float((-i["expenseAmount"]))))
        print("---------")

        if(sum<0):
            print("The total amount spend on "+ categories[count].title() + " items is " +"(${0:.2f})".format(float(sum)))
            if(sum<-100):
                print("You are spending way too much in this category! Cut down!")
            else:
                print("You are thrifty when it comes to "+categories[count]+". Feel free to spend more =]")
            print()
        elif sum==0:
            print("You have no activity in the "+categories[count].title()+" category")
            print()
        else:
            print("Your income/refunds for the month is "+ "(${0:.2f})".format(float(sum)))
            print()
        count+=-1


if __name__ == "__main__": ## this will run only when this program is invoked from the command line. So if we run the reset function, it wont run the whole thing
    run()
