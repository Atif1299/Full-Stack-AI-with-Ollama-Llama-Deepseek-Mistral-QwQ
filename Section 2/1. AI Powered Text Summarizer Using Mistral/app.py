from fastapi import FastAPI , HTTPException, Form

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os 
import json

app = FastAPI()

# Serve the Static files 
app.mount('/static' , StaticFiles(directory='static') , name='static')
OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL_NAME = 'mistral'

@app.get('/')
def serve_homepage():
    'serve the index.html file when accessing the root url'
    return FileResponse(os.path.join('static' , 'index.html'))

@app.post('summarize')
def summarize_text(text:str = Form(...)):
    headers = {'Content-Type' : 'application/json'}

    try:
        response = requests.post(
            OLLAMA_URL , 
            json={'model': MODEL_NAME , 'prompt' : f'Summarize This : {text}' , 'stream' : False},
            headers=headers
        )

        print("Ollama Response : " , response.text)

        # Ensure Valid Json Response
        response_data = response.text.strip()
        try:
            json_response = json.loads(response_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500 , detail= f'Invalid Json Response from Ollama')
        
        # Extract Summarized Text
        summarize_text = json_response.get('response' , 'No Valid Summary Received')
        return {'summary' : summarize_text}
    
    except requests.exceptions.RequestException as e :
        raise HTTPException(status_code=500 , detail=f'Request To Ollama Model Failed : {str(e)}')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app , host ='0.0.0.0' , port = 8000 , reload = True)
