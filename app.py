from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import openai

st.title("Streamlit LLM App")

st.write("""
         各種専門のエージェントが質問に答えます。\n
         専門家を選択し、質問を入力して「実行」ボタンを押してください。\n
         例: 医療エージェント、腰が痛い場合の対処法は？
         """)
selected_item = st.radio(
    "エージェントを選択してください。",
    ["医療エージェント", "法律エージェント"]
)

st.write(f"選択されたエージェント: {selected_item}")
input_text = st.text_area("質問を記入してください。")

def generate_response(selected_item, input_text):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "エラー: OPENAI_API_KEYが設定されていません。"

    openai.api_key = api_key

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"あなたは{selected_item}です。質問に専門家として適切なアドバイスをしてください。また専門外のことは質問に答えず、「申し訳ありませんが、その質問にはお答えできません。」と返答してください。"},
                {"role": "user", "content": input_text}
            ],
            temperature=0.5
        )
        return (response.choices[0].message.content)
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

if st.button("実行"):
    if input_text:
        st.divider()
        st.write(f"エージェント: {selected_item}")
        st.write(f"質問: {input_text}")

        response = generate_response(selected_item, input_text)
        st.write(f"エージェントの回答: {response}")
    else:
        st.write("質問を入力してください。")
