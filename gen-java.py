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

xxx("try- with-resources statement")
xxx("Rules while handling exceptions")
xxx("The Exception Hierarchy")
xxx("Checked Exceptions")
xxx("Unchecked Exceptions")
xxx("throws keyword")
xxx("throw keyword")
xxx("Differences between throw and throws keyword")
xxx("Exception Propagation")
xxx("Nested try block")
xxx("Custom Checked Exception")
xxx("Custom Unchecked Exception")
xxx("final, finally and finalize")
xxx("getClass in Object class")
xxx("hashCode in Object class")
xxx("equals in Object class")
xxx("finalize in Object class")
xxx("clone in Object class")
xxx("Shallow cloning & Deep cloning")
xxx("Mutable and Immutable objects")
xxx("Record classes")
xxx("var - local variable type inference")