import pandas as pd
import gspread

gc = gspread.service_account(filename='creds.json')

def get_reqmnt_list():
    reqmnt_list = ['Oxygen', 'Hospital Beds']
    return reqmnt_list

def get_state_list(reqmnt):
    if (reqmnt == "Oxygen"):
        O = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
        O1=O.worksheet('Sheet For Users')
        # get_all_values gives a list of rows.
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[8:],columns=rows[7])
        df1=df[df['STATUS']=='Available']
        output_1=df1['STATE']
        output_1=output_1.drop_duplicates()
        return list(output_1)
    elif (reqmnt=="Hospital Beds"):
        O = gc.open_by_key('1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k')
        O1=O.worksheet('Sheet for Users')
        # get_all_values gives a list of rows.
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[7:],columns=rows[6])
        df1=df[df['Status']=='Beds Available']
        output_1=df1['State']
        output_1=output_1.drop_duplicates()
        return list(output_1)

def get_city_list(reqmnt,state):
    if (reqmnt == "Oxygen" ):
        O = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
        O1=O.worksheet('Sheet For Users')
        # get_all_values gives a list of rows.
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[8:],columns=rows[7])
        df1=df[df['STATUS']=='Available']
        df1=df1[df1['STATE']==state]
        output_2=df1['LOCATION (CITY)']
        output_2=output_2.drop_duplicates()
        return list(output_2)
    elif (reqmnt=="Hospital Beds"):
        O = gc.open_by_key('1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k')
        O1=O.worksheet('Sheet for Users')
        # get_all_values gives a list of rows.
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[7:],columns=rows[6])
        df1=df[df['Status']=='Beds Available']
        df1=df1[df1['State']==state]
        output_2=df1['City']
        output_2=output_2.drop_duplicates()
        return list(output_2)

def get_info(reqmnt,state,city):
    if (reqmnt == "Oxygen" ):
        O = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
        O1=O.worksheet('Sheet For Users')
        # get_all_values gives a list of rows.
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[8:],columns=rows[7])
        df1=df[df['STATUS']=='Available']
        df1=df1[df1['STATE']==state]
        df2=df1[df1['LOCATION (CITY)']==city]
        return df2
    elif (reqmnt=="Hospital Beds"):
        O = gc.open_by_key('1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k')
        O1=O.worksheet('Sheet for Users')
        # get_all_values gives a list of rows.
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[7:],columns=rows[6])
        df1=df[df['Status']=='Beds Available']
        df1=df1[df1['State']==state]
        df2=df1[df1['City']==city]
        return df2
