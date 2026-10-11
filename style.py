"""Общий стиль и рамка сайта CALIFORNIA.

Фирменные цвета, логотип и пароль меняются здесь, в одном месте,
и подхватываются всеми страницами.
"""

BRAND = {
    "name": "CALIF\u014c",
    "icon": "\u25c6",
    "logo": "",
    "accent": "#DC3E19",
    "accent_dark": "#A82C10",
    "accent_soft": "#FCEBE6",
    "accent_alt": "#0FB5D6",
    "ink": "#0F0F0F",
    "muted": "#6E6E6E",
    "line": "#E6E6E6",
}

PASSWORD = "california2026"  # запасной вариант, если пароль не задан в Secrets

CSS = """
<style>
.block-container { padding-top: 2.2rem; max-width: 1500px; }
html, body, [class*="css"] { font-family: "Helvetica Neue", Arial, sans-serif; }
.brand-line { font-size: .74rem; letter-spacing: 3px; text-transform: uppercase; color: #0F0F0F; font-weight: 700; }
div[data-testid="stMarkdownContainer"] h2.page-title {
    font-size: 1.7rem !important; font-weight: 800 !important; letter-spacing: 1px !important;
    text-transform: uppercase; color: #0F0F0F !important; margin: .3rem 0 .2rem 0; }
div[data-testid="stMarkdownContainer"] h3 {
    font-size: 1.02rem !important; font-weight: 700 !important; text-transform: uppercase;
    letter-spacing: .6px; color: #0F0F0F !important; margin-top: 1.4rem; }
div[data-testid="stMarkdownContainer"] h4 { font-size: .95rem !important; font-weight: 700 !important; color: #0F0F0F !important; }
.page-sub { color: #6E6E6E; font-size: .9rem; margin-bottom: 1rem; }
.rule { height: 2px; background: #0F0F0F; margin: .7rem 0 1.3rem 0; }
.card { border: 1px solid #E6E6E6; border-radius: 2px; padding: 16px 18px; background: #fff; }
.card .k { color: #6E6E6E; font-size: .72rem; text-transform: uppercase; letter-spacing: 1.2px; }
.card .v { color: #0F0F0F; font-size: 1.45rem; font-weight: 700; margin-top: 5px; }
.ct { width: 100%; border-collapse: collapse; font-size: .85rem; }
.ct th { background: #0F0F0F; color: #fff; font-weight: 600; padding: 9px 10px; text-align: right;
    white-space: nowrap; font-size: .72rem; text-transform: uppercase; letter-spacing: .6px; }
.ct th.nm { text-align: left; }
.ct td { padding: 7px 10px; text-align: right; border-bottom: 1px solid #EFEFEF; white-space: nowrap; }
.ct td.nm { text-align: left; }
.ct tr:nth-child(even) td { background: #FAFAFA; }
.ct td.neg { color: #DC3E19; }
.ct tr.sum td { background: #FCEBE6; font-weight: 700; }
.ct tr.tot td { background: #0F0F0F; color: #fff; font-weight: 700; }
section[data-testid="stSidebar"] { border-right: 1px solid #E6E6E6; }
</style>
"""


def _password():
    """Пароль из Secrets приложения, иначе запасной из этого файла."""
    try:
        import streamlit as st
        return st.secrets["site_password"]
    except Exception:
        return PASSWORD


def login_gate(st):
    """Пароль на вход. True, если сайт можно показывать."""
    if "auth" not in st.session_state:
        st.session_state.auth = False
    st.markdown(CSS, unsafe_allow_html=True)
    if st.session_state.auth:
        return True
    st.markdown('<div class="brand-line">' + BRAND["name"] + "</div>", unsafe_allow_html=True)
    st.markdown('<h2 class="page-title">Вход</h2>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Сайт закрыт паролем.</div>', unsafe_allow_html=True)
    pwd = st.text_input("Пароль", type="password", label_visibility="collapsed", placeholder="Пароль")
    if st.button("Войти", type="primary"):
        if pwd == _password():
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Неверный пароль")
    return False


def head(st, title, sub=""):
    """Шапка страницы: название компании, заголовок, подпись, линия."""
    st.markdown('<div class="brand-line">' + BRAND["name"] + "</div>", unsafe_allow_html=True)
    st.markdown('<h2 class="page-title">' + title + "</h2>", unsafe_allow_html=True)
    if sub:
        st.markdown('<div class="page-sub">' + sub + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)


def card(st, key, value, hint=""):
    """Плитка с показателем."""
    h = '<div class="card"><div class="k">' + key + '</div><div class="v">' + value + "</div>"
    if hint:
        h += '<div class="page-sub" style="margin:6px 0 0 0">' + hint + "</div>"
    st.markdown(h + "</div>", unsafe_allow_html=True)


def table(st, head_row, rows):
    """Таблица в фирменной рамке. rows: [(класс, [ячейки]), ...]."""
    h = '<div style="overflow-x:auto"><table class="ct"><thead><tr>'
    for i, c in enumerate(head_row):
        h += '<th class="nm">' + str(c) + "</th>" if i == 0 else "<th>" + str(c) + "</th>"
    h += "</tr></thead><tbody>"
    for cls, vals in rows:
        h += '<tr class="' + cls + '">'
        for i, c in enumerate(vals):
            cl = "nm" if i == 0 else ""
            if isinstance(c, str) and c.startswith("-"):
                cl = (cl + " neg").strip()
            h += '<td class="' + cl + '">' + str(c) + "</td>"
        h += "</tr>"
    st.markdown(h + "</tbody></table></div>", unsafe_allow_html=True)
