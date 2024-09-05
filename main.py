from ShuntingYard import shunting_yard

r = input("Ingresa la expresión regular: ")
#w = input("Ingresa la cadena a validar: ")

postfix = shunting_yard(r)

print (postfix)

