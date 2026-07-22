import g4f
from g4f.client import Client
from g4f.Provider import DuckDuckGo, Blackbox, PollinationsAI

def test_provider(provider):
    try:
        client = Client(provider=provider)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hola"}],
        )
        print(f"SUCCESS {provider.__name__}: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"FAILED {provider.__name__}: {e}")
        return False

print("Testing providers...")
test_provider(DuckDuckGo)
test_provider(Blackbox)
test_provider(PollinationsAI)
