# задание 1
"""
Напишите программу, которая проверяет является ли введенное число в терминале четным и положительным.
все иные ситуации должны так же отрабатываться и писаться в терминале.
Например, если число нечетное и положительное, нечетное и отрицательное и т.д.
На любое число должен быть верный вывод
"""

number = int(input('Введите число: '))
if number > 0 and number % 2 == 0:
    print('Число четное и положительное')
elif number < 0 and number % 2 == 0:
    print('Число четное и отрицательное')
elif number > 0 and number % 2 != 0:
    print('Число нечетное и положительное')
elif number < 0 and number % 2 != 0:
    print('Число нечетное и отрицательное')
else:
    print('Число равно 0')
# задание 2

"""
Напишите программу, генератор паролей, которая на входе спрашивает:
1) длину пароля от 5 до 8 символов, если введено число меньше 5 или больше 8, то генерируется случайное число между 5 и 8
2) надо ли включать в пароль цифры, принимая ответ 'да' или 'нет'
3) надо ли включать в пароль прописные буквы, принимая ответ 'да' или 'нет' 
4) надо ли включать в пароль строчные буквы, принимая ответ 'да' или 'нет'
5) надо ли включать в пароль спецсимволы, принимая ответ 'да' или 'нет'
Всего программа должна задать 5 вопросов и получить ответы в терминале
Программа должна генерировать случайный пароль имеющий нужную длину и все выбранные символы, 
порядок символов или повторение не имеет значения.
Используйте вложенные операторы.
Попробуйте сгенерировать пароль из 5 символов с 4 включенными параметрами.
Попробуйте сгенерировать пароль из 8 символов с 1 включенным параметром (например только из цифр).
Если хотите сделать вариант с использованием цикла, сдавайте 2 варианта решения, с циклом и без.

Не пугайтесь если ваш код будет получаться очень большим и будет много повторяющихся элементов, 
на данном этапе это нормально.
"""
import random

alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
alphabet_upper = alphabet_lower.upper()
numbers = '0123456789'
symbols = '!@#$%^&*()_+-='

len_password = int(input('Введите длину пароля от 5 до 8 символов: '))
if len_password < 5 or len_password > 8:  # проверка на ввод числа меньше 5 или больше 8
    print('Вы ввели неверное значение')
    len_password = random.randint(5, 9)  # генерация случайного числа от 5 до 8
    print(f'Длина пароля будет равна {len_password}')
is_lower = input('Надо ли включать в пароль строчные буквы, принимая ответ "да" или "нет": ')
is_upper = input('Надо ли включать в пароль прописные буквы, принимая ответ "да" или "нет": ')
is_numbers = input('Надо ли включать в пароль цифры, принимая ответ "да" или "нет": ')
is_symbols = input('Надо ли включать в пароль спецсимволы, принимая ответ "да" или "нет": ')

password = ''  # переменная для хранения пароля, изначально пустая строка, куда будут добавляться символы

'''тут генерируется от 1 символа, без использования проверки длины пароля, так как
как пароль в любом случае будет минимум 5 знаков по условиям задачи'''
if is_lower == 'да':  # 1
    password += random.choice(alphabet_lower)
if is_upper == 'да':
    password += random.choice(alphabet_upper)
if is_numbers == 'да':
    password += random.choice(numbers)
if is_symbols == 'да':
    password += random.choice(symbols)

'''тут генерируется от 2 символов, и с 5 возможной генерации символа реализована проверка длины пароля
после чего уже все возможные прибавки символов будет сочетаться с проверкой длинны'''
if is_lower == 'да':
    password += random.choice(alphabet_lower)
