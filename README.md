# panels_core
* Конфигурации для FASTAPI и Typer должны храниться в директории /configs
* config.json - основной конфигураций, в нем хранятся настройки для подключения к БД, а также настройки для запуска приложения...
* config-local.json - локальный конфигураций, используется для переопределения настроек из основного конфига, например для запуска приложения в режиме разработки
* Любые другие файлы конфигураций хранятся также в папке /configs, например currency.json, в нем хранятся данные для работы с валютами

* Запуск тестов FASTAPI:
```bash
pipenv run pytest -v
```  

* Запуск приложения FASTAPI:
```bash
pipenv run uvicorn panels_project.app:app --reload
```
```bash
pipenv run python ./panels_project/app.py
```

* Запуск Typer:
```bash
pipenv run python ./typer_cli/main.py
```

* Команда создания панели(1 аргумент домен, второй булевое значение является ли поддоменом, третий почта, четвертый пароль, пятый валюта)<br>
Далее надо выполнить все миграции и:

```bash
pipenv run python ./typer_cli/main.py create-panel <domain_name> False test@email.com test_password USD
```
Потом необходимо руками занести название созданной дб в таблицу `Panels.panels.db_name`

* Команда создания админа паненели(1 аргумент ID, второй почта, третий праоль)
```bash
"python or python3"

pipenv run python ./typer_cli/main.py create-panel-admin <id> test@test.com 123123123
```

* Команда загрузки всех доступных языков в бд из configs/languages.json
```
pipenv run python ./typer_cli/main.py populate-langs
```

* SLQ запросы для удаления для ручного тестирования:
```sql
DELETE FROM panel_domains;
ALTER TABLE panel_domains AUTO_INCREMENT = 1;

DELETE FROM panel_admin;
ALTER TABLE panel_admin AUTO_INCREMENT = 1;

DELETE FROM panels;
ALTER TABLE panels AUTO_INCREMENT = 1;
```


# alembic для бд panels


* для создания миграций panels_db выполните команду:
```bash
pipenv run alembic -c alembic_panels_db.ini revision --autogenerate -m "..."
```  

* для создания миграций panel_template_db выполните команду:
```bash
pipenv run alembic -c alembic_panel_template_db.ini revision --autogenerate -m "..."
```  

* для применения миграций panels_db выполните команды:
```bash
pipenv run alembic -c alembic_panels_db.ini upgrade head && pipenv run alembic -c alembic_panels_db.ini stamp head
```

* для применения миграций panel_template_db выполните команды:
```bash
pipenv run alembic -c alembic_panel_template_db.ini upgrade head && pipenv run alembic -c alembic_panel_template_db.ini stamp head
```

* для отката миграций panels_db выполните команду:
```bash
pipenv run alembic -c alembic_panels_db.ini downgrade <Revision ID>
```  

* для отката миграций panel_template_db выполните команду:
```bash
pipenv run alembic -c alembic_panel_template_db.ini downgrade <Revision ID>
```  

* для вывода истории миграций panels_db выполните команду:
```bash
pipenv run alembic -c alembic_panels_db.ini history
```  

* для вывода истории миграций panel_template_db выполните команду:
```bash
pipenv run alembic -c alembic_panel_template_db.ini history
```  
___

# Docker образ panel_core

- Сборка проекта и запуск проекта
```bash
docker-compose up -d --build
```  
После сборки проекта FastAPI будет доступен по адресу http://localhost:8000/ .
MySQL будет доступен http://localhost:3306/ .
Redis будет доступен http://localhost:6379/ .

- Gunicorn Docker
Для запуска приложения на Gunicorn нужно раскомментировать строку 'sh -c "pipenv run gunicorn -c gunicorn_config.py panels_project.app:app"' в docker-compose.yml 
и закоментировать sh -c "pipenv run uvicorn panels_project.app:app --host 0.0.0.0 --port 8000 --reload".
- В файле gunicorn_config.py лежат конфиги для запуска. 
```sh
  app:
    container_name: fastapi
    build:
      context: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - .:/app
    command: >
      sh -c "pipenv run uvicorn panels_project.app:app --host 0.0.0.0 --port 8000 --reload"
#      sh -c "pipenv run gunicorn -c gunicorn_config.py panels_project.app:app"
```


