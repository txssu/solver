# Планировщик замены оборудования

## Задание 2025_А11. Замена оборудования

**Авторы**: Рыбин Евгений Андреевич, Кырчикова Софья Михайловна

Репозиторий содержит простую имитационную модель для планирования массовой замены блоков связи. Программа генерирует случайные объекты, оценивает расстояния и вычисляет необходимое количество бригад и стоимость работ для нескольких сценариев.

## Требования

- Python 3.10+
- `numpy`
- `streamlit` (для панели управления)

Установка зависимостей:

```bash
pip install -r requirements.txt
```

## Использование

Запуск расчёта всех четырёх сценариев и генерация отчёта:

```bash
python run_planning.py
```
После выполнения появится файл `report.md`, содержащий технико-экономический отчёт и выводы.

Запуск интерактивной панели управления:

```bash
streamlit run dashboard.py
```

### Быстрый запуск на Windows

Если хочется запускать пример без ручной установки зависимостей, можно
воспользоваться скриптами `run_dashboard.bat` и
`run_planning_report.bat`. Они создают виртуальное окружение `venv`,
устанавливают зависимости и запускают нужную команду.

* `run_dashboard.bat` запускает интерактивный дашборд Streamlit;
* `run_planning_report.bat` рассчитывает сценарии и создаёт `report.md`.

Через панель можно настраивать практически все параметры модели — от количества объектов и складов до зарплат, стоимости транспорта, скорости передвижения и длительности смены. Для тонкой настройки также можно изменить значения в классе `planner.Config`.

## Эвристические правила

На основе прогонки различных вариантов модель формулирует следующие эвристики планирования:

- увеличение срока выполнения работ сокращает требуемое число бригад и снижает итоговые расходы;
- размещение нескольких складов уменьшает транспортные издержки и суммарную стоимость;
- развитая дорожная сеть типа «паутина» сокращает расстояния и расходы по сравнению со схемой «звезда».
