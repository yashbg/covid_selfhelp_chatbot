import pandas as pd
import gspread
from oauth2client.client import GoogleCredentials

gc = gspread.authorize(GoogleCredentials.get_application_default())

def get_reqmnt_list():
    pass

def get_state_list(reqmnt):
    pass

def get_city_list(state):
    pass

def query(type1,place,state):
    if(type1 == "Oxygen" ):
        O = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
        O1=O.worksheet('Sheet For Users')
        # get_all_values gives a list of rows.
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[8:],columns=rows[7])
        df1=df[df['STATE']==state]
        df1=df1[df1['STATUS']=='Available']
        if(len(df1)==0):
            print("no available oxygen centres")
        else:
            df2=df1[df1['LOCATION (CITY)']==place]
            if(len(df2)==0):
                print("no data found for your city..But some of the data of your state are")
                print(df1.head(5))
            else:
                print(df2.head(5))
    elif (type1=="Hospital Beds"):
        O = gc.open_by_key('1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k')
        O1=O.worksheet('Sheet for Users')
        # get_all_values gives a list of rows.
        rows = O1.get_all_values()
        df=pd.DataFrame.from_records(rows[7:],columns=rows[6])
        df1=df[df['State']==state]
        df1=df1[df1['Status']=='Beds Available']
        if(len(df1)==0):
            print("no available beds")
        else:
            df2=df1[df1['City']==place]
            if(len(df2)==0):
                print("no data found for your city..But some of the data of your state are")
                print(df1.head(5))
            else:
                print(df2.head(5))
    elif (type1=="Plasma"):
        O= gc.open_by_key("1cbxCbhLVRWBlyRmzKuEQ-0PG3fsSs6EMIR51d2OoCIg")
        print("Please specify for what you are searching for Organisations or Donors")
        k=input()
        if(k=="Organisations"):
            O1=O.worksheet('Organisations')
            rows=O1.get_all_values()
            df=pd.DataFrame.from_records(rows[7:],columns=rows[6])
            df1=df[df['AVAILIBILITY']=='IN STOCK']
            if(len(df1)==0):
                print("No organisation have stock of plasma")
            else:
                print(df1.head(2))
        else:
            O1=O.worksheet('Donors')
            rows=O1.get_all_values()
            df=pd.DataFrame.from_records(rows[1:],columns=rows[0])
            df1=df[df['Available']=='Available']
            if(len(df1)==0):
                print("Not Available")
            else:
                df2=df1[df1['LOCATION']==place]
                if(len(df2)==0):
                    print(df1.head(2))
                else:
                    print(df2.head(2))
    elif (type1=='Medicines') :
        O=gc.open_by_key("17bc83Sjnakb5DgsEQ7-lRj30-JVrIjSCcQuvwxB4Bc0")
        O1=O.worksheet("Sheet for Users")
        rows=O1.get_all_values()
        df=pd.DataFrame.from_records(rows[11:],columns=rows[0]) 
        df = df.loc[:,~df.columns.duplicated(keep='last')]
        df1=df[df['State']==state]
        # print(df1['Verification'])
        # print(df[df.index.duplicated()])
        df2=df[df['Verification']=='Available']
        if(len(df2)==0):
            print("No Data Found")
        else:
            # k=input("Medicine Required")
            print(df2.head(5))
