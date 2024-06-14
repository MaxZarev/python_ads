# задание 1
'''
Придумай переменные имя, количество акков, сумма дропа, цена ламбо,
количество ламбо и подставь чтобы все считалось сами.
Используйте f строки
'''
name = "Max"
accs = 800
drop = 1000
lambo_price = 300000
print(f"Hello, Brayan, My name is {name}, I have 1000 accs LayerZero")
print(f"I want airdrop {drop}$ for every acc")
print(f"Give me my drop = {drop}$ * {accs} accs = {drop * accs}$")
print(f"I want to buy Lambo, lambo price {lambo_price}$")
print(f"I want to buy {drop * accs // lambo_price} Lambo")  # используем целочисленное деление //

# задание 2
'''
Поменяйте местами значения переменных name и surname не используя дополнительных переменных.
Дополните код так, чтобы переменная full_name содержала имя и фамилию через пробел
'''
surname = "Max"
name = "Zarev"
name, surname = surname, name
full_name = f"{name} {surname}"
print(f"My name is {name}, my surname is {surname}")
print(f"My full name is {full_name}")

# задание 3
'''
Доработайте код чтобы он печатал 10, 20, 30, 40 используя переменную total
'''

total = 0
total = total + 10
print(total)
total = total + 10
print(total)
total = total + 10
print(total)
total = total + 10
print(total)

# задание 4
'''
Напишите программу-рецепт шаурмы, чтобы робот готовил шаурму с курицей, говядиной или овощами
с обычным лавашeм или лавашом с сыром
на старте программы вы должны написать какой лаваш использовать и какая будет начинка, 
а робот должен собрать шаурму и написать об этом в терминале
'''
meat = "курица"
lavash = "лаваш с сыром"

print(f"Используем {lavash} и начинку из овощей и мяса {meat}")
print(f"Берем овощи и мясо - {meat}!")
print(f"Собираем шаурму из овощей и мяса - {meat} в {lavash}!")
print(f"Шаурма готова! Приятного аппетита! Кожаный ублюдок!")
