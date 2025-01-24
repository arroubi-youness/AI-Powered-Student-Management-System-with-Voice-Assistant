import asyncio
import os
import threading

from dotenv import load_dotenv
import json
from openai import AzureOpenAI  
import azure.cognitiveservices.speech as speechsdk
from SpeechToText import Speech_To_Text 
from TextToSpeech import text_to_speech_fnc
import webbrowser

class Voice_Assistant:
    def __init__(self) :
        load_dotenv()
        self.endpoint = "https://zakh-m5jqxxjr-swedencentral.openai.azure.com/"
        self.deployment = "gpt-4"

        self.text_to_speech_fnc = text_to_speech_fnc
        self.subscription_key = "2U5qjJv1j4SYUilaPZqkGTwfuiD3zuzdh0SOBTfDN5IlgyDuoeJgJQQJ99BAACfhMk5XJ3w3AAAAACOGbjM5"
        self.client = AzureOpenAI(  
            azure_endpoint=self.endpoint,  
            api_key=self.subscription_key,  
            api_version="2024-05-01-preview",  
        )


        self.tools=[{
            "type":"function",
            "function":{
                "name":"open_web_page",
                "description":"Opens a specific webpage in the browser, with optional search parameters.",
                "parameters":{
                        "type":"object",
                        "properties":{
                            "website":{
                            "type":"string",
                            "description":"The complete website URL to open, including the protocol (e.g., 'https://www.youtube.com')."
                            },
                            "search_parameters":{
                                "type":"string",
                                "description":"Optional query or search parameters to append to the website URL (e.g., '/search?q=what+is+silero' for a Google search: 'https://www.google.com/search?q=what+is+silero', and '/results?search_query=what+is+silero' for a Youtube search:'https://www.youtube.com/results?search_query=what+is+silero')."
                            }
                        },
                        "required":["website"],
                }
            }
        }]
        self.functions=[{
                "name":"open_web_page",
                "description":"Opens a specific webpage in the browser, with optional search parameters.",
                "parameters":{
                        "type":"object",
                        "properties":{
                            "website":{
                            "type":"string",
                            "description":"The complete website URL to open, including the protocol (e.g., 'https://www.youtube.com')."
                            },
                            "search_parameters":{
                                "type":"string",
                                "description":"Optional query or search parameters to append to the website URL (e.g., '/search?q=what+is+silero' for a Google search: 'https://www.google.com/search?q=what+is+silero', and '/results?search_query=what+is+silero' for a Youtube search:'https://www.youtube.com/results?search_query=what+is+silero')."
                            }
                        },
                        "required":["website"],
                }
            }]

        self.messages = [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "you're a helpful assistant,that can execute many functions and when get a respond as done, it means the function was successfully executed. You can also answer questions "
                        }
                    ]
                }
            ]
        self.prompt_message=""
        self.speech_to_text=Speech_To_Text()
# Generate the completion  
    def set_prompt(self,prompt_message):
        self.prompt_message=prompt_message

    def ask_assistant(self,user_message) :
        self.prompt_message=format(user_message)
        self.messages.append({"role": "user", "content": self.prompt_message})
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=self.messages,

            max_tokens=800,
            temperature=0.5,
            top_p=0.5,
            #tools=self.tools,
            #tool_choice="auto",
            functions=self.functions,
            function_call="auto",
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        assistant_response = dict(completion.choices[0].message)

        #self.messages.append(dict(assistant_response))
        # print("assistant response: ",assistant_response.tool_calls)
        #if assistant_response.tool_calls:

            #for tool_call in assistant_response.tool_calls:
            #    function_name = tool_call.function.name
            #    function_args = json.loads(tool_call.function.arguments)
            #    print(f"Function call: {function_name}")
            #    print(f"Function arguments: {function_args}")

        if assistant_response.get("function_call"):

                print("enterrrrs:", type( assistant_response.get("function_call")))

                function_name=dict(assistant_response.get("function_call")).get("name")
                print(function_name)
                function_args= json.loads(dict(assistant_response.get("function_call")).get("arguments"))
                print(function_args)
                if function_name == "open_web_page":
                    website = function_args.get("website")
                    parameters = function_args.get("search_parameters")
                    if webbrowser.open(website + parameters):
                        function_response = "page opened successfully"

                        self.messages.append({
                            #"tool_call_id": tool_call.id,
                            "role": "function",
                            "name": function_name,
                            "content": function_response,
                        })
                    final_response = self.client.chat.completions.create(
                        model=self.deployment,
                        messages=self.messages,
                    )

                    print("final response", final_response.choices[0].message.content)
                    text_to_speech_fnc(final_response.choices[0].message.content)
        else:
            self.messages.append(assistant_response)
            return completion.choices[0].message.content

            #text_to_speech_fnc(completion.choices[0].message.content)

    def call_voice_assistant(self):
        t1= threading.Thread(target=self.activate_voice_assistant,daemon=True)
        t1.start()
        #asyncio.run(self.activate_voice_assistant())


    def activate_voice_assistant(self):
        print("enters")
        speech_result= self.speech_to_text.recognize_from_microphone()
        print(speech_result)

        if speech_result.reason == speechsdk.ResultReason.NoMatch or speech_result.reason == speechsdk.ResultReason.Canceled:
            pass
        else:
            self.prompt_message=format(speech_result.text)

            print("user: "+self.prompt_message)
            self.messages.append({"role":"user","content": self.prompt_message})
            completion = self.client.chat.completions.create(
                model=self.deployment,
                messages=self.messages,
                max_tokens=800,
                temperature=0.5,
                top_p=0.5,
                #tools=self.tools,
                #tool_choice="auto",
                functions=self.functions,
                function_call="auto",
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False
            )
            assistant_response = completion.choices[0].message

            print(assistant_response)

            # print("assistant response: ",assistant_response.tool_calls)


            if assistant_response.function_call:
                    function_name=assistant_response.to_dict()["function_call"]["name"]
                    function_args=json.loads(assistant_response.to_dict()["function_call"]["arguments"])
                    self.messages.append({
                        "role": "assistant",
                        "content": f"Function call: {function_name} with arguments: {function_args}"
                    })
                    if function_name=="open_web_page":
                        website=function_args.get("website")
                        parameters=function_args.get("search_parameters")
                        if webbrowser.open(str(website)+str(parameters)):
                            function_response="page opened successfully"

                        self.messages.append({
                        #"tool_call_id": tool_call.id,
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                        })
                        final_response = self.client.chat.completions.create(
                            model=self.deployment,
                            messages=self.messages,
                        )
                        print( "final response",final_response.choices[0].message.content)
                        text_to_speech_fnc(final_response.choices[0].message.content)
            else:
                print( "assistant response",completion.choices[0].message.content)
                text_to_speech_fnc(completion.choices[0].message.content)


