import pandas as pd
import numpy as np
import math as m

from scipy.stats import norm

def pd_dataFrame(excel):
    
    global df
    
    df = pd.DataFrame(pd.read_excel(excel));
    
    # #for suppressing scientific notation of big values
    # pd.set_option('display.float_format', lambda x: '%.3f' % x)
    pd.options.mode.chained_assignment = None  # default='warn'
    # df.info()
    # #Handling missing values and renaming cols
    df.rename(columns={"Summary of transaction":"Summary_of_transaction"},inplace=True)
    df.rename(columns={"Transaction Date":"Transaction_Date"},inplace=True)
    df.fillna(value=0, inplace=True)
    
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
    
    # #sorting data
    df.sort_values(by=['CIF','Transaction_Date'],inplace=True)
    
    global avail_cust
    
    avail_cust = df['CIF'].drop_duplicates()
        
    global cust_df
    
    #new list for the parameters required in pod cal for each cust
    cust_df = pd.DataFrame(columns=['CIF','Face_val_loan','Rate','Time','Cust_Val','Volatility'])
    
    #final response to be sent
    global cust_response_df

    cust_response_df = pd.DataFrame(columns=['CIF','POD','Gambling','Amazon','Shopping','Food','Movie','CC_Bill'])

    for i in avail_cust:
          
        #seggregation of data
        df_contains_loan_trans = df[df.eval("Summary_of_transaction == 'Loan disburse' & CIF == @i")]
        df_contains_loan_return_trans = df[df.eval("Summary_of_transaction == 'Loan return' & CIF == @i")]
        df_contains_credit_limit = df[df.eval("Summary_of_transaction =='Credit Card Monthly limit' & CIF == @i")]
        cif_resp_df = df[df.eval("CIF == @i")]
        cif_resp_df.sort_index(axis=0,inplace=True)
          
        if(df_contains_loan_trans.empty | df_contains_loan_return_trans.empty):
            globals().update({'face':  df_contains_credit_limit.iloc[-1]['Credit'],'value': cif_resp_df.iloc[-1]['Balance'] - df_contains_credit_limit.iloc[-1]['Credit'],'time_val':0.00,'loan_rate':0.00})   
        else:
            latest_loan_date = df_contains_loan_trans.iloc[-1]['Transaction_Date']
            globals().update({'face': df_contains_loan_trans.iloc[-1]['Credit'] - df_contains_loan_return_trans[df_contains_loan_return_trans['Transaction_Date'] >= latest_loan_date]['Debit'].sum()+df_contains_credit_limit.iloc[-1]['Credit']
            ,'value':cif_resp_df.iloc[-1]['Balance'] - df_contains_credit_limit.iloc[-1]['Credit'] - df_contains_loan_trans.iloc[-1]['Credit']  + df_contains_loan_return_trans[df_contains_loan_return_trans['Transaction_Date'] >= latest_loan_date]['Debit'].sum()
            ,'time_val':float(df_contains_loan_trans.iloc[-1]['Tenure'].replace('Months',''))/12,'loan_rate':df_contains_loan_trans.iloc[-1]['Loan Rate']})
       
        cust_volatility = np.std(df[df.eval("CIF == @i")]['Balance'])/np.mean(df[df.eval("CIF == @i")]['Balance'])
        
        time_of_loan = (df_contains_credit_limit.iloc[-1]['Credit']/face)*0.08 + ((face-df_contains_credit_limit.iloc[-1]['Credit'])/face)*time_val
    
        cust_df.loc[-1]=[df_contains_credit_limit.iloc[-1]['CIF']] + [face]+[loan_rate]+[time_of_loan]+[value]+[cust_volatility]
        cust_df.index = cust_df.index + 1
        cust_df = cust_df.sort_index()
        
        return createResponse()


def cal_pod_of_cust(dframe):
    index=0
    pod=0
    while(index<len(dframe.index)):
        numerator_of_d1 = round((np.log(dframe.iloc[index]['Face_val_loan']/dframe.iloc[index]['Cust_Val']) - ( dframe.iloc[index]['Rate'] * dframe.iloc[index]['Time'] + (  (dframe.iloc[index]['Volatility'] ** 2) * (dframe.iloc[index]['Time'])*0.5   ))),2)
        deno_of_d1 = round((dframe.iloc[index]['Volatility'] * m.sqrt(dframe.iloc[index]['Time'])),2) 
#         print(numerator_of_d1)
#         print(deno_of_d1)
#         print(pod)
        pod = numerator_of_d1 / deno_of_d1  
        index+=1

    return round(norm.cdf(pod),2)

def createResponse():
    
    for cif in avail_cust:
        
        total_income = df[df.eval("CIF == @cif")]['Credit'].sum()
        cust_response_df.loc[-1] = [cif] + [ cal_pod_of_cust(cust_df[cust_df.eval("CIF == @cif")]) ] + [ (df.query('Summary_of_transaction == "Gambling"' )['Debit'].sum())/total_income ] + [ (df.query('Summary_of_transaction == "Amazon"' )['Debit'].sum())/total_income ] + [(df.query('Summary_of_transaction == "Shopping"' )['Debit'].sum())/total_income] + [ (df.query('Summary_of_transaction == "Food"' )['Debit'].sum())/total_income] + [ (df.query('Summary_of_transaction == "Movie"' )['Debit'].sum())/ total_income ] + [(df.query('Summary_of_transaction == "Credit Card Bill"' )['Debit'].sum())/total_income]
        cust_response_df.index = cust_response_df.index + 1
        cust_response_df.sort_index()
        cust_response_df.drop_duplicates(keep='first',inplace=True)
    return cust_response_df

    
