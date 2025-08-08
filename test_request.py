import requests

data = {
    "url": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the sum insured?",
        "Who is the policyholder?"
    ]
}

res = requests.post("http://127.0.0.1:8000/hackrx/run", json=data)
print(res.status_code)
print(res.json())
