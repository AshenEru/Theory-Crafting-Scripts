import os
from openai import OpenAI

# 1. Directly use the key string for this test to ensure it works
# 2. Add the required OpenRouter headers
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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", # Use the string directly for now
    default_headers={
        "HTTP-Referer": "http://localhost", 
        "X-Title": "Arch Essay Tool",
    }
)

# 3. Use a Chat Completion (the endpoint we actually use) instead of 'retrieve'
try:
    response = client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet",
        messages=[{"role": "user", "content": "Say 'Connection Successful'"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")