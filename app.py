import streamlit as st
import requests
import json

# API 엔드포인트 URL
BLD_URL = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
LAND_URL = "https://api.vworld.kr/ned/data/getLandUseAttr"

st.set_page_config(page_title="대지분석 데이터 조회기", layout="wide")
st.title("토지이음 & 건축HUB 간편 조회기")

# 1. 사이드바 - 인증키 분리 입력
with st.sidebar:
    st.header("서비스별 인증키 설정")
    bld_key = st.text_input(
        "1. 건축HUB(공공데이터포털) 인증키", 
        type="password",
        help="data.go.kr에서 발급받은 일반 인증키"
    )
    land_key = st.text_input(
        "2. 토지이음 / VWorld 인증키", 
        type="password",
        help="vworld.kr 오픈API 또는 토지e음 전용 인증키"
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

# 규격화
bun_str = f"{int(bun):04d}"
ji_str = f"{int(ji):04d}"
pnu =
