# vkmd
VK Music Downloader
Скрипт python3 для скачивания Вашей и не Вашей музыки из вконтакта

## Как использовать:

```bash
pip3 install -r requirements.txt
./src/main.py
```
При запуске без параметров скрипт попросит Вас авторизоваться - ввести логин
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
[Узнать id по имени](http://regvk.com/id/)

Если все было сделано успешно, то Вы увидите примерно следующее:
```bash
Authorization successfull
Getting list, please wait...
113 audio will be downloaded
00001 Ketsa - Good Vibe.mp3 - already exists
00002 Derek Clegg - Rescue Me.mp3 - download completted
...
```

## При вызове без параметров:
    - если нет сохраненных данных для входа, они запрашиваются
    - если есть данные для входа - программа продолжит работу без запроса логина/пароля/id

## Параметры командной строки:
    -h              Показывает помощь
    -a              [Повторный] запрос авторизации
    -u <user>       Логин пользователя
    -p <password>   Пароль пользователя
    -i <user_id>    id пользователя для загрузки музыки
    -d <out_dir>    Путь для сохранения музыки
