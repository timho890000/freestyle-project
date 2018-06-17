# Project Planning

## Problem Statement
Primary User: Individuals with a high volume of expenses that are higher than expected, but no time to keep track of them all

User's Needs: An easy way to see what the user is spending on, and how much in total for a certain category, this way spending can show some constraint going forward.

Application: The application would give a quick easy summary of how much spending a person does over a certain time period for a certain category. It will also tell the user how much more he should spend to be in line of his goal.

Functionality: The application should retrieve data from the user's financial institutions and organize them in way to provide user with useful information. Then the program should give recommendations.

Improvements: Instead of needing to log into each account, and sorting/added up transactions to get you what you want, the app can easily do all that and spit out a recommendation for you to either show some spending restraint, or be free to spend more.

## Information Requirements

### Information Inputs

Inputs: User inputs would include a date range, a financial instituion, or a category of spending that you want to analyze (or all               categories!)
        Data inputs include transaction data from user's financial institutions such as credit card companies and banks.
        This information will come from Buxfer.com, which is a website that you can link all your financial institution accounts to. You         can also upload statements individually to analyze.
        All information will be dollar amounts, as expenses are all going to be in USD.
        There may be some initial setup required, such as logging into your bank account, or putting in a statement.

### Information Outputs

Outputs:Outputs would be in the format of US dollars and strings (such as the category of spending)
        It will take data, most likely use a sum function, or a division function (to find % of budget left) and spit out a relevant             number.

## Technology Requirements

### APIs and Web Service Requirements


I would use the Buxfer APIP (https://www.buxfer.com/help/api)

It would be used to grab financial data from the user's institutions which can be used to do the analysis.

I have not looked deep into the documentatin nor have I tried using them, but a quick glance seems to be very straightforward 

information.

### Python Package Requirements

Third party Python package:

The Requests package will be used to to grab information from the website.

The Pytest package may be used to test the program.

pip install requests

pip install Pytest


### Hardware Requirements

I will be running the program on my own local computer, as I do not know how to do it on a public server yet.
