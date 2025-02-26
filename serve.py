import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langserve import add_routes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()

load_dotenv()
groqKEY = os.getenv("GROQ_API_KEY")

try:
    model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groqKEY)
    print("Groq model instantiated successfully!")
except Exception as e:
    print(f"Error instantiating Groq model: {e}")
    model = None

if model: # Only proceed if the model was successfully instantiated.
    try:
        systemTemplate = "Translate the following into: {language}"
        promptTemplate = ChatPromptTemplate.from_messages([
            ("system", systemTemplate),
            ("user", "{text}")
        ])
        print("Prompt Template created successfully!")

        parser = StrOutputParser()
        print("Parser created successfully!")

        chain = promptTemplate | model | parser
        print("Chain created successfully!")

        add_routes(
            app,
            chain,
            path="/chain"
        )
        print("Routes added successfully!")

    except Exception as e:
        print(f"Error creating chain or adding routes: {e}")

@app.get("/test")
def test_endpoint():
    return {"message": "Test successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)