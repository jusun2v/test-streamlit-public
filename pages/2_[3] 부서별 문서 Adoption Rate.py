import streamlit as st
from utils import *
 
st.set_page_config(layout="wide")
st.set_page_config(page_title="문서 Adoption Rate", page_icon="📊", layout="wide")
st.markdown("## 📊부서별 문서 Adoption Rate")
st.divider()

selected_department = render_sidebar()

# ── 메인 ──────────────────────────────────────────
