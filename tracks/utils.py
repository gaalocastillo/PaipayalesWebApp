from datetime import datetime

def convert_date(orig_date=datetime.now):
    d = orig_date.strftime("%m/%d/%Y, %H:%M:%S")
    #print(d)
    return d