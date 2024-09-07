from ShuntingYard import shunting_yard
from thompson import get_alphabet, thomspon_main
from subset import set_main
import json
r = input("Ingresa la expresión regular: ")

# Convierte a postfix
postfix = shunting_yard(r)
# convierte a no determinista
afn = thomspon_main(postfix)
# convierte a determinista
afd = set_main(afn)

# por ahora, lo guarda en el finite_deterministic.json
with open('finite_deterministic.json', 'w') as json_file:
    json.dump(afd, json_file, indent=4)
    
#w = input("Ingresa la cadena a validar: ")

