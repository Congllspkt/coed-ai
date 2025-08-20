from google import genai  
import time


client = genai.Client(api_key="AIzaSyCC8rEWxTRF4u5ukgTM0xgRVigI01b7GhM")  

def xxx(query: str):
    prompt = query + '''
    
    we have some words:
    outgoing, shy, chatty, lazy, selfish, rude, talkative, 
    friendly, easy-going, sociable, caring, nice, quiet, bossy
    toast,cereal
    half past, quarter
    skateboard, pilates

    we want to translate these words to vietnamese with table include column:
    english, pronounciation, definition, example, vietnamese

    format md file
    '''
    
    response = client.models.generate_content(     
        model="gemini-2.5-flash",     
        contents=prompt )  
    
    # Save response.text into a markdown file
    filename = f"{query}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"End process {filename}")
    time.sleep(10)
    print("NEXT")

    
    return filename

xxx("1-15")  # Call the function with the desired query