if len(password) < len_password:  # тут уже начинаем проверять длину пароля
    if is_upper == 'да':
        password += random.choice(alphabet_upper)
    if is_numbers == 'да' and len(password) < len_password:  # проверка на длину пароля до конца программы
        password += random.choice(numbers)
    if is_symbols == 'да' and len(password) < len_password:
        password += random.choice(symbols)

    # тут генерируется от 3 символов
    if len(password) < len_password:  # проверка на длину пароля, чтобы не выполнять код внутри если мы достигли нужной длины
        if is_lower == 'да':
            password += random.choice(alphabet_lower)
        if is_upper == 'да' and len(password) < len_password:
            password += random.choice(alphabet_upper)
        if is_numbers == 'да' and len(password) < len_password:
            password += random.choice(numbers)
        if is_symbols == 'да' and len(password) < len_password:
            password += random.choice(symbols)

        # тут генерируется от 4 символов
        if len(password) < len_password:  # проверка на длину пароля, чтобы не выполнять код внутри если мы достигли нужной длины
            if is_lower == 'да':
                password += random.choice(alphabet_lower)
            if is_upper == 'да' and len(password) < len_password:
                password += random.choice(alphabet_upper)
            if is_numbers == 'да' and len(password) < len_password:
                password += random.choice(numbers)
            if is_symbols == 'да' and len(password) < len_password:
                password += random.choice(symbols)

            # тут генерируется от 5 символов
            if len(password) < len_password:
                if is_lower == 'да':
                    password += random.choice(alphabet_lower)
                if is_upper == 'да' and len(password) < len_password:
                    password += random.choice(alphabet_upper)
                if is_numbers == 'да' and len(password) < len_password:
                    password += random.choice(numbers)
                if is_symbols == 'да' and len(password) < len_password:
                    password += random.choice(symbols)

                # тут генерируется от 6 символов
                if len(password) < len_password:
                    if is_lower == 'да':
                        password += random.choice(alphabet_lower)
                    if is_upper == 'да' and len(password) < len_password:
                        password += random.choice(alphabet_upper)
                    if is_numbers == 'да' and len(password) < len_password:
                        password += random.choice(numbers)
                    if is_symbols == 'да' and len(password) < len_password:
                        password += random.choice(symbols)

                    # тут генерируется от 7 символов
                    if len(password) < len_password:
                        if is_lower == 'да':
                            password += random.choice(alphabet_lower)
                        if is_upper == 'да' and len(password) < len_password:
                            password += random.choice(alphabet_upper)
                        if is_numbers == 'да' and len(password) < len_password:
                            password += random.choice(numbers)
                        if is_symbols == 'да' and len(password) < len_password:
                            password += random.choice(symbols)

                        # тут генерируется от 8 символов
                        if len(password) < len_password:
                            if is_lower == 'да':
                                password += random.choice(alphabet_lower)
                            if is_upper == 'да' and len(password) < len_password:
                                password += random.choice(alphabet_upper)
                            if is_numbers == 'да' and len(password) < len_password:
                                password += random.choice(numbers)
                            if is_symbols == 'да' and len(password) < len_password:
                                password += random.choice(symbols)
'''
Вложенный условный оператор используется чтобы мы не выполнять весь оставшийся код,
если мы уже достигли нужной длины пароля.
В этом дз мы специально делаем длинный повторяющийся код, чтобы потом познать всю прелесть циклов.
Код имеет такую длину чтобы он правильно отрабатывал ситуацию, если пользователь хочет 
сгенерировать пароль только из цифр или только из строчных букв.
'''
print(password)

# задание 3

"""
Напишите программу которая генерирует:
случайный газ от 15 до 25 (не включительно)
случайный баланс от 0 до 2 (не включительно)
случайное количество транзакций в кошельке от 0 до 3 (не включительно)

Если баланс нулевой делаем вывод с биржи рандомной суммы от 1 до 2. 
Используйте оператор not и прибавляем к балансу.

Далее при помощи тернарного оператора программа кладет в
переменную активность которую нужно делать:
Если газ ниже 20 - кладем активность 'Bridge',
Если газ выше 20 - кладем активность 'Swap'
Далее программа должна используя условный оператор проверить что мы 
должны делать и выполнить нужное действия вычитая его цену из баланса,
отработайте ситуацию в случае если не будет хватать баланса на бридж, 
нужно будет добавить проверку баланса и возможность вывода недостающей суммы на баланс
и напечатать сообщение о проделанной работе.
Бридж стоит 2, свап стоит 1.

Вам нужно сделать программу, которая делает чтобы на кошельке было всего 5 транзакций
с учетом изначально сгенерированного кол-ва транз. транзакции каждый раз выбираться 
в зависимости от газа в конкретный момент.
Перед каждой операцией нужно генерировать новое значение стоимости газа.
Учитывайте вариант, что баланс может быть нулевым и нужно будет сделать вывод с биржи.
Учитывайте что вам нужно сделать 5 операций, но не более.
Учитывайте что на старте количество транзакций в кошельке может быть 0.

Попробуйте реализовать без циклов и функций.
Либо сделайте несколько решений, в одном из которых вы будете использовать
только то что проходили.
"""

import random

# 1 раз
# генерация случайных значений
gas_price = random.randint(15, 26)
balance = random.randint(0, 3)
tx_counter_in_wallet = random.randint(0, 4)
tx_counter_target = 5

# выбираем активность в зависимости от цены газа
activity = 'Bridge' if gas_price < 20 else 'Swap'

# если баланс нулевой, выводим с биржи случайную сумму от 1 до 2
if not balance:
    withdraw_amount = random.randint(1, 3) # генерация случайной суммы
    balance += withdraw_amount # добавление к балансу
    print(f'Баланс нулевой, выведено {withdraw_amount} и добавлено к балансу')
    print(f"Баланс: {balance}")

