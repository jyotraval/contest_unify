

import codeforce_api_data
import leetcode_api_data
import codechef_api_data
import hackearth_api_data
import atcoder_web_scrap

def data_to_insert(codeforce = False, leetcode = False, codechef = False, hackearth = False, atcoder=False, all=True):
    data_db=dict()
    if all or codeforce:
        data_db['codeforce'] = codeforce_api_data.fetch_codeforce_api_data()

    # print(data_db)
    if all or leetcode:
        data_db['leetcode'] = leetcode_api_data.fetch_leetcode_contests()
    # print(data_db)
    if all or codechef:
        data_db['codechef']=codechef_api_data.fetch_codechef_contests()

    if all or hackearth:
        data_db['hackearth']=hackearth_api_data.fetch_hackerath_api_contest()
    
    if all or atcoder:
        data_db['atcoder']=atcoder_web_scrap.fetch_atcoder_contests()


    return data_db

def contest_site_info():
    print(('codeforce', 'leetcode', 'codechef', 'hackearth'))
    return None

###########################################
#############################################
################ database ops ###################
############################################
#############################################


import sqlite3


def database_crud(data_db=dict(),print_data=False):
    # connection with sqllite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('my_db.db')
    cursor = conn.cursor()

    # create contests table if it dont exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contests (
            site VARCHAR(32) NOT NULL,
            contest_title TEXT NOT NULL,
            event_time TEXT NOT NULL,
            weekday VARCHAR(10)
        );
    ''')

    deleteing all existing records from the table
    '''deleteing all existing records from the table
    to ensures table is cleared before inserting updated contest data
    Note: table does not have any primary key or dependencies, so we can safely delete all rows
    why --> (not fielseble for large dataset but initnally works)
    contest data may be repeated or changed since the last fetch, 
    to avoid checking for if exists or using primary keys,
    we simply delete all rows and insert a fresh set.
    his simplifies logic and reduces overhead,
    since filtering and processing are done before handled before insertion.'''


    cursor.execute('DELETE FROM contests;')


    # inert contest data into the contests table
    for site in data_db:
        for contest in data_db[site]:
            title = contest[0]
            time = contest[1][:-1]  #exclude weekday part
            weekday = contest[1][-1]

            # convert timetuple to string 'yyyy-mm-dd hh:mm:ss+timezone'
            event_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}+05:30".format(*time)

            # inserting contest data into table
            cursor.execute('''
                INSERT INTO contests (site, contest_title, event_time, weekday)
                VALUES (?, ?, ?, ?)
            ''', (site, title, event_time, weekday))

    if print_data:
        cursor.execute('''
            SELECT site, contest_title, event_time, weekday
            FROM contests
            ORDER BY event_time ASC;
        ''')

        rows =cursor.fetchall()

        for r in rows:
            print(r[-2],r[-1],'\t',r)

    # commit changes and close/breask connection
    conn.commit()
    conn.close()

if __name__=='__main__:
    data=data_to_insert() 
    database_crud(data,True)
