
Seu trabalho é consumir o endpoint GET https://sdw-2023-prd.up.railway.app/users/{id} (API da Santander Dev Week 2023) para obter os dados de cada cliente.
Depois de obter os dados dos clientes, você vai usar a API do ChatGPT (OpenAI) para gerar uma mensagem de marketing personalizada para cada cliente. Essa mensagem deve enfatizar a importância dos investimentos.
Uma vez que a mensagem para cada cliente esteja pronta, você vai enviar essas informações de volta para a API, atualizando a lista de "news" de cada usuário usando o endpoint PUT https://sdw-2023-prd.up.railway.app/users/{id}.

# Utilize sua própria URL se quiser ;)
# Repositório da API: https://github.com/digitalinnovationone/santander-dev-week-2023-api
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

#Extract

import pandas as pd

df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

import requests
import json

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

#Etapa de transformação, precisou ser adaptada com mensagens geradas no ChatGPT e não dentro do próprio código, devido a problemas com assinatura/créditos.

import requests
import random

def generate_random_message(user):
    "O futuro é construído por aqueles que têm a coragem de investir no presente."
    "Cada investimento é um passo mais próximo da realização dos seus sonhos financeiros."
    "O tempo é seu aliado no mundo dos investimentos; comece hoje a colher os frutos no futuro."
    "Investir é a chave que transforma sonhos em realidade financeira."
    "Não deixe o medo da incerteza deter você; o investimento é o caminho para o crescimento patrimonial."

    phrases = [
        f"Olá {user}! O futuro é construído por aqueles que têm a coragem de investir no presente.",
        f"Caro {user}, cada investimento é um passo mais próximo da realização dos seus sonhos financeiros."
    ]

    random_message = random.choice(phrases)

    return random_message

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

def update_user_messages(user_id, new_messages):
    user_data = get_user(user_id)
    if user_data:
        current_messages = user_data.get('news', [])
        current_messages.extend(new_messages)
        user_data['news'] = current_messages
        response = requests.put(f'{sdw2023_api_url}/users/{user_id}', json=user_data)
        return True if response.status_code == 200 else False

for user_id in user_ids:
    user_data = get_user(user_id)
    if user_data:
        user_name = user_data['name']  
        new_message = generate_random_message(user_name) 
        print(new_message)

#Etapa final - Load

if 'news' not in user_data:
       user_data['news'] = []
       user_data['news'].append({
       "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
       "description": new_message
        })

success = update_user(user_data)
print(f"User {user_name} (ID: {user_id}) updated? {success}")
