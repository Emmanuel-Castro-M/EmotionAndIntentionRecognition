import re
import csv
import  pandas as pd
from openai import OpenAI

df = pd.read_csv('IEMOCAP/DATA/Baseline.csv', encoding='latin-1', quotechar='|')
client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxx", base_url="https://api.deepseek.com")

pattern = re.escape('**') + "(.*?)" + re.escape('**')
question = "In one word, choose between anger, excited, fear, frustrated, happy, neutral, sad, or surprised. Not a summary. What emotion is shown in the next text?: "

with open("IEMOCAP/RESULTS/Baseline_get_emocion.csv", "w", newline='') as f:
    my_csvwriter = csv.writer(f)
    my_csvwriter.writerow("Text, DeepSeek".split(','))
    conversation = 0
    for sentence in df.iterrows():
        text = sentence[1]['Conversation']
        response = client.chat.completions.create(
            model="deepseek-chat",       # to use with the model DeepSeek-v3
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
            emotion = re.findall(pattern, line)
            if len(emotion) != 0:
                sentence = "|" + text + '|°' + line + '°' + emotion[0]
                my_csvwriter.writerow(sentence.split("°"))
            else:
                sentence = "|" + text + '|°' + line
                my_csvwriter.writerow(sentence.split("°"))
        print("______________________________________________")
        conversation += 1
        print("Conversation: " + str(conversation))

