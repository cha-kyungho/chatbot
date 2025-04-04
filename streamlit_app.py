import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬제주도 여행 정보 쳇봇")
st.write(
    "여기 제주도 여행 정보를 제공하는 간단한 챗봇 서비스입니다."
    "이 앱을 사용하려면 OpenAI API 키가 필요하며, 여기에서 발급받을 수 있습니다."
    "제주도 여행에 대한 유용한 팁과 정보를 원하시면, 언제든지 질문해 주세요!"
)

# 사용자에게 OpenAI API 키 입력 요청  
openai_api_key = st.text_input("OpenAI API Key", type="password")  
if not openai_api_key:  
    st.info("계속하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")  
else:  
    # OpenAI 클라이언트 생성  
    client = OpenAI(api_key=openai_api_key)  

    # 세션 상태 변수 생성 - 채팅 메시지를 저장  
    if "messages" not in st.session_state:  
        st.session_state.messages = []  

    # 시스템 메시지 추가  
    if not st.session_state.messages:  
        system_message = {  
            "role": "system",  
            "content": "당신은 제주도 여행에 대한 정보에 친절하고 유용한 챗봇입니다."  
        }  
        st.session_state.messages.append(system_message)  

    # 기존 채팅 메시지 표시  
    for message in st.session_state.messages:  
        with st.chat_message(message["role"]):  
            st.markdown(message["content"])  

    # 사용자 입력 필드 생성 - 제주도 여행 관련 질문 입력  
    if prompt := st.chat_input("제주도 여행에 대해 무엇을 알고 싶으신가요?"):  

        # 현재 프롬프트 저장 및 표시  
        st.session_state.messages.append({"role": "user", "content": prompt})  
        with st.chat_message("user"):  
            st.markdown(prompt)  

        # OpenAI API를 사용하여 응답 생성  
        stream = client.chat.completions.create(  
            #model="gpt-3.5-turbo",
            model="gpt-4o-mini",
            messages=[  
                {"role": m["role"], "content": m["content"]}  
                for m in st.session_state.messages  
            ],  
            stream=True,  
        )  

        # 응답 스트리밍 및 세션 상태에 저장  
        with st.chat_message("assistant"):  
            response = st.write_stream(stream)  
        st.session_state.messages.append({"role": "assistant", "content": response})  
