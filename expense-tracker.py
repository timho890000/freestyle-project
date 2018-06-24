import csv
import os
import requests
import json
import os, shutil

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

def summarize(categories, transactions,budgets):
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
    print("Please note that transactions without key words are categorized as 'other' ")
    count = -1
    for c in reversed(category_payments):
        print("---------")
        print(categories[count].title()+":")
        print("---------")
        sum=0
        for i in c:
            sum = sum-i["expenseAmount"]
            print(i["normalizedDate"]+": "+i["description"]+": "+"(${0:,.2f})".format(float((-i["expenseAmount"]))))

        print("---------")
        print("---------")
        if(sum<0):
            print("The total amount spend on "+ categories[count].title() + " items is " +"(${0:,.2f})".format(float(sum)))
            if(sum<float(budgets[categories[count].lower()])):
                print("You are spending way too much in this category! Cut down!")
            else:
                print("You are meeting your goal when it comes to comes to "+categories[count]+". Feel free to spend more but don't go over the budget!")
            print()
        elif sum==0:
            print("You have no activity in the "+categories[count].title()+" category")
            print()
        else:
            print("Your income/refunds for the month is "+ "(${0:,.2f})".format(float(sum)))
            print()
        count+=-1

def write_list_to_file(filename, list):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")
    with open(filepath, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(list)

def reset():
    print("RESETTING DEFAULTS")

    folder = "db"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    categories = return_list("db default/categories default.csv")
    write_list_to_file("categories.csv",categories)
    for c in categories:
        default_list = return_list("db default/"+c+" default.csv")
        write_list_to_file(c+".csv",default_list)

def set_budget(categories,budgets):
    for c in categories:
        budgets[c] = -float(input("What is your budget for "+ c))
    return budgets




#def group_transactions

#def matching_product(product_identifier,categories):
#    categories_list = [p for p in categories if p["id"] == product_identifier] #makes a list of p in categories that have product ID as ID. (will only have one item in this case)
#    return categories_list[0]

def run():
    #enter login information
    username = "timho890000@yahoo.com"#input("Please enter your email address: ")
    password = "timmy2co"#input("Please enter your password: ")
    #read the available categories (this is a list)


    #retrieve the token for your account's data
    base = "https://www.buxfer.com/api";
    login_url  = base + "/login?userid=" + username + "&password=" + password
    response = requests.get(login_url)
    response_body = json.loads(response.text)
    token = response_body["response"]["token"] # token is used to get information

    start_date = "2018-05-01"# input("What start date would you like to analyze from? (YYYY-MM-DD)")
    end_date = "2018-05-31"#input("What end date would you like to analyze to?(YYYY-MM-DD)")
    account_url =  base + "/accounts?token=" + token #url to get account(s)
    account = show_account(account_url)
    transactions_url =  base + "/transactions?token=" + token +"&startDate="+start_date+"&endDate="+end_date #url to get transactions
    print(transactions_url)
    transactions = list_transactions(transactions_url) #a list of all the transactions
    listed_data = [] #this is a list of all the transactions (which are each a dictionary)
    for t in transactions:
        listed_data.append({"Date":t["normalizedDate"],"Description":t["description"],"Amount":-t["expenseAmount"]})
    budgets = {}
    while True:
        try:
            categories = return_list("db/categories.csv")
        except:
            print("Your list of categories is missing. Let me fix that for you =]")
            reset()
            categories = return_list("db/categories.csv")

        # emptoy dictionaries evaluate to false. https://stackoverflow.com/questions/23177439/python-checking-if-a-dictionary-is-empty-doesnt-seem-to-work

        if bool(budgets)==False:
            for c in categories:
                budgets[c] = 100

        print("--------------------------------------------------")
        print("Here are the current categories of your expenses, along with key words that identify transactions to be in that category, and your budget")
        print("--------------------------------------------------")
        try:
            for c in categories:
                print(c.title()+":")
                print("Key words: "+ str(return_list("db/"+c+".csv")))
                if(c == "income"):
                    print("No budget. This should be as high as possible!")
                else:
                    print("Budget: "+"(${0:,.2f})".format(float(budgets[c])))
                print("--------------------------------------------------")
        except:
            print("You don't have a list for this category. Let me reset the defaults for you")
            reset()
            continue
        print("--------------------------------------------------")
        print()
        print(f"""
        Please select from the following:
            Operation | Description
            --------- | ------------------
            Category  | Adds a category to sort your expenses by
            Key Word  | Adds a key word to a specific category
            Budget    | Sets a budget for a category
            Summarize | Summarizes your expenses
            Reset     | Resets to default key_words and categories
            Finish    | Exit out of the program
            """)
        action = input("Please select an operation: ").title()
        if action not in ["Category","Key Word","Budget","Summarize","Reset","Finish"]:
            print("This is not one of the actions.")
            print("Please enter another action.")
            continue
        elif (action == "Summarize"):
            summarize(categories,transactions,budgets)
        elif action == "Category":
            new_category = input("Please input new category:  ").lower()
            if new_category in categories:
                print("This category already exists!")
                continue
            categories.append(new_category)
            write_list_to_file("categories.csv",categories)
            new_key_words=[]
            while True:
                key_word = input("What are some key_words for this category? Type done when finished.").lower()
                if key_word == "done":
                    break
                else:
                    new_key_words.append(key_word)
            write_list_to_file(new_category+".csv", new_key_words)

            budgets[new_category] = input("What is your budget for " + new_category+"? ")
        elif action == "Key Word":
            category = input("Which category would you like to add to?").lower()
            if(category not in categories):
                print("This category doesnt exist. Please create the category!")
                continue
            elif category == "other":
                print("There is no need to add a key_word to other as all remaining transactions will go into this group.")
                continue
            elif category == "income":
                print("There is no need to add a key_word to income as all positive amounts will go into this group.")
                continue
            print("Here are the current key words for "+category)
            current_key_words = return_list("db/"+category+".csv")
            print(current_key_words)
            while True:
                new_key_word = input("What key words would you like to add? (Type done when finished) ").lower()
                if new_key_word == "done":
                    break
                else:
                    current_key_words.append(new_key_word)
            print("Here are the current key words for "+category)
            print(current_key_words)
            write_list_to_file(category+".csv",current_key_words)
        elif action == "Reset":
            reset()
        elif action == "Budget":
            budgets = set_budget(categories,budgets)
        elif action == "Finish":
            print("Thank you for using our application!")
            exit()



#headers = ["id", "name", "aisle", "department", "price"]

#new_header_info = [header for header in headers if header != "id"]


    #elif action == "Category":
    #    print("CREATING A CATEGORY")
    #    new_header = input("Please input new category:  ").title()
    #    expense_headers.append(new_header)
    #    print("CREATING A NEW CATEGORY", new_header)




if __name__ == "__main__": ## this will run only when this program is invoked from the command line. So if we run the reset function, it wont run the whole thing
    run()
