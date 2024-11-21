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

##  Многострочные комментарии:

{#
Это многострочный
комментарий
#}


##  Массивы:

[ значение значение значение ... ]

##  Словари:

begin
 имя := значение;
 имя := значение;
 имя := значение;
 ...
end

##  Имена:

61
[a-z]+

##  Значения:

• Числа.
• Строки.
• Массивы.
• Словари.

##  Строки:

"Это строка"

##  Объявление константы на этапе трансляции:

имя = значение;

##  Вычисление константы на этапе трансляции:

$имя$

Результатом вычисления константного выражения является значение.

Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.

