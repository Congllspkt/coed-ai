from google import genai  
import time


client = genai.Client(api_key="AIzaSyCC8rEWxTRF4u5ukgTM0xgRVigI01b7GhM")  

def xxx(query: str):
    prompt = query + '''
    
    we have some words:

    superset , utility, detection, launcher, Archive , disassembler
    wizard, Pattern , Sealed , Essential , Visual , profiling , dump , analyzer
    specific, patch  , regularly, independent , allocation , sandboxing, compilation,
    Architecture, several  , Bootstrap , directory, classpath, Metaspace 
    among , newer , Young , Eden Space, Survivor , Permanent , metadata, frames, partial 


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

xxx("e2")  # Call the function with the desired query



