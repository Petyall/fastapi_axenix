# FastAPI - Axenix

Описание: Этот проект был разработан в рамках выполнения кейса от компании Axenix, командой CyberJackals. Данная часть решения предоставляет возможность анализа информации о работе погрузчиков на складе.

## Основные функции

Проект предоставляет следующие функции:

- Вывод пройденного расстояния за период (в разбивке по дням).
- Вывод количества выполненных заказов за период (в разбивке по дням).
- Время проведенное в движении за период (в разбивке по дням).
- Время простоя за период (в разбивке по дням).
- Время нахождения в каждом из статусов за период.
- В разрезе каждой контрольной точки:
  - Количество зафиксированных "проходов" погрузчиков.
  - Количество проходов мимо точки конкретного погрузчика.
- Предусмотрена возможность реализации математической модели на основе имеющейся статистики по скорости перемещения каждого погрузчика и времени разгрузки/загрузки.

## Установка

Для установки и запуска проекта, выполните следующие шаги:

1. Клонируйте репозиторий на свой локальный компьютер:

   ```bash
   git clone https://github.com/Petyall/fastapi_axenix.git
   ```

2. Перейдите в каталог проекта:

   ```bash
   cd fastapi_axenix
   ```

3. Инициализируйте виртуальное окружение:

   ```bash
   py -m venv venv
   ```

4. Активируйте виртуальное окружение:

   ```bash
   venv\scripts\activate
   ```

5. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

6. Запустите проект:

   ```bash
   uvicorn main:app --reload
   ```

## Использование

После запуска проекта, вы можете получить доступ к API для анализа данных погрузчиков.

## Контакты

Если у вас есть вопросы или предложения, свяжитесь со [мной](https://t.me/petyal).