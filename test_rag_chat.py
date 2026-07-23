import requests
import json

url = "http://127.0.0.1:8000/api/chat"

# Test 1: Greeting
print("=" * 60)
print("TEST 1: Saludo")
print("=" * 60)
payload = {"messages": [{"role": "user", "content": "Hola"}]}
r = requests.post(url, json=payload, timeout=30)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()['response'][:500]}")

# Test 2: Programs
print("\n" + "=" * 60)
print("TEST 2: Programas de voluntariado")
print("=" * 60)
payload = {"messages": [{"role": "user", "content": "Que programas de voluntariado hay disponibles?"}]}
r = requests.post(url, json=payload, timeout=30)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()['response'][:500]}")

# Test 3: Stats
print("\n" + "=" * 60)
print("TEST 3: Estadisticas")
print("=" * 60)
payload = {"messages": [{"role": "user", "content": "Cuantos voluntarios hay registrados en el sistema?"}]}
r = requests.post(url, json=payload, timeout=30)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()['response'][:500]}")

# Test 4: Roles
print("\n" + "=" * 60)
print("TEST 4: Roles del sistema")
print("=" * 60)
payload = {"messages": [{"role": "user", "content": "Que roles existen y que permisos tiene cada uno?"}]}
r = requests.post(url, json=payload, timeout=30)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()['response'][:500]}")

# Test 5: Tech stack
print("\n" + "=" * 60)
print("TEST 5: Tecnologias del proyecto")
print("=" * 60)
payload = {"messages": [{"role": "user", "content": "Con que tecnologias esta construido VolunSys?"}]}
r = requests.post(url, json=payload, timeout=30)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()['response'][:500]}")

print("\n" + "=" * 60)
print("TODOS LOS TESTS COMPLETADOS")
print("=" * 60)
