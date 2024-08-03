import requests
import pygame
import os
import ollama
import json

question = input()
refer_wav_path = "" #参考音频路径
prompt_text = ""    #参考音频内容
api_url = "http://127.0.0.1:9880"

if __name__ == '__main__':

  contents = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': question}])
  response = contents['message']['content']
  
  print(response)

params = {
    "refer_wav_path": refer_wav_path,
    "prompt_text": prompt_text,
    "prompt_language": "zh",
    "text": response,
    "text_language": "zh"
    
    
}

response = requests.get(api_url, params=params)

if response.status_code == 200:
    # 保存音频文件
    audio_file_path = "output_audio.wav"
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(response.content)

    # 初始化pygame混音器
    pygame.mixer.init()
    
    # 加载音频文件
    pygame.mixer.music.load(audio_file_path)
    
    # 播放音频文件
    pygame.mixer.music.play()
    
     # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # 播放完成后删除音频文件
    pygame.mixer.quit()
    os.remove(audio_file_path)
else:
    print("从API获取音频失败")