if activity == "Bridge": # если активность бридж
    if balance < 2: # если баланса не хватает на бридж
        withdraw_amount = 2 - balance # считаем сколько надо вывести
        print(f"Баланса не хватило на бридж, вывели {withdraw_amount}")
        balance += withdraw_amount # добавляем к балансу

    balance -= 2 # вычитаем стоимость бриджа
    print(f'Бридж стоит 2, сделана транзакция, баланс: {balance}')
    tx_counter_in_wallet += 1 # увеличиваем счетчик транзакций
    print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")
else: # если активность свап
    balance -= 1 # вычитаем стоимость свапа
    print(f'Свап стоит 1, сделана транзакция, баланс: {balance}')
    tx_counter_in_wallet += 1 # увеличиваем счетчик транзакций
    print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")

# повторяем операции пока не достигнем нужного количества транзакций
# 2 раз
if tx_counter_in_wallet < tx_counter_target:
    if not balance:
        withdraw_amount = random.randint(1, 3)
        balance += withdraw_amount
        print(f'Баланс нулевой, выведено {withdraw_amount} и добавлено к балансу')
        print(f"Баланс: {balance}")

    gas_price = random.randint(15, 26)
    activity = 'Bridge' if gas_price < 20 else 'Swap'

    if activity == "Bridge":
        if balance < 2:
            withdraw_amount = 2 - balance
            print(f"Баланса не хватило на бридж, вывели {withdraw_amount}")
            balance += withdraw_amount

        balance -= 2
        print(f'Бридж стоит 2, сделана транзакция, баланс: {balance}')
        tx_counter_in_wallet += 1
        print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")
    else:
        balance -= 1
        print(f'Свап стоит 1, сделана транзакция, баланс: {balance}')
        tx_counter_in_wallet += 1
        print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")

    # делаем вложенные операции, чтобы в случае достижения нужного количества транзакций пропускать код
    # 3 раз
    if tx_counter_in_wallet < tx_counter_target:
        if not balance:
            withdraw_amount = random.randint(1, 3)
            balance += withdraw_amount
            print(f'Баланс нулевой, выведено {withdraw_amount} и добавлено к балансу')
            print(f"Баланс: {balance}")

        gas_price = random.randint(15, 26)
        activity = 'Bridge' if gas_price < 20 else 'Swap'

        if activity == "Bridge":
            if balance < 2:
                withdraw_amount = 2 - balance
                print(f"Баланса не хватило на бридж, вывели {withdraw_amount}")
                balance += withdraw_amount

            balance -= 2
            print(f'Бридж стоит 2, сделана транзакция, баланс: {balance}')
            tx_counter_in_wallet += 1
            print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")
        else:
            balance -= 1
            print(f'Свап стоит 1, сделана транзакция, баланс: {balance}')
            tx_counter_in_wallet += 1
            print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")

        # 4 раз
        if tx_counter_in_wallet < tx_counter_target:
            if not balance:
                withdraw_amount = random.randint(1, 3)
                balance += withdraw_amount
                print(f'Баланс нулевой, выведено {withdraw_amount} и добавлено к балансу')
                print(f"Баланс: {balance}")

            gas_price = random.randint(15, 26)
            activity = 'Bridge' if gas_price < 20 else 'Swap'

            if activity == "Bridge":
                if balance < 2:
                    withdraw_amount = 2 - balance
                    print(f"Баланса не хватило на бридж, вывели {withdraw_amount}")
                    balance += withdraw_amount

                balance -= 2
                print(f'Бридж стоит 2, сделана транзакция, баланс: {balance}')
                tx_counter_in_wallet += 1
                print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")
            else:
                balance -= 1
                print(f'Свап стоит 1, сделана транзакция, баланс: {balance}')
                tx_counter_in_wallet += 1
                print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")

            # 5 раз
            if tx_counter_in_wallet < tx_counter_target:
                if not balance:
                    withdraw_amount = random.randint(1, 3)
                    balance += withdraw_amount
                    print(f'Баланс нулевой, выведено {withdraw_amount} и добавлено к балансу')
                    print(f"Баланс: {balance}")

                gas_price = random.randint(15, 26)
                activity = 'Bridge' if gas_price < 20 else 'Swap'

                if activity == "Bridge":
                    if balance < 2:
                        withdraw_amount = 2 - balance
                        print(f"Баланса не хватило на бридж, вывели {withdraw_amount}")
                        balance += withdraw_amount

                    balance -= 2
                    print(f'Бридж стоит 2, сделана транзакция, баланс: {balance}')
                    tx_counter_in_wallet += 1
                    print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")
                else:
                    balance -= 1
                    print(f'Свап стоит 1, сделана транзакция, баланс: {balance}')
                    tx_counter_in_wallet += 1
                    print(f"Транзакций в кошельке: {tx_counter_in_wallet}, осталось сделать {tx_counter_target - tx_counter_in_wallet}")
