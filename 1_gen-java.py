from google import genai  
import time


client = genai.Client(api_key="AIzaSyCC8rEWxTRF4u5ukgTM0xgRVigI01b7GhM")  

def xxx(query: str):
    prompt =  query + '''

    IN sql oracle

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
    time.sleep(2)
    print("NEXT")

    
    return filename


xxx("function")
xxx("procedure")
xxx("package")
xxx("trigger")
xxx("cursor")
xxx("exception")
xxx("index")
xxx("view")
xxx("materialized view")
xxx("sequence")
xxx("partition")
xxx("dml")
xxx("ddl")
xxx("transaction")
xxx("join")
xxx("union")
xxx("union all")
xxx("left join")
xxx("right join")
xxx("full join")
xxx("cross join")
xxx("self join")
xxx("natural join")
xxx("subquery")
xxx("cte")
xxx("concatenate strings")
