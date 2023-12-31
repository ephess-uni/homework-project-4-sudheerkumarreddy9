# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date in old_dates:
        new_dates.append(datetime.strptime(date,'%Y-%m-%d').strftime('%d %b %Y'))
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(n,int) or not isinstance(start,str):
        raise TypeError
    dates_list = []
    for i in range(0,n):
        dates_list.append(datetime.strptime(start,'%Y-%m-%d') + timedelta(days=i))
    return dates_list
        


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates_list = []
    for pos,val in enumerate(values):
        dates_list.append((datetime.strptime(start_date,'%Y-%m-%d') + timedelta(days=pos),val))
    return dates_list


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile) as f:
        li = []
        dictreader_obj = DictReader(f)
        for  item in dictreader_obj:
            new_dict = {}
            days_obj = datetime.strptime(item['date_returned'],'%m/%d/%Y') -  datetime.strptime(item['date_due'],'%m/%d/%Y')
            if days_obj.days > 0:
                amount = days_obj.days * 0.25
                new_dict['patron_id'] = item['patron_id']
                new_dict['late_fees'] = round(amount,2)
                li.append(new_dict)
            else:
                new_dict['patron_id'] = item['patron_id']
                new_dict['late_fees'] = float(0)
                li.append(new_dict)
                
        aggregated_data = {}
        for i in li:
            key = i['patron_id']
            aggregated_data[key] =  aggregated_data.get(key,0) + i['late_fees']
        tax = [{'patron_id':key, 'late_fees':value} for key,value in aggregated_data.items()]
        for di in tax:
            for k,v in di.items():
                if k == 'late_fees':
                    if len(str(v).split('.')[-1]) != 2:
                        di[k] = str(v) +'0'
                
        with open(outfile,'w',newline='') as file:
            writer = DictWriter(file,['patron_id','late_fees'])
            writer.writeheader()
            writer.writerows(tax)
    


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
