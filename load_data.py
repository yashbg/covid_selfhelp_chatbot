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
    return sorted(reqmnt_list)

def get_plasma_type_list():
    plasma_type_list = ['Organisations', 'Donors']
    return sorted(plasma_type_list)

def get_state_list(reqmnt):
    if reqmnt == "Oxygen":
        output = oxygen_df['state']
        output = output.drop_duplicates()
        output = [str(item) for item in list(output)]
        return sorted(output)
    elif reqmnt == "Hospital Beds":
        output = hospital_bed_df['state']
        output = output.drop_duplicates()
        output = [str(item) for item in list(output)]
        return sorted(output)
    elif reqmnt == 'Medicines':
        output = medicine_df['state']
        output = output.drop_duplicates()
        output = [str(item) for item in list(output)]
        return sorted(output)

def get_city_list(reqmnt, state):
    if reqmnt == "Oxygen":
        df = oxygen_df[oxygen_df['state'] == state]
        output = df['city']
        output = output.drop_duplicates()
        output = list(output)
        if state == 'Delhi':
            if 'Gurugram Golf Course Ext Road, Opp W Pratiksha Hospital, Gurgaon - 122022 Haryana' in output:
                output.remove('Gurugram Golf Course Ext Road, Opp W Pratiksha Hospital, Gurgaon - 122022 Haryana')
        if state == 'Uttar Pradesh':
            if 'Shree Maa Enterprises, Madhav Complex, Alambagh, Lucknow' in output:
                output.remove('Shree Maa Enterprises, Madhav Complex, Alambagh, Lucknow')
        output = [str(item) for item in list(output)]
        return sorted(output)
    elif reqmnt == "Hospital Beds":
        df = hospital_bed_df[hospital_bed_df['state'] == state]
        output = df['city']
        output = output.drop_duplicates()
        output = [str(item) for item in list(output)]
        return sorted(output)

def get_plasma_city_list(type):
    if type == "Organisations":
        output = plasma_org_df['city']
        output = output.drop_duplicates()
        output = list(output)
        if 'Kurukshetr, Haryana or Jirkpur (Punjab)' in output:
            output.remove('Kurukshetr, Haryana or Jirkpur (Punjab)')
        output = [str(item) for item in list(output)]
        return sorted(output)
    else:
        output = plasma_donor_df['city']
        output = output.drop_duplicates()
        output = [str(item) for item in list(output)]
        return sorted(output)

def get_plasma_donor_bloodgrp_list(city):
    df = plasma_donor_df[plasma_donor_df['city'] == city]
    output = df['bloodgrp']
    output = output.drop_duplicates()
    output = [str(item) for item in list(output)]
    return sorted(output)

def get_info(reqmnt, state, city):
    if reqmnt == "Oxygen":
        df1 = oxygen_df[oxygen_df['state'] == state]
        df2 = df1[df1['city'] == city]
        return df2
    elif reqmnt == "Hospital Beds":
        df1 = hospital_bed_df[hospital_bed_df['state'] == state]
        df2 = df1[df1['city'] == city]
        return df2

def get_medicine_info(state):
    df = medicine_df[medicine_df['state'] == state]
    return df

def get_plasma_org_info(city):
    df = plasma_org_df[plasma_org_df['city'] == city]
    return df

def get_plasma_donor_info(city, bloodgrp):
    df =plasma_donor_df[plasma_donor_df['city'] == city]
    df = df[df['bloodgrp'] == bloodgrp]
    return df
