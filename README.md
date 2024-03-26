# vkmd
Скрипт python3 для скачивания музыки из социальной сети "ВКонтакте".
Скрипт использует ffmpeg для скачивания, поэтому для корректной работы необходимо сначала установить ffmpeg

## Как скачать
```bash
git clone https://github.com/OstrovCity/vkmd.git
```

## Как использовать
Перед первым запуском:
```bash
sudo apt install ffmpeg
sudo apt install python3-pip
cd vkmd
pip3 install -r requirements.txt
chmod a+x ./src/vkmd.py
```
Запуск:
```bash
./src/vkmd.py
```
При первом запуске (или без параметров) скрипт попросит Вас авторизоваться - ввести логин
```bash
Enter login
>
```
пароль
```bash
Enter password
> 
```
и id пользователя/группы музыку которого мы хотим скачать:
```bash
Enter profile ID
> 
```
 Узнать [id по имени](http://regvk.com/id/)

Если все сделано правильно, Вы увидите следующее:
```bash
Authorization successfull
user    <user>
pass    <password>
user_id <user_id>
out_dir <out_dir_name>
Getting list, please wait...
113 audio will be downloaded
0000001 Ketsa - Good Vibe.mp3 - already exists
0000002 Derek Clegg - Rescue Me.mp3 - download completted
...
3587662 Anton Vlasov - Trailer Sport Stylish.mp3 - download completted
...
8839708 AlexGrohl - Electronic Rock (King Around Here).mp3 - download completted
...
```

## При вызове без параметров
    - если нет сохраненных данных для входа, они запрашиваются (и сохраняются для использования в дальнейшем)
    - если есть данные для входа - программа продолжит работу без запроса, используя сохранённые логин/пароль/id

## Параметры командной строки
    -h              Показывает помощь
    -a              [Повторный] запрос авторизации
    -u <user>       Логин пользователя
    -p <password>   Пароль пользователя
    -i <user_id>    id пользователя для загрузки музыки
    -d <out_dir>    Путь для сохранения музыки
