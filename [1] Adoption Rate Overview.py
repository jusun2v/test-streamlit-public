import streamlit as st
 
st.set_page_config(page_title="Adoption rate", page_icon="📊", layout="wide")
st.markdown("## 📊Adoption rate")

#######################################
 
st.markdown(
    """
<br>
첫번째 줄<br>
두번째 줄<br>
<br>
    """
, unsafe_allow_html=True)

st.info('목적', icon="📍", width="stretch")
st.markdown(
    """
    - AE/AM의 신규·기존 고객 세일즈 성과 증진을 위한 Adoption Rate 대시보드 구축
    - 고객의 기능 및 문서 활용 현황을 기반으로 세일즈·확장 포인트 발굴 지원
    """
)
st.info('세그먼트 분류 기준', icon="📍", width="stretch")
st.markdown(
    """
    - 가장 최소 단위의 세그먼트는 ‘부서’ 기준으로 설정
    - 산업은 부서의 상위 그룹(카테고리) 개념으로 활용 예정
    - 요금제 및 기업 규모는 필터 형태로 제공하여 다양한 관점의 분석 지원
    """
)
st.info('고려사항', icon="📍", width="stretch")
st.markdown(
    """
    - 기능별 Adoption Rate뿐만 아니라 문서별 Adoption Rate도 함께 측정 예정
    - 특정 문서 사용 여부가 기능 사용 여부와 직접적으로 연결되는 경우가 많다고 판단
    - 이에 따라 기능·문서 관점을 함께 분석할 수 있도록 구성
    """
)
