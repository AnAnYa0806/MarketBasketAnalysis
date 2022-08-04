from csv import excel
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#Reading Data From Web
#myretaildata = pd.read_excel('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx')
#myretaildata.head()

def process_excel(myretaildata):
    #Data Cleaning
    myretaildata['Description'] = myretaildata['Description'].str.strip() #removes spaces from beginning and end
    myretaildata.dropna(axis=0, subset=['InvoiceNo'], inplace=True) #removes duplicate invoice
    myretaildata['InvoiceNo'] = myretaildata['InvoiceNo'].astype('str') #converting invoice number to be string
    myretaildata = myretaildata[~myretaildata['InvoiceNo'].str.contains('C')] #remove the credit transactions 
    myretaildata.head()

    myretaildata['Country'].value_counts()
    #myretaildata.shape

    #Separating transactions for Germany
    mybasket = (myretaildata[myretaildata['Country'] =="Germany"]
            .groupby(['InvoiceNo', 'Description'])['Quantity']
            .sum().unstack().reset_index().fillna(0)
            .set_index('InvoiceNo'))

            #viewing transaction basket
    mybasket.head()

    #converting all positive vaues to 1 and everything else to 0
    def my_encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    my_basket_sets = mybasket.applymap(my_encode_units)
    my_basket_sets.drop('POSTAGE', inplace=True, axis=1) #Remove "postage" as an item

    #Generatig frequent itemsets
    my_frequent_itemsets = apriori(my_basket_sets, min_support=0.07, use_colnames=True)

    #generating rules
    my_rules = association_rules(my_frequent_itemsets, metric="lift", min_threshold=1)

    #viewing top 100 rules
    my_rules.head(100)

    my_basket_sets['ROUND SNACK BOXES SET OF4 WOODLAND'].sum()

    my_basket_sets['SPACEBOY LUNCH BOX'].sum()

    res = my_rules[ (my_rules['lift'] >= 3) &
        (my_rules['confidence'] >= 0.3) ]

    res.to_csv("./conviction.csv")
       
