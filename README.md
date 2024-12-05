#  Задание 3
#  Вариант 12

Разработать на python инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. 

Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.

Входной текст на учебном конфигурационном языке принимается из
файла, путь к которому задан ключом командной строки. Выходной текст на
языке yaml попадает в стандартный вывод.

## 1. Клонирование репозитория

Клонируйте репозиторий с исходным кодом и тестами:

```bash
git clone <URL репозитория>
cd <директория проекта>
```

## 2. Виртуальное окружение

```shell
python -m venv venv
venv/Scripts/activate
```

## 3. Установка зависимостей

```shell
pip install -r requirements.txt
```

## 4. Запуск программы

Запуск в режиме **GUI**:

```shell
py main.py 
```


## 5. Тестирование

Для запуска тестирования необходимо запустить следующий скрипт:

```shell
pytest -v
```

##  Многострочные комментарии:

```
{#
Это многострочный
комментарий
#}
```


##  Массивы:

```
[ значение значение значение ... ]
```

##  Словари:

```
begin
 имя := значение;
 имя := значение;
 имя := значение;
 ...
end
```

##  Имена:

```
61
[a-z]+
```

##  Значения:

• Числа.
• Строки.
• Массивы.
• Словари.

##  Строки:

```
"Это строка"
```

##  Объявление константы на этапе трансляции:

```
имя = значение;
```

##  Вычисление константы на этапе трансляции:

```
$имя$ 
```

Результатом вычисления константного выражения является значение.

Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.

![image](https://github.com/user-attachments/assets/ca014a75-77e2-4a58-a17e-a2326769b126)


##  Тестирование

![image](https://github.com/user-attachments/assets/26d3fee4-b1d3-432e-b81a-e18b0514ecb4)


![image](https://github.com/user-attachments/assets/644c5d7a-e53b-4274-a347-74d736789759)


