import pandas as pd

def clean_scooter_data_ex05_03(df):
    print()
    print("Performing all cleaning operations on the e-scooter dataset...")

    # Drop unnecessary columns
    df.drop(columns=['region_id'], inplace=True)

    # Drop rows where 'start_location_name' is null
    # df.dropna(subset=['start_location_name'], inplace=True)

    # Drop columns with more than 25% null values
    thresh = int(len(df) * 0.25)
    df.dropna(axis=1, thresh=thresh, inplace=True)

    # Fill null values with specified defaults
    fill_values = {
        'DURATION': '00:00:00',
        'start_location_name': 'Start St.',
        'end_location_name': 'Stop St.'
    }
    df.fillna(value=fill_values, inplace=True)

    # Drop rows where both 'start_location_name' and 'end_location_name' are null
    to_drop = df[(df['start_location_name'].isnull()) & (df['end_location_name'].isnull())]
    df.drop(index=to_drop.index, inplace=True)

    # Drop rows where 'month' is 'May'
    df = df[df['month'] != 'May']

    # df.reset_index(drop=True, inplace=True)

    print("Done")
    print()

    return df

def modify_scooter_data_ex05_04(df):
    """
    Modify and process the e-scooter dataset by performing the following steps:
    - Clean column names
    - Standardize column values
    - Add and modify columns
    - Split and process date and time columns
    - Filter data based on conditions

    Parameters:
    df (pd.DataFrame): The input DataFrame to modify.

    Returns:
    pd.DataFrame: The modified DataFrame.
    """
    print()
    print("Modify-Column processes on the e-scooter dataset...")

    # Make all column names lowercase
    df.columns = [x.lower() for x in df.columns]

    # Rename specific columns for clarity
    df.rename(columns={'duration': 'trip_duration', 'trip_ledger_id': 'trip_ledger'}, inplace=True)

    # Make all values in the 'month' column uppercase
    df['month'] = df['month'].str.upper()

    # Add a column based on a condition using loc
    df['special_trip'] = 'No'
    df.loc[df['trip_id'] == 1613335, 'special_trip'] = 'Yes'

    # Split 'started_at' into 'date' and 'time'
    new = df['started_at'].str.split(expand=True)
    df['date'], df['time'] = new[0], new[1]

    # Convert 'started_at' to datetime
    df['started_at'] = pd.to_datetime(df['started_at'], format='%m/%d/%Y %H:%M')

    print("Done")
    print()
    
    return df