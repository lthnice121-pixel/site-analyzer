import streamlit as st
import requests
import json
import xml.etree.ElementTree as ET

LAND_URL = "https://apis.data.go.kr/1613000/arLandUseInfoService/getLandUseAttr"
BLD_URL = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"

st.set_page_config(page_title="대지분석 데이터 조회기", layout="wide")
st.title("🏛️ 토지이음 & 건축HUB 건축물대장 간편 조회기")

# 1. 공공데이터 인증키 입력 (사이드바)
with st.sidebar:
    st.header("🔑 설정")
    public_data_key = st.text_input(
        "공공데이터 일반 인증키(Encoding/Decoding)", 
        type="password",
        help="공공데이터포털에서 발급받은 인증키를 입력하세요."
    )

# 2. 대상지 정보 입력
st.subheader("📍 대상지 정보 입력")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sigungu = st.text_input("시군구코드 (양양: 51830)", "51830")
with col2:
    bjdong = st.text_input("법정동코드 (조산리: 25024)", "25024")
with col3:
    bun = st.text_input("본번", "0296")
with col4:
    ji = st.text_input("부번", "0000")

if st.button("🚀 공공데이터 자동 조회"):
    if not public_data_key:
        st.warning("⚠️ 왼쪽 사이드바에 공공데이터 인증키를 먼저 입력해 주세요.")
    else:
        with st.spinner("공공데이터 서버와 통신 중..."):
            pnu = f"{sigungu}{bjdong}1{int(bun):04d}{int(ji):04d}"
            
            # 1. 토지이용계획정보 조회
            land_res = requests.get(LAND_URL, params={
                "serviceKey": public_data_key,
                "pnu": pnu,
                "numOfRows": 50,
                "pageNo": 1
            })
            
            # 2. 건축물대장 표제부 조회
            bld_res = requests.get(BLD_URL, params={
                "serviceKey": public_data_key,
                "sigunguCd": sigungu,
                "bjdongCd": bjdong,
                "platGbCd": "0",
                "bun": f"{int(bun):04d}",
                "ji": f"{int(ji):04d}",
                "_type": "json"
            })
            
            st.success("조회가 완료되었습니다!")
            
            tab1, tab2 = st.tabs(["토지이용계획 결과", "건축물대장 표제부 결과"])
            with tab1:
                st.text_area("토지이용계획 Raw Data (XML)", land_res.text, height=300)
            with tab2:
                try:
                    st.json(bld_res.json())
                except:
                    st.text(bld_res.text)
