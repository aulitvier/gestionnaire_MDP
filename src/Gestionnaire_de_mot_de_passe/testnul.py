# chaine = "UVGGUV"

# lettres = " ".join(list(chaine))
# lettres_virgules = lettres.replace(" ", ", ")

# liste_mots = lettres_virgules.split(',')
# # finded = []
# # for element in liste_mots:
# #     match element:
# #         case "V" | "U" | "G":
# #             finded += element
        
    
# # print(finded)
# # print(liste_mots)


# finded = []


# for i in liste_mots:
#     match i:
#         case "V" | "U" | "G":
#             finded += i            
#             liste_mots = liste_mots.remove(i)
#     print(finded)

# chaine = "ozrfzeozdzcffzuzfzeu"
# lettres_recherchees = ['o', 'u']
# i = 0

# for caractere in chaine:
#     if caractere in lettres_recherchees:
#         i += 1
#         break
#     else :
#         print("1")
#     print("E")
# print(i)

from django.contrib.auth.hashers import make_password

# def measure_pbkdf2_speed():
#     password = 'Oli458$&!TGS'
#     # nbtent = 100000  # Nombre d'itérations à mesurer
#     # duration = timeit.timeit(lambda: make_password(password, iterations=nbtent), number=1)
#     # print(f"Temps d'exécution PBKDF2 : {duration} secondes")
#     # iterations = PBKDF2PasswordHasher.iterations * 100

# password = 'Oli458$&!TGS'
# my_password = make_password(password)

# print(my_password)