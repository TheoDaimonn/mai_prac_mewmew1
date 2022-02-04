import configparser  # импортируем библиотеку

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("cfg.ini")
print(config['Pepega']['serv_adress'])