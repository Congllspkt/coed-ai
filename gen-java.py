from google import genai  

client = genai.Client(api_key="AIzaSyCC8rEWxTRF4u5ukgTM0xgRVigI01b7GhM")  

def xxx(query: str):
    prompt = query + '''
    
    in java 
    
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
    
    return filename


(xxx("static methods in interfaces"))
(xxx("Multiple Inheritance using interfaces"))
(xxx("Functional Interface"))
(xxx("Class Vs Abstract Class Vs Interface"))
(xxx("Array"))
(xxx("BufferedReader"))
(xxx("Scanner"))
(xxx("Logging"))
(xxx("try-catch block"))