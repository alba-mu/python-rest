# ---------------------------------------------------------------
# Script per fer proves amb l'API sense accedir al navegador
# ---------------------------------------------------------------

import urllib3
import json

# Funció que permet fer requests a l'API i retorna el json de resposta
def request(path: str, json: dict, headers: dict | None = None) -> dict:
    resp = urllib3.request(
    "POST",
    f"http://127.0.0.1:8000{path}",
    json= json,
    headers={"Content-Type": "application/json"}
    )
    return resp.json()



item_dict = {
    "name": "Apple",
    "description": "Apple",
    "price": 45.2,
    "tax": 2.5
}



# Funció json.dumps() permet printar json pretty (més llegible)
print(json.dumps(request("/item", json=item_dict), indent=2))
