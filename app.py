import streamlit as st
import requests

BLD_URL = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
LAND_BASE_URL = "https://apis.data.go.kr/1613000/arLandUseInfoService"

st.set_page_config(page_title="대지분석 데이터 조회기", layout="wide")
st.title("토지이음 & 건축HUB 간편 조회기")

with st.sidebar:
    st.header("인증키 설정")
    api_key = st.text_input("공공데이터포털 일반 인증키", type="password")
    land_op = st.text_input("토지이용규제 상세기능명", value="getArLandUseInfo")

st.subheader("대상지 정보 입력")
c1, c2, c3, c4 = st.columns(4)
sigungu = c1.text_input("시군구코드 (양양: 51830)", "51830")
bjdong = c2.text_input("법정동코드 (조산리: 25024)", "25024")
bun = c3.text_input("본번", "296")
ji = c4.text_input("부번", "0")

bun_str = f"{int(bun):04d}"
ji_str = f"{int(ji):04d}"
pnu = f"{sigungu}{bjdong}1{bun_str}{ji_str}"

tab1, tab2 = st.tabs(["건축물대장 표제부", "토지이용규제정보"])

with tab1:
    if st.button("건축물대장 조회 실행"):
        if not api_key:
            st.warning("왼쪽 사이드바에 인증키를 입력해 주세요.")
        else:
            params = {
                "serviceKey": api_key,
                "sigunguCd": sigungu,
                "bjdongCd": bjdong,
                "platGbCd": "0",
                "bun": bun_str,
                "ji": ji_str,
                "numOfRows": "20",
                "pageNo": "1",
                "_type": "json",
            }
            try:
                res = requests.get(BLD_URL, params=params, timeout=10)
                data = res.json()
                if int(data.get("response", {}).get("body", {}).get("totalCount", 0)) == 0:
                    params.pop("platGbCd", None)
                    data = requests.get(BLD_URL, params=params, timeout=10).json()
                st.success("건축물대장 조회 완료")
                st.json(data)
            except Exception as e:
                st.error(f"오류: {e}")

with tab2:
    if st.button("토지이용규제 조회 실행"):
        if not api_key:
            st.warning("왼쪽 사이드바에 인증키를 입력해 주세요.")
        else:
            url = f"{LAND_BASE_URL}/{land_op.strip()}"
            params = {
                "serviceKey": api_key,
                "pnu": pnu,
                "numOfRows": "50",
                "pageNo": "1",
            }
            try:
                res = requests.get(url, params=params, timeout=10)
                st.success("토지이용규제 조회 완료")
                st.text_area("응답 원본 (XML)", res.text, height=350)
            except Exception as e:
                st.error(f"오류: {e}")
