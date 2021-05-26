import pandas as pd
import gspread
from search_google import *

gc = gspread.service_account(filename='creds.json')

sheet_1 = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
sheet_2 = gc.open_by_key('1SXBaISO7rlmxBkEhS7Gz98BtCQSJLs9JyV3RKDE4KEc')
oxygen_db_1 = sheet_1.worksheet('Sheet For Users')
oxygen_db_2 = sheet_2.worksheet('Sheet For Users')
rows_1 = oxygen_db_1.get_all_values()
rows_2=oxygen_db_2.get_all_values()
oxygen_df_1 = pd.DataFrame.from_records(rows_1[8:], columns=rows_1[7])
oxygen_df_2 = pd.DataFrame.from_records(rows_2[8:], columns=rows_2[7])
oxygen_df_2['ADDITIONAL INFO']=pd.NA
oxygen_data=[oxygen_df_1,oxygen_df_2]
oxygen_df=pd.concat(oxygen_data)
oxygen_df = oxygen_df[((oxygen_df['STATUS'] == 'Available')| (oxygen_df['STATUS']=='Needs Verification')) & pd.notna(oxygen_df['STATE']) & pd.notna(oxygen_df['LOCATION (CITY)'])]

oxygen_data=[oxygen_df['NAME'],oxygen_df['CONTACT NUMBER'],oxygen_df['STATE'],oxygen_df['LOCATION (CITY)'],oxygen_df['STATUS']
                                   ,oxygen_df['DATE AND TIME OF VERIFICATION (AUTOMATED; DO NOT EDIT)'],oxygen_df['ADDITIONAL INFO']]
# oxygen_data = oxygen_df[['NAME', 'CONTACT NUMBER', 'STATE', 'LOCATION (CITY)', 'STATUS', 'DATE AND TIME OF VERIFICATION (AUTOMATED; DO NOT EDIT)', 'ADDITIONAL INFO']]
# oxygen_data.rename(columns={'NAME': 'name', 'CONTACT NUMBER': 'contact', 'STATE': 'state', 'LOCATION (CITY)': 'city', 'STATUS': 'status', 'DATE AND TIME OF VERIFICATION (AUTOMATED; DO NOT EDIT)': 'date_time', 'ADDITIONAL INFO': 'info'})
headers = ["name", "contact","state","city","status","date_time","info"]
oxygen_df_final = pd.concat(oxygen_data, axis=1, keys=headers)
oxygen_df_final = oxygen_df_final.reset_index(drop=True)
oxygen_df_final.loc[:, 'state'] = oxygen_df_final['state'].apply(lambda x: search(x, 'state'))
oxygen_df_final.loc[:, 'city'] = oxygen_df_final['city'].apply(lambda x: search(x, 'city'))


sheet_1 = gc.open_by_key('1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k')
sheet_2 = gc.open_by_key('1yZGlGJ0OWMAiwTXQ3R2PIJhiBrl8EzQKL-ba4RjlGos')
hospital_bed_db_1 = sheet_1.worksheet('Sheet for Users')
hospital_bed_db_2 = sheet_2.worksheet('Sheet For Users')

rows_1 = hospital_bed_db_1.get_all_values()
rows_2=hospital_bed_db_2.get_all_values()
hospital_bed_df_1 = pd.DataFrame.from_records(rows_1[7:], columns=rows_1[6])
hospital_bed_df_2 = pd.DataFrame.from_records(rows_2[4:], columns=rows_2[3])
hospital_bed_df_1 = hospital_bed_df_1[((hospital_bed_df_1['Status'] == 'Beds Available') | (hospital_bed_df_1['Status'] == 'Home Setup') | (hospital_bed_df_1['Status'] == 'Call to check soon')) 
                    & pd.notna(hospital_bed_df_1['State']) & pd.notna(hospital_bed_df_1['City'])]
               
hospital_bed_df_2 = hospital_bed_df_2[((hospital_bed_df_2['Status'] == 'Available') | (hospital_bed_df_2['Status'] == 'Needs Verification') ) 
                     & pd.notna(hospital_bed_df_2['State']) & pd.notna(hospital_bed_df_2['City'])]
                  
hospital_bed_data_1=[hospital_bed_df_1['Name of Hospital'],hospital_bed_df_1['Phone Number'],hospital_bed_df_1['State'],hospital_bed_df_1['City']
                     , hospital_bed_df_1['Status'],hospital_bed_df_1['Time of Verification (hh:mm AM/PM)'],hospital_bed_df_1['Special Notes']]
headers_1=["name","contact","state","city","status","date_time","info"]
hospital_bed_df_2['Special Notes']=pd.NA
hospital_bed_data_2=[hospital_bed_df_2['Name of Hospital'],hospital_bed_df_2['Phone Number'],hospital_bed_df_2['City'],hospital_bed_df_2['State']
                       , hospital_bed_df_2['Status'],hospital_bed_df_2.iloc[:,5],hospital_bed_df_2['Special Notes']]
hospital_bed_df_1_change_header = pd.concat(hospital_bed_data_1, axis=1, keys=headers_1)

hospital_bed_df_2_change_header = pd.concat(hospital_bed_data_2, axis=1, keys=headers_1)
hospital_bed_data = [hospital_bed_df_2_change_header,hospital_bed_df_1_change_header]

