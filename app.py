from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import configs.config as config
import scraper
import processing.documents as document_processing
from stores.chroma import store_embeddings
import speech_to_text.gemini as gemini

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load environment variables
config.set_envs()

# Optional scraping
if config.START_WEB_SCRAPING_MYSCHEMES:
    scraper.scrape_and_store_to_json_file()

# Load documents
documents = document_processing.load_json_to_langchain_document_schema("myschemes_scraped.json")
documents = document_processing.split_documents(documents)

# Store embeddings
faiss_db = store_embeddings(documents, config.EMBEDDINGS)

retriever = faiss_db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 8, "fetch_k": 10}
)

# Language schema
class Language(BaseModel):
    text: str
    language: str
    language_code: str


# Gemini client
from google import genai
import os

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))


@app.post("/chat")
async def chat(text: str = Form(...), language: str = Form("en-US")):
    try:
        user_input = text
        user_language_code = language

        lang_name_map = {
            "en-US": "English",
            "hi-IN": "Hindi",
            "pa-IN": "Punjabi"
        }

        user_language = lang_name_map.get(language, "English")

        # -------- TRANSLATE QUERY TO ENGLISH --------
        search_query = user_input

        if language != "en-US":
            translation_prompt = f"""
Translate the following {user_language} text into English.
Only output translated English text.

Text:
{user_input}
"""

            translation = client.models.generate_content(
                model="gemma-3-4b-it",
                contents=translation_prompt
            )

            search_query = translation.text.strip()

        # Improve semantic search
        search_query = f"Indian government scheme related to {search_query}"

        docs = retriever.invoke(search_query)

        print("Retrieved docs:", docs)

        context = "\n\n".join(
            [doc.page_content for doc in docs if hasattr(doc, "page_content")]
        )

        # -------- IF DATABASE HAS INFO --------
        if context:

            final_prompt = f"""
You are an expert assistant for Indian Government Schemes.

Use the context to answer the question.

Provide answer in this format:

Scheme Name:
Benefits:
Eligibility:
How to Apply:

Question:
{user_input}

Context:
{context}

Answer:
"""

            response = client.models.generate_content(
                model="gemma-3-4b-it",
                contents=final_prompt
            )

            answer = response.text

        # -------- FALLBACK IF NO CONTEXT --------
        else:

            fallback_prompt = f"""
You are an expert assistant on Indian Government Schemes.

Answer clearly using general knowledge.

Provide:

Scheme Name
Benefits
Eligibility
How to Apply

User Question:
{user_input}
"""

            fallback = client.models.generate_content(
                model="gemma-3-4b-it",
                contents=fallback_prompt
            )

            answer = fallback.text

        # -------- TRANSLATE OUTPUT --------
        if user_language != "English":

            translate_prompt = f"""
Translate the following text into {user_language}.
Keep meaning accurate.

Text:
{answer}
"""

            translated = client.models.generate_content(
                model="gemma-3-4b-it",
                contents=translate_prompt
            )

            answer = translated.text

        # -------- TEXT TO SPEECH --------
        gemini.tts(answer, user_language_code)

        return {"response": answer}

    except Exception as e:
        import traceback
        logger.error(f"An error occurred: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An internal error occurred")


@app.get("/download")
def download_file():
    file_path = "output.mp3"
    return FileResponse(file_path, media_type="audio/mpeg", filename="output.mp3")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)