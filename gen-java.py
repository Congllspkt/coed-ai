from google import genai  
import time


client = genai.Client(api_key="AIzaSyCC8rEWxTRF4u5ukgTM0xgRVigI01b7GhM")  

def xxx(query: str):
    prompt =  '''
    
    what's docker, image, container, networking, volume, docker-compose, dockerfile, docker hub, docker-swarm
    
    give me detail and have examples (include input, output)
    
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


xxx("docker")










