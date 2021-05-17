import pandas as pd
from search_google import *

oxygen_df = pd.read_csv('data/oxygen_df.csv')
hospital_bed_df = pd.read_csv('data/hospital_bed_df.csv')
medicine_df = pd.read_csv('data/medicine_df.csv')
plasma_org_df = pd.read_csv('data/plasma_org_df.csv')
plasma_donor_df = pd.read_csv('data/plasma_donor_df.csv')

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
    if reqmnt == "Oxygen":
        output = oxygen_df['STATE']
        output = output.drop_duplicates()
        return list(output)
    elif reqmnt == "Hospital Beds":
        output = hospital_bed_df['State']
        output = output.drop_duplicates()
        return list(output)
    elif reqmnt == 'Medicines':
        output = medicine_df['State']
        output = output.drop_duplicates()
        return output

def get_city_list(reqmnt, state):
    if reqmnt == "Oxygen":
        df = oxygen_df[oxygen_df['STATE'] == state]
        output = df['LOCATION (CITY)']
        output = output.drop_duplicates()
        return list(output)
    elif reqmnt == "Hospital Beds":
        df = hospital_bed_df[hospital_bed_df['State'] == state]
        output = df['City']
        output = output.drop_duplicates()
        return list(output)

def get_plasma_city_list(type):
    if type == "Organisations":
        output = plasma_org_df['LOCATION']
        output = output.drop_duplicates()
        return output
    else:
        output = plasma_donor_df['LOCATION']
        output = output.drop_duplicates()
        return output

def get_plasma_donor_bloodgrp_list(city):
    df = plasma_donor_df[plasma_donor_df['LOCATION'] == city]
    output = df['BLOOD GROUP']
    output = output.drop_duplicates()
    return output

def get_info(reqmnt, state, city):
    if reqmnt == "Oxygen":
        df1 = oxygen_df[oxygen_df['STATE'] == state]
        df2 = df1[df1['LOCATION (CITY)'] == city]
        return df2
    elif reqmnt == "Hospital Beds":
        df1 = hospital_bed_df[hospital_bed_df['State'] == state]
        df2 = df1[df1['City'] == city]
        return df2

def get_medicine_info(state):
    df = medicine_df[medicine_df['State'] == state]
    return df

def get_plasma_org_info(city):
    df = plasma_org_df[plasma_org_df['LOCATION'] == city]
    return df

def get_plasma_donor_info(city, bloodgrp):
    df =plasma_donor_df[plasma_donor_df['LOCATION'] == city]
    df = df[df['BLOOD GROUP'] == bloodgrp]
    return df
