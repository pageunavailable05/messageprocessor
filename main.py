from dotenv import load_dotenv
import os

load_dotenv()

print("Environment ready!")
print(f"DB_HOST: {os.getenv('DB_HOST', 'not set')}")