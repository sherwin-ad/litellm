import cohere

co = cohere.ClientV2(api_key="ZaogZhzbsVthBDh7UdMh1pAXv0rqX65vFyW6hVxi")

response = co.chat(
    model="command-a-03-2025",
    messages=[
        {"role": "user", "content": "hello"}
    ]
)

print(response)