Требуется так же проверить ваш .env и config.json., изменить localhost на db.
```
DATABASE_PANELS_URL=mysql+mysqlconnector://root:root@db:3306/panels
DATABASE_PANEL_TEMPLATE_URL=mysql+mysqlconnector://root:root@db:3306/panel_template
```  
- Для того чтобы выполнить миграции или другие команды перейдите в терминал контейнера:
```bash
docker compose exec [OPTIONS] SERVICE COMMAND [ARGS...]
```  
Пример с app (FastAPI):
```bash
docker compose exec app sh
# Выйти из sh exit
```  
- Запуск проекта
```bash
docker-compose up 
```  
- Вывод журналов сервисов:
```bash
docker-compose logs -f [service name]
```  
- Вывод список образов 
```bash
docker-compose images
```  
- Проверка статусов контейнеров: Чтобы убедиться, что контейнеры успешно запущены, выполните:
```bash
docker-compose ps
```  
- Остановка контейнеров: Выполните команду для остановки контейнеров:
```bash
docker-compose down
```  

Какие могут быть ошибки при выполнение сборки проекта:
1. /mysql_data/#innodb_redo: permission denied. Ошибка, которую вы видите, "permission denied", связана с отсутствием прав доступа для записи в директорию mysql_data, которая используется как том для данных внутри контейнера MySQL. Требуется удалить при новом билде.

Решение для ubuntu: 
```bash
sudo chmod -R 777 mysql_data
 ```  
Решение для mac: 
```bash 
chmod 644 /путь/к/папке_или_файлу
```
2. Конфликт портов MySQL. 

Решение для ubuntu: 
```bash
# остановить сервис локально у себя 
service mysql stop
 ```  
Решение для mac: 
```bash 
# Один из вариантов: перейти в папку MySQL и найти файл mysqld. Щелкните правой кнопкой мыши по этому файлу и выберите «Стоп».
sudo /etc/init.d/mysql stop
```

