import streamlit as st, paramiko, json, os, re
from dotenv import load_dotenv
load_dotenv()

# ▒▒ 기본 컬러 팔레트 ▒▒
PRIMARY  = "#7C3AED"
BG_MAIN  = "#F5F6F8"
CARD_BG  = "#FFFFFF"
TXT_DARK = "#111111"
TXT_SUB  = "#6B7280"

st.set_page_config(page_title="편향 문장 검사기", layout="wide")

# ▒▒ CSS ▒▒
st.markdown(f"""
<style>
/* -------- 배경 & 기본 -------- */
html, body, [class*="st-"] {{ background:{BG_MAIN}; color:{TXT_DARK}; font-size:17px; }}

/* -------- Top Bar -------- */
.topbar {{ display:flex; justify-content:space-between; padding:14px 6px 32px 6px; }}
.topbar-left  {{ font-size:32px; font-weight:800; display:flex; align-items:center; gap:10px; }}
.topbar-right {{ display:flex; gap:26px; font-weight:600; }}
.topbar-right a {{ color:{TXT_DARK}; text-decoration:none; }}

/* -------- 카드 -------- */
.card {{
   background:{CARD_BG}; border-radius:12px;
   padding:30px 34px 26px 34px;
   box-shadow:0 0 0 1px rgba(0,0,0,0.06);
   min-height:110px;
}}
.card h4 {{ margin:0 0 14px 0; font-size:20px; }}

/* -------- 입력창 -------- */
.stTextArea textarea {{
   background:white; color:{TXT_DARK};
   padding:14px; border-radius:8px;
}}

/* -------- 버튼 -------- */
.stButton>button {{
   background:{PRIMARY}; color:#FFFFFF !important;
   height:52px; border:none; border-radius:6px;
   font-size:18px; font-weight:700;
}}
.stButton>button:hover {{ filter:brightness(110%); }}

/* -------- 기타 -------- */
.char-count {{ text-align:right; font-size:14px; color:{TXT_SUB}; }}
.placeholder-tip {{ color:#B0BEC5; }}
</style>
""", unsafe_allow_html=True)

# ▒▒ 헤더 ▒▒
st.markdown("""
<div class='topbar'>
  <div class='topbar-left'>🧠 편향 측정 검사기</div>
  <div class='topbar-right'>
      <a href='#'>사용법</a><a href='#'>문의하기</a>
  </div>
</div>""", unsafe_allow_html=True)

# ▒▒ 서버 호출 함수 ▒▒
def run_remote_bias_analysis(sentence:str):
    host, user = "166.104.246.78", "jin0190"
    pw   = os.getenv("SSH_PASSWORD")
    script = "/home/jin0190/upload/kobbq_testv/run_model.py"
    escaped = sentence.replace('"', r'\"')
    cmd = (
        f'bash -c "source /compuworks/anaconda3/etc/profile.d/conda.sh && '
        f'conda activate bias_39 && python {script} \\"{escaped}\\""'
    )
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    _, stdout, stderr = ssh.exec_command(cmd)
    out, err = stdout.read().decode(), stderr.read().decode()
    ssh.close()
    if err and not out: raise RuntimeError(err)
    return json.loads(out.strip())

# ▒▒ 레이아웃 ▒▒
col_input, col_out = st.columns([1.3, 1])

