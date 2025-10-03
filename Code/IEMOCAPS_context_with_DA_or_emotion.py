import re
import csv
import  pandas as pd
from openai import OpenAI

df = pd.read_csv('IEMOCAP/DATA/Context_with_DA.csv', encoding='latin-1', quotechar='|')
client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxxxxxxxxx", base_url="https://api.deepseek.com")
pattern = re.escape('**') + "(.*?)" + re.escape('**')

# use to get emotions classification in context and with cues of DAs
# question = "According to the context of the conversation and its dialogical act classification, choose between anger, excited, fear, frustrated, happy, neutral, sad, or surprised. Each sentence has been labeled according to the dialogical act shown in parentheses. Answer each sentence in one word with a list and corresponding number. Not a summary. What emotion is shown in each sentence?: "

# use to get DA classification in context and with cues of emotions
question = "According to the context of the conversation and its classification of the emotional state, choose between Greeting, Question, Answer, Statement Opinion, Statement Non Opinion, Apology, Command, Agreement, Disagreement, Acknowledge, Backchannel, and Others. Each sentence has been labeled according to the emotion shown in parentheses. Answer each sentence in one word with a list and a corresponding number. Not a summary. What dialogical act is shown in each sentence of each conversation?: "

# for DAs
# with open("IEMOCAP/RESULTS/context_with_cues_to_get_DA.csv", "w", newline='') as f:

# for emotions
with open("IEMOCAP/RESULTS/context_with_cues_to_get_emotion.csv", "w", newline='') as f:
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
                print("len(emotion)")
                print(len(emotion))
                sentence = emotion[0] + '°' + emotion[len(emotion)-1].strip()
                my_csvwriter.writerow(sentence.split("°"))
                print(sentence)
        print("______________________________________________")
        conversation += 1
        print("conversation: " + str(conversation))
