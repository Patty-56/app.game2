import streamlit as st
import json

with open('python_quizzes.json', 'r', encoding='utf-8') as f:
    python_quizzes = json.load(f)
with open('story_days.json', 'r', encoding='utf-8') as f:
    story_days = json.load(f)

TOTAL_DAYS = 21

if 'user' not in st.session_state:
    st.session_state.user = None
if 'water' not in st.session_state:
    st.session_state.water = 0
if 'current_day' not in st.session_state:
    st.session_state.current_day = 1
if 'amount' not in st.session_state:
    st.session_state.amount = 0
if 'step' not in st.session_state:
    st.session_state.step = 'input'

st.title("21天飲水＆推理＆Python打卡計畫")

if st.session_state.user is None:
    st.subheader("輸入身高與體重")
    height = st.number_input("身高 (cm)", min_value=90, max_value=250)
    weight = st.number_input("體重 (kg)", min_value=20, max_value=200)
    if st.button("送出"):
        st.session_state.user = {"height": height, "weight": weight}
        st.session_state.water = round(weight * 35)
        st.session_state.step = 'water'
    st.stop()

if st.session_state.current_day > TOTAL_DAYS:
    st.success('🎉 恭喜你完成21天打卡與推理冒險！你的健康與腦力都 Level Up 了！')
    st.stop()

st.info(f"建議今日飲水量：{st.session_state.water} ml")
st.header(f"第 {st.session_state.current_day} 天")

if st.session_state.step == 'water':
    amount = st.number_input("今日已喝 (ml)", min_value=0, max_value=5000, value=st.session_state.amount)
    if st.button("打卡成功"):
        if amount < st.session_state.water:
            st.warning("請喝到建議量再打卡！")
        else:
            st.session_state.amount = amount
            st.session_state.step = 'story'
    st.stop()

if st.session_state.step == 'story':
    story = story_days[st.session_state.current_day - 1]
    st.subheader("故事劇情")
    st.write(story['story'])
    st.write(f"**今日線索：**{story['clue']}")
    if st.button("進入 Python 小題目"):
        st.session_state.step = 'quiz'
    st.stop()

if st.session_state.step == 'quiz':
    quiz = python_quizzes[st.session_state.current_day - 1]
    st.subheader("Python 小題目")
    st.code(quiz['question'])
    user_ans = st.text_area("請輸入你的答案")
    def is_correct(a, b):
        return a.replace(' ', '').replace('\n', '') == b.replace(' ', '').replace('\n', '')
    if st.button("送出"):
        if is_correct(user_ans, quiz['answer']):
            st.session_state.step = 'suspect'
        else:
            st.error("答案不正確，請再試試！")
            st.info(f"提示：{quiz.get('hint','')}")
    st.stop()

if st.session_state.step == 'suspect':
    story = story_days[st.session_state.current_day - 1]
    st.subheader("推理時間！誰最可疑？")
    suspect = st.radio("請選擇嫌疑人：", story['suspects'])
    if st.button("選擇"):
        if suspect == story['correct']:
            st.success(f"答對！{story['reason']}")
            st.session_state.current_day += 1
            st.session_state.amount = 0
            st.session_state.step = 'water'
        else:
            st.error("答錯了，可以再試一次！")
    st.progress(st.session_state.current_day - 1, f"進度：{st.session_state.current_day - 1}/{TOTAL_DAYS} 天")