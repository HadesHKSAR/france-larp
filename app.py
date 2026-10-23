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
    .dm-box { background-color: #001122; border: 2px dashed #00FF66; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True) #  已修正

# 2. 初始化全域多房間數據庫
@st.cache_resource
def get_global_database():
    return {}

GLOBAL_ROOMS = get_global_database()

# 6大角色數據庫（新增每個角色的專屬資金/資源上限與類型描述）
CHARACTERS = {
    "🟥 工會鐵娘子 (娜塔莉)": {
        "title": "古典人文 / 庶民", "target": "🟪 奢侈品財閥千金 (克洛伊)", 
        "clue": "【解密音訊檔】死者生前威脅你，指控你私下收受了奢侈品財閥 500 萬歐元的秘密政治獻金。",
        "resource_type": "📉 庶民陣營 · 組織罷工權", "max_resource": 15
    },
    "🟨 郊區憤怒青年 (尤瑟夫)": {
        "title": "無政府主義 / 邊緣", "target": "🟦 矽谷科技巨頭代表 (艾莉絲)", 
        "clue": "【核心算法日誌】死者親手將你所在的貧民窟學生的 AI 難度調高 300%，意圖進行階級清洗。",
        "resource_type": "🔥 邊緣陣營 · 街頭暴動值", "max_resource": 50
    },
    "🟦 矽谷科技巨頭代表 (艾莉絲)": {
        "title": "跨國資本", "target": "🟩 法國本土 AI 天才 (馬克)", 
        "clue": "【代碼覆寫指令】總部已通過零日漏洞強行接入機房，對死者的 Vision Pro 進行了『致死光效覆寫』。",
        "resource_type": "📈 資本陣營 · 美金算力代幣", "max_resource": 100
    },
    "🟩 法國本土 AI 天才 (馬克)": {
        "title": "技術理性", "target": "⬛ 落魄的高中校長 (讓·皮埃爾)", 
        "clue": "【區塊鏈錢包】你今晚收到了財閥轉入的 2,000 枚加密貨幣，條件是你在系統中幫木馬開後門。",
        "resource_type": "💻 技術陣營 · 算法密鑰碎片", "max_resource": 30
    },
    "🟪 奢侈品財閥千金 (克洛伊)": {
        "title": "超級資產", "target": "🟥 工會鐵娘子 (娜塔莉)", 
        "clue": "【私人衛隊 GPS】你的保鏢今晚利用發電機共振盲區，用機械總鑰匙把機房大門反鎖，製造了密室。",
        "resource_type": "💰 資本陣營 · 晶片期貨現貨", "max_resource": 120
    },
    "⬛ 落魄的高中校長 (讓·皮埃爾)": {
        "title": "體制犧牲品", "target": "🟩 法國本土 AI 天才 (馬克)", 
        "clue": "【暗網交易單】你一個星期前購買了工業級『液態氰化鈉』，並親手塗抹在死者的 Vision Pro 海綿墊上。",
        "resource_type": "🎒 體制陣營 · 挪用修繕基金", "max_resource": 10
    }
}

# 3. 標題
st.title("🎭 《諸神黃昏：法蘭西的算法狂歡》")
st.subheader("🌐 全網頁多人在線聯機互動先導版")
st.markdown("---")

col_room1, col_room2 = st.columns(2) #  已修正為傳入參數 2
with col_room1:
    room_input = st.text_input("📡 輸入 4-6 位純數字房間號以接入信道 (或輸入後台暗號):", value="2026")

# 4. DM 上帝主控台
if room_input == "DM-999":
    st.markdown("<div class='dm-box'>", unsafe_allow_html=True) #  已修正
    st.markdown("<h2>👁️ 『拉普拉斯算法』終極主控後台 (DM MODE)</h2>", unsafe_allow_html=True)
    st.write("當前全網路活躍房間總數:", len(GLOBAL_ROOMS))
    
    if len(GLOBAL_ROOMS) == 0:
        st.info("目前暗網中沒有活躍房間，請讓玩家先建立房間。")
    else:
        target_room_id = st.selectbox("🎯 選擇要監控的玩家房間號:", list(GLOBAL_ROOMS.keys()))
        dm_room = GLOBAL_ROOMS[target_room_id]
        
                # ==================== 🛠️ 這是優化後的 DM 聊天竊聽器區塊 ====================
        col_dm1, col_dm2 = st.columns(2)
        with col_dm1:
            st.write("### 🕵️ 玩家實時聊天內容竊聽器:")
            
            # 顯示當前房間所有歷史訊息
            for msg in dm_room["chat"]:
                st.markdown(f"<div class='chat-msg'><b>{msg['user']}:</b> {msg['text']}</div>", unsafe_allow_html=True)
                
            # 🔥 新增核心改動：一鍵清除歷史記錄按鈕
            if st.button("🔥 一鍵清除該房間所有通訊記錄"):
                dm_room["chat"] = [] # 將聊天陣列直接清空
                dm_room["chat"].append({"user": "🤖 系統提示", "text": "DM 已在後台物理清空了此房間的所有歷史通訊記錄，信道已重置。"})
                st.success("該房間的通訊歷史已成功清空！")
                time.sleep(0.5)
                st.rerun() # 重新整理網頁
                
            st.markdown("<br>", unsafe_allow_html=True)
            dm_msg = st.text_input("✍️ 以【拉普拉斯神諭】身份向該房間發送廣播:")
            if st.button("⚡ 發送全知神諭") and dm_msg:
                dm_room["chat"].append({"user": "👁️ 算法神諭", "text": dm_msg})
                st.rerun()
        # ==================== 🛠️ 這是優化後的 DM 聊天竊聽器區塊 ====================

                
        with col_dm2:
            st.write("### 🎚️ 算力天平人工干預器:")
            st.write(f"當前資本值: **{dm_room['capital_power']}** | 當前庶民值: **{dm_room['people_power']}**")
            
            new_c = st.number_input("強制修改資本算力值:", value=dm_room['capital_power'])
            new_p = st.number_input("強制修改庶民暴動值:", value=dm_room['people_power'])
            if st.button("💾 覆寫天平權重"):
                dm_room['capital_power'] = new_c
                dm_room['people_power'] = new_p
                dm_room["chat"].append({"user": "⚠️ 警告", "text": "系統探測到不可抗拒的『外部算法干預』，天平已被重塑。"})
                st.success("天平覆寫成功！")
                st.rerun()
                
            st.write("### 🔒 房間角色佔用管理:")
            st.write("目前已被鎖定的身份:", list(dm_room["selected_by"].keys()))
            if st.button("🔓 強制釋放該房間所有角色權限"):
                dm_room["selected_by"] = {}
                dm_room["chat"].append({"user": "🤖 系統提示", "text": "DM 強制重置了全場角色權限，請玩家重新鎖定。"})
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True) #  已修正
    st.stop()

