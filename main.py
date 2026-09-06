import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="김탁곤드레밥 생존기", page_icon="🇨🇳", layout="centered")

# --- 상태 초기화 ---
if 'alive' not in st.session_state:
    st.session_state.alive = True
    st.session_state.ending = False
    st.session_state.stage = 'birth'
    st.session_state.status_message = ""
    st.session_state.status_title = ""
    st.session_state.mom_type = None

def reset_game():
    st.session_state.alive = True
    st.session_state.ending = False
    st.session_state.stage = 'birth'
    st.session_state.status_message = ""
    st.session_state.status_title = ""
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

def process_action(next_stage=None, fatal=False, fatal_reason="", fatal_title="", is_ending=False, win_msg="", win_title=""):
    other_sudden_deaths = [
        ("사망 메시지가 맞춤법을 틀려서 주것씁이다!!", "세종대왕 극대노"),
        ("방금 나타난 사망 메시지가 오타가 나서 죽었습니다!", "버그 갓겜"),
        ("놀라서 뒤1졌습니다!", "진성 개복치"),
    ]
    
    random_death_rate = 0.08 if st.session_state.mom_type == 'exploded' else 0.05
    if not fatal and not is_ending and random.random() < random_death_rate:
        r, t = random.choice(other_sudden_deaths)
        die(r, t)
        st.rerun()
        return

    if fatal:
        die(fatal_reason, fatal_title)
    elif is_ending:
        win(win_msg, win_title)
    elif next_stage:
        st.session_state.stage = next_stage
    st.rerun()

# 배경 이미지 매핑
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
        'idle_start': "https://images.unsplash.com/photo-1555636222-cae831e670b3?auto=format&fit=crop&w=1920&q=80",
        'idle_taobao': "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=1920&q=80",
        'job_start': "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1920&q=80",
        'job_tanghulu': "https://images.unsplash.com/photo-1559828456-125ddcb6f4b6?auto=format&fit=crop&w=1920&q=80",
        'job_panda': "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1920&q=80",
        'game_start': "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1920&q=80",
        'game_lol': "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1920&q=80",
        'game_genshin': "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?auto=format&fit=crop&w=1920&q=80"
    }
    return bg_map.get(st.session_state.stage, bg_map['main'])

bg_url = get_background_url()

