import datetime
import random

def generate_a_receipt_number(business_name,total_amount):
    '''Generate a unique receipt number '''
    current_time=datetime.datetime.now().time()
    sqstring = str(business_name)+str(total_amount)+str(current_time)
    sqlist =list(sqstring)
    random.shuffle(sqlist)
    sqstring=str(sqlist).replace(':','').replace('\'','').replace(',','').replace(' ','').replace('.','').\
            replace('[','').replace(']','')
    return sqstring