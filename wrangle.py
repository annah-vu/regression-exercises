import pandas as pd 
import numpy as np
import os 
from env import username, host, password

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
    where contract_type_id = 2'''
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

def wrangle_telco():
    '''acquire and clean our dataframe'''
    df = get_telco_charge_data()
    df = df.replace(r'^\s*$', np.NaN, regex=True)
    df.total_charges = pd.to_numeric(df.total_charges, errors='coerce').astype('float64')
    df.total_charges = df.total_charges.fillna(value=df.total_charges.mean()).astype('float64')
    return df 

