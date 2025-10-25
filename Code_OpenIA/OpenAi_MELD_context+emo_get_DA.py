import re
import csv
import  pandas as pd
# from openai import OpenAI
import requests

API_="sk-pF_xxxxxxxxxxxx"
API_URL = "https://api.openai.com/v1/chat/completions"

df = pd.read_csv('MELD/DATA/context+emotion.csv', encoding='latin-1', quotechar='|')
pattern = re.escape('**') + "(.*?)" + re.escape('**')

question = "According to the context of the conversation and its classification of the emotional state, choose between Greeting, Question, Answer, Statement Opinion, Statement Non Opinion, Apology, Command, Agreement, Disagreement, Acknowledge, Backchannel, and Others. Each sentence has been labeled according to the emotion shown in parentheses. Answer each sentence in one word with a list and a corresponding number. Not a summary. What dialogical act is shown in each turn of the conversation?: "

with open("MELD/RES_MELD+Emo_DA/Context+emo_gets_DA.csv", "w", newline='') as f:
    my_csvwriter = csv.writer(f)
    my_csvwriter.writerow("Conversation, ChatGPT".split(','))
    conversation = 0

    with open('MELD/RES_MELD+Emo_DA/Logs/Context+emo_gets_DA_496.txt', 'w') as file:

        for sentence in df.iterrows():
            text = sentence[1]['Conversation']

            headers = {
                'Authorization': f'Bearer {API_}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'gpt-4',
                'messages': [
                    {'role': 'user', 'content': question + text}
                ]
            }
            response = requests.post(API_URL, headers=headers, json=data)
            response_json = response.json()
            response = response_json['choices'][0]['message']['content']
            result = re.split(r'\n|\r\n', response)
            # print(result)

            for line in result:
                emotion = line.split(".")
                if len(emotion) == 2:
                    sentence = emotion[0] + '°' + emotion[1].strip()
                    my_csvwriter.writerow(sentence.split("°"))
                    print(sentence)
                    file.write(sentence + "\n")

                elif len(emotion) > 2:
                    sentence = emotion[0] + '°' + emotion[1].strip()
                    my_csvwriter.writerow(sentence.split("°"))
                    print(sentence)
                    file.write(line + "\n")
                    print(line)
            file.write(text + "\n")
            print(text)
            print("______________________________________________")
            conversation += 1
            print("conversation: " + str(conversation))

