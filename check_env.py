from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("HUGGINGFACE_API_KEY")
print("KEY FOUND:", key is not None)
print("VALUE:", key)
