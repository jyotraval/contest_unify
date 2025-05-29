import requests                                     # https reqs for APIs
from datetime import datetime, timedelta,timezone   # date and time manipulation
from bs4 import BeautifulSoup                       # web scraping, webpage extraition
import sqlite3                                      # database manipuation    
import logging                                      # for logging errors/info/debug messages
from typing import List, Tuple, Dict

# configure logging/ audits
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('contest_fetcher.log'), logging.StreamHandler()]
)
# ex 2025-05-28 19:45:12,345 - INFO - Fetched 10 contests
# levels 
# INFO-> geneaml info 
# Warning -> something unexpected but not a crash 
# ERROR- something failed (ex API call) 
# CRITICAL: very serious error

logger = logging.getLogger(__name__)

class ContestFetcherError(Exception):
    """custom exception for contest fetching errors"""
    pass

class ContestFetcher:
    """class to fetch and manage programming contest data"""
    
    CONFIG = {
        'codeforces_url': 'https://codeforces.com/api/contest.list',
        'leetcode_url': 'https://leetcode.com/graphql',
        'codechef_url': 'https://www.codechef.com/api/list/contests/all',
        'hackerearth_url': 'https://www.hackerearth.com/api/events/upcoming/',
        'atcoder_url': 'https://atcoder.jp/contests/',
        'request_timeout': 15
    } # holds base urls for api, dicitonary/hashmap

    def __init__(self):
        #session for http reqs get and post(leetcode - graph ql)
        self.session = requests.Session()
        
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'}) # headers to mimic real browser

    def fetch_codeforce_contests(self, limit: int = 10) -> List[Tuple[str, Tuple]]:
        """fetch upcoming Codeforces contests"""
        try:
            # get req to codeforce public api with timeout
            response = self.session.get(self.CONFIG['codeforces_url'], timeout=self.CONFIG['request_timeout'])
            response.raise_for_status() #raise erroe if status is not 200 = ok

            contests = response.json().get('result', [])[:limit] # parse json and slice list of contests upto limit
            res = [] #will hold filtered contest

            for contest in contests:
                if contest.get("phase", "").lower() == 'before':
                    start_time = contest.get("startTimeSeconds") #unix time stamp - number of sec that have passed since 1 Jan 1970 
                    if start_time:
                        ist = timezone(timedelta(hours=5, minutes=30))
                        dt = datetime.fromtimestamp(start_time, ist) #unix into ist time

                        # (year, month, day, hour, minute, second, weekday)
                        time_tuple = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.strftime('%A'))
                        res.append((contest.get("name", "Unknown Title"), time_tuple))

            logger.info(f"Fetched {len(res)} Codeforces contests") #Log how many contests were fetched successfully

            return res
        
        except requests.RequestException as e:
            logger.error(f"Failed to fetch Codeforces contests: {e}")
            raise ContestFetcherError(f"Codeforces API error: {e}")
    
    def fetch_leetcode_contests(self, limit: int = 2) -> List[Tuple[str, Tuple]]:
        # limit is set to 2 cause weekly and biweeks are only contests 
        try:
            headers = {'Content-Type': 'application/json', 
                       'Referer': 'https://leetcode.com/contest/'}
            query = {"query": "{ allContests { title startTime duration } }"} # graph ql query to get contest, starttime, duration
            response = self.session.post(
                self.CONFIG['leetcode_url'], 
                json=query, 
                headers=headers, 
                timeout=self.CONFIG['request_timeout']
            ) # post req to run query
            response.raise_for_status()
            contests = response.json()['data']['allContests'] # prase jason response to get list of evey contests
            current_time = int(datetime.now().timestamp()) # unix time
            classified = [] # stores filteres contest
            for contest in contests:
                start = contest['startTime']
                if current_time < start: # if start time > current time --> upcomming
                    ist = timezone(timedelta(hours=5, minutes=30))
                    dt = datetime.fromtimestamp(start, ist) # ist (conventional)
                    time_tuple = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.strftime('%A'))
                    classified.append((contest['title'], time_tuple))
                if len(classified) >= limit:
                    break
            logger.info(f"Fetched {len(classified)} LeetCode contests")

            return classified
        
        except requests.RequestException as e:
            logger.error(f"Failed to fetch LeetCode contests: {e}")
            raise ContestFetcherError(f"LeetCode API error: {e}")

    def fetch_codechef_contests(self, limit: int = 2) -> List[Tuple[str, Tuple]]:
        # api alredy retues only 2 contest but for flexibility
        try:
            # get req to get api contest data data
            response = self.session.get(self.CONFIG['codechef_url'], timeout=self.CONFIG['request_timeout'])
            response.raise_for_status()
            
            # api retieves in filtered form
            # response.json().keys() --> 
            # $$ dict_keys(['status', 'message', 'present_contests', 'future_contests', 'practice_contests', 'past_contests', 'skill_tests', 'banners'])

            contests = response.json().get('future_contests', [])
            res = [] # store contest in desired form
            for contest in contests:
                title = contest['contest_name']
                start_str = contest['contest_start_date']
                # api privides in ist +5.30
                dt = datetime.strptime(start_str, "%d %b %Y %H:%M:%S")
                contest_tuple = (title, (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.strftime("%A")))
                res.append(contest_tuple)
                if len(res)>= limit:
                    break
            logger.info(f"Fetched {len(res)} CodeChef contests")
            return res
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Failed to fetch CodeChef contests: {e}")
            raise ContestFetcherError(f"CodeChef API error: {e}")

    def fetch_hackerearth_contests(self) -> List[Tuple[str, Tuple]]:
        try:
            # get req
            response = self.session.get(self.CONFIG['hackerearth_url'], timeout=self.CONFIG['request_timeout'])
            response.raise_for_status()
            contests = response.json()['response']
            res = []
            for contest in contests:
                # NOTE: this only fetch upcming contests
                if contest["status"].lower() == "upcoming":
                    date_str = contest['start_utc_tz'] # ist time is provded but fetching utc 0.00 time to reduce bugs
                    # date_str = contest['start_tz'] # ist time
                    dt_part, tz_part = date_str[:-6], date_str[-6:] # date and timzone part diffrent
                    # '2025-05-29 14:23:00'  '+00:00'
                    dt = datetime.strptime(dt_part, "%Y-%m-%d %H:%M:%S") # changing converting dt_part (string) into datetime object
                    
                    # Parsing timezone offset as it is in str form
                    sign = 1 if tz_part[0] == '+' else -1
                    offset_hours = int(tz_part[1:3])
                    offset_minutes = int(tz_part[4:6])
                    offset = timedelta(hours=sign * offset_hours, minutes=sign * offset_minutes)

                    dt_utc = dt - offset # conveting into utc

                    # utc to ist
                    ist_offset = timedelta(hours=5, minutes=30)
                    dt_ist = dt_utc + ist_offset
                    
                    time_tuple = (dt_ist.year, dt_ist.month, 
                                  dt_ist.day, dt_ist.hour, 
                                  dt_ist.minute, dt_ist.second, 
                                  dt_ist.strftime('%A')) # (year,month,day,hour,min,sec, weekday)
                    res.append((contest['title'], time_tuple))
            logger.info(f"Fetched {len(res)} HackerEarth contests")
            return res
        
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Failed to fetch HackerEarth contests: {e}")
            raise ContestFetcherError(f"HackerEarth API error: {e}")

    def fetch_atcoder_contests(self) -> List[Tuple[str, Tuple]]:
        # NOTE: Could not find public API for atcoder, realying on web scarping as contest data is in static html form
        # not using heavy js for contest data -> could use web scrap
        try:
            response = self.session.get(self.CONFIG['atcoder_url'], timeout=self.CONFIG['request_timeout'])
            if response.status_code != 200:
                raise ContestFetcherError(f"AtCoder request failed: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser') # parsing full HTML response using beautifulsoup

            upcoming_header = soup.find('h3', string='Upcoming Contests') # Find the 'Upcoming Contests' section by header

            if not upcoming_header:
                raise ContestFetcherError("Could not find 'Upcoming Contests' section")
            
            #Find the table that immediately follows the header
            table = upcoming_header.find_next_sibling('div').find('table')

            contests = []
            # it is in table form
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')

                if len(cols) < 2:
                    continue # skip if row doesnt have enough column
                    
                time_str = cols[0].text.strip()
                name = cols[1].text.strip()[4:]  # Strip prefix like / contest title

                # time string with timezone (e.g., JST = +0900)
                start_time_jst = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S%z')

                # define ist manually as utc+05:30
                ist = timezone(timedelta(hours=5, minutes=30))

                # fetch time Convert to UTC
                start_time_utc = start_time_jst.astimezone(timezone.utc)

                # convert UTC to IST
                start_time_ist = start_time_utc.astimezone(ist)

                dt_tuple = (
                    start_time_ist.year, start_time_ist.month,
                    start_time_ist.day, start_time_ist.hour,
                    start_time_ist.minute, start_time_ist.second,
                    start_time_ist.strftime('%A')
                )

                contests.append((name, dt_tuple))
            logger.info(f"Fetched {len(contests)} AtCoder contests")
            return contests
        
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Failed to fetch AtCoder contests: {e}")
            raise ContestFetcherError(f"AtCoder scraping error: {e}")



class ContestDatabase:
    def __init__(self, db_name: str = 'contest.db'):
        self.db_name = db_name
        self._initialize_database()
    
    def time_tuple_to_unix(self, year, month, day, hr, minute, sec):
        # Define the offset for +5:30
        offset = timedelta(hours=5, minutes=30)
        # Create a timezone object for +5:30
        tz = timezone(offset)
        
        # Create a datetime object with the given time and the +5:30 timezone
        dt = datetime(year, month, day, hr, minute, sec, tzinfo=tz)
        
        # Convert to UTC timestamp (seconds since epoch)
        unix_timestamp = dt.timestamp()
        
        return int(unix_timestamp)

    def _initialize_database(self) -> None:
        """Initialize the contests table."""
        try:
            #connect with sqlite/ databse
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # site | contest_title | event_time | weekday | unix_time_stamp
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS contests (
                        site VARCHAR(32) NOT NULL,
                        contest_title TEXT NOT NULL,
                        event_time TEXT NOT NULL,
                        weekday VARCHAR(10),
                        unix_time_stamp INTEGER NOT NULL
                    );
                ''')
                conn.commit()
                logger.info("Initialized contests table")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise ContestFetcherError(f"Database error: {e}")

    def store_contests(self, data_db: Dict[str, List[Tuple]], print_data: bool = False) -> None:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                cursor.execute('DELETE FROM contests;')
                    # deleteing all existing records from the table
                    # Note: table does not have any primary key or dependencies, so we can safely delete all rows
                    # why --> (not fielseble for large dataset but initnally works)
                    # to ensures table is cleared before inserting updated contest data
                    # contest data may be repeated or changed since the last fetch, 
                    # to avoid checking for if exists or using primary keys, reduce cheeking and more loops
                    # we simply delete all rows and insert a fresh set.
                    # this simplifies logic and reduces overhead
                    # since filtering and processing are done before handled before insertion.

                for site in data_db:
                    for contest in data_db[site]:
                        # (title, (time(YEAR, MONTH, DAY, HOUR, MIN, SEC, WEEKDAY))
                        title = contest[0]
                        time = contest[1][:-1]
                        weekday = contest[1][-1]
                        unix_time= self.time_tuple_to_unix(*time)
                        # iso 8601 time formate YYYY-MM-DDTHH:mm:ss[tz]
                        event_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}+05:30".format(*time)
                        cursor.execute('''
                            INSERT INTO contests (site, contest_title, event_time, weekday,unix_time_stamp)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (site, title, event_time, weekday, unix_time))
                
                logger.info("Stored contest data in database")

                
                # printnf data for testing purpose
                if print_data:
                    cursor.execute('''
                        SELECT site, contest_title, event_time, weekday, unix_time_stamp
                        FROM contests
                        ORDER BY unix_time_stamp ASC;
                    ''')
                    rows = cursor.fetchall()
                    for row in rows:
                        # print(row[-3],row[-2], row[-1], sep='\t')
                        pass
                    logger.info(f"{len(rows)} contest records retrieved from the database and displayed.")
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database operation error: {e}")
            raise ContestFetcherError(f"Database error: {e}")

