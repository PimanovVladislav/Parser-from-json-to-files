# Parser-from-json-to-files
Скрипт получает по ссылке два json-файла и формирует текстовые отчеты из их данных
в первом файле хранится информация о пользователях, во втором - задачи, которые каждый пользователь выполнил или не выполнил
отчет формируется по каждому пользователю с информацией о количестве решенных и нерешенных задач
если отчет по данному пользователю уже существует, то существующий файл переименовывается с добавлением даты создания отчета. Таким образом, можно отличить архивный отчет и актуальный
