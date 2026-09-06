import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="김탁곤드레밥 생존기", page_icon="🇨🇳", layout="centered")

# --- 상태 초기화 ---
if 'alive' not in st.session_state:
    st.session_state.alive = True
    st.session_state.ending = False
    st.session_state.stage = 'birth'
    st.session_state.status_message = ""
    st.session_state.status_title = ""
    st.session_state.last_click_time = time.time()
    st.session_state.effect_key = 0
    st.session_state.mom_type = None

def reset_game():
    st.session_state.alive = True
    st.session_state.ending = False
    st.session_state.stage = 'birth'
    st.session_state.status_message = ""
    st.session_state.status_title = ""
    st.session_state.last_click_time = time.time()
    st.session_state.effect_key += 1
    st.session_state.mom_type = None

def die(reason, title):
    st.session_state.alive = False
    st.session_state.ending = False
    st.session_state.status_message = reason
    st.session_state.status_title = title

def win(message, title):
    st.session_state.alive = True
    st.session_state.ending = True
    st.session_state.status_message = message
    st.session_state.status_title = title

# --- 가만히 있는 시간 체크 후 사망했으면 즉시 리런 트리거 ---
def check_idle_death():
    if not st.session_state.alive or st.session_state.ending:
        return False
        
    current_time = time.time()
    elapsed_seconds = int(current_time - st.session_state.last_click_time)
    
    if elapsed_seconds > 0:
        # 초당 1% 누적 확률
        death_probability = 1.0 - (0.99 ** elapsed_seconds)
        if random.random() < death_probability:
            reasons = [
                ("아무것도 안하고 가만히 숨만 쉬다가 뒤1졌습니다!", "무소유의 최후"),
                ("생각을 너무 오래 하다가 뇌가 굳어서 사망했습니다!", "생각 정지"),
                ("멍 때리다가 공안에게 간첩으로 오인받아 끌려갔습니다!", "멍 때리기 죄")
            ]
            reason, title = random.choice(reasons)
            die(reason, title)
            return True
    return False

def do_action(next_stage=None, fatal=False, fatal_reason="", fatal_title="", is_ending=False, win_msg="", win_title=""):
    st.session_state.effect_key += 1
    st.session_state.last_click_time = time.time()  
        
    other_sudden_deaths = [
        ("사망 메시지가 맞춤법을 틀려서 주것씁이다!!", "세종대왕 극대노"),
        ("방금 나타난 사망 메시지가 오타가 나서 죽었습니다!", "버그 갓겜"),
        ("놀라서 뒤1졌습니다!", "진성 개복치"),
    ]
    
    random_death_rate = 0.08 if st.session_state.mom_type == 'exploded' else 0.05
    if not fatal and not is_ending and random.random() < random_death_rate:
        r, t = random.choice(other_sudden_deaths)
        die(r, t)
        return

    if fatal:
        die(fatal_reason, fatal_title)
    elif is_ending:
        win(win_msg, win_title)
    elif next_stage:
        st.session_state.stage = next_stage


# --- 배경 이미지 매핑 ---
def get_background_url():
    if not st.session_state.alive:
        return "https://images.unsplash.com/photo-1505635552518-34483a15c138?auto=format&fit=crop&w=1920&q=80"
    if st.session_state.ending:
        return "https://images.unsplash.com/photo-1533327325824-76bc4e62d560?auto=format&fit=crop&w=1920&q=80"

    bg_map = {
        'birth': "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=1920&q=80",
        'mom_select': "https://images.unsplash.com/photo-1516627145497-ae6968895b74?auto=format&fit=crop&w=1920&q=80",
        'main': "https://images.unsplash.com/photo-1514395462725-fb4566210144?auto=format&fit=crop&w=1920&q=80",
        'eat_start': "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1920&q=80",
        'eat_walk': "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1920&q=80", 
        'eat_door': "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=1920&q=80",
        'eat_order': "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=1920&q=80",
        'eat_walk_normal': "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1920&q=80",
        'out_start': "https://images.unsplash.com/photo-1517540216132-23467643ef81?auto=format&fit=crop&w=1920&q=80",
        'out_street': "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=1920&q=80",
        'out_bike': "https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=1920&q=80",
        'chinese_start': "https://images.unsplash.com/photo-1508804052814-cd3ba865a116?auto=format&fit=crop&w=1920&q=80",
        'chinese_shout': "https://images.unsplash.com/photo-1508804052814-cd3ba865a116?auto=format&fit=crop&w=1920&q=80",
        'chinese_broadcast': "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=1920&q=80",
        'idle_start': "