hospital_bed_df_final=pd.concat([hospital_bed_df_1_change_header, hospital_bed_df_2_change_header],ignore_index=True)[hospital_bed_df_1_change_header.columns]

hospital_bed_df_final.loc[:, 'state'] = hospital_bed_df_final['state'].apply(lambda x: search(x, 'state'))
hospital_bed_df_final.loc[:, 'city'] = hospital_bed_df_final['city'].apply(lambda x: search(x, 'city'))     


sheet_1 = gc.open_by_key("17bc83Sjnakb5DgsEQ7-lRj30-JVrIjSCcQuvwxB4Bc0")
sheet_2 = gc.open_by_key("1QHHA2p-WSSsx7-F1_6v0TvF0fEKPx74h7B2UkkErnyQ")
medicine_db_1 = sheet_1.worksheet("Sheet for Users")
medicine_db_2 = sheet_2.worksheet("Sheet For Users")
rows_1 = medicine_db_1.get_all_values()
rows_2 = medicine_db_2.get_all_values()
medicine_df_1 = pd.DataFrame.from_records(rows_1[11:], columns=rows_1[0])
medicine_df_2 = pd.DataFrame.from_records(rows_2[4:],columns=rows_2[3])
medicine_df_1 = medicine_df_1.loc[:, ~medicine_df_1.columns.duplicated(keep='last')]
medicine_df_1 = medicine_df_1[(medicine_df_1['Verification'] == 'Available') & pd.notna(medicine_df_1['State'])]
medicine_df_2 = medicine_df_2[((medicine_df_2['STATUS']=='Available') | (medicine_df_2['STATUS']=='Needs Verification')) & 
                                pd.notna(medicine_df_2['STATE']) & pd.notna(medicine_df_2['      LOCATION (CITY)'])]
medicine_data_1 = [medicine_df_1['Name'],medicine_df_1['Contact'],medicine_df_1['State'],medicine_df_1['Location'],medicine_df_1['Verification'],
                         medicine_df_1['Time'],medicine_df_1['Medicine']]
medicine_data_2 = [medicine_df_2['NAME'],medicine_df_2['CONTACT NO'],medicine_df_2['STATE'],medicine_df_2['      LOCATION (CITY)'],medicine_df_2['STATUS'],medicine_df_2['VERIFIED DATE AND TIME'],medicine_df_2['TYPE OF MEDICINE     ']]   
headers = ["name", "contact","state","city","status","date_time","info"]
medicine_df_1_change_header = pd.concat(medicine_data_1,axis=1,keys=headers)
medicine_df_2_change_header = pd.concat(medicine_data_2,axis=1,keys=headers)
medicine_df_final = pd.concat([medicine_df_1_change_header,medicine_df_2_change_header])                                       
medicine_df_final.loc[:, 'state'] = medicine_df_final['state'].apply(lambda x: search(x, 'state'))


sheet = gc.open_by_key("1cbxCbhLVRWBlyRmzKuEQ-0PG3fsSs6EMIR51d2OoCIg")
plasma_org = sheet.worksheet('Organisations')
plasma_donor = sheet.worksheet('Donors')

rows = plasma_org.get_all_values()
plasma_org_df = pd.DataFrame.from_records(rows[7:89], columns=rows[6])
plasma_org_df = plasma_org_df[pd.notna(plasma_org_df['LOCATION'])]
plasma_org_data=[plasma_org_df['NAME'],plasma_org_df['CONTACT NUMBER'],plasma_org_df['LOCATION'],plasma_org_df['AVAILIBILITY']
                      ,plasma_org_df['TIME & DATE VERIFIED'],plasma_org_df['Additional Info']]
headers = ["name", "contact","city","status","date_time","info"]
plasma_org_final = pd.concat(plasma_org_data,axis=1,keys=headers)                     
plasma_org_final.loc[:, 'city'] = plasma_org_final['city'].apply(lambda x: search(x, 'city'))


rows = plasma_donor.get_all_values()
plasma_donor_df = pd.DataFrame.from_records(rows[1:], columns=rows[0])
plasma_donor_df = plasma_donor_df[((plasma_donor_df['Available'] == 'Available')|(plasma_donor_df['Available']=='Busy/ Ringing')) & pd.notna(plasma_donor_df['LOCATION'])]
plasma_donor_data = [plasma_donor_df['NAME'],plasma_donor_df['CONTACT NUMBER'],plasma_donor_df['LOCATION'],
                     plasma_donor_df['BLOOD GROUP'],plasma_donor_df['Available'],plasma_donor_df.iloc[:,7],plasma_donor_df['Additional Information/ Co-morbidity']]
headers = ["name", "contact","city","bloodgrp","status","date_time","info"]  
plasma_donor_final=pd.concat(plasma_donor_data,axis=1,keys=headers)
plasma_donor_final.loc[:, 'city'] = plasma_donor_final['city'].apply(lambda x: search(x, 'city'))


oxygen_df_final.to_csv('data/oxygen_df.csv', index=False)
hospital_bed_df_final.to_csv('data/hospital_bed_df.csv', index=False)
medicine_df_final.to_csv('data/medicine_df.csv', index=False)
plasma_org_final.to_csv('data/plasma_org_df.csv', index=False)
plasma_donor_final.to_csv('data/plasma_donor_df.csv', index=False)
