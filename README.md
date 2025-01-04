Этот скрипт предназначен для загрузки исторических данных по криптовалютным парам с биржами Bybit, их обработки и сохранения в формате CSV. Он использует асинхронный подход для оптимизации работы с API Bybit и поддерживает длительные временные интервалы. Основные функции включают загрузку данных, их формирование и сохранение в двух вариантах CSV-файлов.

Основные функции и логика:
Импорт необходимых библиотек:

aiohttpи asyncioдля асинхронных HTTP-запросов.
pandasдля работы с табличными данными.
datetimeи timedeltaдля управления временными метками.
nest_asyncioдля работы с асинхронным циклом в среде вроде Jupyter Notebook.
Основные параметры:

symbol: Торговая пара (например, ETHUSDT).
interval: Интервал данных меньше (например, 60).
start_timeи end_time: Временные рамки для загрузки данных в формате UNIX (миллисекунды).
Асинхронные функции:

fetch_bybit_ohlcv: Загружает данные за указанный временной интервал с помощью API Bybit.
fetch_all_ohlcv: Делит указанный диапазон на сутки и собирает данные для каждого из них с использованием асинхронных задач.
Форматирование данных:

format_data: Преобразует данные в pandas.DataFrame, вносит временные метки, сортирует и приводит данные к числовому формату.
format_data_prep: Преобразует данные для специальной подготовки в формате CSV с датой, временем и упрощенными заголовками.
Сохранение данных:

save_to_csv: Сохраняет отформатированные данные в стандартный CSV-файл с разделителем ;.
save_to_prep_csv: Сохран передает данные в упрощенном формате без заголовков и со фиксированным обозначением знаков после запятой.
Главная функция:

main:
Собирает все данные через fetch_all_ohlcv.
Форматирует их с помощью format_data.
Сохраняет в двух разных CSV-файлах: полный ( data.csv) и упрощенный ( prep_data.csv).
Запуск скрипта: Используемые события цикла asyncioдля выполнения асинхронной главной функции.

Результат работы:
Данные OHLCV (Open, High, Low, Close, Volume) за заданный период отображаются в двух файлах:
data.csv— полный набор данных.
prep_data.csv— упрощенный формат данных для работы в TSLab.
Примечания:
Скрипт рассчитан на долгосрочную обработку данных, поэтому следует учитывать лимиты API Bybit и возможные ограничения по частоте запросов.
Для корректной работы необходимо наличие интернет-соединения.




