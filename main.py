import chromadb, os
from chromadb.utils import embedding_functions
from pydantic import BaseModel
import uvicorn
from ai_tests import run_tests
from chromadb.config import Settings
import make_embeds
import pathlib
from fastapi import FastAPI
import openai
from api_key import API_KEY
from integrations import open_reader, READER_TO_USE, ENABLE_HIGHLIGHT
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = API_KEY
SUMMARISE_WITH_GPT = True
USE_OPENAI_EMBEDDINGS = False

COLLECTION_NAME = "all_collection"
LIB_PATH = 'content'  # => 'content'
DB_PATH = ".chromadb"  # => 'chromadb'

if API_KEY == "":
    SUMMARISE_WITH_GPT = False
    print("Disabling summarisation & openAI embeddings since OpenAI key not found.(You can Add it in api_key.py")
    USE_OPENAI_EMBEDDINGS = False

if READER_TO_USE is not None:
    print(f"Using PDF Reader {READER_TO_USE}")

if USE_OPENAI_EMBEDDINGS:
    embedding_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai.api_key,
        model_name="text-embedding-ada-002"
    )

else:
    embedding_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=DB_PATH,
    ))

print("Available collections: ", [x.name for x in chroma_client.list_collections()])
if COLLECTION_NAME in [x.name for x in chroma_client.list_collections()]:
    collection = chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_ef)
else:
    print("Creating Collection ", COLLECTION_NAME)
    collection = chroma_client.create_collection(name=COLLECTION_NAME, embedding_function=embedding_ef)
    docs, metas, ids = make_embeds.make(LIB_PATH)
    collection.add(
        documents=docs,
        metadatas=metas,
        ids=ids
    )

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Prompt(BaseModel):
    data: str
    num: int = 3
    summarised: bool = False


def makeUri(pdf, pageNo):
    if READER_TO_USE is not None:
        return pdf
    path_string = os.path.join(os.getcwd(), LIB_PATH, pdf)
    uri = pathlib.Path(path_string).as_uri()
    return f"{uri}#page={pageNo}"


def chatSummarise(content, prompt):
    if not SUMMARISE_WITH_GPT:
        return content
    prompt = f"get information related to  \"{prompt}\" from this text : " + content
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    answer = response["choices"][0]["message"]["content"]
    print("Summarised: ", answer)
    return answer


current_outputs = []
current_prompt = ""


def get_results(prompt: Prompt):
    results = collection.query(
        query_texts=[prompt.data],
        n_results=prompt.num
    )
    print(
        f"DEBUG: {prompt.data} => Page {results['metadatas'][0][0]['page']}, {results['metadatas'][0][0]['pdf']} : {results['documents'][0][0]}")

    outputs = []
    sum_outputs = []
    qpdfs = {}
    for i in range(len(results['ids'][0])):
        pdf = results['metadatas'][0][i]['pdf']
        pageNo = results['metadatas'][0][i]['page']
        content = results['documents'][0][i]
        output = {
            "pdf": pdf,
            "pageNo": [pageNo],
            "uri": makeUri(pdf, pageNo),
            "content": content
        }
        outputs.append(output)
        if not prompt.summarised:
            continue

        if not pdf in qpdfs:
            qpdfs[pdf] = i
            sum_outputs.append(output)
            continue

        if len(sum_outputs[qpdfs[pdf]]["pageNo"]) > 2:
            continue
        if len(content) > 1000:
            continue
        sum_outputs[qpdfs[pdf]]["pageNo"].append(pageNo)
        sum_outputs[qpdfs[pdf]]["content"] += "\n" + content

    for out in sum_outputs:
        if len(out["pageNo"]) > 1:
            out["content"] = chatSummarise(out["content"], prompt.data)

    global current_outputs, current_prompt
    current_outputs = outputs
    current_prompt = prompt.data
    if not prompt.summarised:
        return outputs
    return sum_outputs


@app.post("/")
async def root(prompt: Prompt):
    return get_results(prompt)


@app.get('/open-reader/{index}')
async def run_reader(index):
    highlight = ""
    if ENABLE_HIGHLIGHT:
        highlight = current_prompt
    open_reader(
        READER_TO_USE,
        os.path.join(LIB_PATH, current_outputs[int(index)]["pdf"]),
        current_outputs[int(index)]["pageNo"][0],
        highlight
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
