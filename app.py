"""CALIFORNIA · управленческий сайт компании. Главная страница."""
import streamlit as st

from style import BRAND, card, head, login_gate

st.set_page_config(page_title=BRAND["name"] + " · отчётность",
                   page_icon=BRAND["icon"], layout="wide")

if not login_gate(st):
    st.stop()

head(st, "Главная", "Магазины, онлайн и мерч-направление. Управленческая отчётность.")

c1, c2, c3 = st.columns(3)
with c1:
    card(st, "Выручка", "—", "подключим данные, и здесь будут цифры")
with c2:
    card(st, "Товар на складе", "—", "подключим данные, и здесь будут цифры")
with c3:
    card(st, "Деньги на счетах", "—", "подключим данные, и здесь будут цифры")

st.markdown("### Разделы в работе")
st.markdown("- Продажи: магазины, онлайн, по месяцам\n"
            "- Товар и склад: остатки, оборот, зависшие позиции\n"
            "- Бренды и маржа по товару\n"
            "- Заказы California CUSTOM: тираж, себестоимость, маржа\n"
            "- Деньги: счета, кассы, фонды\n"
            "- Отчёт месяца одной страницей")

st.markdown("### Как страница встаёт в эту рамку")
st.markdown("Файл страницы лежит в папке pages, имя начинается с номера порядка:")
st.code("pages/1_Продажи.py")
st.markdown("Внутри страница подключает общий стиль, пароль и чтение таблицы:")
st.code("import streamlit as st\n"
        "from style import head, card, table, login_gate\n"
        "from data import values, num, fmt, pct\n\n"
        "if not login_gate(st):\n"
        "    st.stop()\n\n"
        'head(st, "Продажи", "на 01.01.2026")')
