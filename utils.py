import streamlit as st
import pandas as pd
import plotly.graph_objects as go

default_department = "인사"
department_list = ["개발","경영지원","고객만족","구매","기획","디자인","마케팅","법무","생산","연구","영업","운영","인사","총무","홍보","회계","총괄","소속없음","기타"]

###########################################
# 사이드바 부서 필터
###########################################
def render_sidebar():
    
    # 1. 세션 상태(session_state) 초기화
    if "selected_department" not in st.session_state:
        st.session_state.selected_department = default_department

    # 2. 사이드바 UI 요소 배치 및 값 동기화
    st.session_state.selected_department = st.sidebar.selectbox(
        "부서를 선택해주세요", 
        department_list, 
        index=department_list.index(st.session_state.selected_department)
    )
    return st.session_state.selected_department 

###########################################
# 스코어카드
###########################################
def inject_scorecard_style():
    """카드 공통 스타일 — 페이지당 한 번만 호출"""
    st.markdown(
        """
        <style>
        .scorecard {
            background: white;
            border-radius: 16px;
            padding: 20px 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
            gap: 6px;
            min-height: 110px;
        }
        .card-label {
            font-size: 12px;
            color: #888;
            font-weight: 500;
            letter-spacing: 0.02em;
        }
        .card-value-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .card-value {
            font-weight: 800;
            line-height: 1.2;
        }
        .card-sub {
            font-size: 12px;
            color: #888;
            margin-top: 2px;
        }
        .icon-badge {
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            flex-shrink: 0;
        }
        .icon-badge.rounded  { border-radius: 12px; }
        .icon-badge.circle   { border-radius: 50%; border: 2px solid; font-size: 18px; }
        .icon-badge.bg-blue  { background: #ebf4ff; }
        .icon-badge.bg-green { background: #f0fff4; border-color: #68d391; }
        .icon-badge.bg-orange{ background: #fffaf0; border-color: #f6ad55; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_scorecard(
    label: str,
    value: str,
    sub_text: str,
    icon: str,
    value_color: str = "#1a1a1a",   # 값 글자색  (예: "#e53e3e")
    value_size: str = "36px",        # 값 글자 크기
    sub_color: str = "#888",         # 서브텍스트 색
    icon_style: str = "rounded bg-blue",  # 아이콘 배지 클래스
):
    """
    scorecard 카드 하나를 렌더링합니다.

    Parameters
    ----------
    label       : 상단 라벨 (예: "전체 HR ADOPTION RATE")
    value       : 메인 수치 (예: "30%", "서명요청_기본<br>(100%)")
    sub_text    : 하단 보조 문구
    icon        : 이모지 또는 HTML 아이콘
    value_color : 메인 수치 색상 (기본 검정)
    value_size  : 메인 수치 폰트 크기 (기본 36px)
    sub_color   : 보조 문구 색상 (기본 회색)
    icon_style  : 배지 CSS 클래스 조합
                  shape  → "rounded" | "circle"
                  color  → "bg-blue" | "bg-green" | "bg-orange"
    """
    html = f"""
    <div class="scorecard">
        <div class="card-label">{label}</div>
        <div class="card-value-row">
            <div class="card-value" style="font-size:{value_size}; color:{value_color};">
                {value}
            </div>
            <div class="icon-badge {icon_style}">{icon}</div>
        </div>
        <div class="card-sub" style="color:{sub_color};">{sub_text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

##########################################
# 막대그래프
##########################################
def render_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "차트",
    subtitle: str = "",
    avg_line: float | None = None,
    avg_label: str = "평균선",
    threshold: float | None = None,
    color_above: str = "#4C8BF5",   # 임계값 이상 막대 색
    color_below: str = "#F5924C",   # 임계값 미만 막대 색
    y_range: list | None = None,
    height: int = 480,
):
    """
    HR 기능별 도입 비율 스타일의 막대 차트를 렌더링합니다.
 
    Parameters
    ----------
    df           : 데이터가 담긴 DataFrame
    x_col        : X축으로 사용할 컬럼명
    y_col        : Y축으로 사용할 컬럼명 (수치)
    title        : 차트 제목
    subtitle     : 제목 아래 부제목 (빈 문자열이면 숨김)
    avg_line     : 평균선 Y값 (None이면 미표시)
    avg_label    : 범례에 표시할 평균선 레이블
    threshold    : 막대 색 구분 기준값 (None이면 color_above 단색)
    color_above  : threshold 이상 막대 색
    color_below  : threshold 미만 막대 색
    y_range      : Y축 범위 [min, max] (None이면 자동)
    height       : 차트 높이 (px)
    """
 
    # 막대 색상 결정
    if threshold is not None:
        colors = [
            color_above if v >= threshold else color_below
            for v in df[y_col]
        ]
    else:
        colors = [color_above] * len(df)
 
    fig = go.Figure()
 
    # ── 막대 ──────────────────────────────────────
    fig.add_trace(
        go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker_color=colors,
            name="기능 Adoption Rate (%)",
            hovertemplate="%{x}<br>%{y}%<extra></extra>",
        )
    )
 
    # ── 평균선 ────────────────────────────────────
    if avg_line is not None:
        fig.add_hline(
            y=avg_line,
            line=dict(color="red", width=2, dash="dot"),
            annotation_text=avg_label,
            annotation_position="top right",
            annotation_font_color="red",
        )
        # 범례용 더미 트레이스
        fig.add_trace(
            go.Scatter(
                x=[None], y=[None],
                mode="lines",
                line=dict(color="red", width=2, dash="dot"),
                name=avg_label,
            )
        )
 
    # ── 레이아웃 ──────────────────────────────────
    fig.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=20, b=60, l=40, r=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
            font=dict(size=12),
        ),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=11),
            showgrid=False,
            linecolor="#ddd",
        ),
        yaxis=dict(
            range=y_range,
            showgrid=True,
            gridcolor="#eeeeee",
            ticksuffix="",
            linecolor="#ddd",
            dtick=10,
        ),
        bargap=0.4,
        showlegend=True,
    )
 
    # ── 제목 + 부제목 ─────────────────────────────
    if subtitle:
        st.markdown(
            f"**{title}**  \n"
            f"<span style='font-size:12px; color:#888;'>{subtitle}</span>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"**{title}**")
 
    st.plotly_chart(fig, use_container_width=True)

##########################################
# 고객리스트
##########################################
# ── 공통 스타일 주입 ───────────────────────────────────────────────────────────
def inject_table_style():
    st.markdown(
        """
        <style>
        /* 테이블 행 호버 */
        .company-row {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1.2fr 0.8fr;
            align-items: center;
            padding: 10px 14px;
            border-bottom: 1px solid #f0f0f0;
            cursor: pointer;
            border-radius: 8px;
            transition: background 0.15s;
            font-size: 14px;
        }
        .company-row:hover { background: #f8f9ff; }
        .company-row.selected { background: #eef2ff; }

        .table-header {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1.2fr 0.8fr;
            padding: 8px 14px;
            font-size: 12px;
            color: #888;
            font-weight: 600;
            border-bottom: 2px solid #eee;
            margin-bottom: 4px;
        }

        /* 도트 색상 */
        .dot { width:8px; height:8px; border-radius:50%; display:inline-block; margin-right:8px; }
        .dot.red    { background:#e53e3e; }
        .dot.orange { background:#f5924c; }
        .dot.blue   { background:#4c8bf5; }

        /* Adoption Rate 색 */
        .rate-low    { color: #f5924c; font-weight: 700; }
        .rate-mid    { color: #4c8bf5; font-weight: 700; }
        .rate-high   { color: #38a169; font-weight: 700; }

        /* 평균 배지 */
        .badge-above { background:#e6f4ea; color:#38a169; padding:2px 8px; border-radius:20px; font-size:11px; font-weight:600; }
        .badge-below { background:#fff3e0; color:#f5924c; padding:2px 8px; border-radius:20px; font-size:11px; font-weight:600; }

        /* 드릴다운 패널 */
        .drill-panel {
            background: #1a2236;
            border-radius: 16px;
            padding: 0;
            overflow: hidden;
            color: white;
            height: 100%;
        }
        .drill-header {
            background: #1a2236;
            padding: 20px 22px 16px;
            border-bottom: 1px solid #2e3a52;
        }
        .drill-label {
            font-size: 10px;
            letter-spacing: 0.12em;
            color: #7a8fb0;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .drill-company {
            font-size: 22px;
            font-weight: 800;
            color: #fff;
        }
        .drill-sub {
            font-size: 12px;
            color: #7a8fb0;
            margin-top: 4px;
        }

        /* 기능 아이템 */
        .feature-item {
            display: flex;
            align-items: center;
            padding: 12px 22px;
            border-bottom: 1px solid #f5f5f5;
            gap: 12px;
        }
        .feature-icon { font-size: 18px; width: 28px; text-align: center; }
        .feature-info { flex: 1; }
        .feature-name { font-size: 14px; font-weight: 600; color: #1a1a1a; }
        .feature-desc { font-size: 11px; color: #aaa; margin-top: 1px; }
        .on-badge  { color: #38a169; font-size: 12px; font-weight: 700; white-space: nowrap; }
        .off-badge { color: #bbb;    font-size: 12px; font-weight: 700; white-space: nowrap; }

        /* 액션 카드 */
        .action-card {
            background: #fff;
            border-radius: 12px;
            padding: 14px 16px;
            margin: 12px 0 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }
        .action-title { font-size: 13px; font-weight: 700; color: #1a1a1a; }
        .action-desc  { font-size: 11px; color: #888; margin-top: 2px; }
        .action-btn {
            background: #4c8bf5;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── 회사 목록 테이블 ───────────────────────────────────────────────────────────
def render_company_table(
    df: pd.DataFrame,
    company_col: str = "회사명",
    size_col: str = "규모",
    active_col: str = "활성 기능수",
    rate_col: str = "adoption_rate",
    total_features: int = 15,
    avg_threshold: float = 30.0,
    search_key: str = "search",
    size_filter_key: str = "size_filter",
    selected_key: str = "selected_company",
):
    """
    HR 고객사 분석 목록 테이블을 렌더링합니다.

    Parameters
    ----------
    df               : 고객사 데이터프레임
    company_col      : 회사명 컬럼
    size_col         : 규모 컬럼 (스타트업 / 중견기업 / 엔터프라이즈)
    active_col       : 활성 기능수 컬럼 (숫자)
    rate_col         : Adoption Rate 컬럼 (0~100 숫자)
    total_features   : 전체 기능 수 (기본 15)
    avg_threshold    : 평균 기준선 (기본 30%)
    search_key       : st.session_state 검색어 키
    size_filter_key  : st.session_state 규모 필터 키
    selected_key     : st.session_state 선택 회사 키
    """
    # session_state 초기화
    if selected_key not in st.session_state:
        st.session_state[selected_key] = None

    # ── 필터 영역 ──────────────────────────────────
    filter_col1, filter_col2, filter_col3 = st.columns([3, 2, 2])
    with filter_col1:
        search = st.text_input("", placeholder="🔍 고객사 이름 검색...", key=search_key, label_visibility="collapsed")
    with filter_col2:
        size_options = ["전체 규모"] + sorted(df[size_col].dropna().unique().tolist())
        size_filter = st.selectbox("", size_options, key=size_filter_key, label_visibility="collapsed")
    with filter_col3:
        below_only = st.toggle("평균 이하만 보기", value=False)

    # ── 필터 적용 ──────────────────────────────────
    filtered = df.copy()
    if search:
        filtered = filtered[filtered[company_col].str.contains(search, na=False)]
    if size_filter != "전체 규모":
        filtered = filtered[filtered[size_col] == size_filter]
    if below_only:
        filtered = filtered[filtered[rate_col] < avg_threshold]

    # ── 테이블 헤더 ────────────────────────────────
    st.markdown(
        """
        <div class="table-header">
            <span>회사명</span>
            <span>규모</span>
            <span>활성 기능수</span>
            <span>ADOPTION RATE</span>
            <span>평균</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 행 렌더링 ──────────────────────────────────
    for _, row in filtered.iterrows():
        company = row[company_col]
        rate    = row[rate_col]
        active  = row[active_col]

        # 색 결정
        if rate >= avg_threshold:
            dot_cls  = "blue"
            rate_cls = "rate-high"
            badge    = '<span class="badge-above">평균 이상</span>'
        elif rate >= avg_threshold * 0.6:
            dot_cls  = "orange"
            rate_cls = "rate-mid"
            badge    = '<span class="badge-below">평균 이하</span>'
        else:
            dot_cls  = "red"
            rate_cls = "rate-low"
            badge    = '<span class="badge-below">평균 이하</span>'

        selected_cls = "selected" if st.session_state[selected_key] == company else ""

        st.markdown(
            f"""
            <div class="company-row {selected_cls}">
                <span><span class="dot {dot_cls}"></span>{company}</span>
                <span>{row[size_col]}</span>
                <span>{active} / {total_features}개</span>
                <span class="{rate_cls}">{rate}%</span>
                <span>{badge}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # 클릭 버튼 (투명하게 행 위에 겹치는 느낌)
        if st.button(company, key=f"btn_{company}", use_container_width=True):
            st.session_state[selected_key] = company
            st.rerun()

    return filtered


# ── 드릴다운 패널 ──────────────────────────────────────────────────────────────
def render_drill_panel(
    company_name: str,
    size: str,
    adoption_rate: float,
    avg_threshold: float,
    features: list[dict],
    action: dict | None = None,
):
    """
    우측 드릴다운 패널을 렌더링합니다.

    Parameters
    ----------
    company_name   : 회사명
    size           : 기업 규모
    adoption_rate  : Adoption Rate (0~100)
    avg_threshold  : 평균 기준값
    features       : 기능 목록 [{"name": str, "desc": str, "icon": str, "on": bool}]
    action         : 액션 카드 {"title": str, "desc": str, "btn": str} or None
    """
    avg_badge = (
        '<span style="background:#4caf50;color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;">평균 이상</span>'
        if adoption_rate >= avg_threshold
        else '<span style="background:#f5924c;color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;">평균 이하</span>'
    )

    # 헤더
    st.markdown(
        f"""
        <div style="background:#1a2236;border-radius:16px 16px 0 0;padding:20px 22px 16px;color:white;">
            <div style="font-size:10px;letter-spacing:.12em;color:#7a8fb0;font-weight:600;margin-bottom:8px;">DRILL-DOWN PANEL</div>
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="font-size:22px;font-weight:800;">{company_name}</div>
                {avg_badge}
            </div>
            <div style="font-size:12px;color:#7a8fb0;margin-top:4px;">
                기업 규모: {size} | 활성화율 {adoption_rate}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 기능 목록
    st.markdown(
        '<div style="background:white;border-radius:0 0 16px 16px;padding:16px 0 8px;">'
        '<div style="font-size:13px;font-weight:600;color:#333;padding:0 22px 10px;">15가지 핵심 기능 적용 상태</div>',
        unsafe_allow_html=True,
    )

    for feat in features:
        on_html = (
            '<span class="on-badge">✅ ON</span>'
            if feat["on"]
            else '<span class="off-badge">❌ OFF</span>'
        )
        st.markdown(
            f"""
            <div class="feature-item">
                <div class="feature-icon">{feat['icon']}</div>
                <div class="feature-info">
                    <div class="feature-name">{feat['name']}</div>
                    <div class="feature-desc">{feat['desc']}</div>
                </div>
                {on_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 액션 카드
    if action:
        st.markdown(
            f"""
            <div style="padding:12px 22px 16px;">
                <div style="font-size:12px;color:#f5924c;font-weight:600;margin-bottom:8px;">⚠️ 이 기업을 위한 세일즈/CS 타겟 액션 권장안</div>
                <div class="action-card">
                    <div>
                        <div class="action-title">{action['title']}</div>
                        <div class="action-desc">{action['desc']}</div>
                    </div>
                    <button class="action-btn">{action['btn']}</button>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
