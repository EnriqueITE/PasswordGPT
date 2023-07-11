import os
import requests
import json
import argparse
import sys

print("""
    ____                                          ____________  ______
   / __ \____ ____________      ______  _________/ / ____/ __ \/_  __/
  / /_/ / __ `/ ___/ ___/ | /| / / __ \/ ___/ __  / / __/ /_/ / / /   
 / ____/ /_/ (__  |__  )| |/ |/ / /_/ / /  / /_/ / /_/ / ____/ / /    
/_/    \__,_/____/____/ |__/|__/\____/_/   \__,_/\____/_/     /_/                                                                                                   
""")

parser = argparse.ArgumentParser(description="\nEnter words that serve as a basis for ChatGPT to generate related passwords.")
parser.add_argument("-a", "--amount", nargs='?', default=20, type=int, help="Number of passwords to generate.")
parser.add_argument("-w", "--words", nargs='+', help="\nWords separated by commas.")
args = parser.parse_args()

limit = 500
amount = args.amount

if not args.words:
    print("Please provide information to generate the password dictionary.")
    exit()

elif len(args.words) > limit:
    print(f"\nWord list too long. Change this limit ({limit} words) to use more tokens.")
    exit()

else:
    words = args.words

def chat_with_gpt(prompt):
    
    sys.stdout.write(" -> Requesting the wordlist to ChatGPT... ")
    sys.stdout.flush()

    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a password generator.'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.3,
        'max_tokens': 1000, # If the number of passwords is lower than requested, probably you will need to use more tokens.
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    except:
        print(" ERROR: Something happened with the connection. Are you connected to Internet?\n")
        exit()

    if response.status_code != 200:
        print(" ERROR: Something wrong happened, please try again.")
        exit()   
    else:
        sys.stdout.write(" Received!\n")
        sys.stdout.flush()

        response_data = response.json()
        wordList = response_data['choices'][0]['message']['content']
    
        return wordList

promptMsg = f"Make {amount} passwords given the following information: " + ",".join(words)  + ". Do not enumerate them, write all of them separated by '\n'"

chatGPTresults = chat_with_gpt(promptMsg)

# print(chatGPTresults) # Print available for debugging.

filename = "passwords.txt"

with open(filename, "w") as file:
    file.write(chatGPTresults)

file_path = os.path.abspath(filename)

sys.stdout.write(f"\n -> Password list created on: {file_path}\n\n")
sys.stdout.flush()