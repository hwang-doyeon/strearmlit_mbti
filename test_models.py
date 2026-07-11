import google.generativeai as genai
import re

with open('.streamlit/secrets.toml', 'r') as f:
    content = f.read()
key = re.search(r'"([^"]+)"', content).group(1)

genai.configure(api_key=key)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
