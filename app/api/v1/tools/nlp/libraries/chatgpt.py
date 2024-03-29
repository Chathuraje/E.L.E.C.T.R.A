from . import load_tools
main_tool_name, tool_data = load_tools("chatgpt")

import openai, time
from app.libraries import secrets
from fastapi import HTTPException, status
from ..schemas import MetaData

async def __client(conversation):
    openai.api_key = secrets.OPEN_AI_API_KEY
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        n=1
    )
        
    conversation = {'role': response.choices[0].message.role, 'content': response.choices[0].message.content}
    return conversation
    
    
async def __gpt_generation(conversation):
    try:
        response = await __client(conversation)
    except Exception as e:
        try:
            time.sleep(20)
            response = await __client(conversation)
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error in chat gpt generation")

    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)            
    return response    


async def __ask(prompt):
    conversation = []
    
    conversation.append({'role': 'system', 'content': prompt})
    conversation_response = await __gpt_generation(conversation)
    conversation.append(conversation_response)
    output = conversation[-1]['content'].strip()
    
    return output
                
async def ask(prompt):
    output = await __ask(prompt)
    return {'prompt': prompt, 'output': output}