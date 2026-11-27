import streamlit as st
import requests
import json
import xml.etree.ElementTree as ET

# API 엔드포인트 URL
BLD_URL = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
LAND_URL = "https://api.vworld.kr/ned/data/getLandUseAttr"

st.set_page_config(page_title="대지분석 데이터 조회기", layout="wide")
st.title("🏛️ 토지이음 & 건축HUB 간편 조회기")

# 1. 사이드바 - 인증키 분리 입력
with st.sidebar:
    st.header("🔑 서비스별 인증키 설정")
    bld_key = st.text_input(
        "1. 건축HUB(공공데이터포털) 인증키", 
        type="password",
        help="공공데이터포털(data.go.kr)에서 발급받은 일반 인증키(Encoding 또는 Decoding)"
    )
    land_key = st.text_input(
        "2. 토지이음 / VWorld 인증키", 
        type="password",
        help="브이월드(vworld.kr) 오픈API 또는 토지e음 전용 인증키"
    )

# 2. 메인 화면 - 대상지 정보 입력
st.subheader("📍 대상지 정보 입력")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sigungu = st.text_input("시군구코드 (양양: 51830)", "51830")
with col2:
    bjdong = st.text_input("법정동코드 (조산리: 25024)", "25024")
with col3:
    bun = st.text_input("본번", "296")
with col4:
    ji = st.text_input("부번", "0")

# 4자리 규격화 및 PNU 생성
bun_str = f"{int(bun):04d}"
ji_str = f"{int(ji):04d}"
pnu = f"{sigungu}{bjdong}1{bun_str}{ji_str}"

tab1, tab2 = st.tabs(["🏢 건축물대장 표제부 (건축HUB)", "🗺️ 토지이용계획 (토지이음/VWorld)"])

# 탭 1: 건축물대장 표제부 조회
with tab1:
    if st.button("🏢 건축물대장 조회 실행"):
        if not bld_key:
            st.warning("⚠️ 왼쪽 사이드바에 '건축HUB 인증키'를 입력해 주세요.")
        else:
            with st.spinner("건축HUB 서버와 통신 중..."):
                # 기본 요청 파라미터 (일반대지 platGbCd="0")
                params = {
                    "serviceKey": bld_key,
                    "sigunguCd": sigungu,
                    "bjdongCd": bjdong,
                    "platGbCd": "0",
                    "bun": bun_str,
                    "ji": ji_str,
                    "numOfRows": "20",
                    "pageNo": "1",
                    "_type": "json"
                }
                
                try:
                    res = requests.get(BLD_URL, params=params, timeout=10)
                    res_json = res.json()
                    total_cnt = res_json.get("response", {}).get("body", {}).get("totalCount", 0)
                    
                    # platGbCd="0" 지정 시 0건인 경우, 파라미터를 제거하고 재조회
                    if int(total_cnt) == 0:
                        params.pop("platGbCd", None)
                        retry_res = requests.get(BLD_URL, params=params, timeout=10)
                        res_json = retry_res.json()
                    
                    st.success("건축물대장 조회가 완료되었습니다.")
                    st.json(res_json)
                except Exception as e:
                    st.error(f"통신 중 오류가 발생했습니다: {e}")
                    if 'res' in locals():
                        st.text_area("서버 응답 원본", res.text, height=250)

# 탭 2: 토지이용계획 속성 조회
with tab2:
    if st.button("🗺️ 토지이용계획 조회 실행"):
        if not land_key:
            st.warning("⚠️ 왼쪽 사이드바에 '토지이음 / VWorld 인증키'를 입력해 주세요.")
        else:
            with st.spinner("토지이용계획 서버와 통신 중..."):
                params = {
                    "key": land_key,
                    "pnu": pnu,
                    "numOfRows": "50",
                    "pageNo": "1",
                    "format": "json"
                }
                try:
                    res = requests.get(LAND_URL, params=params, timeout=10)
                    st.success("토지이용계획 조회가 완료되었습니다.")
