""""""



"""
Сделайте программу, которая берёт 3 файла:
	•	список номеров профилей,
	•	список прокси,
	•	список IP-адресов.
Программа извлекает списки из файлов, по очереди берёт профиль, устанавливает туда прокси,
запускает профиль и переходит по ссылке https://api.ipify.org/?format=json, чтобы получить
текущий IP-адрес. Программа сравнивает IP-адрес с тем, что был взят из файла.
Если IP-адреса совпадают, программа пишет в лог "№ {номер профиля} Success".
"""