st.markdown(f"""
<style>
    .stApp {{
        background-image: linear-gradient(rgba(12, 12, 15, 0.85), rgba(12, 12, 15, 0.85)), url('{bg_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff !important;
    }}
    h1, h2, h3, h4, p, span, div {{
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }}
    .stButton > button {{
        background-color: rgba(26, 26, 26, 0.8) !important;
        color: #ff4747 !important;
        border: 2px solid #ff3300 !important;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: 0.2s;
    }}
    .stButton > button:hover {{
        background-color: rgba(255, 51, 0, 0.9) !important;
        color: #ffffff !important;
        border-color: #ffff00 !important;
        box-shadow: 0 0 15px #ff3300, 0 0 30px #ffff00;
    }}
    .game-container {{
        padding: 20px;
        border-radius: 15px;
        background-color: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(5px);
    }}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    st.title("김탁곤드레밥 생존기")
    st.markdown("---")

    if not st.session_state.alive:
        st.error(f"## [{st.session_state.status_title}]")
        st.header(f"사인: {st.session_state.status_message}")
        st.markdown("---")
        if st.button("다시 환생하기", key="btn_restart_dead"):
            reset_game()
            st.rerun()

    elif st.session_state.ending:
        st.balloons()
        st.success(f"## 🎉 [{st.session_state.status_title}]")
        st.header(st.session_state.status_message)
        st.markdown("---")
        if st.button("처음부터 다시하기", key="btn_restart_win"):
            reset_game()
            st.rerun()

    else:
        if st.session_state.stage == 'birth':
            st.subheader("응애! 생명의 탄생")
            st.write("김탁곤드레밥이 세상에 나오려 합니다. 어떻게 하시겠습니까?")
            
            if st.button("힘차게 태어나기", key="btn_birth_1"):
                if random.random() < 0.05:  
                    death_type = random.randint(1, 3)
                    if death_type == 1:
                        die("태어나서 죽었습니다!", "초광속 스피드런")
                    elif death_type == 2:
                        die("입양당해서 죽었습니다!", "가혹한 운명")
                    else:
                        die("태어났는데 공산당이 잡아갔습니다!", "체포조 출동")
                else:
                    st.session_state.mom_type = 'normal'
                    st.session_state.stage = 'main'
                st.rerun()
                        
            if st.button("엄마가 마음에 들지 않는다", key="btn_birth_2"):
                process_action(next_stage='mom_select')

        elif st.session_state.stage == 'mom_select':
            st.subheader("새로운 엄마를 스카우트하러 갑니다. 누구를 고르시겠습니까?")
            
            if st.button("재벌가 마라탕집 사장님 엄마", key="btn_mom_choice_1"):
                st.session_state.mom_type = 'exploded' if random.random() < 0.15 else 'rich'
                st.session_state.stage = 'main'
                st.rerun()
            if st.button("무술 고수 대륙의 어머니", key="btn_mom_choice_2"):
                st.session_state.mom_type = 'exploded' if random.random() < 0.15 else 'fighter'
                st.session_state.stage = 'main'
                st.rerun()
            if st.button("평범하고 인자한 시골 어머니", key="btn_mom_choice_3"):
                st.session_state.mom_type = 'exploded' if random.random() < 0.15 else 'gentle'
                st.session_state.stage = 'main'
                st.rerun()

        elif st.session_state.stage == 'main':
            if st.session_state.mom_type == 'exploded':
                st.error("💥 엄마가 선택 도중 과열되어 쾅 터져버렸습니다! **[무소속 고아 상태]**로 생성되었습니다.")
            elif st.session_state.mom_type == 'rich':
                st.success("💰 재벌가 엄마 버프 발동: 든든한 자본 속에서 무난하게 시작합니다.")
            elif st.session_state.mom_type == 'fighter':
                st.success("🥋 무술가 엄마 버프 발동: 험난한 대륙에서 버티는 힘이 솟아납니다.")
            elif st.session_state.mom_type == 'gentle':
                st.info("🍵 시골 엄마 버프 발동: 평온한 멘탈을 유지합니다.")
            else:
                st.success("기적적으로 숨을 쉬고 있습니다! 무엇을 할까요?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("밥 먹으러 가기", key="main_btn_eat"): process_action(next_stage='eat_start')
                if st.button("대륙의 얼 표출하기", key="main_btn_china"): process_action(next_stage='chinese_start')
                if st.button("취업 전선 뛰어들기", key="main_btn_job"): process_action(next_stage='job_start')
            with col2:
                if st.button("집 밖으로 외출하기", key="main_btn_out"): process_action(next_stage='out_start')
                if st.button("방구석에서 잉여짓 하기", key="main_btn_idle"): process_action(next_stage='idle_start')
                if st.button("PC방 가서 게임하기", key="main_btn_game"): process_action(next_stage='game_start')

        elif st.session_state.stage == 'eat_start':
            st.subheader("밥을 먹기로 결심했습니다. 어디로 갈까요?")
            if st.button("마라탕 골목으로 간다", key="eat_s_1"): process_action(next_stage='eat_walk')
            if st.button("든든한 백반집으로 간다", key="eat_s_2"): process_action(next_stage='eat_walk_normal')

        elif st.session_state.stage == 'eat_walk':
            st.subheader("마라탕집으로 걷는 중입니다. 앞에 횡단보도가 초록불입니다.")
            if st.button("여유롭게 건넌다", key="eat_w_1"): process_action(fatal=True, fatal_reason="파란불에 여유롭게 걷다가 배달 오토바이에 치여서 납치당해 죽었습니다!", fatal_title="무법지대")
            if st.button("좌우를 살피며 전력질주한다", key="eat_w_2"): process_action(next_stage='eat_door')

        elif st.session_state.stage == 'eat_door':
            st.subheader("마라탕집 문 앞에 도착했습니다. 문에 [당기시오]라고 적혀있습니다.")
            if st.button("힘차게 당긴다", key="eat_d_1"): process_action(next_stage='eat_order')
            if st.button("상남자답게 밀고 들어간다", key="eat_d_2"): process_action(fatal=True, fatal_reason="문을 힘차게 밀다가 유리에 머리를 박고 놀라서 뒤1졌습니다!", fatal_title="진성 개복치")
            
        elif st.session_state.stage == 'eat_order':
            st.subheader("가게에 들어왔습니다. 마라탕 맵기를 선택하세요.")
            if st.button("0단계 (백탕)", key="eat_o_1"): process_action(fatal=True, fatal_reason="마라탕집에서 백탕을 시켰다가 주방장에게 암살당해 죽었습니다!", fatal_title="명예훼손")
            if st.button("2단계 (적당히 매운맛)", key="eat_o_2"): process_action(is_ending=True, win_msg="마라탕을 적절히 즐기고 황홀한 얼얼함 속에 대륙의 식신으로 거듭났습니다!", win_title="엔딩 1: 마라탕의 신")
            if st.button("4단계 (미친맛)", key="eat_o_3"): process_action(fatal=True, fatal_reason="마라탕을 너무 맵게 먹어서 뒤1졌습니다1!!!1!", fatal_title="위장관 용암지대")

        elif st.session_state.stage == 'eat_walk_normal':
            st.subheader("백반집에 도착해 밥을 한 숟갈 떴습니다.")
            if st.button("차분하게 꼭꼭 씹어 먹는다", key="eat_wn_1"): process_action(is_ending=True, win_msg="소화가 무사히 잘 되어 건강한 몸으로 100세까지 장수했습니다!", win_title="엔딩 2: 건강한 장수인")
            if st.button("허겁지겁 입에 밀어넣는다", key="eat_wn_2"): process_action(fatal=True, fatal_reason="밥먹다가 그냥 죽었ㅅ브니다!", fatal_title="식도 가출")
            if st.button("반찬 투정을 한다", key="eat_wn_3"): process_action(fatal=True, fatal_reason="반찬 투정하다가 식당 이모한테 등짝을 맞고 사1망했습니다!", fatal_title="유리몸")

        elif st.session_state.stage == 'out_start':
            st.subheader("외출하려고 신발장을 열었습니다.")
            if st.button("운동화를 구겨 신고 밖으로 나선다", key="out_s_1"): process_action(next_stage='out_street')
            if st.button("공유 자전거를 타고 출동한다", key="out_s_2"): process_action(next_stage='out_bike')

        elif st.session_state.stage == 'out_street':
            st.subheader("큰 길가에 나와 걸어갑니다. 누군가 어깨를 툭 칩니다.")
            if st.button("뒤돌아서 누군지 확인한다", key="out_str_1"): process_action(fatal=True, fatal_reason="길을 걷다가 납치를 당해서 죽었습니다!", fatal_title="인체의 신비")
            if st.button("무시하고 앞만 보고 뛴다", key="out_str_2"): process_action(fatal=True, fatal_reason="뛰어가다가 신발끈이 풀려 넘어지면서 턱을 박아 쇼크사했습니다!", fatal_title="안면 브레이커")

        elif st.session_state.stage == 'out_bike':
            st.subheader("공유 자전거 페달을 밟고 속도를 내는 중입니다. 내리막길입니다!")
            if st.button("적절히 속도를 줄이며 무사히 정지한다", key="out_b_1"): process_action(is_ending=True, win_msg="자전거 운전을 기가 막히게 해내어 라이딩 마스터가 되었습니다!", win_title="엔딩 3: 따릉이 베스트 드라이버")
            if st.button("브레이크를 미친듯이 잡는다", key="out_b_2"): process_action(fatal=True, fatal_reason="급정거를 너무 심하게 해서 자전거랑 같이 공중으로 3바퀴 돌고 떨어져 뒤졌습니다!", fatal_title="자전거 스턴트")
            if st.button("바람을 즐기며 브레이크를 놓는다", key="out_b_3"): process_action(fatal=True, fatal_reason="브레이크가 고장 나서 폭주하다가 트럭과 정면충돌했습니다!", fatal_title="속도의 한계")

        elif st.session_state.stage == 'chinese_start':
            st.subheader("베이징 광장 한복판에 섰습니다. 무슨 짓을 할까요?")
            if st.button("허파에 바람을 넣고 소리를 지른다", key="chi_s_1"): process_action(next_stage='chinese_shout')
            if st.button("스마트폰을 꺼내 방송을 켠다", key="chi_s_2"): process_action(next_stage='chinese_broadcast')

        elif st.session_state.stage == 'chinese_shout':
            st.subheader("목청을 가다듬고 문구를 외치려 합니다.")
            if st.button("자부심 넘치게 외치기", key="chi_sh_1"): process_action(fatal=True, fatal_reason="워 쓰 중꿔러! 하오! 하오! 하오쯔! 타 쿼 스!", fatal_title="대륙의 기상")
            if st.button("성조를 살짝 다르게 꼬아본다", key="chi_sh_2"): process_action(fatal=True, fatal_reason="중국어 성조를 잘못 발음해서 죽었 쓰! 니다!", fatal_title="성조 파괴자")

        elif st.session_state.stage == 'chinese_broadcast':
            st.subheader("라이브 방송을 켜고 개인기를 시전합니다.")
            if st.button("신들린 비트박스와 함께 대륙 랩을 소화한다", key="chi_b_1"): process_action(is_ending=True, win_msg="틱톡 10억 팔로워를 달성하며 세계적인 힙합 스타가 되었습니다!", win_title="엔딩 4: 대륙의 틱톡 스타")
            if st.button("요즘 유행하는 힙합 랩 시전", key="chi_b_2"): process_action(fatal=True, fatal_reason="탁원이 탁원이 (RED RED) 중국인 중국인 (RED RED) 워쓰어중궈러 죽었습니다!", fatal_title="쇼미더대륙")
            if st.button("갑자기 광장무 댄스 브레이크", key="chi_b_3"): process_action(fatal=True, fatal_reason="춤을 너무 격렬하게 추다가 골반이 탈골되어 쓰러져 사망했습니다!", fatal_title="뼈다귀 이탈")

        elif st.session_state.stage == 'idle_start':
            st.subheader("침대에 누워 스마트폰을 켭니다. 무엇을 볼까요?")
            if st.button("타오바오 앱을 켜서 쇼핑하기", key="idle_s_1"): process_action(next_stage='idle_taobao')
            if st.button("SNS 악플 읽으며 멘탈 갈리기", key="idle_s_2"): process_action(fatal=True, fatal_reason="악플을 읽다가 멘탈이 가루가 되어 증발해 버렸습니다!", fatal_title="쿠쿠다스 멘탈")

        elif st.session_state.stage == 'idle_taobao':
            st.subheader("장바구니에 폭탄 세일 물품들이 가득합니다. 무엇을 결제할까요?")
            if st.button("리뷰 1만개 평점 5.0 정상적인 이불 구매", key="idle_t_1"): process_action(is_ending=True, win_msg="푹신한 이불 속에서 귤을 까먹으며 신선처럼 영생을 누렸습니다!", win_title="엔딩 5: 방구석 신선")
            if st.button("초특가 990원 대용량 보조배터리", key="idle_t_2"): process_action(fatal=True, fatal_reason="택배를 뜯자마자 배터리가 폭발해서 그냥 뒤졌습니다!", fatal_title="이유 없는 반항")
            if st.button("리뷰 0개짜리 정체불명 명품 티셔츠", key="idle_t_3"): process_action(fatal=True, fatal_reason="사망 메시지가 맞춤법을 틀려서 주것씁이다!!", fatal_title="세종대왕 극대노")

        elif st.session_state.stage == 'job_start':
            st.subheader("통장 잔고가 0원입니다. 일자리를 구해야 합니다.")
            if st.button("탕후루 프랜차이즈 알바 면접", key="job_s_1"): process_action(next_stage='job_tanghulu')
            if st.button("판다 사육사 모집 공고 지원", key="job_s_2"): process_action(next_stage='job_panda')
            
        elif st.session_state.stage == 'job_tanghulu':
            st.subheader("면접관이 탕후루 꼬치를 쥐어주며 시연을 요구합니다.")
            if st.button("현란한 손놀림으로 과일을 코팅한다", key="job_t_1"): process_action(is_ending=True, win_msg="완벽한 설탕 코팅 비율을 선보여 월매출 1억 탕후루 CEO가 되었습니다!", win_title="엔딩 6: 탕후루 마스터")
            if st.button("면접관 면상에 설탕 시럽을 뿌린다", key="job_t_2"): process_action(fatal=True, fatal_reason="면접관을 화상 입혀서 체포당해 사형당했습니다!", fatal_title="매운맛 면접")
            if st.button("설탕 시럽을 통째로 마셔버린다", key="job_t_3"): process_action(fatal=True, fatal_reason="급성 당뇨 쇼크로 그 자리에서 쓰러져 죽었습니다!", fatal_title="단맛의 최후")

        elif st.session_state.stage == 'job_panda':
            st.subheader("면접장인 동물원에 도착했습니다. 판다가 탈출해 당신에게 달려옵니다!")
            if st.button("판다를 업어치기로 제압한다", key="job_p_1"): process_action(fatal=True, fatal_reason="국보인 귀여운 판다를 다치게 하여 공안에게 끌려가 죽었습니다!", fatal_title="국보 훼손죄")
            if st.button("대나무를 꺼내며 침착하게 달랜다", key="job_p_2"): process_action(is_ending=True, win_msg="판다를 완벽히 진정시키고 최고 대우 수석 사육사로 특채되었습니다!", win_title="엔딩 7: 판다의 영웅")
            if st.button("죽은 척을 하며 바닥에 눕는다", key="job_p_3"): process_action(fatal=True, fatal_reason="달려오던 판다가 당신을 푹신한 쿠션인 줄 알고 깔고 앉아 압사당했습니다!", fatal_title="판다 방석")

        elif st.session_state.stage == 'game_start':
            st.subheader("스트레스 해소를 위해 PC방에 왔습니다. 무슨 게임을 할까요?")
            if st.button("중국 서버 리그 오브 레전드 접속", key="game_s_1"): process_action(next_stage='game_lol')
            if st.button("원신에 접속해 가챠를 돌린다", key="game_s_2"): process_action(next_stage='game_genshin')
            
        elif st.session_state.stage == 'game_lol':
            st.subheader("팀원들이 시작부터 채팅으로 미친듯이 싸우고 있습니다.")
            if st.button("화려한 중국어로 패드립에 참전한다", key="game_l_1"): process_action(fatal=True, fatal_reason="타자 속도를 못 이기고 혈압이 한계치까지 올라 뇌출혈로 사망했습니다!", fatal_title="키보드 워리어의 최후")
            if st.button("채팅을 모두 차단하고 묵묵히 백도어를 간다", key="game_l_2"): process_action(is_ending=True, win_msg="신들린 백도어로 넥서스를 깨고 프로팀 스카우터의 눈에 띄었습니다!", win_title="엔딩 8: 협곡의 지배자")
            if st.button("우물에서 잠수를 탄다", key="game_l_3"): process_action(fatal=True, fatal_reason="분노한 팀원 중 한 명이 당신의 IP를 추적해 현실 갱킹을 와서 죽었습니다!", fatal_title="현실 갱킹")

        elif st.session_state.stage == 'game_genshin':
            st.subheader("모아둔 원석으로 10연차를 돌렸습니다. 화면에 황금빛이 번쩍입니다!")
            if st.button("경건한 마음으로 스킵 버튼을 누른다", key="game_g_1"): process_action(is_ending=True, win_msg="원하는 한정 캐릭터 5마리가 동시에 나오는 기적을 맛보고 승천했습니다!", win_title="엔딩 9: 가챠의 신")
            if st.button("소리를 지르며 키보드를 내려친다", key="game_g_2"): process_action(fatal=True, fatal_reason="키보드를 부수다 빡친 PC방 사장님에게 뚝배기를 맞고 사망했습니다!", fatal_title="물리적 로그아웃")
            if st.button("옆자리 아저씨에게 화면을 보여주며 자랑한다", key="game_g_3"): process_action(fatal=True, fatal_reason="폭사한 옆자리 아저씨가 질투에 눈이 멀어 휘두른 키보드에 맞아 죽었습니다!", fatal_title="질투의 화신")

    st.markdown('</div>', unsafe_allow_html=True)
