import random

# my_colors = ['red', 'green', 'blue']
# print(id(my_colors))
# print(my_colors)
#
# # получение элемента по индексу
# print(my_colors[0])
#
# # изменение элемента по индексу
# my_colors[0] = 'orange'
# print(my_colors)
#
# # добавление элемента в конец списка
# my_colors.append('yellow')
# print(my_colors)
#
# # добавление элемента на определенную позицию
# my_colors.insert(1, 'black')
# print(id(my_colors))
# print(my_colors)
#
# # удаление элемента по значению
# del my_colors[0]
# print(my_colors)

# удаление элемента по индексу и возврат его значения
# my_colors = ['red', 'green', 'blue']
# print(my_colors)
# # el = my_colors.pop(2)
# # print(my_colors)
# # print(el)
# my_colors.pop(2)
# print(my_colors)

# удаление элемента по значению
# my_colors = ['red', 'green', 'blue']
# print(my_colors)
# my_colors.remove('yellow')
# print(my_colors)

# удаление всех элементов
# my_colors = ['red', 'green', 'blue']
# print(my_colors)
# print(id(my_colors))
# my_colors.clear()
# print(my_colors)
# print(id(my_colors))

# получение индекса элемента
# my_colors = ['red', 'green', 'blue', 'red', 'green', 'blue']
# print(my_colors.index('green'))

# поиск элемента в списке
# my_colors = ['red', 'green', "1", 'red', 'green', 'blue']
# print(1 in my_colors)  # искомое значение == значение списка

# chain = "MOONBEAM"
# if chain not in ["BSC", "ETH", "MATIC"]:
#    print("Invalid chain")
#    print("Меняем сеть на BSC")

# конкатенация списков
# my_chains = ["BSC", "ETH", "MATIC"]
# print(id(my_chains))
# new_chains = ["AVAX", "SOL"]
# chains = my_chains + new_chains
# print(chains)
# print(id(chains))

# повторение списка
# my_chains = ["BSC", "ETH", "MATIC"]
# print(id(my_chains))
# chains = my_chains * 3
# print(chains)
# print(id(chains))

# преобразование списка в строку
# my_chains = ["BSC", "ETH", "MATIC"]
# text_chains = ' '.join(my_chains)
# print(type(text_chains))
# print(text_chains)

# получение длинны списка
# my_chains = ["BSC", "ETH", "MATIC", 1]
# print(len(my_chains))

# my_numbers = [0.5, 1, 2, 3, 4, 5.0]
#
# # наименьшее значение в списке
# print(min(my_numbers))
#
# # наибольшее значение в списке
# print(max(my_numbers))
#
# # сумма всех элементов списка
# print(sum(my_numbers))

# соединение списков
# my_chains = ["BSC", "ETH", "MATIC"]
# print(id(my_chains))
# new_chains = ["AVAX", "SOL"]
# my_chains.extend(new_chains)
# print(my_chains)
# print(id(my_chains))

# создание списка в цикле
# my_numbers = []
# while len(my_numbers) < 10:
#     random_num = random.randint(1, 1000)
#     if random_num not in my_numbers:
#         my_numbers.append(random_num)
#     else:
#         print(f"Число {random_num} уже есть в списке")
#
# print(my_numbers)
# print(len(my_numbers))
#
# index = 0
# while index < len(my_numbers):
#     print(f"элемент под индексом {index} - {my_numbers[index]}")
#     index += 1
#
# index = 0
# while index < len(my_numbers):
#     my_numbers[index] = my_numbers[index] * 2
#     print(f"элемент под индексом {index} - {my_numbers[index]}")
#     index += 1

# chains = ["BSC", "ETH", "MATIC"]
# index = 0
# while index < len(chains):
#     print(chains[index], end=' ')
#     index += 1
#
# print()
# print(chains)

# chains = ["BSC", "ETH", "MATIC", "AVAX", "SOL"]
# print(*chains, sep=', ')

# chain1, chain2, *chain3 = chains
# print(chain1)
# print(chain2)
# print(chain3)

# сортировка исходного списка
# numbers = [5, 3, 8, 1, 2, 7.5, 4, 6]
# print(numbers)
# numbers.sort()
# print(numbers)
# numbers.sort(reverse=True)
# print(numbers)
#
# chains = ["BSC", "ETH", "MATIC", "AVAX", "SOL"]
# print(chains)
# print(id(chains))
# chains.sort()
# print(chains)
# chains.sort(reverse=True)
# print(chains)
# print(id(chains))

# сортировка списка без изменения исходного
# numbers = [5, 3, 8, 1, 2, 7.5, 4, 6]
# print(numbers)
# sorted_numbers = sorted(numbers, reverse=True)
# print(sorted_numbers)
# print(numbers)

# обратная сортировка списка
# numbers = [5, 3, 8, 1, 2, 7.5, 4, 6]
# print(numbers)
# numbers.reverse()
# print(numbers)

# вложенные списки
# chains = [["BSC", "ETH"], ["MATIC", "AVAX", "SOL"]]
# print(chains[1][1])
# chains[1][1] = "FTM"
# print(chains)
# chains[1] = [[[[]]]]
# print(chains)

# копирование списка
chains = ["BSC", "ETH", "MATIC", "AVAX", ["SOL", "FTM"]]
# copy_chains = chains  # ссылка на оригинальный список
# print(copy_chains)
#
# chains[0] = "SOL"
# print(chains)
# print(copy_chains)
# print(id(chains))
# print(id(copy_chains))

# copy_chains = chains.copy()  # копирование списка
# print(copy_chains)
# chains.pop(1)
# print(id(chains))
# print(id(copy_chains))
# copy_chains = chains[:]

# deepcopy
# import copy
#
# chains = ["BSC", "ETH", "MATIC", "AVAX", ["SOL", "FTM"]]
# copy_chains = copy.deepcopy(chains)









































