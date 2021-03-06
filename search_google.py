from bs4 import BeautifulSoup
import requests

def search(query, type):
    
    if len(query) == 0:
        return query

    if 'delhi' in query.lower() or 'ncr' in query.lower():
        return 'Delhi'

    query1 = query + ' ' + type
    
    # making query
    query_string = query1.replace(" ", "%20")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    r = requests.get(f'https://www.google.com/search?q={query_string}', headers=headers)
    # query ends here

    # Sensitive code starts here
    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('h2', class_='qrShPb kno-ecr-pt PZPZlf mfMhoc')
    if result is not None:
        index = str(result).index("span")
        result = str(result)[index+5:]
        index = result.index("<")
        result = result[:index]
    # Sensitive code ends here

    # if str(result) == "None":
    #     result = soup.find('h2', class_='qrShPb kno-ecr-pt PZPZlf mfMhoc EaHP9c')
    #     print(str(result))

    if result != None:
        return str(result)
    return query