def fetch_all_contests( codeforce: bool=False,leetcode: bool=False,codechef: bool=False,
                        hackearth: bool=False, atcoder: bool=False,all: bool=True) -> Dict[str, List[Tuple]]:
    """central controller of code base"""

    fetcher = ContestFetcher() # create instance of the fetcher
    data_db = {} # dict to store results
    try:
        # if `all` is True or the individual site flag is True
        # fetch contests from that platform and store them in the dictionary.

        if all or codeforce:
            data_db['codeforce'] = fetcher.fetch_codeforce_contests()
        if all or leetcode:
            data_db['leetcode'] = fetcher.fetch_leetcode_contests()
        if all or codechef:
            data_db['codechef'] = fetcher.fetch_codechef_contests()
        if all or hackearth:
            data_db['hackearth'] = fetcher.fetch_hackerearth_contests()
        if all or atcoder:
            data_db['atcoder'] = fetcher.fetch_atcoder_contests()
        return data_db
    except ContestFetcherError as e:
        logger.error(f"Error fetching contests: {e}")
        raise

def contest_site_info() -> None:
    """Print available contest sites."""
    print(('codeforce', 'leetcode', 'codechef', 'hackearth', 'atcoder'))

def main():
    try:
        # step 1.. fetch contest data from all platforms
        data = fetch_all_contests() # defualt fetch all contests

        # step 2... initialize the database connection (creates table if needed)
        db = ContestDatabase()

         # step 3.. store the fetched data in the database
        db.store_contests(data, print_data_global) # print_data=True means it will also print stored contests to the console

    except ContestFetcherError as e:
        logger.error(f"Main execution error: {e}")
        print(f"Error: {e}")

print_data_global=False

if __name__ == "__main__":
    # This block runs only if the script is executed directly
    print_data_global=True
    main()
    