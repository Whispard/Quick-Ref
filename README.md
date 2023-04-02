# Quick Ref

Chromme Extensions to get references quickly from your local files.
then you can open each page and summarise the results.

Star button is to summarise (same pdfs)


## Setup
1. Clone the repo
2. Go to `chrome://extensions` and enable developer mode
3. Click on Load unpacked and select the `quick-ref` folder to load the extension
4. set openAI key in `api_key.py`
5. install dependencies `pip install -r requirements` (use venv in case of conflicts)
6. run `python main.py`
7. put PDF files you want to use on, inside content folder
8. run `python -m http.server` in that directory (any directory will work if you change `LIB_PATH`)
9. Enjoy!

## Made With
- Chroma
- OpenAI (embeddings & Chat Completion)
- FastAPI
- PyPDF2
- Bootstrap

## Screenshots
![Sample](screenshots/sample.png)
![Hack1](screenshots/hack1.png)
![Hack2](screenshots/hack2.png)
![Hack3](screenshots/hack3.png)