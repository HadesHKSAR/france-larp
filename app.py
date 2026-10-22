import streamlit as st
import time

# 1. 網頁基本配置與賽博朋克風格 CSS
st.set_page_config(page_title="諸神黃昏：法蘭西的算法狂歡", page_icon="🎭", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #00FF66; font-family: 'Courier New', monospace; }
    h1, h2, h3 { color: #FF007F !important; text-shadow: 0 0 10px #FF007F; }
    .stButton>button { 
        background-color: #FF007F !important; color: white !important; 
        border: 1px solid #00FF66 !important; box-shadow: 0 0 15px #FF007F;
        transition: all 0.3s; width: 100%;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px #00FF66; }
    .stButton>button:disabled { background-color: #333333 !important; color: #666666 !important; border: 1px solid #555 !important; box-shadow: none !important; }
    .clue-box { background-color: #1A1C23; border-left: 5px solid #00FF66; padding: 15px; margin: 10px 0; border-radius: 5px; }
    .secret-box { background-color: #2D1B2A; border-left: 5px solid #FF007F; padding: 15px; margin: 10px 0; border-radius: 5px; color: #FFB3D1; }
    .chat-msg { background-color: #111; padding: 8px; margin: 5px 0; border-radius: 3px; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# 2. 初始化全域多房間數據庫（跨用戶數據共享）
if "GLOBAL_ROOMS" not in st.session_state:
    st.session_state["GLOBAL_ROOMS"] = {}

# 6大獨佔角色數據庫設定
CHARACTERS = {
    "🟥 工會鐵娘子 (娜塔莉)": {"title": "古典人文 / 庶民", "target": "🟪 奢侈品財閥千金 (克洛伊)", "clue": "【解密音訊檔】死者生前威脅你，指控你私下收受了奢侈品財閥 500 萬歐元的秘密政治獻金。"},
    "🟨 郊區憤怒青年 (尤瑟夫)": {"title": "無政府主義 / 邊緣", "target": "🟦 矽谷科技巨頭代表 (艾莉絲)", "clue": "【核心算法日誌】死者親手將你所在的貧民窟學生的 AI 難度調高 300%，意圖進行階級清洗。"},
    "🟦 矽谷科技巨頭代表 (艾莉絲)": {"title": "跨國資本", "target": "🟩 法國本土 AI 天才 (馬克)", "clue": "【代碼覆寫指令】總部已通過零日漏洞強行接入機房，對死者的 Vision Pro 進行了『致死光效覆寫』。"},
    "🟩 法國本土 AI 天才 (馬克)": {"title": "技術理性", "target": "⬛ 落魄的高中校長 (讓·皮埃爾)", "clue": "【區塊鏈錢包】你今晚收到了財閥轉入的 2,000 枚加密貨幣，條件是你在系統中幫木馬開後門。"},
    "🟪 奢侈品財閥千金 (克洛伊)": {"title": "超級資產", "target": "🟥 工會鐵娘子 (娜塔莉)", "clue": "【私人衛隊 GPS】你的保鏢今晚利用發電機共振盲區，用機械總鑰匙把機房大門反鎖，製造了密室。"},
    "⬛ 落魄的高中校長 (讓·皮埃爾)": {"title": "體制犧牲品", "target": "🟩 法國本土 AI 天才 (馬克)", "clue": "【暗網交易單】你一個星期前購買了工業級『液態氰化鈉』，並親手塗抹在死者的 Vision Pro 海綿墊上。"}
}

# 3. 標題與簡便房號登入
st.title("🎭 《諸神黃昏：法蘭西的算法狂歡》")
st.subheader("🌐 全網頁多人在線聯機互動先導版")
st.markdown("---")

col_room1, col_room2 = st.columns([1, 2])
with col_room1:
    # 改動一：改為純數字房號限制，預設 2026
    room_input = st.text_input("📡 輸入 4-6 位純數字暗網房間號:", value="2026", max_chars=6)

# 驗證輸入是否為純數字
if room_input and not room_input.isdigit():
    st.error("❌ 錯誤：房間號必須全部為純數字！")
    st.stop()

if room_input:
    room_id = str(room_input)
    # 初始化全域房間狀態
    if room_id not in st.session_state["GLOBAL_ROOMS"]:
        st.session_state["GLOBAL_ROOMS"][room_id] = {
            "chat": [],
            "capital_power": 50,
            "people_power": 50,
            "selected_by": {}  # 紀錄哪個角色被哪位玩家鎖定
        }
    room = st.session_state["GLOBAL_ROOMS"][room_id]

    # 4. STEP 1: 角色選擇（改動二：加入獨佔限制機制，最多6人）
    st.header("⚡ STEP 1: 鎖定你的賽博烙印（每房每角色限一人）")
    st.write(f"ℹ️ 當前房間：`{room_id}` | 請點擊鎖定未被選取的角色。")
    
    cols = st.columns(3)
    my_name = st.session_state.get("my_name", None)

    for idx, (name, data) in enumerate(CHARACTERS.items()):
        with cols[idx % 3]:
            # 檢查這個角色是否已經被同房其他人揀咗
            is_taken = name in room["selected_by"]
            
            st.markdown(f"### {name}")
            st.markdown(f"🧬 *{data['title']}*")
            
            if is_taken:
                # 如果被揀咗，顯示鎖定狀態並停用按鈕
                st.button(f"🔒 已被他人鎖定", key=f"char_{idx}", disabled=True)
            else:
                # 未被揀，而且玩家自己未揀角色時可以點擊
                if st.button(f"🔗 意識接入與鎖定", key=f"char_{idx}", disabled=(my_name is not None)):
                    st.session_state["my_name"] = name
                    room["selected_by"][name] = True
                    room["chat"].append({"user": "🤖 系統提示", "text": f"【{name}】已成功登入並鎖定該身份，信道關閉。"})
                    st.rerun()

    # 清除角色按鈕（方便測試或換人）
    if my_name:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("❌ 釋放當前角色權限（重新選擇）"):
            if my_name in room["selected_by"]:
                del room["selected_by"][my_name]
            room["chat"].append({"user": "🤖 系統提示", "text": f"【{my_name}】已主動斷開連線，釋放角色權限。"})
            st.session_state["my_name"] = None
            st.rerun()

    # 5. STEP 2: 即時通訊與深度線索
    if my_name:
        st.markdown("---")
        st.header(f"🔑 STEP 2: 獨立加密信道 —— 當前身份：{my_name}")
        
        chat_col1, chat_col2 = st.columns(2)
        with chat_col1:
            st.write("📥 密碼學加密信道歷史 (手動重新整理或發言以同步):")
            for msg in room["chat"][-5:]:
                st.markdown(f"<div class='chat-msg'><b>{msg['user']}:</b> {msg['text']}</div>", unsafe_allow_html=True)
            
            user_msg = st.text_input("✍️ 輸入你的加密訊息 (按 Enter 發送):", key="chat_input")
            if st.button("📡 發送訊號") and user_msg:
                room["chat"].append({"user": my_name, "text": user_msg})
                st.rerun()

        with chat_col2:
            st.write("👁️ 你的專屬【深層黑幕數據庫】:")
            if st.button("🔥 破解個人隱私數據包"):
                st.markdown(f"<div class='secret-box'>{CHARACTERS[my_name]['clue']}</div>", unsafe_allow_html=True)

        # 6. STEP 3: 算力天平即時對賭
        st.markdown("---")
        st.header("⚖️ STEP 3: 歐盟算力天平（同房玩家即時同步影響）")
        
        c_power = room["capital_power"]
        p_power = room["people_power"]
        
        st.progress(c_power / (c_power + p_power) if (c_power + p_power) > 0 else 0.5)
        st.write(f"📈 資本陣營控制權: **{c_power}** | 📉 庶民陣營暴動值: **{p_power}**")

        st.write(f"📢 你的宿敵是：`{CHARACTERS[my_name]['target']}`。調度你的力量拉動天平：")
        my_bet = st.slider("選擇調度的資源點數 (0 - 50):", 0, 50, 10)
        
        col_bet1, col_bet2 = st.columns(2)
        with col_bet1:
            if st.button("🔺 注入【大資本 · 晶片算力】"):
                room["capital_power"] += my_bet
                room["chat"].append({"user": "⚖️ 天平公告", "text": f"【{my_name}】向資本天平注入了 {my_bet} 點算力！"})
                st.rerun()
        with col_bet2:
            if st.button("🔻 激活【底層庶民 · 街頭暴動】"):
                room["people_power"] += my_bet
                room["chat"].append({"user": "⚖️ 天平公告", "text": f"【{my_name}】激活了 {my_bet} 點街頭暴動值！"})
                st.rerun()

        # 7. 卡點與眾籌跳轉
        if c_power > 120 or p_power > 120:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #FF007F;'>🚨 WARNING: DATA OVERLOAD 🚨</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #00FF66;'>數據過載！『拉普拉斯算法』已被鎖死，請立刻前往實體/完整版進行最終清算。</p>", unsafe_allow_html=True)
            st.columns(3)[1].button("🚀 前往 Kickstarter / 嘖嘖眾籌頁面解鎖實體盒裝")

st.markdown("<br><br><br><hr><p style='text-align: center; color: #555;'>© 2026 Ragnarok: The Algorithmic Carnival of France.</p>", unsafe_allow_html=True)
