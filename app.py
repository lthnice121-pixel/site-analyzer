import streamlit as st
import requests

# API 엔드포인트 URL
BLD_URL = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
LAND_BASE_URL = "https://apis.data.go.kr/1613000/arLandUseInfoService"

st.set_page_config(page_title="대지분석 데이터 조회기", layout="wide")
st.title("토지이음 & 건축HUB 간편 조회기")

# 1. 사이드바 - 공공데이터포털 통합 인증키 입력 (코드 비노출)
with st.sidebar:
    st.header("인증키 설정")
    api_key = st.text_input(
        "공공데이터포털 일반 인증키",
        type="password",
        help="data.go.kr에서 발급받은 일반 인증키 1개만 입력하면 됩니다."
    )
    land_op = st.text_input(
        "토지이용규제 상세기능명",
        value="getArLandUseInfo",
        help="오류(코드 12) 발생 시 공공데이터포털 [상세기능정보]의 영문 기능명으로 변경하세요."
    )

# 2. 메인 화면 - 대상지 정보 입력
st.subheader("대상지 정보 입력")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sigungu = st.text_input("시군구코드 (양양: 51830)", "51830")
with col2:
    bjdong = st.text_input("법정동코드 (조산리: 25024)", "25024")
with col3:
    bun = st.text_input("본번", "296")
with col4:
    ji = st.text_input("부번", "0")

bun_str = f"{int(bun):04d}"
ji_str = f"{int(ji):04d}"
pnu = f"{sigungu}{bjdong}1{bun_str}{ji_str}"

tab1, tab2 = st.tabs(["건축물대장 표제부", "토지이용규제정보"])

# 탭 1: 건축물대장 표제부 (건축HUB)
with tab1:
    if st.button("건축물대장 조회 실행"):
        if not api_key:
            st.warning("왼쪽 사이드바에 공공데이터포털 인증키를 입력해 주세요.")
        else:
            with st.spinner("건축HUB 서버 조회 중..."):
                params = {
                    "serviceKey": api_key,
                    "sigunguCd": sigungu,
                    "bjdongCd": bjdong,
                    "platGbCd": "0",
                    "bun": bun_str,
                    "ji": ji_str,
                    "numOfRows": "20",
                    "pageNo": "1",
                    "_type": "json"
