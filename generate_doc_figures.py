# -*- coding: utf-8 -*-
import os
import glob
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r'c:\Users\user\Desktop\AI課\jiuyuan-temple\docs\images'
os.makedirs(OUT_DIR, exist_ok=True)

# Fonts
FONT_HEITI = "msyh.ttc"
FONT_KAITI = "kaiu.ttf"

def get_font(name, size, bold=False):
    try:
        return ImageFont.truetype(name, size)
    except:
        return ImageFont.load_default()

# -------------------------------------------------------------
# 1. 首頁與品牌形象展示圖 (doc_img_hero.png)
# -------------------------------------------------------------
def make_hero_figure():
    w, h = 1200, 680
    im = Image.new('RGB', (w, h), (38, 5, 8))
    draw = ImageDraw.Draw(im)

    # Gradient / texture
    for y in range(h):
        r = int(58 - (y / h) * 35)
        g = int(8 - (y / h) * 5)
        b = int(12 - (y / h) * 8)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Border
    gold = (212, 175, 55)
    draw.rectangle([20, 20, w - 20, h - 20], outline=gold, width=3)
    draw.rectangle([28, 28, w - 28, h - 28], outline=(160, 120, 30), width=1)

    # Nav bar mockup
    draw.rectangle([30, 30, w - 30, 90], fill=(25, 3, 5))
    draw.line([(30, 90), (w - 30, 90)], fill=gold, width=2)
    f_title = get_font(FONT_KAITI, 32)
    draw.text((60, 42), "台中烏日九元宮 官方數位服務平台", fill=gold, font=f_title)
    
    f_nav = get_font(FONT_HEITI, 18)
    navs = ["首頁", "本宮沿革", "最新消息", "慶典活動花絮", "參拜指南", "鸞文寶庫", "線上擲杯", "九元宮三十六籤", "線上科儀"]
    nx = 520
    for n in navs:
        draw.text((nx, 48), n, fill=(240, 230, 210), font=f_nav)
        nx += 74

    # Hero Content
    f_main = get_font(FONT_KAITI, 56)
    draw.text((w // 2, 180), "九天應元雷聲普化天尊", fill=(255, 235, 170), font=f_main, anchor="mm")
    
    f_sub = get_font(FONT_KAITI, 28)
    draw.text((w // 2, 240), "總司三十六雷府 ｜ 普化十方 ｜ 消災解厄 ｜ 福佑黎民", fill=(220, 190, 110), font=f_sub, anchor="mm")

    # Quick Feature Cards (3 cards)
    cards = [
        ("九元宮三十六籤", "遵循淨心、搖筒、擲筊、解籤古禮\n三十六天罡靈籤為信眾排憂解惑", (180, 40, 40)),
        ("慶典活動花絮", "收錄廈門謁祖四祖廟巡禮實錄\n安營換符與炮炸武財神影音紀實", (160, 30, 30)),
        ("線上科儀登記", "光明燈/文昌燈/太歲燈/補財庫\n生成防偽疏文並自動同步雲端試算表", (140, 20, 20)),
    ]
    cx = 60
    cw = 340
    for c_title, c_desc, c_bg in cards:
        draw.rectangle([cx, 320, cx + cw, 560], fill=c_bg, outline=gold, width=2)
        # card header
        draw.rectangle([cx, 320, cx + cw, 380], fill=(70, 8, 12))
        draw.text((cx + cw // 2, 350), c_title, fill=gold, font=get_font(FONT_KAITI, 26), anchor="mm")
        
        # card text
        draw.text((cx + 25, 420), c_desc, fill=(255, 245, 235), font=get_font(FONT_HEITI, 18))
        
        # button
        draw.rectangle([cx + 50, 490, cx + cw - 50, 535], fill=gold)
        draw.text((cx + cw // 2, 512), "進入系統 ➔", fill=(50, 5, 5), font=get_font(FONT_HEITI, 18), anchor="mm")
        cx += 370

    # Footer note
    draw.text((w // 2, 630), "網址：https://ann1130520.github.io/jiuyuan-temple/  ｜  RWD 跨載具響應式設計", fill=(200, 180, 140), font=get_font(FONT_HEITI, 18), anchor="mm")

    p = os.path.join(OUT_DIR, 'doc_img_hero.png')
    im.save(p)
    print("Saved:", p)

# -------------------------------------------------------------
# 2. 活動花絮影音專區展示圖 (doc_img_highlights.png)
# -------------------------------------------------------------
def make_highlights_figure():
    w, h = 1200, 720
    im = Image.new('RGB', (w, h), (26, 8, 12))
    draw = ImageDraw.Draw(im)

    gold = (212, 175, 55)
    draw.rectangle([15, 15, w - 15, h - 15], outline=gold, width=2)

    # Title
    draw.text((w // 2, 50), "【慶典活動花絮】影音多媒體專區（最新至最舊排序）", fill=gold, font=get_font(FONT_KAITI, 32), anchor="mm")

    # 4 Highlight Cards Mockup with real thumbnails if possible
    hl_items = [
        {
            "date": "115.10.7-10.10",
            "title": "廈門謁祖進香祈安實錄",
            "sub": "巡禮四大祖廟：玉真法院、飛天四聖廟\n白礁慈濟宮（國母獅、皇帝祭天台）\n皇渡庵（皇帝井、神將操令現場實況）",
            "tag": "1080p 影片 (1分23秒)",
            "img_src": r'C:\Users\user\.gemini\antigravity\brain\56be5df4-93d5-4cfd-92e6-349cb1edd1cb\xiamen_verify2\sec_29.jpg'
        },
        {
            "date": "115.09.05",
            "title": "關懷弱勢兒少獲頒感謝狀",
            "sub": "中元普渡白米物資濟貧弱\n落實雷尊慈悲濟世宗旨\n榮獲家扶基金會致贈感謝狀",
            "tag": "公益慈善紀實",
            "img_src": r'c:\Users\user\Desktop\AI課\jiuyuan-temple\images\highlights\hl_charity_certificate.png'
        },
        {
            "date": "115.04.19",
            "title": "安營換符祈安實錄",
            "sub": "五方旗揚定四方神將營盤\n敕化神符掃除草野陰霾\n精選一分鐘現場法會紀實影片",
            "tag": "科儀影片 (1分鐘)",
            "img_src": r'c:\Users\user\Desktop\AI課\jiuyuan-temple\images\highlights\hl_anying_cover.jpg'
        },
        {
            "date": "114.04.12",
            "title": "炮炸武財神迎財納福盛典",
            "sub": "恭迎武財神聖駕萬炮齊鳴\n配樂震撼洗滌穢煞祥瑞臨門\n祈願地方商賈興旺財源廣進",
            "tag": "盛典影片 (配樂震撼)",
            "img_src": r'c:\Users\user\Desktop\AI課\jiuyuan-temple\images\highlights\hl_wucai_cover.jpg'
        }
    ]

    card_w = 265
    card_h = 560
    xs = [40, 330, 620, 910]

    for idx, (x, item) in enumerate(zip(xs, hl_items)):
        draw.rectangle([x, 100, x + card_w, 100 + card_h], fill=(45, 10, 15), outline=gold, width=2)
        
        # Thumbnail area
        thumb_h = 190
        draw.rectangle([x + 6, 106, x + card_w - 6, 106 + thumb_h], fill=(20, 5, 8))
        if os.path.exists(item["img_src"]):
            try:
                t_img = Image.open(item["img_src"])
                t_img = t_img.resize((card_w - 12, thumb_h), Image.Resampling.LANCZOS)
                im.paste(t_img, (x + 6, 106))
            except Exception as e:
                pass
        
        # Tag
        draw.rectangle([x + 12, 112, x + 160, 138], fill=(160, 20, 25))
        draw.text((x + 86, 125), item["tag"], fill=(255, 240, 200), font=get_font(FONT_HEITI, 13), anchor="mm")

        # Info
        draw.text((x + 15, 315), "📅 " + item["date"], fill=(220, 180, 80), font=get_font(FONT_HEITI, 14))
        draw.text((x + 15, 345), item["title"], fill=(255, 235, 180), font=get_font(FONT_KAITI, 20, bold=True))
        
        # Sub
        draw.text((x + 15, 395), item["sub"], fill=(225, 215, 205), font=get_font(FONT_HEITI, 14))

        # Bottom play button
        draw.rectangle([x + 20, 595, x + card_w - 20, 635], fill=gold)
        draw.text((x + card_w // 2, 615), "點擊全螢幕觀看", fill=(40, 5, 8), font=get_font(FONT_HEITI, 15), anchor="mm")

    # Bottom caption
    draw.text((w // 2, 690), "※ 影片均完成 YouTube 規格最佳化與配樂對齊，點擊即可開啟專屬全螢幕燈箱播放", fill=(200, 180, 140), font=get_font(FONT_HEITI, 16), anchor="mm")

    p = os.path.join(OUT_DIR, 'doc_img_highlights.png')
    im.save(p)
    print("Saved:", p)

# -------------------------------------------------------------
# 3. 九元宮三十六籤（三十六天罡靈籤）與立體擲筊 (doc_img_qian.png)
# -------------------------------------------------------------
def make_divination_figure():
    w, h = 1200, 680
    im = Image.new('RGB', (w, h), (32, 6, 10))
    draw = ImageDraw.Draw(im)

    gold = (212, 175, 55)
    draw.rectangle([15, 15, w - 15, h - 15], outline=gold, width=2)

    # Title
    draw.text((w // 2, 50), "【線上虔誠請旨】九元宮三十六籤（三十六天罡靈籤）與立體紅木筊杯解籤系統", fill=gold, font=get_font(FONT_KAITI, 30), anchor="mm")

    # Left: Divination Ritual Steps (Flowchart)
    draw.rectangle([40, 95, 480, 630], fill=(45, 10, 15), outline=gold, width=1)
    draw.text((260, 130), "正統請旨四部儀軌", fill=gold, font=get_font(FONT_KAITI, 24), anchor="mm")

    steps = [
        ("步驟一：淨心稟報", "點燃心香，端正身心，恭敬稟報\n信士姓名、生辰八字、現居地址與所求事宜。"),
        ("步驟二：搖筒抽籤", "點擊籤筒搖動求取靈籤，系統隨機抽取\n九元宮三十六天罡靈籤中之一支籤首。"),
        ("步驟三：擲筊請旨", "向雷祖擲筊請旨，須擲得「聖杯」\n方為神明恩准領籤（笑杯/陰杯須重抽）。"),
        ("步驟四：開籤詳解", "開示三十六天罡籤詩、神尊藏頭詩、吉凶\n與求財、求醫、事業、姻緣、健康分項指引。")
    ]
    sy = 175
    for s_title, s_desc in steps:
        draw.rectangle([60, sy, 460, sy + 95], fill=(70, 15, 20), outline=(180, 140, 40), width=1)
        draw.text((75, sy + 15), s_title, fill=(255, 220, 120), font=get_font(FONT_KAITI, 18))
        draw.text((75, sy + 45), s_desc, fill=(235, 225, 215), font=get_font(FONT_HEITI, 14))
        sy += 110

    # Right: Sample Qian Card Display
    draw.rectangle([510, 95, 1160, 630], fill=(255, 252, 245), outline=gold, width=2)
    
    # Red inner frame for Qian
    draw.rectangle([530, 115, 1140, 610], outline=(160, 20, 30), width=2)
    draw.text((835, 145), "台中烏日九元宮 三十六天罡靈籤（九元宮三十六籤）", fill=(160, 20, 30), font=get_font(FONT_KAITI, 25), anchor="mm")
    
    draw.text((835, 180), "【第一籤 天魁首】 上上籤 ｜ 藏頭：玉皇大天尊 ｜ 貴人：四方", fill=(80, 30, 30), font=get_font(FONT_HEITI, 16), anchor="mm")
    draw.line([(560, 205), (1110, 205)], fill=(160, 20, 30), width=1)

    # 5-line genuine poem from parsed_qian.json
    poem = [
        "玉恩在地百壽添",
        "皇聖助求下福來",
        "大賜恩澤廣三才",
        "天聖助順百樣好",
        "尊靈添香助再登"
    ]
    py = 230
    for line in poem:
        draw.text((835, py), line, fill=(40, 10, 10), font=get_font(FONT_KAITI, 23), anchor="mm")
        py += 34

    draw.line([(560, 405), (1110, 405)], fill=(160, 20, 30), width=1)
    
    # Interpretation fields
    interp = [
        ("【籤意淺釋】", "玉皇大天尊降福庇佑，百壽添福，恩澤廣被，凡事順遂，行善再登高峰。"),
        ("【貴人求財】", "貴人四方相扶；求財有，投資可，財源順暢，誠心祈求可獲豐盛。"),
        ("【求學事業】", "求學有成，求事業佳，求官有心可成，家運昌榮。"),
        ("【健康身心】", "身體無恙，一般人吉；行車安，出遊可，凡事光明。"),
        ("【求子姻緣】", "求子得女；求姻緣若已有對象者為好對象。")
    ]
    iy = 420
    for ik, iv in interp:
        draw.text((560, iy), ik, fill=(160, 20, 30), font=get_font(FONT_KAITI, 16))
        draw.text((670, iy), iv, fill=(40, 40, 40), font=get_font(FONT_HEITI, 14.5))
        iy += 34

    p = os.path.join(OUT_DIR, 'doc_img_qian.png')
    im.save(p)
    print("Saved:", p)

# -------------------------------------------------------------
# 4. 線上科儀登記與防偽疏文憑證 (doc_img_form_cert.png)
# -------------------------------------------------------------
def make_form_cert_figure():
    w, h = 1200, 680
    im = Image.new('RGB', (w, h), (28, 6, 8))
    draw = ImageDraw.Draw(im)

    gold = (212, 175, 55)
    draw.rectangle([15, 15, w - 15, h - 15], outline=gold, width=2)

    draw.text((w // 2, 50), "【線上科儀登記】祈福表單與加蓋宮印防偽疏文憑證", fill=gold, font=get_font(FONT_KAITI, 32), anchor="mm")

    # Left: Web Form UI
    draw.rectangle([40, 95, 540, 630], fill=(45, 10, 15), outline=gold, width=1)
    draw.text((290, 130), "線上點燈 / 補財庫登記表單", fill=gold, font=get_font(FONT_KAITI, 22), anchor="mm")

    form_fields = [
        ("科儀類別", "● 雷祖光明燈  ○ 文昌智慧燈  ○ 安太歲  ○ 補運補財庫"),
        ("信士姓名", "陳○明"),
        ("性別 / 稱謂", "乾造（男）"),
        ("農曆生辰", "歲次甲子年八月初五日子時"),
        ("聯絡電話", "0912-345-678"),
        ("現居地址", "台中市烏日區三榮路○段○號"),
        ("祈求事項", "祈求闔家平安、元辰光彩、事業鴻圖大展、財源廣進")
    ]
    fy = 165
    for fk, fv in form_fields:
        draw.text((65, fy), fk, fill=(235, 205, 130), font=get_font(FONT_HEITI, 15))
        draw.rectangle([65, fy + 24, 515, fy + 58], fill=(20, 4, 6), outline=(140, 100, 30), width=1)
        draw.text((80, fy + 33), fv, fill=(245, 235, 225), font=get_font(FONT_HEITI, 14))
        fy += 64

    # Submit button
    draw.rectangle([150, 580, 430, 615], fill=gold)
    draw.text((290, 597), "虔誠送出登記 ➔", fill=(40, 5, 8), font=get_font(FONT_HEITI, 16), anchor="mm")

    # Right: Resulting Certificate (疏文憑證)
    draw.rectangle([580, 95, 1160, 630], fill=(250, 245, 235), outline=gold, width=2)
    # Red border
    draw.rectangle([600, 115, 1140, 610], outline=(160, 20, 30), width=2)
    
    draw.text((870, 145), "台中烏日九元宮 祈福消災登記憑證", fill=(160, 20, 30), font=get_font(FONT_KAITI, 24), anchor="mm")
    draw.text((870, 180), "疏文憑證字號：JY-2026-10-0088", fill=(80, 80, 80), font=get_font(FONT_HEITI, 14), anchor="mm")
    draw.line([(620, 200), (1120, 200)], fill=(160, 20, 30), width=1)

    cert_lines = [
        "伏以",
        "焚香虔誠 恭對天顏 具疏奏陳",
        "奉 道祈安求賜福事",
        "今據 娑婆世界 南瞻部洲 中華民國台灣省",
        "台中市烏日區三榮路○段○號 吉宅居住",
        "信士 陳○明 誠心叩稟",
        "歲次甲子年八月初五日子時 建生",
        "敬投 台中烏日九元宮 列位尊神座前",
        "祈求：雷尊庇佑、元辰光彩、災厄冰消、闔府迎祥",
        "天運歲次丙午年吉月吉日 具疏"
    ]
    cy = 220
    for l in cert_lines:
        draw.text((640, cy), l, fill=(40, 20, 20), font=get_font(FONT_KAITI, 18))
        cy += 28

    # Temple Red Seal (Stamp)
    stamp_x, stamp_y = 1000, 480
    draw.rectangle([stamp_x, stamp_y, stamp_x + 100, stamp_y + 100], outline=(200, 20, 30), width=3)
    draw.rectangle([stamp_x + 5, stamp_y + 5, stamp_x + 95, stamp_y + 95], outline=(200, 20, 30), width=1)
    draw.text((stamp_x + 50, stamp_y + 35), "台中烏日", fill=(200, 20, 30), font=get_font(FONT_KAITI, 18), anchor="mm")
    draw.text((stamp_x + 50, stamp_y + 65), "九元宮印", fill=(200, 20, 30), font=get_font(FONT_KAITI, 18), anchor="mm")

    p = os.path.join(OUT_DIR, 'doc_img_form_cert.png')
    im.save(p)
    print("Saved:", p)

# -------------------------------------------------------------
# 5. Suno AI 創作與影音管線 (doc_img_suno.png)
# -------------------------------------------------------------
def make_suno_figure():
    w, h = 1200, 680
    im = Image.new('RGB', (w, h), (18, 12, 35))
    draw = ImageDraw.Draw(im)

    neon_gold = (245, 200, 75)
    neon_purple = (180, 110, 255)
    draw.rectangle([15, 15, w - 15, h - 15], outline=neon_gold, width=2)

    draw.text((w // 2, 50), "【課堂工具應用】Suno AI 人工智慧音樂創作與影音渲染管線", fill=neon_gold, font=get_font(FONT_KAITI, 32), anchor="mm")

    # Left: Suno AI Engine
    draw.rectangle([40, 95, 570, 630], fill=(28, 18, 52), outline=neon_purple, width=1)
    draw.text((305, 130), "Suno AI 音樂生成架構與設定", fill=neon_purple, font=get_font(FONT_KAITI, 24), anchor="mm")

    suno_details = [
        ("AI 生成模型", "Suno v3.5 / Chirp Audio Engine"),
        ("歌曲命名", "Incense Gong-Beat（香火鐘鼓慶典神曲）"),
        ("音樂風格 Prompt", "Taiwanese Temple Ceremony, Traditional Suona Solo,\nThunder Battle Drum, Bronze Bell Chime, Taoist Hymn,\nCinematic Epic, Powerful, Sacred 128 BPM"),
        ("專屬台語詩詞創作", "香煙繚繞九元宮，鐘聲響亮入雲中；\n金面威嚴鎮宮內，德澤萬里普大同。\n九天應元雷聲普化天尊，雷祖顯靈動乾坤；\n霹靂一聲邪氣散，萬民敬拜奉神靈！"),
        ("音訊輸出規格", "立體聲 WAV / 48000Hz 320kbps 高音質母帶"),
        ("應用整合場景", "活動花絮影片背景音樂（廈門謁祖進香、炮炸武財神）")
    ]
    sy = 170
    for sk, sv in suno_details:
        draw.text((60, sy), "• " + sk + "：", fill=neon_gold, font=get_font(FONT_KAITI, 17))
        draw.text((80, sy + 25), sv, fill=(240, 235, 255), font=get_font(FONT_HEITI, 14))
        sy += 72

    # Right: Video Pipeline Diagram
    draw.rectangle([610, 95, 1160, 630], fill=(25, 16, 46), outline=neon_gold, width=1)
    draw.text((885, 130), "Python + FFmpeg 自動化影音渲染管線", fill=neon_gold, font=get_font(FONT_KAITI, 24), anchor="mm")

    pipeline_steps = [
        ("步驟 1：素材預處理", "讀取 19 張高解析歷史照片與 20.MOV 神將實況影片\nLanczos 高品質無重影插值，建構古風絳紅金框底板。"),
        ("步驟 2：書法字幕排版", "精準對應四大祖廟（玉真法院、飛天四聖廟、\n白礁慈濟宮【國母獅/皇帝祭天台】、皇渡庵【皇帝井】）。"),
        ("步驟 3：Suno 音畫對齊", "載入 Suno AI 生成音訊，精確對齊鼓點與轉場，\n片頭 2.5 秒淡入，片尾 3 秒自然淡出。"),
        ("步驟 4：1080p 終端編碼", "透過 FFmpeg libx264 進行 YUV420p 二次編碼，\n輸出標準 YouTube 1080p 30fps Full HD MP4。")
    ]
    py = 175
    for pk, pv in pipeline_steps:
        draw.rectangle([635, py, 1135, py + 95], fill=(42, 25, 75), outline=(160, 130, 220), width=1)
        draw.text((650, py + 12), pk, fill=neon_gold, font=get_font(FONT_KAITI, 18))
        draw.text((650, py + 42), pv, fill=(240, 235, 250), font=get_font(FONT_HEITI, 14))
        py += 110

    p = os.path.join(OUT_DIR, 'doc_img_suno.png')
    im.save(p)
    print("Saved:", p)

# -------------------------------------------------------------
# 6. Google 試算表後端同步與資料流 (doc_img_cloud_sync.png)
# -------------------------------------------------------------
def make_cloud_sync_figure():
    w, h = 1200, 680
    im = Image.new('RGB', (w, h), (10, 25, 20))
    draw = ImageDraw.Draw(im)

    gold = (212, 175, 55)
    cyan = (80, 220, 180)
    draw.rectangle([15, 15, w - 15, h - 15], outline=gold, width=2)

    draw.text((w // 2, 50), "【課堂工具應用】Google Apps Script 串接 Google 試算表自動化管線", fill=gold, font=get_font(FONT_KAITI, 32), anchor="mm")

    # Flowchart: User -> Frontend -> GAS Webhook -> Google Sheets -> Temple Operations
    boxes = [
        ("信眾填表", "網頁線上填寫\n點燈/補財庫資料", 50, 120),
        ("即時憑證", "瀏覽器即時生成\n防偽加蓋印疏文", 270, 120),
        ("GAS Webhook", "Google Apps Script\n無伺服器 API 接收", 490, 120),
        ("Google 試算表", "雲端試算表自動寫入\n無人力抄寫遺漏", 710, 120),
        ("法會疏文唱名", "法師/道長直接列印\n登科開壇大醮", 930, 120),
    ]

    for title, desc, bx, by in boxes:
        draw.rectangle([bx, by, bx + 190, by + 120], fill=(18, 48, 38), outline=cyan, width=2)
        draw.text((bx + 95, by + 30), title, fill=gold, font=get_font(FONT_KAITI, 20), anchor="mm")
        draw.text((bx + 95, by + 75), desc, fill=(230, 245, 240), font=get_font(FONT_HEITI, 13), anchor="mm")
        if bx < 900:
            draw.text((bx + 205, by + 60), "➔", fill=cyan, font=get_font(FONT_HEITI, 24))

    # Bottom Table Mockup: Google Sheets View
    draw.rectangle([50, 280, 1150, 620], fill=(255, 255, 255), outline=gold, width=2)
    # Header bar (Google Sheets green)
    draw.rectangle([50, 280, 1150, 325], fill=(15, 157, 88))
    draw.text((70, 302), "Google Sheets 雲端即時同步資料庫（台中烏日九元宮 信眾點燈補庫登記錄）", fill=(255, 255, 255), font=get_font(FONT_HEITI, 16), anchor="lm")

    # Table columns
    cols = ["登記時間", "疏文編號", "信士姓名", "科儀類別", "生辰八字", "聯絡電話", "現居地址", "處理狀態"]
    col_w = [130, 130, 90, 110, 150, 120, 240, 100]
    
    # Table header row
    rx = 50
    draw.rectangle([50, 325, 1150, 365], fill=(240, 243, 240))
    for c_name, cw in zip(cols, col_w):
        draw.rectangle([rx, 325, rx + cw, 365], outline=(200, 200, 200), width=1)
        draw.text((rx + cw // 2, 345), c_name, fill=(50, 50, 50), font=get_font(FONT_HEITI, 14, bold=True), anchor="mm")
        rx += cw

    # Sample rows
    rows_data = [
        ("2026/10/08 14:20", "JY-2026-10-0088", "陳○明", "雷祖光明燈", "甲子年八月初五日子時", "0912-345-678", "台中市烏日區三榮路○段○號", "已完成開疏"),
        ("2026/10/08 15:45", "JY-2026-10-0089", "林○華", "四季補財庫", "乙丑年三月十二日午時", "0923-456-789", "台中市南屯區文心南路○號", "排入大醮名冊"),
        ("2026/10/09 09:10", "JY-2026-10-0090", "張○芬", "文昌智慧燈", "丙寅年六月十九日辰時", "0934-567-890", "台中市烏日區興祥街○號", "已點亮排座"),
        ("2026/10/09 11:32", "JY-2026-10-0091", "黃○祥", "安太歲保運", "戊辰年十一月初三日酉時", "0945-678-901", "彰化市中山路○段○號", "已完成開疏"),
        ("2026/10/09 16:15", "JY-2026-10-0092", "李○玲", "雷祖光明燈", "庚午年九月初十日戌時", "0956-789-012", "台中市西區公益路○號", "已完成開疏"),
    ]
    ry = 365
    for r_idx, r_data in enumerate(rows_data):
        rx = 50
        bg_col = (255, 255, 255) if r_idx % 2 == 0 else (248, 250, 248)
        draw.rectangle([50, ry, 1150, ry + 42], fill=bg_col)
        for val, cw in zip(r_data, col_w):
            draw.rectangle([rx, ry, rx + cw, ry + 42], outline=(220, 220, 220), width=1)
            draw.text((rx + cw // 2, ry + 21), val, fill=(30, 30, 30), font=get_font(FONT_HEITI, 13), anchor="mm")
            rx += cw
        ry += 42

    p = os.path.join(OUT_DIR, 'doc_img_cloud_sync.png')
    im.save(p)
    print("Saved:", p)

if __name__ == '__main__':
    make_hero_figure()
    make_highlights_figure()
    make_divination_figure()
    make_form_cert_figure()
    make_suno_figure()
    make_cloud_sync_figure()
