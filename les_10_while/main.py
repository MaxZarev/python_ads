# import random
#
# password_length = 20
# alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
# alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# digits = '0123456789'
#
# password = ''
#
# if len(password) < password_length:
#     password += random.choice(alphabet_lower)
#     if len(password) < password_length:
#         password += random.choice(alphabet_upper)
#         if len(password) < password_length:
#             password += random.choice(digits)
#             if len(password) < password_length:
#                 password += random.choice(alphabet_lower)
#                 if len(password) < password_length:
#                     password += random.choice(alphabet_upper)
#                     if len(password) < password_length:
#                         password += random.choice(digits)
#                         if len(password) < password_length:
#                             password += random.choice(alphabet_lower)
#                             if len(password) < password_length:
#                                 password += random.choice(alphabet_upper)
#                                 if len(password) < password_length:
#                                     password += random.choice(digits)
#                                     if len(password) < password_length:
#                                         password += random.choice(alphabet_lower)
#                                         if len(password) < password_length:
#                                             password += random.choice(alphabet_upper)
#                                             if len(password) < password_length:
#                                                 password += random.choice(digits)
#                                                 if len(password) < password_length:
#                                                     password += random.choice(alphabet_lower)
#                                                     if len(password) < password_length:
#                                                         password += random.choice(alphabet_upper)
#                                                         if len(password) < password_length:
#                                                             password += random.choice(digits)
#                                                             if len(password) < password_length:
#                                                                 password += random.choice(alphabet_lower)
#                                                                 if len(password) < password_length:
#                                                                     password += random.choice(alphabet_upper)
#                                                                     if len(password) < password_length:
#                                                                         password += random.choice(digits)
#                                                                         if len(password) < password_length:
#                                                                             password += random.choice(alphabet_lower)
#                                                                             if len(password) < password_length:
#                                                                                 password += random.choice(alphabet_upper)
#                                                                                 if len(password) < password_length:
#                                                                                     password += random.choice(digits)
#                                                                                     if len(password) < password_length:
#                                                                                         password += random.choice(alphabet_lower)
#                                                                                         if len(password) < password_length:
#                                                                                             password += random.choice(alphabet_upper)
#                                                                                             if len(password) < password_length:
#                                                                                                 password += random.choice(digits)
#
# print(password)
#
#
# import random
#
#
# alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
# alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# digits = '0123456789'
# print("Программа генерации пароля запущена")
# # while - пока условие верно, выполняется код внутри цикла
# password = ''
#
# password_length = 20
#
# while len(password) < password_length:
#
#     if random.randint(0, 2):
#         password += random.choice(alphabet_lower)
#
#     if random.randint(0, 2):
#         password += random.choice(alphabet_upper)
#
#     if random.randint(0, 2):
#         password += random.choice(digits)
#
#
# print(f"Программа завершена, пароль {password} {len(password)}")


import random
import time

gas_price = 45
GAS_LIMIT = 25

while gas_price > GAS_LIMIT:
    print(f"Цена на газ {gas_price} выше порога {GAS_LIMIT}")
    time.sleep(1)
    gas_price = random.randint(20, 50)

print("Запускаем программу")

