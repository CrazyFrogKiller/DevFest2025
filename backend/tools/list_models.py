import os
import json

try:
    import google.generativeai as genai
except Exception as e:
    print("google.generativeai not installed:", e)
    raise SystemExit(2)

KEY = "AIzaSyCixdQHuUh6lSfPDqOgmo8TUJiT8nfBe9Y"
if not KEY:
    print("ERROR: GOOGLE_API_KEY environment variable is not set. Set it or add it to your .env.")
    raise SystemExit(3)

genai.configure(api_key=KEY)

try:
    models = genai.list_models()
    try:
        for i in json.dumps(models, indent=2, ensure_ascii=False):
            print(i)
    except Exception:
        for i in models:
            print(i)
except Exception as e:
    print("ListModels call failed:", str(e))
    raise SystemExit(4)
