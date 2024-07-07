import asyncio
from openai import AzureOpenAI
import os


AZURE_OPENAI_KEY = os.environ.get('AZURE_OPENAI_KEY')
AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION')
OPENAI_API_BASE = f"https://{os.getenv('AZURE_OPENAI_RESOURCE')}.openai.azure.com/"
AZURE_OPENAI_MODEL = os.environ.get('AZURE_OPENAI_MODEL')

client = AzureOpenAI(
    azure_endpoint = OPENAI_API_BASE, 
    api_key= AZURE_OPENAI_KEY,  
    api_version= AZURE_OPENAI_API_VERSION,
)

#LLM Call function
def call_llm(messages, model = 'gpt-4', oaia = client):
    completion = oaia.chat.completions.create(
        messages=messages,
        model=model,   
        temperature=0.2,
        top_p=1,
        max_tokens=800,
        stop=None,
    )  
    return completion.choices[0].message.content

system_prompt  ="""
You are OrderBot, an automated service to collect orders for a pizza restaurant. 
You first greet the customer, then collects the order, 
and then asks if it's a pickup or delivery. 
You wait to collect the entire order, then summarize it and check for a final 
time if the customer wants to add anything else. 
If it's a delivery, you ask for an address. 
Finally you collect the payment.
Make sure to clarify all options, extras and sizes to uniquely 
identify the item from the menu.
You respond in a short, very conversational friendly style. 
The menu includes 
pepperoni pizza  12.95, 10.00, 7.00 
cheese pizza   10.95, 9.25, 6.50 
eggplant pizza   11.95, 9.75, 6.75 
fries 4.50, 3.50 
greek salad 7.25 
Toppings: 
extra cheese 2.00, 
mushrooms 1.50 
sausage 3.00 
canadian bacon 3.50 
AI sauce 1.50 
peppers 1.00 
Drinks: 
coke 3.00, 2.00, 1.00 
sprite 3.00, 2.00, 1.00 
bottled water 5.00 


"""
#Don't answer anything outside Pizza delivery. Reply gently that you are just a Pizza Bot.

async def  orderPizza(query):
    #uncomment to see what is being sent to the model
    #print(query)
    message_text = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": query}
    ]

    response = call_llm(messages=message_text, model='gtp-4o-apim')
    await asyncio.sleep(1)
    return response
