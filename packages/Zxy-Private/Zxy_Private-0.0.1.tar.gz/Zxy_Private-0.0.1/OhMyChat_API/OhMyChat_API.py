# -*- encoding: utf-8 -*-
'''
@Project_name    :  OhMyChat_API
@ProjectDescription: ..........
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/8/8 9:25     zxy       1.0         None
'''
import json
import time
import traceback

import requests


class Test_Class():
    def __init__(self):
        pass

    def timeStamp_to_datetime(self,timeStamp):
        timeStamp = float(timeStamp)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime
    def get_chat_api(self, query="", rety_num=0):
        url = "https://cfwus02.opapi.win/v1/chat/completions"

        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ],
            "stream": True
        })
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            "Authorization": "Bearer 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",
            'Content-Type': 'application/json'
        }
        try:
            if query:
                if not rety_num:
                    raise
                response = requests.post(url, headers=headers, data=payload,stream=True)
                for index,line in enumerate(response.iter_lines()):
                    yield bytes.decode(line),index
        except:
            if rety_num<3:
                for line_data,index in self.get_chat_api(query,rety_num+1):
                    yield line_data,index
        else:
            return None

    def handler_api_result(self, line_data:str,index:int):
        if not line_data or line_data.endswith("[DONE]"):
            return
        data = json.loads(str(line_data).split(":",1)[-1])
        if not index:
            release_time = self.timeStamp_to_datetime(data["created"])
            model = data["model"]
        else:
            release_time,model="",""
        for choice in data["choices"]:
            if not index:
                username = choice["delta"]["role"]
                start_str = f"{username}({model})({release_time}){'='*100}"
                print(start_str)
                self.header_lenth = len(start_str)
            if choice["finish_reason"]:
                equalSign_num = (self.header_lenth-14)//2
                print(f"\n{'='*equalSign_num} divisionLine {'='*equalSign_num}")
            else:
                content = choice["delta"]["content"]
                print(content,end="")

    def run(self):
        while True:
            try:
                query = input("please input your question:")
                if not query:
                    continue
                elif query.lower() in ('q', 'quit', 'exit'):
                    while True:
                        query = input("Do you want to terminate (Y/N)?:")
                        if query.lower() == "y":
                            print("Welcome to use it next time")
                            return
                        elif query.lower() == 'n':
                            break
                        else:
                            print("Your input is illegal!")
                            continue
                    continue
                else:
                    print("Please be patient and wait for a response . . .")

                for line_data,index in self.get_chat_api(query):
                    self.handler_api_result(line_data,index)
            except:
                traceback.print_exc()
                print("There is a problem with your API interface !!!")
                return







if __name__ == '__main__':
    X = Test_Class()
    X.run()
