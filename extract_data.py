import pandas as pd
import gspread

gc = gspread.service_account(filename='creds.json')

def get_reqmnt_list():
    """Oxygen: State -> City -> Info
    Hospital Beds: State -> City -> Info
    Medicines: State -> Info
    Plasma: Type -> City
    Plasma (Organisations) -> Info
    Plasma (Donors) -> Blood Group -> Info"""
    
    reqmnt_list = ['Oxygen', 'Hospital Beds', 'Medicines', 'Plasma']
    return reqmnt_list

def get_plasma_type_list():
    plasma_type_list = ['Organisations', 'Donors']
    return plasma_type_list

def get_state_list(reqmnt):
    if (reqmnt == "Oxygen"):
        O = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
        O1=O.worksheet('Sheet For Users')
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[8:],columns=rows[7])
        df1=df[df['STATUS']=='Available']
        output_1=df1['STATE']
        output_1=output_1.drop_duplicates()
        return list(output_1)
    elif (reqmnt=="Hospital Beds"):
        O = gc.open_by_key('1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k')
        O1=O.worksheet('Sheet for Users')
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[7:],columns=rows[6])
        df1=df[df['Status']=='Beds Available']
        output_1=df1['State']
        output_1=output_1.drop_duplicates()
        return list(output_1)
    elif (reqmnt=='Medicines') :
        O=gc.open_by_key("17bc83Sjnakb5DgsEQ7-lRj30-JVrIjSCcQuvwxB4Bc0")
        O1=O.worksheet("Sheet for Users")
        rows=O1.get_all_values()
        df=pd.DataFrame.from_records(rows[11:],columns=rows[0]) 
        df = df.loc[:,~df.columns.duplicated(keep='last')]
        df2=df[df['Verification']=='Available']
        output_2=df2['State']
        output_2=output_2.drop_duplicates()
        return output_2

def get_city_list(reqmnt,state):
    if (reqmnt == "Oxygen" ):
        O = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
        O1=O.worksheet('Sheet For Users')
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
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[7:],columns=rows[6])
        df1=df[df['Status']=='Beds Available']
        df1=df1[df1['State']==state]
        output_2=df1['City']
        output_2=output_2.drop_duplicates()
        return list(output_2)

def get_plasma_city_list(type):
    O= gc.open_by_key("1cbxCbhLVRWBlyRmzKuEQ-0PG3fsSs6EMIR51d2OoCIg")
    if(type=="Organisations"):
        O1=O.worksheet('Organisations')
        rows=O1.get_all_values()
        df=pd.DataFrame.from_records(rows[7:78],columns=rows[6])
        output_1=df['LOCATION']
        output_1=output_1.drop_duplicates()
        return output_1
    else:
        O1=O.worksheet('Donors')
        rows=O1.get_all_values()
        df=pd.DataFrame.from_records(rows[1:],columns=rows[0])
        df1=df[df['Available']=='Available']
        output_2=df1['LOCATION']
        output_2=output_2.drop_duplicates()
        return output_2

def get_plasma_donor_bloodgrp_list(city):
    O= gc.open_by_key("1cbxCbhLVRWBlyRmzKuEQ-0PG3fsSs6EMIR51d2OoCIg")
    O1=O.worksheet('Donors')
    rows=O1.get_all_values()
    df=pd.DataFrame.from_records(rows[1:],columns=rows[0])
    df1=df[df['Available']=='Available']
    output_2=df1['LOCATION']
    output_2=output_2.drop_duplicates()
    df2=df1[df1['LOCATION']==city]
    output_2=df2['BLOOD GROUP']
    output_2=output_2.drop_duplicates()
    return output_2

def get_info(reqmnt,state,city):
    if (reqmnt == "Oxygen" ):
        O = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
        O1=O.worksheet('Sheet For Users')
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[8:],columns=rows[7])
        df1=df[df['STATUS']=='Available']
        df1=df1[df1['STATE']==state]
        df2=df1[df1['LOCATION (CITY)']==city]
        return df2
    elif (reqmnt=="Hospital Beds"):
        O = gc.open_by_key('1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k')
        O1=O.worksheet('Sheet for Users')
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[7:],columns=rows[6])
        df1=df[df['Status']=='Beds Available']
        df1=df1[df1['State']==state]
        df2=df1[df1['City']==city]
        return df2

def get_medicine_info(state):
    O=gc.open_by_key("17bc83Sjnakb5DgsEQ7-lRj30-JVrIjSCcQuvwxB4Bc0")
    O1=O.worksheet("Sheet for Users")
    rows=O1.get_all_values()
    df=pd.DataFrame.from_records(rows[11:],columns=rows[0]) 
    df = df.loc[:,~df.columns.duplicated(keep='last')]
    df2=df[df['Verification']=='Available']
    df2=df2[df2['State']==state]
    return df2

def get_plasma_org_info(city):
    O= gc.open_by_key("1cbxCbhLVRWBlyRmzKuEQ-0PG3fsSs6EMIR51d2OoCIg")
    O1=O.worksheet('Organisations')
    rows=O1.get_all_values()
    df=pd.DataFrame.from_records(rows[7:78],columns=rows[6])
    df1=df[df['LOCATION']==city]
    return df1

def get_plasma_donor_info(city, bloodgrp):
    O= gc.open_by_key("1cbxCbhLVRWBlyRmzKuEQ-0PG3fsSs6EMIR51d2OoCIg")
    O1=O.worksheet('Donors')
    rows=O1.get_all_values()
    df=pd.DataFrame.from_records(rows[1:],columns=rows[0])
    df1=df[df['Available']=='Available']
    
    df2=df1[df1['LOCATION']==city]
    df2=df2[df2['BLOOD GROUP']==bloodgrp]
    return df2