### DarkMode
Что бы вручную протестировать DarkMode, а так же бранч с авторизацией нужно создать через консольную команду (выше) админа и:
1. SQL Query
```sql
ALTER TABLE panels.panel_domains DROP INDEX ix_panels_panel_domains_domain_type;
```
2. SQL Query panels.PanelAdminHash
```sql
INSERT INTO panels.panel_admin_hash (panel_admin_id, hash, rand_string, ip, remember, super_admin, created_at, updated_at) 
VALUES 
(1, 'hash_value_1', 'random_string_1', '2130706433', 0, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(2, 'hash_value_2', 'random_string_2', '2130706434', 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
(3, 'hash_value_3', 'random_string_3', '2130706435', 1, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
```
3. SQL Query panels.Panels
```sql
INSERT INTO panels.panels (id, domain, created_at, expired_at, currency,
plan_id, db_name, status)
    VALUES
    (1, '<your_domain>', 1628540400, 1660076400, 'USD', 1, 'db_name1', 1),
    (2, 'example2.com', 1628540500, 1660076500, 'USD', 2, 'db_name2', 1),
    (3, 'example3.com', 1628540600, 1660076600, 'USD', 1, 'db_name3', 1);
```
4. SQL Query panels.PanelAdmin
```sql
INSERT INTO panels.panel_admin (panel_id, email, password, password_salt, authorization_at, status, created_at, updated_at, dark_mode, rules, lang_code, lastip)
    VALUES
    (1, 'user@example.com', 'password1', 'salt1', 1629000000, 1, 1629000000, 1629000001, 0, '{"rule": "admin"}', 'en', 123456789),
    (2, 'user2@example.com', 'password2', 'salt2', 1629000001, 1, 1629000001, 1629000002, 1, '{"rule": "admin"}', 'en', 987654321),
    (3, 'user3@example.com', 'password3', 'salt3', 1629000002, 2, 1629000002, 1629000003, 0, '{"rule": "admin"}', 'en', 111222333);
```
5. SQL Query panels.PanelDomains
```sql
INSERT INTO panels.panel_domains (id, panel_id, domain, domain_type) 
VALUES 
(1, 1, '<your_domain>', 1),
(2, 1, 'system1.<your_domain>', 2),
(3, 1, 'additional1.<your_domain>', 3),
(4, 2, 'example2.com', 1),
(5, 2, 'system2.example.com', 2),
(6, 2, 'additional2.example.com', 3), 
(7, 3, 'example3.com', 1),
(8, 3, 'system3.example.com', 2),
(9, 3, 'additional3.example.com', 3);
```
6. SQL Query panels.UserAgentList
```sql
INSERT INTO panels.user_agent_list (user_agent_name) VALUES
('Mozilla/5.0'),
('Googlebot/2.1'),
('Bingbot/2.0');
```
7. Create Database
```sql
create schema panel_first_domain;
```
8. SQL Query panel_template.ActivityLog
```sql
-- Пример 1
INSERT INTO activity_log 
(panel_admin_id, user_agent_id, super_admin, created_at, ip, details_id, url, event_id) 
VALUES 
(1, 1, 0, UNIX_TIMESTAMP(), '192.168.0.1', 1, 'http://shved15.my/event1', 1);

-- Пример 2
INSERT INTO activity_log 
(panel_admin_id, user_agent_id, super_admin, created_at, ip, details_id, url, event_id) 
VALUES 
(2, 2, 1, UNIX_TIMESTAMP(), '192.168.0.2', 2, 'http://example2.com/event2', 2);

-- Пример 3
INSERT INTO activity_log 
(panel_admin_id, user_agent_id, super_admin, created_at, ip, details_id, url, event_id) 
VALUES 
(3, 3, 0, UNIX_TIMESTAMP(), '192.168.0.3', 3, 'http://example3.com/event3', 3);
````
9. SQL Query Create Database
```sql
CREATE SCHEMA db_name1;
```
10. SQL Query Create Database
```sql
USE db_name1;
```
11. SQL Query Create Table
```sql
CREATE TABLE `activity_log` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `panel_admin_id` INT,
  `user_agent_id` INT,
  `super_admin` INT,
  `created_at` INT,
  `ip` VARCHAR(39),
  `details_id` INT,
  `url` VARCHAR(1000),
  `event_id` INT,
  FOREIGN KEY (`panel_admin_id`) REFERENCES `panels`.`panel_admin`(`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (`user_agent_id`) REFERENCES `panels`.`user_agent_list`(`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;
```
12. SQL Query db_name1.ActivityLog
```sql
-- Пример 1
INSERT INTO activity_log 
(panel_admin_id, user_agent_id, super_admin, created_at, ip, details_id, url, event_id) 
VALUES 
(1, 1, 0, UNIX_TIMESTAMP(), '192.168.0.1', 1, 'http://shved15.my/event1', 1);

-- Пример 2
INSERT INTO activity_log 
(panel_admin_id, user_agent_id, super_admin, created_at, ip, details_id, url, event_id) 
VALUES 
(2, 2, 1, UNIX_TIMESTAMP(), '192.168.0.2', 2, 'http://example2.com/event2', 2);

-- Пример 3
INSERT INTO activity_log 
(panel_admin_id, user_agent_id, super_admin, created_at, ip, details_id, url, event_id) 
VALUES 
(3, 3, 0, UNIX_TIMESTAMP(), '192.168.0.3', 3, 'http://example3.com/event3', 3);
```
13. SQL Query Create Table
```sql
CREATE TABLE `activity_log_details` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `request_data` TEXT,
  `activity_log_details_id` INT,
  FOREIGN KEY (`activity_log_details_id`) REFERENCES `activity_log`(`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;
```
14. SQL Query db_name1.ActivityLogDetails
```sql
INSERT INTO `activity_log_details` (`request_data`, `activity_log_details_id`) VALUES
('Some request data 1', 1),
('Some request data 2', 2),
('Some request data 3', 3);
```

15. Запуск
```bash
pipenv run python3 ./panels_project/admin_dashboard/api/v1/account/main.py
```
16. В localhost/docs отправляете post запрос: /admin/api/v1/account/darkmode указывая panel_id, dark_mode(1 or 0)
17. Если все ок вернет status: ok
18. И посмотреть измененилось ли состояние в таблице
```sql
SELECT * FROM panels.panel_admin WHERE panel_id = 1;
```

