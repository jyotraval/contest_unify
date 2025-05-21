
# from datetime import datetime, timezone, timedelta
from datetime import datetime, timezone, timedelta
def normalize_time(timestamp):
    # Define UTC+5:30 timezone (indian time)
    ist_offset = timezone(timedelta(hours=5, minutes=30))

    # Convert timestamp to datetime in ISt
    dt_ist = datetime.fromtimestamp(timestamp, tz=ist_offset)

    # print("IST timing:", dt_ist, type(dt_ist))

    weekday_name = dt_ist.strftime("%A")
    # print("Weekday name:", weekday_name)

    # Extract date and time parts into a list
    dt_array = (
        dt_ist.year,
        dt_ist.month,
        dt_ist.day,
        dt_ist.hour,
        dt_ist.minute,
        dt_ist.second,
        weekday_name
    )
    
    return dt_array



import codeforce_api_data

codeforce_data= codeforce_api_data.fetch_api_data() # tuple of contest data --> dictionary
codeforce_db=dict()
for i in codeforce_data:
    phase=i['phase']
    if phase.lower()=='before':
        time_temp=normalize_time(i['startTimeSeconds'])
        #time_temp formate (YYYY, MM, DD, HH, MM, SS, Weekday)
        codeforce_db[i['id']]=(i['name'],time_temp)
# print(codeforce_data)
print(codeforce_db)
# print(len(codeforce_data)==len(codeforce_db))

