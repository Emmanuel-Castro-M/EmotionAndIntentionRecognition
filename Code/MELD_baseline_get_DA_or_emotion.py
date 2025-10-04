import re
import csv
import  pandas as pd
from openai import OpenAI

df = pd.read_csv('MELD/DATA/baseline.csv', encoding='latin-1', quotechar='|')
client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxx", base_url="https://api.deepseek.com")
pattern = re.escape('**') + "(.*?)" + re.escape('**')

# use to get DA classification
# question = "In one word, choose between Greeting, Question, Answer, Statement Opinion, Statement Non Opinion, Apology, Command, Agreement, Disagreement, Acknowledge, Backchannel, and Others. Not a summary. Do not give me the reasoning. What dialogical act is shown in the next text?: "

# use to get emotion classification
question = "In one word, choose between anger, disgust, fear, joy, neutral, sadness, or surprised. Not a summary. Do not give me the reasoning. What emotion is shown in the next text?: "

# for DAs
# with open("MELD/RESULTS/Baseline_get_DA.csv", "w", newline='') as f:

# for emotions
with open("MELD/RESULTS/Baseline_get_emotion.csv", "w", newline='') as f:
    my_csvwriter = csv.writer(f)
    my_csvwriter.writerow("Text, DeepSeek".split(','))
    conversation = 0
    for sentence in df.iterrows():
        texto = sentence[1]['Conversation']
        response = client.chat.completions.create(
            model="deepseek-chat",  # to use with the model DeepSeek-v3
            # model="deepseek-reasoner", # to use with the model DeepSeek-r1
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": question + texto
                 },
            ],
            stream=False
        )
        result = re.split(r'\n|\r\n', response.choices[0].message.content)
        print(result)
        for linea in result:
            emotion = re.findall(pattern, linea)
            if len(emotion) != 0:
                sentence = "|" + texto + '|°' + linea + '°' + emotion[0]
                my_csvwriter.writerow(sentence.split("°"))
            else:
                sentence = "|" + texto + '|°' + linea
                my_csvwriter.writerow(sentence.split("°"))
        print("______________________________________________")
        conversation += 1
        print("varConversation: " + str(conversation))
