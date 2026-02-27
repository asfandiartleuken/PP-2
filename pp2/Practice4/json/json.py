import json

# JSON файлын ашып, оқу
with open('sample-data.json', 'r') as file:
    data = json.load(file)

# Интерфейстер тізімін алу (imdata ішінде орналасқан)
interfaces = data['imdata']

# Кестенің тақырыбын шығару
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6}")
print(f"{'-'*50} {'-'*20} {'-'*8} {'-'*6}")

# Суреттегідей алғашқы 3 интерфейсті шығару
for i in range(3):
    # 'attributes' бөліміне қол жеткізу
    attributes = interfaces[i]['l1PhysIf']['attributes']
    
    # Қажетті мәндерді алу
    dn = attributes.get('dn', '')
    descr = attributes.get('descr', '')
    speed = attributes.get('speed', '')
    mtu = attributes.get('mtu', '')
    
    # Жолды форматтап шығару
    print(f"{dn:<50} {descr:<20} {speed:<8} {mtu:<6}")