import xml.etree.ElementTree as ET
import requests


url = f"http://cep.republicavirtual.com.br/web_cep.php?cep=80215901&formato=xml"

resp = requests.get(url)
root = ET.fromstring(resp.text)
print(root.findtext('tipo_logradouro'), root.findtext('logradouro'))
print(root.findtext('bairro'))
print(root.findtext('cidade'), root.findtext('uf'), sep='-')
