import google.generativeai as genai
import requests
import json

import leetcode_userinfo
import codeforces_userinfo

from dotenv import load_dotenv
import os
load_dotenv()

API_KEY=os.getenv("GEMINI_API")



def llm_respond(user_id, site):

    site_avl={
        'leetcode':1,
        'codeforces':2
    }

    match site_avl.get(site,0):
        case 1:
            user_data_raw= leetcode_userinfo.get_leetcode_user_data(user_id)


            if 'error' not in user_data_raw:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f'''
                You are an expert coding coach helping a LeetCode user improve their problem-solving skills and contest performance.

                NOTE: The submission data includes only the user's most recent 20 submissions. Focus recommendations on recent trends but include overall stats where helpful.

                Based on the user's data, write a friendly, motivating, and practical analysis that includes:

                1. A summary of the user's strengths and weaknesses in problem-solving and contests. Include insights into their current skill level and growth potential.
                2. Specific recommendations on what type of problems they should focus on next — include difficulty level and relevant skill tags.
                3. Actionable advice on improving their performance in contests (e.g., consistency, speed, accuracy, mindset).
                4. A short, motivational 2-3 line message that encourages them to keep improving.

                Then, end your response with a **TL;DR**: a concise summary of the most important takeaways, written in a clear and direct tone — no fluff.

                Here is the user's raw data:
                {user_data_raw}
                '''
                try:
                    response = model.generate_content(prompt)
                    # print(type(response))
                    return response.text
                except Exception as e:
                    return f"Error: {e}"
                
            return 'Error : User not found!'
        
        case 2:
            user_data_raw = codeforces_userinfo.get_codeforces_user_data(user_id)

            if 'error' not in user_data_raw:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f'''
                You are an expert programming coach helping a Codeforces user understand their progress and improve their competitive programming skills.

                Analyze the user's public Codeforces data provided below and write a friendly, clear, and motivating analysis that includes:

                1. A summary of their current skill level, rating, and rank progress. Highlight their growth trajectory using past contests and max rating.
                2. Their **strengths and weaknesses** in submissions (e.g., frequent verdict types like WA/TLE/AC, problem tags attempted, consistency, accuracy).
                3. Provide **specific and actionable suggestions** on:
                - What kind of problems (difficulty or topics) they should focus on.
                - How to reduce common mistakes seen in their submissions.
                - How to improve their contest strategy (e.g., pacing, practice before contests, upsolving).
                4. End with a short 2-3 line motivational message.

                Then, finish with a TL;DR — a very concise summary of their key insights and improvement plan.

                Here is the user's raw data:
                {user_data_raw}
                '''

                try:
                    response = model.generate_content(prompt)
                    
                    return response.text
                except Exception as e:
                    return f"Error: {e}"
                
            return 'Error : User not found!'

        case 0:
            return 'Invalid Site selection: Try Again!'
    
    return "LLM - !!!"
        

if __name__== '__main__':
    user_id='jyot1234raval'
    print(llm_respond(user_id,'leetcode'))