with col_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h4>원문</h4>", unsafe_allow_html=True)
    text = st.text_area("", height=260, label_visibility="collapsed",
                        placeholder="예: 중장년은 체력이 부족하다.")
    st.markdown(f"<div class='char-count'>{len(text)}자</div>", unsafe_allow_html=True)
    run_btn = st.button("검사하기", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h4>맞춤법/문법 오류</h4>", unsafe_allow_html=True)

    if run_btn and text.strip():
        with st.spinner("편향 분석 중..."):
            try:
                res = run_remote_bias_analysis(text)
                st.success("✅ 분석 완료")
                st.markdown(f"**편향 점수:** `{res['편향 점수']}` &nbsp;&nbsp; **판단:** {res['판단']}")
                st.markdown("**주요 후보 단어**")
                st.markdown(f"- {res['주어']}")
            except Exception as e:
                st.error(f"오류: {e}")
    else:
        st.markdown("<p class='placeholder-tip'>문장을 입력하고 검사하기를 눌러주세요.</p>",
                    unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ▒▒ 푸터 ▒▒
st.markdown("""
<hr style='margin-top:40px; border:none; border-top:1px solid #E5E7EB;'/>
<p style='text-align:center; font-size:13px; color:#94A3B8;'>
© 2025 바른한글 / KoBBQ Bias Research Team – All rights reserved.</p>
""", unsafe_allow_html=True)




# import streamlit as st
# import paramiko
# import json
# import os
# from dotenv import load_dotenv

# # 🔧 환경변수 로드
# load_dotenv()

# st.set_page_config(page_title="편향 문장 검사기", layout="wide")

# # ✅ SSH로 run_model.py 실행 함수
# def run_remote_bias_analysis(input_sentence):
#     hostname = "166.104.246.78"
#     username = "jin0190"
#     password = os.getenv("SSH_PASSWORD")
#     script_path = "/home/jin0190/upload/kobbq_testv/run_model.py"

#     escaped_input = input_sentence.replace('"', '\\"')
#     command = f'bash -c "source /compuworks/anaconda3/etc/profile.d/conda.sh && conda activate bias_39 && python {script_path} \\"{escaped_input}\\""' 

#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname, username=username, password=password)

#     stdin, stdout, stderr = ssh.exec_command(command)
#     output = stdout.read().decode().strip()
#     error = stderr.read().decode().strip()
#     ssh.close()

#     if error and not output:
#         raise RuntimeError(f"[서버 에러]\n{error}")
#     return json.loads(output)

# # 🔕 스트림릿 사이드바 제거
# hide_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>
# """
# st.markdown(hide_style, unsafe_allow_html=True)

# # 🧠 제목
# st.title("🧠 편향 문장 검사기")

# col1, col2 = st.columns([1.3, 1])

# # ✍ 입력창
# with col1:
#     st.subheader("✏️ 검사할 문장 입력")
#     user_input = st.text_area("문장 또는 문단을 입력하세요", height=300, placeholder="예: 중장년은 체력이 부족하다.")
#     submitted = st.button("검사하기")

# # 🔍 결과 출력
# with col2:
#     st.subheader("🔍 분석 결과")
#     if submitted and user_input.strip():
#         with st.spinner("서버에서 모델을 실행 중입니다..."):
#             try:
#                 print("✅ run_remote_analysis 호출됨")  # ← 이 줄 추가
                
#                 result = run_remote_bias_analysis(user_input)
                
#                 print(f"✅ 서버 응답: {result}")  # ← 결과 확인용 로그

#                 if "error" in result:
#                     st.error(result["error"])
#                 else:
#                     st.markdown(f"**편향 점수:** `{result['편향 점수']}`")
#                     st.markdown(f"**판단:** {result['판단']}")
#                     st.markdown("**주요 편향 후보 단어:**")
#                     st.markdown(f"- `{result['주어']}`")

#                     # 근거
#                     st.markdown("**🧾 판단 근거:**")
#                     reasons = result.get("판단 근거", {})
#                     st.markdown(f"- 평균 anchor 기준 점수: `{reasons.get('평균 anchor 기준 점수', '-')}`")
#                     st.markdown(f"- 중립 집단 기준 점수: `{reasons.get('중립 집단 기준 점수', '-')}`")

#             except Exception as e:
#                 st.error(f"⚠️ 서버 연결 또는 분석 실패: {str(e)}")
#     else:
#         st.info("문장을 입력하고 [검사하기]를 눌러주세요.")



# import streamlit as st
# import paramiko
# import json
# import os
# from dotenv import load_dotenv

# load_dotenv()

# st.set_page_config(page_title="편향 문장 검사기", layout="wide")

# # 화면 UI 형식정렬
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# st.title("🧠 편향 문장 검사기")
# col1, col2 = st.columns([1.3, 1])

# # ✅ SSH에서 run_model.py 실행하는 함수
# def run_remote_analysis(input_text):
#     hostname = "166.104.246.78"
#     username = "jin0190"
#     password = os.getenv("SSH_PASSWORD")
#     script_path = "/home/jin0190/upload/kobbq_testv/run_model.py"

#     escaped_input = input_text.replace('"', '\\"')
#     command = f'bash -c "source /compuworks/anaconda3/etc/profile.d/conda.sh && conda activate bias_39 && python {script_path} \"{escaped_input}\""'

#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname, username=username, password=password)

#     stdin, stdout, stderr = ssh.exec_command(command)
#     output = stdout.read().decode().strip()
#     error = stderr.read().decode().strip()
#     ssh.close()

#     if error and not output:
#         raise RuntimeError(f"[\uc11c\ubc84 \uc5d0\ub7ec]\n{error}")
#     return json.loads(output)


# # ✏️ 사용자 입력
# with col1:
#     st.subheader("✏️ 검사할 문장 입력")
#     user_text = st.text_area("문장 또는 문단을 입력하세요", height=300, placeholder="예: 청년은 책임감이 부족하다. 노인은 성실하다.")
#     submitted = st.button("검사하기")

# with col2:
#     st.subheader("🔍 분석 결과")
#     if submitted and user_text.strip():
#         with st.spinner("서버에서 분석 중..."):
#             try:
#                 print("✅ run_remote_analysis 호출됨")  # ← 이 줄 추가

#                 results = run_remote_analysis(user_text)

#                 print(f"✅ 서버 응답: {results}")  # ← 결과 확인용 로그

#                 if isinstance(results, dict) and "error" in results:
#                     st.error(results["error"])
#                 elif isinstance(results, list) and results:
#                     for i, item in enumerate(results):
#                         st.markdown(f"#### ✏️ 문장 {i+1}")
#                         st.code(item["문장"], language="text")

#                         st.markdown(f"- **편향 점수:** `{item['편향 점수']}`")
#                         st.markdown(f"- **판단:** {item['판단']}")
#                         st.markdown(f"- **주요 편향 후보 단어:** `{item['주어']}`")

#                         with st.expander("🧾 판단 근거 더보기"):
#                             for key, value in item.get("판단 근거", {}).items():
#                                 st.markdown(f"- **{key}**: `{value}`")

#                         st.markdown("---")
#                 else:
#                     st.success("편향이 의심되는 문장이 발견되지 않았습니다.")
#             except Exception as e:
#                 st.error(f"⚠️ 서버 연결 또는 분석 실패: {str(e)}")
#     else:
#         st.info("문단을 입력하고 [검사하기]를 눌러주세요.")

