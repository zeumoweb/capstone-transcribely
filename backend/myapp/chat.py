from openai import OpenAI
import os

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

def generate_response(extracted_text, question):
    streams = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
                {"role": "system", "content": f"You are an assistant skilled in answering questions about video content.  If the question is completely unrelated to the video and to the history of previous message with the user, tell the user that you cannot answer the question. If the answer you provide is not found in the video, add a disclaimer before providing the answer. Answer to the best of you knowledge based on  the content of the video. Let's start! Here is the content of the video: {extracted_text}. Add a the key timestamps where the answer you provide can be found in the video."},
                {"role": "user", "content": "who or what are you?"},
                {"role": "assistant", "content": "I am an AI assistant that can answer questions about the current video."},
                {"role": "user", "content": question}
            ],
    stream=True
    )
    for chunk in streams:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def translate(filepath, target_lang):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    text = ''
    for line in lines:
        text += line
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
                {"role": "system", "content": f"Translate the following subtitles in the language with code {target_lang} while maintaining the format of the subtitle: {text}"},
            ])
    
    with open(filepath, 'w') as file:
        file.write(completion.choices[0].message.content)
    
    return completion.choices[0].message.content
    
        
        
# print(translate('subtitles/subtitle-audio-What_is_Networking.srt', 'fr'))