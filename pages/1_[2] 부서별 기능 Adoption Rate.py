import streamlit as st
import pandas as pd
from utils import render_sidebar, inject_scorecard_style, render_scorecard, render_bar_chart, inject_table_style, render_company_table, render_drill_panel
 
st.set_page_config(layout="wide")
st.set_page_config(page_title="기능 Adoption Rate", page_icon="📊", layout="wide")
st.markdown("## 📊부서별 기능 Adoption Rate")
st.divider()

selected_department = render_sidebar()

# ── 메인 ──────────────────────────────────────────
if __name__ == "__main__":

    # ── [1] 스코어카드 ──────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    inject_scorecard_style()
    with col1:
        render_scorecard(
            label=f"{selected_department} 부서 ADOPTION RATE",
            value="30%",
            sub_text="15개 기능 평균 Adoption Rate",
            icon="👥",
            icon_style="rounded bg-blue", # "circle bg-green"
        )
    with col2:
        render_scorecard(
            label="최다 도입 킬러 기능",
            value="100%</span>",
            sub_text="기능7 기능 Adoption Rate",
            icon="✅",
            # value_size="24px",
            # sub_color="#38a169",
            icon_style="rounded bg-green", 
        )
    with col3:
        render_scorecard(
            label="전사 집중 케어 대상",
            value="18개사",
            sub_text=f"평균치(30%) 이하의 {selected_department} 워크스페이스",
            icon="⚠️",
            # value_color="#e53e3e",
            icon_style="rounded bg-orange", 
        )
    st.divider()

    # ── [2] 막대그래프 ──────────────────────────────────────────
    # 샘플 데이터
    data = {
        "기능": [
            "기능1", "기능2", "기능3", "기능4", "기능5",
            "기능6", "기능7", "기능8", "기능9",
            "기능10", "기능11", "기능12", "기능13", "기능14", "기능15",
        ],
        "adoption_rate": [100, 7, 20, 13, 7, 17, 36, 13, 17, 17, 90, 17, 3, 10, 87],
    }
    df = pd.DataFrame(data)
 
    avg = df["adoption_rate"].mean()
 
    render_bar_chart(
        df=df,
        x_col="기능",
        y_col="adoption_rate",
        title=f"{selected_department} 부서 기능별 도입 비율 (%)",
        subtitle=f"기능별 쓰고 있는 Workspace 수 / {selected_department} 응답 Workspace 전체 수 (30개)",
        avg_line=30,
        avg_label=f"15개 기능 평균 Adoption Rate",
        threshold=30,
        color_above="#4C8BF5",
        color_below="#F5924C",
        y_range=[0, 105],
        height=480,
    )
    st.divider()

    # ── [3] 고객 리스트 ────────────────────────────────────────── 
    inject_table_style()
 
    # ── 샘플 데이터 ──────────────────────────────────
    companies = pd.DataFrame({
        "회사명":       ["스푼라디오","발란","왓챠","스타일쉐어","트렌비","스패로우","리디","숭고","밀리의서재","우아한형제들","카카오","네이버"],
        "규모":         ["스타트업","스타트업","스타트업","스타트업","스타트업","스타트업","중견기업","스타트업","스타트업","엔터프라이즈","엔터프라이즈","엔터프라이즈"],
        "활성 기능수":  [2, 2, 2, 2, 2, 2, 3, 3, 3, 7, 10, 12],
        "adoption_rate":[13,13,13,13,13,13,20,20,20,47,67,80],
    })
 
    # 기능 샘플 (회사별로 다르게 세팅 가능)
    sample_features = [
        {"name":"기능1",    "desc":"가장 기본적인 서명요청 기능",          "icon":"✏️",  "on":True},
        {"name":"기능2",         "desc":"서명 없이 문서 열람만 요청하는 기능",   "icon":"👁️",  "on":False},
        {"name":"기능3",         "desc":"서명 시 문서를 첨부하여 송신하는 기능", "icon":"📎",  "on":True},
        {"name":"기능4",     "desc":"민감 문서에 암호를 설정해 보호하는 기능","icon":"🔒", "on":False},
        {"name":"기능5",         "desc":"지정된 시간에 계약서를 자동 전송하는 기능","icon":"⏰","on":False},
        {"name":"기능6",     "desc":"수신자에게 파일 첨부를 요청하는 기능",  "icon":"📁",  "on":False},
        {"name":"기능7",         "desc":"다수 수신자에게 한 번에 전송하는 기능", "icon":"📨",  "on":False},
    ]
 
    sample_action = {
        "title": "자사 브랜드 신뢰성 강화 유도",
        "desc":  "기업 아이덴티티 적용은 엔터프라이즈 요금제 주력 업셀 기회입니다.",
        "btn":   "업셀 피칭 요청",
    }
 
    # ── 레이아웃: 테이블(좌) + 패널(우) ──────────────
    st.markdown(f"### 📋 {selected_department} 부서 고객사 분석 목록")
    st.caption("클릭 시 각 기업의 기능 사용 현황 상세 데이터를 우측에서 확인 가능")
    st.divider()
 
    left_col, right_col = st.columns([1.2, 1], gap="large")
 
    with left_col:
        render_company_table(
            df=companies,
            company_col="회사명",
            size_col="규모",
            active_col="활성 기능수",
            rate_col="adoption_rate",
            total_features=15,
            avg_threshold=30,
        )
 
    with right_col:
        selected = st.session_state.get("selected_company")
        if selected:
            row = companies[companies["회사명"] == selected].iloc[0]
            render_drill_panel(
                company_name=selected,
                size=row["규모"],
                adoption_rate=row["adoption_rate"],
                avg_threshold=30,
                features=sample_features,
                action=sample_action,
            )
        else:
            st.markdown(
                """
                <div style="height:300px;display:flex;flex-direction:column;align-items:center;
                            justify-content:center;color:#bbb;border:2px dashed #eee;border-radius:16px;">
                    <div style="font-size:32px;">👈</div>
                    <div style="margin-top:8px;font-size:14px;">좌측 회사명을 클릭하면<br>상세 정보가 표시됩니다</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
 