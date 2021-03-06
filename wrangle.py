import pandas as pd 
import numpy as np
import os 
from env import username, host, password
from sklearn.model_selection import train_test_split

#Telco
#get connection to database
def get_connection(db, username=username, host=host, password=password):
    '''
    Creates a connection URL
    '''
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'

def new_telco_charge_data():
    '''
    Returns telco_charge into a dataframe
    '''
    sql_query = '''select customer_id, monthly_charges, tenure, total_charges from customers
    join internet_service_types using(internet_service_type_id)
    join contract_types using(contract_type_id)
    join payment_types using(payment_type_id)
    where contract_type_id = 3'''
    df = pd.read_sql(sql_query, get_connection('telco_churn'))
    return df 

def get_telco_charge_data():
    '''get connection, returns telco_charge into a dataframe and creates a csv for us'''
    if os.path.isfile('telco_charge.csv'):
        df = pd.read_csv('telco_charge.csv', index_col=0)
    else:
        df = new_telco_charge_data()
        df.to_csv('telco_charge.csv')
    return df

def clean_telco(df):
    '''cleans our data'''
    df = df.replace(r'^\s*$', np.NaN, regex=True)
    df.total_charges = pd.to_numeric(df.total_charges, errors='coerce').astype('float64')
    df.total_charges = df.total_charges.fillna(value=df.total_charges.mean()).astype('float64')
    df = df.set_index("customer_id")
    return df 


def split_telco(df):
    '''
    Takes in a cleaned df of telco data and splits the data appropriatly into train, validate, and test.
    '''
    
    train_val, test = train_test_split(df, train_size =  0.8, random_state = 123)
    train, validate = train_test_split(train_val, train_size =  0.7, random_state = 123)
    return train, validate, test

def wrangle_telco():
    '''acquire and our dataframe, returns a df'''
    df = clean_telco(get_telco_charge_data())
    return df


def wrangle_split_telco():
    '''acquire, clean, split our dataframe'''
    df = clean_telco(get_telco_charge_data())
    return split_telco(df)

#Zillow

def new_zillow():
    sql_query ='''select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips from properties_2017
 	join propertylandusetype using(propertylandusetypeid)
 	where propertylandusetypeid = 261'''
    df = pd.read_sql(sql_query, get_connection('zillow'))
    return df 

def get_zillow_data():
    '''get connection, returns Zillow into a dataframe and creates a csv for us'''
    if os.path.isfile('zillow.csv'):
        df = pd.read_csv('zillow.csv', index_col=0)
    else:
        df = new_zillow()
        df.to_csv('zillow.csv')
    return df