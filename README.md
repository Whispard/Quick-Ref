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
6. put PDF files you want to use on, inside content folder
7. run `python -m http.server` in that directory (any directory will work if you change `LIB_PATH`)
8. Enjoy!

