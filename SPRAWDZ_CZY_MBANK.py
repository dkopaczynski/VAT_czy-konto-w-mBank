import requests
import pandas as pd
from tqdm import tqdm

df = pd.DataFrame(columns=['name', 'nip', 'regon', 'result'])

with open('nipy.txt', 'r') as f:
    nips = f.readlines()

for nip in tqdm(nips):
    nip = nip.strip()
    url = f'https://wl-api.mf.gov.pl/api/search/nip/{nip}?date=2023-01-28'
    response = requests.get(url)
    data = response.json()
    try:
        name = data['result']['subject']['name']
        regon = data['result']['subject']['regon']
        account_numbers = data['result']['subject']['accountNumbers']
        found = False
        for number in account_numbers:
            if number[2:6] == '1140':
                found = True
                break
        if found:
            df = pd.concat([df, pd.DataFrame({'name': [name], 'nip': [nip], 'regon': [regon], 'result': ['TAK']})], ignore_index=True)
        else:
            df = pd.concat([df, pd.DataFrame({'name': [name], 'nip': [nip], 'regon': [regon], 'result': ['NIE']})], ignore_index=True)
    except KeyError:
        pass
    except:
        print(data)

df.to_excel('result.xlsx', index=False)
