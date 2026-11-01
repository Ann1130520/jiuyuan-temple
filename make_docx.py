# -*- coding: utf-8 -*-
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def create_element(name):
    return OxmlElement(name)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = create_element('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = create_element('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = create_element(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_run_font(run, font_name="標楷體", size_pt=12, bold=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color_rgb)

def add_styled_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    if level == 1:
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        set_run_font(run, font_name="標楷體", size_pt=17, bold=True, color_rgb=(140, 20, 30))
    elif level == 2:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        set_run_font(run, font_name="標楷體", size_pt=14, bold=True, color_rgb=(109, 12, 21))
    elif level == 3:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        set_run_font(run, font_name="標楷體", size_pt=12.5, bold=True, color_rgb=(180, 40, 40))
    return p

def add_body_paragraph(doc, text, bold_prefix="", indent=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.25
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.28)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        set_run_font(r_pre, font_name="標楷體", size_pt=11.5, bold=True, color_rgb=(66, 6, 11))
    
    r_body = p.add_run(text)
    set_run_font(r_body, font_name="標楷體", size_pt=11.5, bold=False, color_rgb=(40, 40, 40))
    return p

def add_image_figure(doc, img_path, caption):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.0))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption)
        set_run_font(r_cap, font_name="標楷體", size_pt=10, bold=True, color_rgb=(100, 100, 100))

