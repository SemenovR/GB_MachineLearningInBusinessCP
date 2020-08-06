### Итоговый проект курса "Машинное обучение в бизнесе"

Стек:
1. ML: sklearn, pandas, numpy, lightgbm
2. API: flask

Данные: с kaggle - https://www.kaggle.com/kemical/kickstarter-projects

Задача: предсказать по входным данным вероятность успешного привлечения денежных средств по схеме краудфандинга. Бинарная классификация.

Используемые признаки:
1. name (text)
2. category (text)
3. main_category (text)
4. country (text)
5. launched (date)
6. deadline (date)
7. usd_goal_real (float)

Целевая переменная: state

Преобразования: tfidf

Модель: lightgbm