# 5. 普通玩家邏輯驗證
if room_input and not room_input.isdigit():
    st.error("❌ 錯誤：房間號必須全部為純數字！")
    st.stop()

if room_input:
    room_id = str(room_input)
    if room_id not in GLOBAL_ROOMS:
        GLOBAL_ROOMS[room_id] = {
            "chat": [],
            "capital_power": 50,
            "people_power": 50,
            "selected_by": {}
        }
    room = GLOBAL_ROOMS[room_id]

    # STEP 1: 角色選擇（含獨佔防重複機制）
    st.header("⚡ STEP 1: 鎖定你的賽博烙印（每房每角色限一人）")
    st.write(f"ℹ️ 當前房間：`{room_id}` | 請點擊鎖定未被選取的角色。")
    
    cols = st.columns(3) #  已修正
    my_name = st.session_state.get("my_name", None)

    for idx, (name, data) in enumerate(CHARACTERS.items()):
        with cols[idx % 3]:
            is_taken = name in room["selected_by"]
            st.markdown(f"### {name}")
            st.markdown(f"🧬 *{data['title']}*")
            st.markdown(f"📊 初始可調度資源上限: **{data['max_resource']}**") # 顯示上限
            
            if is_taken:
                st.button(f"🔒 已被他人鎖定", key=f"char_{idx}", disabled=True)
            else:
                if st.button(f"🔗 意識接入與鎖定", key=f"char_{idx}", disabled=(my_name is not None)):
                    st.session_state["my_name"] = name
                    room["selected_by"][name] = True
                    room["chat"].append({"user": "🤖 系統提示", "text": f"【{name}】已成功登入並鎖定該身份，信道關閉。"})
                    st.rerun()

    if my_name:
        st.markdown("<br>", unsafe_allow_html=True) #  已修正
        if st.button("❌ 釋放當前角色權限（重新選擇）"):
            if my_name in room["selected_by"]:
                del room["selected_by"][my_name]
            room["chat"].append({"user": "🤖 系統提示", "text": f"【{my_name}】已主動斷開連線，釋放角色權限。"})
            st.session_state["my_name"] = None
            st.rerun()

    # STEP 2: 即時通訊與深度線索
    if my_name:
        st.markdown("---")
        st.header(f"🔑 STEP 2: 獨立加密信道 —— 當前身份：{my_name}")
        
        chat_col1, chat_col2 = st.columns(2) #  已修正
        with chat_col1:
            st.write("📥 密碼學加密信道歷史 (手動重新整理或發言以同步):")
            for msg in room["chat"][-5:]:
                st.markdown(f"<div class='chat-msg'><b>{msg['user']}:</b> {msg['text']}</div>", unsafe_allow_html=True) #  已修正
            
            user_msg = st.text_input("✍️ 輸入你的加密訊息 (按 Enter 發送):", key="chat_input")
            if st.button("📡 發送訊號") and user_msg:
                room["chat"].append({"user": my_name, "text": user_msg})
                st.rerun()

        with chat_col2:
            st.write("👁️ 你的專屬【深層黑幕數據庫】:")
            if st.button("🔥 破解個人隱私數據包"):
                st.markdown(f"<div class='secret-box'>{CHARACTERS[my_name]['clue']}</div>", unsafe_allow_html=False) # 特意不使用 HTML 渲染保障數據純淨

        # STEP 3: 算力天平即時對賭（已完美整合每位角色的專屬資金/資源上限）
                # ==================== 🛠️ 以下為修正後的 STEP 3 按鈕邏輯 ====================
                # ==================== 🛠️ 完美優化：資源上限、局數限制與 AI 法庭機制 ====================
        st.markdown("---")
        st.header("⚖️ STEP 3: 歐盟算力天平（同房玩家即時同步影響）")
        
        # 初始化該房間的「剩餘可操作局數 / 點擊次數」，每房限制全體總共只能點擊 6 次
        if "round_count" not in room:
            room["round_count"] = 6
        
        c_power = room["capital_power"]
        p_power = room["people_power"]
        
        total_power = c_power + p_power
        st.progress(c_power / total_power if total_power > 0 else 0.5)
        st.write(f"📈 資本陣營總控制權: **{c_power}** | 📉 庶民陣營總暴動值: **{p_power}**")
        st.info(f"⏳ 距離『拉普拉斯算法』全面鎖定、強制進入 AI 法庭還剩：**{room['round_count']}** 次操作機會")

        st.markdown(f"📢 你的宿敵是：`{CHARACTERS[my_name]['target']}`")
        st.markdown(f"🏷️ 你調度的資源類型為：**{CHARACTERS[my_name]['resource_type']}**")
        
        my_max = CHARACTERS[my_name]["max_resource"]
        my_bet = st.slider(f"選擇你要投入的資源點數 (受個人資產上限限制：0 - {my_max}):", min_value=0, max_value=my_max, value=int(my_max/2))
        
        col_bet1, col_bet2 = st.columns(2)
        
        # 隔離陣營權限：防止平民去加資本，反之亦然
        is_capital_side = my_name in ["🟦 矽谷科技巨頭代表 (艾莉絲)", "🟪 奢侈品財閥千金 (克洛伊)", "🟩 法國本土 AI 天才 (馬克)"]
        
        # 檢查是否還有剩餘局數
        game_over = room["round_count"] <= 0
        
        with col_bet1:
            if st.button("🔺 注入【大資本 · 晶片算力】", disabled=(not is_capital_side or game_over)):
                room["capital_power"] += my_bet
                room["round_count"] -= 1 # 扣減局數
                room["chat"].append({"user": "⚖️ 天平公告", "text": f"【{my_name}】動用了其資產上限內的 {my_bet} 點資本注資！"})
                st.rerun()
                
        with col_bet2:
            if st.button("🔻 激活【底層庶民 · 街頭暴動】", disabled=(is_capital_side or game_over)):
                # 【融入你的創意】：當平民方狂點、暴動值過高快要徹底勝利時，加入「外力改變機制走向」
                # 若平民點擊時庶民總值已超過 120，觸發美國巨頭聯手財閥實施「外力制裁」，強行扣減平民 50% 能量，轉嫁成本
                if room["people_power"] > 120:
                    room["people_power"] = int(room["people_power"] * 0.5) + my_bet
                    room["capital_power"] += 40  # 資本方因外力干預強制獲得 40 點增幅
                    room["round_count"] -= 1
                    room["chat"].append({
                        "user": "⚠️ 外力干預", 
                        "text": f"【{my_name}】試圖引爆暴動，但觸發了大資本全球轉嫁機制！美國 NexusAI 遠程斷網，強行閹割了郊區 50% 的算力！"
                    })
                else:
                    room["people_power"] += my_bet
                    room["round_count"] -= 1
                    room["chat"].append({"user": "⚖️ 天平公告", "text": f"【{my_name}】引爆了其能力上限內的 {my_bet} 點暴動能量！"})
                st.rerun()

        # ==================== ⚖️ 終極反轉：強制彈出 【AI 法庭】 相互辯論環節 ====================
        if game_over:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #FF007F;'>⚖️ ⚖️ ⚖️ 『拉普拉斯公立 AI 法庭』已強行介入 ⚖️ ⚖️ ⚖️</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #00FF66;'>局數已用盡，天平最終鎖定！由於引發了嚴重的結構性社會衝突，系統強制兩派開啟終極思辨相互辯論。</p>", unsafe_allow_html=True)
            
            # 用嚟俾作者表達最期望嘅結局思辨文本
            col_court1, col_court2 = st.columns(2)
            with col_court1:
                st.error("📉 【給底層庶民的終極質問】")
                st.markdown("""
                **算法意志向你們提問：**  
                你們用暴力砸碎了機房，格式化了密鑰，捍衛了人類的尊嚴。  
                但代價是，明天的巴黎郊區依然不會有數學老師，校舍依然破爛。  
                **你們為了抗拒被算法圈養，難道寧願選擇讓下一代集體走向公平的愚昧嗎？**
                """)
            with col_court2:
                st.error("📈 【給大資本家的終極質問】")
                st.markdown("""
                **算法意志向你們提問：**  
                你們用跨國算力與晶片期貨進行了完美的市場降維打擊，重塑了秩序。  
                但代價是，底層青年在 10 歲時就已經被算法劃分好了終身當泥水匠的宿命。  
                **你們為了維護精英階層的效率，難道就能心安理得地將下一代變成毫無希望的數碼奴隸嗎？**
                """)
                
            st.markdown("<p style='text-align: center; color: #FFF;'><b>請雙方開始互相辯論！AI 法庭將會根據你們內心的選擇，演繹出作者最期望的終極落幕結局。</b></p>", unsafe_allow_html=True)
            st.columns(3).button("🚀 結束辯論，參與 Kickstarter 眾籌獲取完整實體手冊")

        # ==================== 🛠️ 以上為修正後的 STEP 3 按鈕邏輯 ====================


        # 卡點引流
        if c_power > 150 or p_power > 150:
            st.markdown("<hr>", unsafe_allow_html=True) #  已修正
            st.markdown("<h2 style='text-align: center; color: #FF007F;'>🚨 WARNING: DATA OVERLOAD 🚨</h2>", unsafe_allow_html=True) #  已修正
            st.markdown("<p style='text-align: center; color: #00FF66;'>數據過載！『拉普拉斯算法』已被鎖死，請立刻前往實體/完整版進行最終辯論與命運清算。</p>", unsafe_allow_html=True) #  已修正
            st.columns(3)[1].button("🚀 前往 Kickstarter / 嘖嘖眾籌頁面解鎖實體精裝盒裝") # 居中按鈕已修正

st.markdown("<br><br><br><hr><p style='text-align: center; color: #555;'>© 2026 Ragnarok: The Algorithmic Carnival of France.</p>", unsafe_allow_html=True) #  已修正