def main():
    doc = docx.Document()

    # 頁面邊界設定
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # 封面 / 頂部大標題
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(15)
    title_p.paragraph_format.space_after = Pt(4)
    run_t1 = title_p.add_run("台中烏日九元宮")
    set_run_font(run_t1, font_name="標楷體", size_pt=26, bold=True, color_rgb=(140, 20, 30))

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(15)
    run_t2 = sub_p.add_run("官方數位化資訊服務平台建置計畫書暨期中專案報告")
    set_run_font(run_t2, font_name="標楷體", size_pt=19, bold=True, color_rgb=(180, 130, 20))

    # 企劃基本資料表
    info_table = doc.add_table(rows=6, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_data = [
        ("專案名稱", "台中烏日九元宮官方數位化資訊服務平台建置暨線上信眾服務系統"),
        ("主祀神祇", "九天應元雷聲普化天尊（雷祖總司三十六雷府）"),
        ("發起/主管單位", "台中烏日九元宮 管理委員會"),
        ("正式發布網址", "https://ann1130520.github.io/jiuyuan-temple/"),
        ("核心技術應用", "Suno AI 音樂生成、Google Antigravity/Gemini、Google Apps Script / Sheets、GitHub Pages、OpenCV / FFmpeg"),
        ("報告製表日期", "中華民國一一五年（2026年）十月吉日")
    ]
    for row_idx, (k, v) in enumerate(table_data):
        row = info_table.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        
        cell_k.width = Inches(2.0)
        cell_v.width = Inches(4.5)
        
        set_cell_background(cell_k, "6D0C15")
        set_cell_background(cell_v, "FAF4EE")
        set_cell_margins(cell_k)
        set_cell_margins(cell_v)
        
        p_k = cell_k.paragraphs[0]
        p_k.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_k = p_k.add_run(k)
        set_run_font(r_k, font_name="標楷體", size_pt=11, bold=True, color_rgb=(255, 240, 200))
        
        p_v = cell_v.paragraphs[0]
        r_v = p_v.add_run(v)
        set_run_font(r_v, font_name="標楷體", size_pt=10.5, bold=False, color_rgb=(50, 50, 50))

    doc.add_page_break()

    # =========================================================
    # 壹、專案概念與宗旨
    # =========================================================
    add_styled_heading(doc, "壹、專案概念與宗旨", level=1)
    add_body_paragraph(doc, 
        "台中烏日九元宮座落於台中烏日高鐵特區與大里溪畔之靈秀福地，恭奉道教雷部最高主神「九天應元雷聲普化天尊」，總司天界三十六雷府，執掌天地正氣與生殺消長，護國佑民、消弭災愆。多年來香火鼎盛，為地方重要之道教文化信仰重心。", 
        indent=True)
    add_body_paragraph(doc, 
        "隨著現代社會生活步調加快與數位科技普及，傳統廟宇面臨信眾年輕化、跨地域參拜及線上即時訊息傳遞之時代需求。為貫徹雷祖「普化十方、廣種福田」之濟世慈悲，本宮特推動本項「官方數位化資訊服務平台建置計畫」，打破時間與空間限制，讓海內外善信能隨時隨地透過手機與電腦親近雷祖威儀、參拜祈福，弘揚正統道教文化。", 
        indent=True)

    add_styled_heading(doc, "1.1 專案核心概念", level=2)
    add_body_paragraph(doc,
        "本專案立足於「道法自然、科技弘道」之核心理念，將千百年歷史之正統道教科儀、神明典故、鸞堂聖訓與信眾祈福儀禮，藉由現代生成式 AI 與網頁雲端技術進行全方位數位化轉型。設計風格嚴格依循宮殿絳紅（#6D0C15）、宮廷正金（#D4AF37）與祥雲古樸框線，既具備莊嚴肅穆之宗教道場氛圍，又兼具現代網頁載入迅速、流暢互動、全平台自適應之操作體驗。")

    # =========================================================
    # 貳、解決的問題（痛點分析與創新方案）
    # =========================================================
    add_styled_heading(doc, "貳、解決的問題（痛點分析與解決方案）", level=1)
    add_body_paragraph(doc, "本專案針對傳統宮廟在資訊化、信眾服務與歷史典藏過程中所遭遇之四大關鍵痛點，提出具體而創新之數位解決方案：")

    issues = [
        ("一、傳統宮廟數位化不足與年輕世代信仰斷層：",
         "【痛點】：傳統宮廟多仰賴口耳相傳或布告欄張貼，年輕世代習慣以智慧型手機獲取資訊，缺乏正統而有質感的線上平台，導致文化傳承出現斷層。\n"
         "【解決方案】：建置高規格官方入口門戶，引進繁體楷書 WebFont、直覺漢堡導航選單與行動端 RWD 響應式排版，打造年輕世代亦樂於探索與親近的宮廟數位品牌。"),

        ("二、傳統紙本疏文謄寫繁複、易漏出錯與歸檔不易：",
         "【痛點】：信眾登記光明燈、文昌燈、安太歲與補財庫時，常因人工手寫字跡模糊、同名同姓混淆或疏文紙本遺失，造成法會唱名與登科排座困擾。\n"
         "【解決方案】：開發線上科儀表單系統，信眾填單後立即生成加蓋「台中烏日九元宮印」之防偽祈福疏文憑證；並透過 Google Apps Script 無伺服器 Webhook 技術，即時自動同步至廟方 Google 試算表（Google Sheets）資料庫，實現零紙本、零謄寫錯誤之自動化管線。"),

        ("三、歷史謁祖進香與出巡科儀影像散佚、缺乏高畫質影音典藏：",
         "【痛點】：宮廟歷年舉辦之重大科儀（如歲次丙午年赴閩南廈門謁祖進香：玉真法院、飛天四聖廟、白礁慈濟宮、皇渡庵四大祖廟巡禮；安營換符；炮炸武財神）之照片與影片往往零散於信眾手機，解析度參差且無配樂剪輯，難以永久典藏與宣化。\n"
         "【解決方案】：利用 Python、FFmpeg 與 OpenCV 自動化影音渲染管線，將 20 個高畫質歷史照片與現場實況影片逐一對齊書法字幕與歷史景點考證，並結合 Suno AI 創作之專屬宮廟戰鼓嗩吶配樂，輸出符合 YouTube 1080p 規格之專業紀錄片，並完整嵌入活動花絮相簿。"),

        ("四、信眾跨地域即時請旨與求籤解籤之儀軌體驗痛點：",
         "【痛點】：旅外遊子、出差信士或行動不便之長者，遇到人生疑難時無法親臨廟宇抽籤擲筊。\n"
         "【解決方案】：開發高度擬真之「線上擲杯（立體紅木筊杯）」與「九元宮三十六籤（三十六天罡靈籤）求籤解籤系統」，遵循【淨心稟報】➔【搖筒抽籤】➔【擲筊請旨（得聖杯方可領籤）】➔【開籤詳解】之四部古禮，並使用 Web Audio API 原生合成清脆木筊碰撞聲，提供身歷其境的宗教精神寄託。")
    ]
    for pfx, txt in issues:
        add_body_paragraph(doc, txt, bold_prefix=pfx)

    # =========================================================
    # 參、課堂上教授之工具與前瞻技術整合
    # =========================================================
    add_styled_heading(doc, "參、課堂上教授之工具與技術整合", level=1)
    add_body_paragraph(doc, "本專案全面整合課堂上所教授之 AI 人工智慧工具、雲端協作生態與多媒體自動化技術，具體落實於各系統模組中：")

    tools = [
        ("1. Suno AI 人工智慧音樂生成工具（歌曲專屬製作）：",
         "【工具角色】：音訊生成與主題配樂創作大師。\n"
         "【實務應用】：本專案特別指定運用 Suno AI 生成宮廟專屬主題神曲《Incense Gongbeat》（白礁慈濟保生大帝救世神曲）。歌詞以典雅台語深情刻劃：『慈心大道萬里真仙，普成聖顯現救世間…風雲變色驚濤海浪，先民李氏意志比石堅；白礁慈濟回頭看故鄉，思念雙親淚落黑水溝；五月初二白鶴穿雲飛，保生三帝顯赫救世間；絲線診脈奇蹟救國母，施方濟藥仁德顯四方…』，完美呼應廈門謁祖行程中之白礁慈濟宮與宋代國寶「國母獅」歷史傳奇。音樂自 0 秒起即以磅礡宏偉的大合唱與戰鼓合奏切入，由 Suno AI 生成高音質立體聲配樂，賦予影片無比莊嚴的神聖感染力。"),

        ("2. Google Antigravity / Gemini 生成式 AI 開發平台：",
         "【工具角色】：架構規劃、程式碼自動化生成與代理人協作。\n"
         "【實務應用】：利用多代理人模式（Multi-Agent System）進行網站全端架構設計、九元宮三十六天罡靈籤資料庫結構化解析（包含天魁、天罡、天機等三十六天罡神名、吉凶判定、神尊藏頭詩、白話詳解、貴人、求醫、求財、投資、求學、求子、求姻緣、求事業、求官、家運、運途、官司、外居、出遊、行車等十八項全方位指引），並自動撰寫 Python 自動化影音渲染管線，大幅提昇系統開發效率與穩定度。"),

        ("3. Google 雲端生態系（Google Docs, Google Sheets, Google Apps Script）：",
         "【工具角色】：無伺服器後台資料庫與文件整合。\n"
         "【實務應用】：運用課堂講授之 Google Apps Script（GAS）架構 Webhook API，信眾於前台送出點燈與補財庫祈福表單後，GAS 即時將資料格式化並回填寫入廟方 Google 試算表（Google Sheets）資料庫；此外，專案報告與計畫書均嚴格遵循 Google 文件規範進行排版，達成雲端協作無縫傳遞。"),

        ("4. GitHub & GitHub Pages 雲端託管服務：",
         "【工具角色】：版本控制、持續整合與全球伺服器託管。\n"
         "【實務應用】：專案代碼與資產全面納入 Git 版本控管，發布於 GitHub 儲存庫（Ann1130520/jiuyuan-temple），並藉由 GitHub Pages 提供自帶全球 SSL 安全憑證與 CDN 高速分發之無伺服器託管，實現 24 小時不中斷、全天候零主機租金運作。"),

        ("5. OpenCV & FFmpeg & Python Pillow 影音渲染引擎：",
         "【工具角色】：高畫質影音自動合成與視覺排版。\n"
         "【實務應用】：撰寫 Python 腳本調用 FFmpeg 與 Pillow，以 Lanczos 演算法進行 1920x1080 靜態底板預渲染與高解析插值，完全消除插值疊影；精確對齊四大祖廟（玉真法院、飛天四聖廟、白礁慈濟宮、皇渡庵）書法字幕與神將操令實況影片，產出標準 YouTube 1080p 30fps Full HD 影片。"),

        ("6. 現代原生前端架構（HTML5 / CSS3 / ES6+ JavaScript / Web Audio API）：",
         "【工具角色】：極速流暢的前端體驗與原生音效合成。\n"
         "【實務應用】：捨棄肥重第三方框架，採用原生 JavaScript 實現無依賴極速載入；行動端引入 Google Fonts「LXGW WenKai TC」繁體雲端楷體防止手機字型跑版；並運用 Web Audio API 原生物理演算法即時合成木質筊杯碰撞落地與金鐘磬音。"),

        ("7. YouTube 影音串流發布平台：",
         "【工具角色】：全球影音串流分發與文化推廣。\n"
         "【實務應用】：將製作完成之高畫質慶典影片（廈門謁祖進香、炮炸武財神）上傳發布至 YouTube 影音平台，提供全球信眾隨選點播，並整合至官網活動花絮燈箱中。")
    ]
    for pfx, txt in tools:
        add_body_paragraph(doc, txt, bold_prefix=pfx)

    # =========================================================
    # 肆、系統功能模組詳細規劃
    # =========================================================
    add_styled_heading(doc, "肆、系統功能模組詳細規劃", level=1)
    
    modules = [
        ("1. 廟宇歷史與道統沿革：", "詳載烏日九元宮立廟肇基歷程、福地人文歷史。詳介九天應元雷聲普化天尊聖紀典故，以及陪祀鄧辛張陶四天君與招財金虎爺將軍神職特性。"),
        ("2. 最新消息與慶典活動發布：", "分為「全部公告」、「慶典法會」、「廟務公告」、「慈善志業」四大分類標籤，支援無縫動態篩選。預載八月初五雷祖聖誕千秋大醮、天赦日補財庫等重要法會時程。"),
        ("3. 慶典活動花絮相簿（依時間最新至最舊排序）：", "以圖文與高畫質影片完整呈現：① 115.10.7-10.10 廈門謁祖進香祈安實錄（玉真法院、飛天四聖廟、白礁慈濟宮、皇渡庵）；② 115.09.05 中元普渡關懷弱勢兒少獲頒家扶感謝狀；③ 115.04.19 安營換符祈安實錄；④ 114.04.12 慶讚天官武財神聖誕千秋 炮炸武財神盛典。"),
        ("4. 參拜指南與科儀禮節：", "圖解「天公爐 ➔ 主殿雷祖 ➔ 配祀諸天君 ➔ 招財金虎爺」之完整參拜動線與奉香順序；彙整鮮花素果供品推薦清單、稟報生辰八字與祈願疏文要訣。"),
        ("5. 鸞文資料庫系統：", "支援「年份篩選（2026/2025）」、「月份篩選（1~12月）」與「精確日曆點選」多維度檢索，並支援關鍵字全文檢索與一鍵複製鸞文功能。"),
        ("6. 線上虔誠擲杯系統：", "全新立體紅木切面設計，呈現自然剖木（陽平）與半月圓脊（陰凸），免生硬字樣；採用 Web Audio API 純原生合成清脆落地碰撞聲與金磬清音，即時判定聖杯、笑杯、陰杯與連續三聖杯累計燈號。"),
        ("7. 九元宮三十六籤（三十六天罡靈籤）求籤解籤系統：", "嚴謹遵循【淨心稟報】➔【搖筒抽籤】➔【擲筊請旨（得聖杯方可領籤）】➔【開籤詳解】四部儀軌；包含三十六天罡神名、神尊藏頭詩五言絕句、吉凶判定、籤意淺釋與十八項人生行事指引，並支援列印存查。"),
        ("8. 線上科儀登記與 Google 試算表同步：", "提供雷祖光明燈、文昌智慧燈、太歲消災燈、四季補庫求財法會切換；填單後即時生成加蓋宮印之防偽祈福疏文憑證，並自動寫入廟方 Google 試算表。"),
        ("9. 交通指引與服務聯絡：", "詳列台中高鐵站、新烏日火車站、台中捷運高鐵站之轉乘與公車路線，結合高清晰定位點與一鍵 Google Maps 導航啟動。")
    ]
    for pfx, txt in modules:
        add_body_paragraph(doc, txt, bold_prefix=pfx)

    # =========================================================
    # 伍、介面截圖與系統展示（圖文並茂）
    # =========================================================
    doc.add_page_break()
    add_styled_heading(doc, "伍、系統介面截圖與功能展示", level=1)
    add_body_paragraph(doc, "以下收錄本系統各項核心模組之實際操作介面截圖、多媒體成果與後台資料流展示：")

    img_dir = r'c:\Users\user\Desktop\AI課\jiuyuan-temple\docs\images'

    # 圖 5.1 首頁形象
    add_image_figure(doc, 
        os.path.join(img_dir, 'doc_img_hero.png'), 
        "圖 5.1 台中烏日九元宮 官方數位服務平台首頁入口與核心導航介面")
    add_body_paragraph(doc, 
        "【介面說明】：首頁採用深宮絳紅與正金邊框設計，橫幅導航列支援單頁平滑滾動（Smooth Scroll）與漢堡選單；頂部主視覺彰顯九天應元雷聲普化天尊雷部道統，下方具備直覺之核心功能快速導覽卡片。",
        indent=True)

    # 圖 5.2 活動花絮
    add_image_figure(doc, 
        os.path.join(img_dir, 'doc_img_highlights.png'), 
        "圖 5.2 慶典活動花絮多媒體專區（由最新至最舊嚴謹排序，支援全螢幕影片燈箱）")
    add_body_paragraph(doc, 
        "【介面說明】：活動花絮由最新至最舊依序展示：① 115.10.7-10.10 廈門謁祖進香（巡禮玉真法院、飛天四聖廟、白礁慈濟宮【國母獅/皇帝祭天台】、皇渡庵【皇帝井/操令錄影】）；② 115.09.05 關懷弱勢兒少家扶感謝狀；③ 115.04.19 安營換符；④ 114.04.12 炮炸武財神。點擊卡片即可啟動專屬全螢幕播放器。",
        indent=True)

    # 圖 5.3 靈籤與擲杯
    add_image_figure(doc, 
        os.path.join(img_dir, 'doc_img_qian.png'), 
        "圖 5.3 九元宮三十六籤（三十六天罡靈籤）與立體紅木筊杯解籤系統介面（四部古禮與籤詩詳解）")
    add_body_paragraph(doc, 
        "【介面說明】：左側引導信眾依序完成【淨心稟報】➔【搖筒抽籤】➔【擲筊請旨】➔【開籤詳解】四部儀軌；右側為籤詩展示卡，詳列三十六天罡神名、玉皇大天尊等神尊藏頭詩五句、吉凶及貴人、求財、求學事業、健康、婚姻分項指引。",
        indent=True)

    # 圖 5.4 科儀表單與防偽疏文
    add_image_figure(doc, 
        os.path.join(img_dir, 'doc_img_form_cert.png'), 
        "圖 5.4 線上科儀登記祈福表單與加蓋「台中烏日九元宮印」防偽疏文憑證")
    add_body_paragraph(doc, 
        "【介面說明】：信眾於左側填妥點燈、補財庫資料後，系統即時於前端合成右側加蓋正式宮廟大印之祈福疏文憑證（具備唯一防偽編號），信眾可截圖保存或列印憑證。",
        indent=True)

    # 圖 5.5 Suno AI 音樂創作
    add_image_figure(doc, 
        os.path.join(img_dir, 'doc_img_suno.png'), 
        "圖 5.5 課堂工具應用：Suno AI 人工智慧音樂創作與 Python FFmpeg 自動化影音渲染管線")
    add_body_paragraph(doc, 
        "【介面說明】：展示以 Suno AI 創作專屬神曲《Incense Gong-Beat》之提示詞設定、台語詩詞歌詞與輸出規格；右側為 Python + FFmpeg 之四步驟自動化影音渲染流程，確保音畫精準對齊。",
        indent=True)

    # 圖 5.6 雲端試算表同步
    add_image_figure(doc, 
        os.path.join(img_dir, 'doc_img_cloud_sync.png'), 
        "圖 5.6 課堂工具應用：Google Apps Script 串接 Google 試算表（Google Sheets）後台資料庫架構")
    add_body_paragraph(doc, 
        "【介面說明】：展示信眾線上填表後，透過 Google Apps Script 無伺服器 API 即時回填寫入廟方專屬 Google 試算表資料庫之完整資料流，徹底取代傳統紙本手抄作業。",
        indent=True)

    # =========================================================
    # 陸、YouTube 影音串流發布規劃與元數據
    # =========================================================
    doc.add_page_break()
    add_styled_heading(doc, "陸、YouTube 影音串流發布規劃與元數據", level=1)
    add_body_paragraph(doc, "本專案所製作之兩支高畫質宣傳紀錄片已全面完成 YouTube 格式規格優化，以下為對應之發布元數據：")

    # Video 1
    add_styled_heading(doc, "6.1 影片一：歲次丙午年 廈門謁祖進香祈安實錄", level=2)
    v1_data = [
        ("影片檔案", "C:\\Users\\user\\Desktop\\AI課\\台中烏日九元宮_廈門謁祖進香實錄.mp4"),
        ("視訊規格", "1920x1080 (1080p Full HD) ｜ 30 fps ｜ 時長 83 秒 ｜ 檔案大小 18.55 MB"),
        ("配樂來源", "Suno AI 原創創作《Incense Gongbeat》（白礁慈濟保生大帝救世神曲，自 0 秒磅礡大合唱帶入）"),
        ("YouTube 標題", "【台中烏日九元宮】歲次丙午年 廈門謁祖進香祈安實錄 ｜ 巡禮四大祖廟：玉真法院・飛天四聖廟・白礁慈濟宮・皇渡庵"),
        ("章節時間軸 (Timestamp)", 
         "00:00 謁祖啟程與片頭介紹（《Incense Gongbeat》自 0 秒磅礡帶入）\n"
         "00:02 【玉真法院】福建廈門同安 飛天大聖祖廟、正殿神龕、主尊飛天大聖金身（善信敬披黃綾）、靈感虎爺叼菸\n"
         "00:17 【飛天四聖廟】閩南傳統燕尾亭閣、山門御匾「飛天四聖」、開基古佛巍坐法台\n"
         "00:26 【白礁慈濟宮】保生大帝祖宮、宋代國寶石雕「國母獅」、古代皇帝祭天的地方、飛天藻井\n"
         "00:50 【皇渡庵】宋代傳奇歷史聖蹟「皇帝井」、正殿飛天大聖金身爐前真火\n"
         "00:59 【皇渡庵廟埕】神將演法操令珍貴現場實況錄影（乩身操五方令旗）\n"
         "01:17 兩岸會香圓滿 祈願國泰民安 片尾吉慶"),
        ("建議標籤 (Tags)", "台中烏日九元宮, 九天應元雷聲普化天尊, 飛天大聖, 廈門謁祖, 玉真法院, 飛天四聖廟, 白礁慈濟宮, 國母獅, 古代皇帝祭天台, 皇渡庵, 皇帝井, 道教科儀, Suno AI")
    ]
    for vk, vv in v1_data:
        add_body_paragraph(doc, vv, bold_prefix="• " + vk + "：\n" if "\n" in vv else "• " + vk + "：")

    # Video 2
    add_styled_heading(doc, "6.2 影片二：歲次乙巳年 慶讚天官武財神聖誕 炮炸武財神盛典", level=2)
    v2_data = [
        ("影片檔案", "C:\\Users\\user\\Desktop\\AI課\\jiuyuan-temple\\videos\\paozha_wucaishen.mp4"),
        ("視訊規格", "1920x1080 (1080p Full HD) ｜ 60 fps ｜ 時長 34 秒 ｜ 檔案大小 8.87 MB"),
        ("配樂來源", "Suno AI 宮廟盛典磅礡戰鼓與嗩吶配樂"),
        ("YouTube 標題", "【台中烏日九元宮】歲次乙巳年 慶讚天官武財神聖誕千秋 炮炸武財神迎財納福盛典"),
        ("說明欄文字", "台中烏日九元宮歲次乙巳年慶祝天官武財神聖誕千秋，舉行震撼人心之「炮炸武財神」迎財祈安盛典。萬炮齊鳴如雷霆破空，洗滌四方穢氣，火光煙霞騰騰如祥瑞聚寶，護佑信眾商賈興旺、招財納福、利市亨通、闔家吉慶！"),
        ("建議標籤 (Tags)", "台中烏日九元宮, 天官武財神, 炮炸武財神, 武財神聖誕, 迎財納福, 烏日宮廟, 宗教文化, 傳統信仰, 補財庫")
    ]
    for vk, vv in v2_data:
        add_body_paragraph(doc, vv, bold_prefix="• " + vk + "：\n" if "\n" in vv else "• " + vk + "：")

    # =========================================================
    # 柒、預期效益與未來展望
    # =========================================================
    add_styled_heading(doc, "柒、預期效益與未來展望", level=1)
    benefits = [
        ("一、信仰傳播無遠弗屆：", "讓行動不便之長者、求學就業之異鄉遊子，皆能隨時經由手機線上向雷祖擲筊請益、求籤排難解惑。"),
        ("二、廟務管理高度自動化：", "信眾點燈、安太歲與補財庫名冊自動彙整於 Google 試算表，免除紙本抄寫遺漏與辨識錯誤，利於道長統整唱名法會疏文。"),
        ("三、珍貴宗教文史數位永久典藏：", "透過專業影音剪輯與 Suno AI 配樂，將廈門謁祖四大祖廟歷史行腳、安營換符與武財神科儀永久留存於雲端與 YouTube，代代相傳。"),
        ("四、永久免主機維護成本：", "採用 GitHub Pages 與 Google 雲端生態託管，自帶全球 SSL 綠色安全憑證與 CDN 高速分發，全天候零主機租金運作。")
    ]
    for pfx, txt in benefits:
        add_body_paragraph(doc, txt, bold_prefix=pfx)

    add_body_paragraph(doc,
        "本「台中烏日九元宮官方數位化資訊服務平台」現已全面建置完成並正式對外發布上線（https://ann1130520.github.io/jiuyuan-temple/）。本專案不僅完整結合了課堂上所傳授之 Suno AI 音樂創作、Google 生成式 AI、Google 試算表無伺服器整合與 GitHub Pages 託管技術，更成功打造了兼具古典信仰美學與現代前瞻科技之模範宮廟平台。未來將進一步整合 LINE 官方帳號推播，持續擴大雷祖文化弘道宣化之效益，祈願雷祖神威長存，福澤萬民。",
        indent=True)

    # 存檔至桌面與專案 docs 目錄
    out_desktop = r"c:\Users\user\Desktop\AI課\台中烏日九元宮_官方網站建置計畫書.docx"
    out_docs = r"c:\Users\user\Desktop\AI課\jiuyuan-temple\docs\台中烏日九元宮_官方網站建置計畫書.docx"
    doc.save(out_desktop)
    doc.save(out_docs)
    print("DOCX successfully generated at:")
    print("1.", out_desktop)
    print("2.", out_docs)

if __name__ == '__main__':
    main()
