import pandas as pd
import gspread
from search_google import *

gc = gspread.service_account(filename='creds.json')

sheet = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
oxygen_db = sheet.worksheet('Sheet For Users')
rows = oxygen_db.get_all_values()
oxygen_df = pd.DataFrame.from_records(rows[8:], columns=rows[7])
oxygen_df = oxygen_df[(oxygen_df['STATUS'] == 'Available') & (oxygen_df['STATE'] != '') & (oxygen_df['LOCATION (CITY)'] != '')]
oxygen_df.loc[:, 'STATE'] = oxygen_df['STATE'].apply(lambda x: search(x, 'state'))
oxygen_df.loc[:, 'LOCATION (CITY)'] = oxygen_df['LOCATION (CITY)'].apply(lambda x: search(x, 'city'))

sheet = gc.open_by_key('1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k')
hospital_bed_db = sheet.worksheet('Sheet for Users')
rows = hospital_bed_db.get_all_values()
hospital_bed_df = pd.DataFrame.from_records(rows[7:], columns=rows[6])
hospital_bed_df = hospital_bed_df[(hospital_bed_df['Status'] == 'Beds Available') & (hospital_bed_df['State'] != '') & (hospital_bed_df['City'] != '')]
hospital_bed_df.loc[:, 'State'] = hospital_bed_df['State'].apply(lambda x: search(x, 'state'))
hospital_bed_df.loc[:, 'City'] = hospital_bed_df['City'].apply(lambda x: search(x, 'city'))

sheet = gc.open_by_key("17bc83Sjnakb5DgsEQ7-lRj30-JVrIjSCcQuvwxB4Bc0")
medicine_db = sheet.worksheet("Sheet for Users")
rows = medicine_db.get_all_values()
rows = medicine_db.get_all_values()
medicine_df = pd.DataFrame.from_records(rows[11:], columns=rows[0]) 
medicine_df = medicine_df.loc[:, ~medicine_df.columns.duplicated(keep='last')]
medicine_df = medicine_df[(medicine_df['Verification'] == 'Available') & (medicine_df['State'] != '')]
medicine_df.loc[:, 'State'] = medicine_df['State'].apply(lambda x: search(x, 'state'))

sheet = gc.open_by_key("1cbxCbhLVRWBlyRmzKuEQ-0PG3fsSs6EMIR51d2OoCIg")
plasma_org = sheet.worksheet('Organisations')
plasma_donor = sheet.worksheet('Donors')

rows = plasma_org.get_all_values()
plasma_org_df = pd.DataFrame.from_records(rows[7:89], columns=rows[6])
plasma_org_df = plasma_org_df[plasma_org_df['LOCATION'] != '']
plasma_org_df.loc[:, 'LOCATION'] = plasma_org_df['LOCATION'].apply(lambda x: search(x, 'city'))

rows = plasma_donor.get_all_values()
plasma_donor_df = pd.DataFrame.from_records(rows[1:], columns=rows[0])
plasma_donor_df = plasma_donor_df[(plasma_donor_df['Available'] == 'Available') & (plasma_donor_df['LOCATION'] != '')]
plasma_donor_df.loc[:, 'LOCATION'] = plasma_donor_df['LOCATION'].apply(lambda x: search(x, 'city'))

oxygen_df.to_csv('data/oxygen_df.csv', index=False)
hospital_bed_df.to_csv('data/hospital_bed_df.csv', index=False)
medicine_df.to_csv('data/medicine_df.csv', index=False)
plasma_org_df.to_csv('data/plasma_org_df.csv', index=False)
plasma_donor_df.to_csv('data/plasma_donor_df.csv', index=False)
