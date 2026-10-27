# Контрольная работа №2

Галанов А.В., ЭФБО-03-24. Номер в списке 5 соответствует варианту 1:
`api.devops.local`, порт приложения 8001. Рабочая ветка `kr2/variant-1`.

## Развёртывание

Сначала доставить проект с хоста, сохраняя серверный секрет:

```bash
rsync -avz --delete --exclude=.env --exclude=.git --dry-run ./ devops:kr2/
rsync -avz --delete --exclude=.env --exclude=.git ./ devops:kr2/
```

На VM, от имени devops, создать `.env` со случайным паролем минимум
32 шестнадцатеричных символа и правами 600. Для первоначального создания
из консоли student: `sudo python3 /home/devops/kr2/docs/create_server_env.py`.
Существующий секрет скрипт не перезаписывает.

```bash
cd /home/devops/kr2
docker build -t kr2-app:1.0 .
docker compose up -d
docker compose ps
docker compose top
docker compose exec app getent hosts redis
docker compose exec redis redis-cli ping
docker compose port app 8001
docker compose port redis 6379
python3 docs/verify-secrets.py
```

Redis без пароля должен возвращать NOAUTH. Приложение опубликовано только
на 127.0.0.1:8001; Redis не опубликован. Не выводить `docker compose config`
или полный `docker inspect`: они раскрывают серверный пароль.

## HTTPS

Из консоли VM с sudo:

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/kr2.key -out /etc/ssl/certs/kr2.crt -config /home/devops/kr2/docs/openssl.cnf
sudo chmod 600 /etc/ssl/private/kr2.key
sudo chown root:root /etc/ssl/private/kr2.key
sudo install -m 644 /home/devops/kr2/docs/kr2-nginx.conf /etc/nginx/sites-available/kr2
sudo ln -s /etc/nginx/sites-available/kr2 /etc/nginx/sites-enabled/kr2
sudo nginx -t
sudo systemctl reload nginx
```

При уже существующей ссылке повторное создание не требуется.
Сертификат и ключ не перевыпускать при обычной доставке кода.
Конфигурация devops-site и UFW остаются прежними.

На хосте требуется запись `192.168.56.101 api.devops.local` в hosts.
Получить только открытый сертификат командой
`scp devops:/etc/ssl/certs/kr2.crt ~/kr2.crt`, затем проверить:

```bash
curl -I http://api.devops.local/
curl --cacert ~/kr2.crt https://api.devops.local/
curl --cacert ~/kr2.crt https://api.devops.local/whoami
curl -m 3 http://api.devops.local:8001/health
```

Ожидаются 301, персональный счётчик, scheme https и отказ прямого доступа.
`docker compose down` сохраняет данные в kr2_redis_data; флаг `-v` в этой
контрольной не используется. PR оставляется открытым до защиты.
