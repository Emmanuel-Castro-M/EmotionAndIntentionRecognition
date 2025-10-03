import re
import csv
import  pandas as pd
from openai import OpenAI

df = pd.read_csv('MELD/DATA/context_with_emotion.csv', encoding='latin-1', quotechar='|')
client = OpenAI(api_key="sk-2ae94313bb8e4dd8bbf4c38b540f7101", base_url="https://api.deepseek.com")
pattern = re.escape('**') + "(.*?)" + re.escape('**')

# use for emotions
# question = "According to the context of the conversation, and its dialogical acts, choose between anger, disgust, fear, joy, neutral, sadness, or surprised. Each sentence has been labeled according to its dialogical act, shown in parentheses. Answer each sentence in one word with a list and a corresponding number. Not a summary. Do not give me the reasoning. What emotion is shown in each turn of the conversation?: "

# use for DAs
question = "According to the context of the conversation and the classification of the emotional state, choose between choose between Greeting, Question, Answer, Statement Opinion, Statement Non Opinion, Apology, Command, Agreement, Disagreement, Acknowledge, Backchannel, and Others. Each sentence has been labeled according to its emotional state, shown in parentheses. Answer each sentence in one word with a list and a corresponding number. Not a summary. Do not give me the reasoning. What dialogical act is shown in each turn of the conversation?: "

# use for emotions
# with open("MELD/context_with_DA.csv", "w", newline='') as f:

# use for DAs
with open("MELD/RESULTS/context_with_emotion_to_get_DA.csv", "w", newline='') as f:
    my_csvwriter = csv.writer(f)
    my_csvwriter.writerow("Text, DeepSeek".split(','))
    conversation = 0
    for sentence in df.iterrows():
        text = sentence[1]['Conversation']
        response = client.chat.completions.create(
            model="deepseek-chat",  # to use with the model DeepSeek-v3
            # model="deepseek-reasoner", # to use with the model DeepSeek-r1
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": question + text
                 },
            ],
            stream=False
        )
        result = re.split(r'\n|\r\n', response.choices[0].message.content)
        print(result)
        for line in result:
            emotion = line.split(".")
            if len(emotion) == 2:
                sentence = emotion[0] + '°' + emotion[1].strip()
                my_csvwriter.writerow(sentence.split("°"))
            elif len(emotion) > 2:
                sentence = emotion[0] + '°' + emotion[len(emotion)-1].strip()
                my_csvwriter.writerow(sentence.split("°"))
                print(sentence)
            else:
                sentence = "|" + text + '|°' + line
                my_csvwriter.writerow(sentence.split("°"))
        print("______________________________________________")
        conversation += 1
        print("Conversation: " + str(conversation))
