# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import openai  # Make sure to install the 'openai' library using pip

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

def analyze_text(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [char for char in tokens if char not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]

    return {"tokens": lemmatized_words, "response": "should be Tunisian recipe"}

class AnalyseTexteInput(BaseModel):
    texte: str

@app.post("/analyse")
def analyse_endpoint(analyse_input: AnalyseTexteInput):
    analyzed_data = analyze_text(analyse_input.texte)
    
    # Call OpenAI GPT-3.5-turbo for generating a response
    response_from_gpt = generate_response_with_openai(analyzed_data)
    
    return {"analyzed_data": analyzed_data, "recette": response_from_gpt}

def generate_response_with_openai(analyzed_data):
    # Prepare a prompt for OpenAI GPT-3.5-turbo
    prompt = f"You are a helpful assistant. {analyzed_data['response']}. User: {analyzed_data['tokens']}"
    
    # Make a request to OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the appropriate GPT-3.5-turbo engine
        prompt=prompt,
        max_tokens=100,  # Adjust the max_tokens parameter as needed
        temperature=0.7,  # Adjust the temperature parameter as needed
        stop=None  # You can add stop words to limit the response length
    )
    
    return response.choices[0].text.strip()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
