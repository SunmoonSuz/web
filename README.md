## web
Это приложение на django для управления задачами(ToDoList) с использованием Redis
## URLS:
/register - Регистрация пользователя  
/authorization - Авторизация пользователя  
/tasks/user_id - Главная страница с задачами  
/tasks/user_id/create - Создание задачи  
/tasks/user_id/read/task_id - Чтение задачи  
/tasks/user_id/edit/task_id - Редактирование задачи  
/tasks/user_id/delete/task_id - Удаление задачи

## Configuration
Создайте файл .env в корне проекта  
SECRET_KEY=your_secret_key  
DEBUG=0  
DB_NAME=name_your_db  
DB_USER=username  
DB_PASSWORD=password  
DB_HOST=db  
DB_PORT=5432  
REDIS_URL=redis://redis:6379/0  
В корне проекта создайте виртуальное окружение  
python -m venv name_your_venv
## app_start

git clone https://github.com/SunmoonSuz/web.git  
cd project  
docker-compose up --build
