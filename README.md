site: transmetrica.com

# Сохранятель треков автобусов в Москве
По неофициальным данным пассажиропоток Московского автобуса сократился более чем в 2 раза за последние несколько лет. Интервалы движения трамваев возросли до 15-20 минут, а средняя скорость движения остается на очень низком уровне. Сокращение выпуска автобусов, неудобные пересадки, высокая цена билета (по сравнению с метро), большие интервалы не могли не сказаться негативно на качестве предоставляемых услуг.  Однако до недавних пор у нас не было никаких доказательств этого.

# Что мы сделали?
В нарушение Федерального закона «Об обеспечении доступа к информации о деятельности государственных органов и органов местного самоуправления» №8 ФЗ Московсие власити скрывают статистику по наземному транспорту. Однако всю информацию можно выгрузить самим из треков яндекс карт или любого приложения, покзывающего когда автобус будет на остановке. Сгруперировав информацию по всем остановкам в горде мы можем оценить картину в целом

# Использование парсера
``` python3 main.py --debug --stations [csv_file_with_coords] --proxy_file [file_with_proxy] ```

Если у вас нет бОльшого числа прокси вы можете использовать тор, добавив флаг `--tor`

Доступные аргументы
* --`stops x` - работать только с первыми x остановками из файла
* --`threads x` - создавать х потоков (но не более чем число остановок)
* `--debug` - сохранять или показывать больше отладочной информации
* `--time_limit x` ограничить время работы скрипта х сек.
* `--stations f_name` - файл откуда брать остаовки
* `--proxy_file f_name` - файл откуда брать прокси
* `--proxy` - использовать прокси из кофигурационного файла
* `--tor` - использовать tor. У вас он должен быть уже установлен

Для корректной работы с Postgres (вместо sqlite) нужно указать в параметрах окружения db-login db-host db-pass db-port - данные для доступа к удаленной базе данных. Название базы данных - transmetrika. Во время первого запуска нужо запустить файл db/db.py для создания таблиц.
