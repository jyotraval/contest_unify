# Contest Unify — Backend Module

## Overview


The backend_index.py script serves as the core backend module for the [Contest Unify](https://github.com/jyotraval/contest_unify) project. Its primary function is to *automatically fetch and aggregate upcoming programming contest data* from various online judging platforms and persist this information into a PostgreSQL database. 
> This module is designed for *independent execution*, meaning it operates without direct dependencies on frameworks like Django. Its automation can be seamlessly managed through GitHub Actions (as implemented), or by integrating it with manual triggers, cron jobs, CI/CD pipelines, or serverless functions for periodic updates.


## Features

* *Multi-Platform Support*
  - Codeforces (REST API)
  - LeetCode (GraphQL)
  - CodeChef (API)
  - HackerEarth (API)
  - AtCoder (via static HTML scraping)

* *Persistent Data Storage:* All collected contest data is securely stored within a PostgreSQL database, serving as a centralized data source. *
*  *Automated Data Refresh:* Engineered for periodic execution to ensure the contest data remains current and accurate. 
* *Standardized Timezone Handling:* All fetched contest start times are consistently converted and stored in *Indian Standard Time (IST - UTC+05:30)*. 
* *Comprehensive Error Logging:* Leverages Python's logging module to provide detailed logs, categorizing messages as INFO, WARNING, or ERROR for effective monitoring and debugging. 
* *Idempotent Data Management:* Guarantees data integrity by systematically clearing outdated upcoming contest entries and inserting fresh data with each run, effectively preventing duplicates and maintaining an up-to-date dataset.

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Supabase account for PostgreSQL database access
- Environment variables for database connection (stored in a .env file)

### Environment Variables

This backend uses environment variables for database connection details. Create a .env 
Add the following, replacing placeholders with your Supabase credentials:
   
   user=your_supabase_user
   password=your_supabase_password
   host=your_supabase_host
   port=your_supabase_port
   dbname=your_supabase_dbname
   

## Usage
1. Run the backend script to fetch and store contests:
   bash
   python backend_index.py
   
2. The script will:
   - Fetch upcoming contests from all platforms (default behavior).
   - Store the data in the Supabase database table contests.
   - Log operations and errors to contest_fetcher.log.
   - Print stored contests to the console, sorted by UNIX timestamp.
3. Example output:
   
   https://codeforces.com/contests   2025-06-23 17:35:00+05:30  Mon  1753440900  Codeforces Round #900
   https://leetcode.com/contest/     2025-06-25 20:30:00+05:30  Wed  1753625400  Weekly Contest 350
   

## Code Structure
- **backend_index.py**: The main script containing:
  - ContestFetcher class: Handles API requests and web scraping for contest data.
  - ContestDatabase class: Manages database initialization and data storage.
  - fetch_all_contests(): Central controller to fetch contests from selected platforms.
  - print_contest(): Retrieves and displays stored contests.
  - main(): Orchestrates fetching, storing, and printing contest data.
 
 ## What It Does

- Fetches *upcoming contests* from:
  - Codeforces (API)
  - LeetCode (GraphQL API)
  - CodeChef (API)
  - HackerEarth (API)
  - AtCoder (via HTML scraping)
- Converts times to *IST (UTC+5:30)*
- Stores them in a *PostgreSQL* table
- Deletes outdated entries, inserts updated ones
- Logs everything to a rotating log file

### Example Code Explanation
python
def fetch_codeforce_contests(self, limit: int = 10) -> List[Tuple[str, Tuple]]:
    """fetch upcoming Codeforces contests"""
    try:
        response = self.session.get(self.CONFIG['codeforces_url'], timeout=self.CONFIG['request_timeout'])
        response.raise_for_status()
        contests = response.json().get('result', [])[:limit]
        res = []
        for contest in contests:
            if contest.get("phase", "").lower() == 'before':
                start_time = contest.get("startTimeSeconds")
                if start_time:
                    ist = timezone(timedelta(hours=5, minutes=30))
                    dt = datetime.fromtimestamp(start_time, ist)
                    time_tuple = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.strftime('%A'))
                    res.append((contest.get("name", "Unknown Title"), time_tuple))
        logger.info(f"Fetched {len(res)} Codeforces contests")
        return res
    except requests.RequestException as e:
        logger.error(f"Failed to fetch Codeforces contests: {e}")
        raise ContestFetcherError(f"Codeforces API error: {e}")

*Description*: This method fetches upcoming Codeforces contests using their public API. It filters contests in the "before" phase, converts UNIX timestamps to IST, and returns a list of tuples containing contest titles and time details (year, month, day, hour, minute, second, weekday).

## Database Schema
The contests table is created with the following structure:
| Column            | Type        | Description                              |
|-------------------|-------------|------------------------------------------|
| site            | VARCHAR(63) | Contest platform URL (e.g., https://codeforces.com/contests) |
| contest_title   | TEXT        | Title of the contest                     |
| event_time      | TEXT        | Event time in ISO 8601 format (e.g., 2025-06-23 17:35:00+05:30) |
| weekday         | VARCHAR(10) | Weekday of the event (e.g., Monday)      |
| unix_time_stamp | BIGINT      | UNIX timestamp of the event              |

A unique constraint ensures no duplicate entries for the same (site, contest_title, event_time).