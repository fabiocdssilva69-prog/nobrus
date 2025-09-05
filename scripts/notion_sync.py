#!/usr/bin/env python3
"""
Script para sincronizar conteúdos com um banco de dados do Notion.
Exemplos de uso:
  # Listar itens do banco de dados
  python notion_sync.py --token <seu_token> --database-id <id>

  # Criar um novo item com título e conteúdo
  python notion_sync.py --token <seu_token> --database-id <id> --title "Meu Título" --content "Conteúdo do diário"
"""
import argparse
import json
import os
import requests

NOTION_API_BASE_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def list_database_items(database_id: str, token: str) -> dict:
    url = f"{NOTION_API_BASE_URL}/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_page(database_id: str, properties: dict, token: str) -> dict:
    url = f"{NOTION_API_BASE_URL}/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

def update_page(page_id: str, properties: dict, token: str) -> dict:
    url = f"{NOTION_API_BASE_URL}/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    payload = {"properties": properties}
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Sincroniza conteúdos com um banco de dados do Notion.")
    parser.add_argument("--token", required=True, help="Token de integração do Notion")
    parser.add_argument("--database-id", required=True, help="ID do banco de dados do Notion")
    parser.add_argument("--title", help="Título do item a ser criado (opcional)")
    parser.add_argument("--content", help="Conteúdo do item a ser criado (opcional)")
    args = parser.parse_args()

    if args.title and args.content:
        properties = {
            "Name": {"title": [{"text": {"content": args.title}}]},
            "Content": {"rich_text": [{"text": {"content": args.content}}]},
        }
        page = create_page(args.database_id, properties, args.token)
        print("Página criada:", page.get("id"))
    else:
        data = list_database_items(args.database_id, args.token)
        print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
