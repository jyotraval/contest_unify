import requests
import json

LEETCODE_URL = "https://leetcode.com/graphql/"

headers = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "User-Agent": "Mozilla/5.0"
}

def run_query(query, variables=None):
    response = requests.post(LEETCODE_URL, json={"query": query, "variables": variables or {}}, headers=headers)
    response.raise_for_status()
    # print(response.json())
    return response.json()

def get_leetcode_user_data(username):
    # 1. User Profile
    user_profile_query = '''
    query($username: String!) {
      matchedUser(username: $username) {
        username
        profile {
          realName
          aboutMe
          skillTags
          reputation
          ranking
        }
      }
    }
    '''

    # 2. Contest Info
    contest_query = '''
    query($username: String!) {
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
      }
    }
    '''

    # 3. Question Solved Stats
    question_stats_query = '''
    query($userSlug: String!) {
      userProfileUserQuestionProgressV2(userSlug: $userSlug) {
        numAcceptedQuestions {
          difficulty
          count
        }
      }
    }
    '''

    # 4. Skills by Tag
    tag_query = '''
    query($username: String!) {
      matchedUser(username: $username) {
        tagProblemCounts {
          advanced {
            tagName
            problemsSolved
          }
          intermediate {
            tagName
            problemsSolved
          }
          fundamental {
            tagName
            problemsSolved
          }
        }
      }
    }
    '''

    # 5. Recent Accepted Submissions
    solved_problems_query = '''
    query($username: String!) {
      recentAcSubmissionList(username: $username) {
        id
        title
        titleSlug
        timestamp
      }
    }
    '''

    # 6. User's Problem Status Summary
    problem_status_summary_query = '''
    query($username: String!) {
      matchedUser(username: $username) {
        problemsSolvedBeatsStats {
          difficulty
          percentage
        }
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
      }
    }
    '''

    # 7. Submission statistics per problem
    problem_submission_stats_query = '''
    query($username: String!) {
      recentSubmissionList(username: $username) {
        titleSlug
        status
        timestamp
      }
    }
    '''

    # Run queries without problematic ones
    profile = run_query(user_profile_query, {"username": username})

    if 'errors' in tuple(profile.keys()):
      return {"error": "User not found"}
    

    contest = run_query(contest_query, {"username": username})
    question_stats = run_query(question_stats_query, {"userSlug": username})

    skills = run_query(tag_query, {"username": username})
    solved_problems = run_query(solved_problems_query, {"username": username})

    problem_status_summary = run_query(problem_status_summary_query, {"username": username})
    submission_stats = run_query(problem_submission_stats_query, {"username": username})


    data= {
        "profile": profile["data"]["matchedUser"],
        "contest": contest["data"]["userContestRanking"],
        "question_stats": question_stats["data"]["userProfileUserQuestionProgressV2"],
        "skills": skills["data"]["matchedUser"]["tagProblemCounts"],
        "recent_ac_submissions": solved_problems["data"]["recentAcSubmissionList"],
        "problem_status_summary": problem_status_summary["data"]["matchedUser"],
        "submission_stats": submission_stats.get("data", {}).get("recentSubmissionList", [])
    }
    # data=json.dumps(data, indent=2) # makesn its str -> pretty print!!
    return data

if __name__ == "__main__":
    username = "jyot1234raval"
    data = get_leetcode_user_data(username)
    # print(data.keys())
    if 'error' in data:
       print("DNE")
       print(data)
    else:
       data=json.dumps(data, indent=2)
       print(data)
