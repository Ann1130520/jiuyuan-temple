/**
 * 台中烏日九元宮 - 網站核心互動邏輯
 * 包含：音效引擎、最新消息、鸞文庫搜尋、線上擲杯、六十甲子籤解籤、科儀活動登記
 */

// -------------------------------------------------------------
// 1. 音效引擎 (使用 Web Audio API，無需外掛音訊檔，純原生合成高擬真廟宇音效)
// -------------------------------------------------------------
class TempleAudioEngine {
    constructor() {
        this.ctx = null;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    // 擲筊木頭碰撞聲 (叩喀！咚！)
    playBiaoSound() {
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;

        // 第一次清脆撞擊
        this.makeWoodTap(now, 260, 0.08);
        // 第二次沉實落地
        this.makeWoodTap(now + 0.12, 180, 0.14);
        // 第三次微滾動反彈
        this.makeWoodTap(now + 0.22, 140, 0.06);
    }

    makeWoodTap(time, freq, duration) {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, time);
        osc.frequency.exponentialRampToValueAtTime(60, time + duration);

        gain.gain.setValueAtTime(0.7, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + duration);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(time);
        osc.stop(time + duration);
    }

    // 抽籤筒搖竹籤聲
    playStickShake() {
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        for (let i = 0; i < 5; i++) {
            const tapTime = now + i * 0.08 + Math.random() * 0.03;
            const freq = 350 + Math.random() * 200;
            this.makeWoodTap(tapTime, freq, 0.05);
        }
    }

    // 吉祥金磬鐘聲
    playChime() {
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, now); // A5 高音清澈
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.5);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 2.6);
    }
}

const templeAudio = new TempleAudioEngine();

// -------------------------------------------------------------
// 2. DOM Ready 初始化
// -------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    initNav();
    initNews();
    initHighlights();
    initLuanDatabase();
    initBiaoSystem();
    initQianSystem();
    initRegistration();
});

// -------------------------------------------------------------
// 3. 導航列與平滑錨點
// -------------------------------------------------------------
function initNav() {
    const navLinks = document.querySelectorAll('.nav-links a');
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const navMenu = document.getElementById('nav-menu');

    if (mobileBtn && navMenu) {
        mobileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            navMenu.classList.toggle('mobile-open');
        });

        // 點擊任一導航連結後，自動關閉手機選單並平滑滾動
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('mobile-open');
            });
        });

        // 點擊網頁其他地方自動關閉手機選單
        document.addEventListener('click', (e) => {
            if (!navMenu.contains(e.target) && e.target !== mobileBtn) {
                navMenu.classList.remove('mobile-open');
            }
        });
    }

    // 捲動監聽更新當前選單 active 狀態
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        let scrollY = window.pageYOffset;
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 120;
            const sectionId = current.getAttribute('id');
            const link = document.querySelector(`.nav-links a[href*="${sectionId}"]`);
            if (link) {
                if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            }
        });
    });
}

// -------------------------------------------------------------
// 4. 最新消息篩選
// -------------------------------------------------------------
function initNews() {
    const tabBtns = document.querySelectorAll('.news-tab-btn');
    const cards = document.querySelectorAll('.news-card');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const category = btn.getAttribute('data-category');

            cards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// -------------------------------------------------------------
// 4.5 慶典活動花絮相簿與燈箱互動
// -------------------------------------------------------------
const HIGHLIGHTS_DATA = [
    {
        title: "捐贈普渡品關懷弱勢兒少獲頒家扶感謝狀",
        meta: "📅 115年9月5日 ｜ 📍 台灣兒童暨家庭扶助基金會",
        desc: "台中烏日九元宮熱心公益，積極關懷台中市弱勢兒少，中元普渡圓滿後捐贈普渡物資一批，嘉惠貧困家庭及兒童。榮獲家扶基金會致贈感謝狀肯定，實踐雷尊慈悲濟世之善心懿行：「懂得給予及憐恤人的，是最富足的。」",
        img: "images/highlights/hl_charity_certificate.png",
        category: "charity"
    },
    {
        title: "安營換符祈安實錄",
        meta: "📅 115年04月19日 ｜ 📍 烏日四方營盤",
        desc: "神劍定營驅邪煞，五方旗揚鎮乾坤。安設五營神兵神將，敕化平安神符，掃除草野陰霾，庇佑合境平安吉慶。本片精選安營換符精彩科儀紀實，長度一分鐘，歡迎善信同霑神恩。",
        img: "images/highlights/hl_anying_cover.jpg",
        video: "videos/anying_ritual.mp4",
        category: "anying"
    },
    {
        title: "炮炸武財神祈安盛典",
        meta: "📅 114年04月12日 ｜ 📍 九元宮廟埕壇前",
        desc: "恭迎武財神聖駕，萬炮齊鳴雷霆萬鈞，掃除四方穢煞，煙雲繚繞生祥瑞，祈求商賈亨通、財源廣進、合境安泰。影片搭配宮廟盛典鼓樂配樂，現場磅礡震撼！",
        img: "images/highlights/hl_wucai_cover.jpg",
        video: "videos/paozha_wucaishen.mp4",
        category: "wucai"
    }
];

let currentHlIndex = 0;

function initHighlights() {
    const tabBtns = document.querySelectorAll('.hl-tab-btn');
    const cards = document.querySelectorAll('.highlight-card');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.getAttribute('data-filter');

            cards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-category') === filter) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // 鍵盤左右鍵切換燈箱
    window.addEventListener('keydown', (e) => {
        const modal = document.getElementById('hl-lightbox-modal');
        if (modal && modal.classList.contains('active')) {
            if (e.key === 'Escape') closeHighlightModal();
            if (e.key === 'ArrowLeft') changeHighlightSlide(-1);
            if (e.key === 'ArrowRight') changeHighlightSlide(1);
        }
    });
}

function openHighlightModal(index) {
    currentHlIndex = index;
    const modal = document.getElementById('hl-lightbox-modal');
    updateHighlightContent();
    if (modal) modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // 防止背景滑動
}

function closeHighlightModal(e) {
    if (e && e.target && e.target.classList && !e.target.classList.contains('hl-lightbox-modal') && !e.target.classList.contains('hl-lightbox-close')) {
        return;
    }
    const modal = document.getElementById('hl-lightbox-modal');
    const video = document.getElementById('hl-lightbox-video');
    if (video) {
        video.pause();
    }
    if (modal) modal.classList.remove('active');
    document.body.style.overflow = '';
}

function changeHighlightSlide(dir, e) {
    if (e) e.stopPropagation();
    const video = document.getElementById('hl-lightbox-video');
    if (video) {
        video.pause();
    }
    currentHlIndex = (currentHlIndex + dir + HIGHLIGHTS_DATA.length) % HIGHLIGHTS_DATA.length;
    updateHighlightContent();
}

function updateHighlightContent() {
    const item = HIGHLIGHTS_DATA[currentHlIndex];
    if (!item) return;

    const img = document.getElementById('hl-lightbox-img');
    const video = document.getElementById('hl-lightbox-video');
    const title = document.getElementById('hl-lightbox-title');
    const meta = document.getElementById('hl-lightbox-meta');
    const desc = document.getElementById('hl-lightbox-desc');

    if (item.video) {
        if (img) img.style.display = 'none';
        if (video) {
            video.style.display = 'block';
            video.src = item.video;
            video.currentTime = 0;
            video.play().catch(function() {});
        }
    } else {
        if (video) {
            video.pause();
            video.style.display = 'none';
            video.src = '';
        }
        if (img) {
            img.style.display = 'block';
            img.src = item.img;
        }
    }

    if (title) title.textContent = item.title;
    if (meta) meta.textContent = item.meta;
    if (desc) desc.textContent = item.desc;
}

// -------------------------------------------------------------
// 5. 鸞文資料庫系統 (仿北港武德宮鸞文庫規格，支援多維度日期檢索)
// -------------------------------------------------------------
function initLuanDatabase() {
    const container = document.getElementById('luan-cards-container');
    const searchInput = document.getElementById('luan-search-input');
    const filterYear = document.getElementById('luan-filter-year');
    const filterMonth = document.getElementById('luan-filter-month');
    const filterExactDate = document.getElementById('luan-filter-exact-date');
    const filterTheme = document.getElementById('luan-filter-theme');
    const btnReset = document.getElementById('btn-reset-luan-filter');
    const countDisplay = document.getElementById('luan-results-count');

    if (!container || !window.LUAN_DATABASE) return;

    function renderLuanList(list) {
        container.innerHTML = '';
        if (countDisplay) {
            countDisplay.innerHTML = `共檢索出 <strong style="color:var(--bright-gold); font-size:1.1rem;">${list.length}</strong> 篇聖訓鸞文`;
        }

        if (list.length === 0) {
            container.innerHTML = `
                <div style="text-align:center; padding: 3.5rem 1rem; color: var(--text-muted); background: rgba(20,3,5,0.6); border-radius:8px; border:1px dashed var(--border-gold);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.8rem; color:var(--imperial-gold);">📜</div>
                    <p style="font-size: 1.25rem; color:var(--pale-gold); margin-bottom: 0.5rem; font-family:var(--font-kaiti);">查無符合條件之聖訓鸞文</p>
                    <p style="font-size: 0.95rem;">建議調整關鍵字、清除指定日期或選擇「全部年份 / 全部月份」重新檢索</p>
                    <button id="btn-empty-reset" class="btn-temple btn-temple-outline" style="margin-top:1.2rem; padding:6px 18px; font-size:0.9rem;">🔄 重置所有條件</button>
                </div>
            `;
            const emptyReset = document.getElementById('btn-empty-reset');
            if (emptyReset) emptyReset.addEventListener('click', resetFilters);
            return;
        }

        list.forEach(item => {
            const card = document.createElement('div');
            card.className = 'luan-card chinese-border';
            
            // 處理詩句中的標紅高亮（支援 <span class="luan-char-highlight"> 或直接帶 HTML 標籤）
            const versesHtml = item.verses.map(v => {
                // 如果詩句本身尚未帶 HTML，且有指定 highlight 模式時自動高亮首尾
                let rendered = v;
                if (!rendered.includes('class=')) {
                    if (item.highlightType === 'head') {
                        // 藏頭：首字標紅
                        const first = rendered.charAt(0);
                        const rest = rendered.slice(1);
                        rendered = `<span class="luan-char-highlight">${first}</span>${rest}`;
                    } else if (item.highlightType === 'head-tail') {
                        // 藏頭藏尾：首字與末字標紅
                        const first = rendered.charAt(0);
                        const middle = rendered.slice(1, -1);
                        const last = rendered.charAt(rendered.length - 1);
                        rendered = `<span class="luan-char-highlight">${first}</span>${middle}<span class="luan-char-highlight">${last}</span>`;
                    }
                }
                return `<div class="luan-verse-line">${rendered}</div>`;
            }).join('');
            
            const tagsHtml = item.tags.map(t => `<span class="luan-tag">#${t}</span>`).join('');

            card.innerHTML = `
                <div class="luan-card-top">
                    <div class="luan-card-title-group">
                        <h4>${item.title}</h4>
                        <div class="luan-card-date">
                            <div class="luan-date-row"><span>🗓️</span> <strong>${item.solarDate || item.date}</strong></div>
                            <div class="luan-date-row" style="color:var(--bright-gold); margin-top:2px;"><span>🏮</span> <strong>${item.lunarDate}</strong></div>
                        </div>
                    </div>
                    <span class="luan-god-badge">⚡ ${item.god}</span>
                </div>
                <div class="luan-verses-box">
                    ${versesHtml}
                </div>
                <div class="luan-explanation-box">
                    <strong style="color:var(--bright-gold);">【聖意白話淺釋】</strong><br/>
                    ${item.interpretation}
                </div>
                <div class="luan-card-footer">
                    <div class="luan-tags-group">${tagsHtml}</div>
                    <button class="btn-luan-copy" data-id="${item.id}">📋 複製本篇鸞文</button>
                </div>
            `;
            container.appendChild(card);
        });

        // 綁定複製按鈕
        container.querySelectorAll('.btn-luan-copy').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-id');
                const target = window.LUAN_DATABASE.find(x => x.id === id);
                if (target) {
                    // 複製時過濾掉 HTML 標籤，保留純文本
                    const plainVerses = target.verses.map(v => v.replace(/<[^>]+>/g, '')).join('\n');
                    const fullText = `【台中烏日九元宮 聖訓鸞文】\n篇名：${target.title}\n降筆神祇：${target.god}\n${target.solarDate || target.date}\n${target.lunarDate}\n\n【詩文】：\n${plainVerses}\n\n【聖意白話淺釋】：\n${target.interpretation}`;
                    navigator.clipboard.writeText(fullText).then(() => {
                        window.godCursor?.showToast('鸞文已成功複製至剪貼簿！');
                    });
                }
            });
        });
    }

    function filterData() {
        const query = (searchInput?.value || '').trim().toLowerCase();
        const year = filterYear?.value || 'all';
        const month = filterMonth?.value || 'all';
        const exactDate = filterExactDate?.value || '';
        const theme = filterTheme?.value || 'all';

        const filtered = window.LUAN_DATABASE.filter(item => {
            // 主題篩選
            const matchesTheme = (theme === 'all') || (item.theme === theme);

            // 年份篩選
            const matchesYear = (year === 'all') || (String(item.year) === String(year));

            // 月份篩選
            const matchesMonth = (month === 'all') || (String(item.month) === String(month));

            // 指定具體日期篩選 (YYYY-MM-DD)
            const matchesExactDate = !exactDate || (item.isoDate === exactDate);

            // 關鍵字檢索 (包含標題、詩文、神尊、淺釋、農曆、國曆日期字串)
            const fullContent = (
                item.title + 
                item.god + 
                item.verses.join('') + 
                item.interpretation + 
                item.tags.join('') + 
                item.date + 
                (item.lunarDate || '')
            ).toLowerCase();
            const matchesQuery = !query || fullContent.includes(query);

            return matchesTheme && matchesYear && matchesMonth && matchesExactDate && matchesQuery;
        });

        renderLuanList(filtered);
    }

    function resetFilters() {
        if (searchInput) searchInput.value = '';
        if (filterYear) filterYear.value = 'all';
        if (filterMonth) filterMonth.value = 'all';
        if (filterExactDate) filterExactDate.value = '';
        if (filterTheme) filterTheme.value = 'all';
        filterData();
        window.godCursor?.showToast('已重置所有檢索條件');
    }

    if (searchInput) searchInput.addEventListener('input', filterData);
    if (filterYear) filterYear.addEventListener('change', filterData);
    if (filterMonth) filterMonth.addEventListener('change', filterData);
    if (filterExactDate) filterExactDate.addEventListener('change', filterData);
    if (filterTheme) filterTheme.addEventListener('change', filterData);
    if (btnReset) btnReset.addEventListener('click', resetFilters);

    // 初次載入渲染
    renderLuanList(window.LUAN_DATABASE);
}

// -------------------------------------------------------------
// 6. 線上擲杯系統 (Moon Blocks)
// -------------------------------------------------------------
function initBiaoSystem() {
    const btnToss = document.getElementById('btn-toss-biao');
    const btnReset = document.getElementById('btn-reset-biao');
    const biaoScene = document.getElementById('biao-scene');
    const biaoLeft = document.getElementById('biao-left');
    const biaoRight = document.getElementById('biao-right');
    const biaoLeftLabel = document.getElementById('biao-left-label');
    const biaoRightLabel = document.getElementById('biao-right-label');
    const combinationDesc = document.getElementById('biao-combination-desc');
    const resultTitle = document.getElementById('biao-result-title');
    const resultDesc = document.getElementById('biao-result-desc');
    const dotRecords = document.querySelectorAll('.biao-dot-record');

    let shengCount = 0;
    let isTossing = false;

    if (!btnToss) return;

    btnToss.addEventListener('click', () => {
        if (isTossing) return;
        isTossing = true;
        btnToss.disabled = true;

        templeAudio.playBiaoSound();
        biaoScene.classList.add('biao-tossing');
        if (combinationDesc) combinationDesc.textContent = "筊杯凌空旋轉中...";
        resultTitle.textContent = "擲筊請示中...";
        resultTitle.className = "result-badge-text";
        resultDesc.textContent = "九天應元雷聲普化天尊 鑑察所求中...";

        setTimeout(() => {
            biaoScene.classList.remove('biao-tossing');

            // 隨機擲筊 (flat: 陽面/平面朝上, round: 陰面/圓凸面朝上)
            const leftState = Math.random() < 0.5 ? 'flat' : 'round';
            const rightState = Math.random() < 0.5 ? 'flat' : 'round';

            // 更新杯形 SVG
            biaoLeft.innerHTML = `<img src="images/biao_${leftState}.svg" alt="筊杯" />`;
            biaoRight.innerHTML = `<img src="images/biao_${rightState}.svg" alt="筊杯" />`;

            // 微隨機傾斜角度
            const degL = Math.floor(Math.random() * 30 - 15);
            const degR = Math.floor(Math.random() * 30 - 15);
            biaoLeft.style.transform = `rotate(${degL}deg)`;
            biaoRight.style.transform = `rotate(${degR}deg) scaleX(-1)`;

            // 更新各筊杯獨立標籤
            const leftText = leftState === 'flat' ? '陽面 (平)' : '陰面 (凸)';
            const rightText = rightState === 'flat' ? '陽面 (平)' : '陰面 (凸)';

            if (biaoLeftLabel) {
                biaoLeftLabel.textContent = `左筊：${leftText}`;
                biaoLeftLabel.className = `biao-state-pill ${leftState}`;
            }
            if (biaoRightLabel) {
                biaoRightLabel.textContent = `右筊：${rightText}`;
                biaoRightLabel.className = `biao-state-pill ${rightState}`;
            }

            // 判斷三種杯型結果
            if ((leftState === 'flat' && rightState === 'round') || (leftState === 'round' && rightState === 'flat')) {
                // 【聖杯】：一陽一陰（一平一凸）
                shengCount++;
                templeAudio.playChime();
                if (combinationDesc) combinationDesc.innerHTML = `<span style="color:#2ECC71; font-weight:bold;">【一陽一陰 ➔ 一平一凸】</span>`;
                resultTitle.textContent = `🟢【聖 杯】(神明允准) - 已累計 ${shengCount} 聖杯`;
                resultTitle.className = "result-badge-text sheng";
                resultDesc.textContent = "天尊開恩允准！所求吉利順遂，神明默祐扶持，請依正道行之。";
                
                // 更新連續進度球
                if (shengCount <= 3) {
                    dotRecords[shengCount - 1]?.classList.add('active');
                }
                if (shengCount === 3) {
                    resultDesc.textContent = "🎉 連續擲得【三聖杯】！雷祖隆恩大喜，科儀大吉圓滿！";
                    window.godCursor?.showToast("恭喜！連續擲得三聖杯！大吉大利！");
                }
            } else if (leftState === 'flat' && rightState === 'flat') {
                // 【笑杯】：兩陽朝上（兩平朝上）
                shengCount = 0;
                resetDots();
                if (combinationDesc) combinationDesc.innerHTML = `<span style="color:#F1C40F; font-weight:bold;">【雙陽朝上 ➔ 兩平朝上】</span>`;
                resultTitle.textContent = "🟡【笑 杯】(神明微笑或事情未定)";
                resultTitle.className = "result-badge-text xiao";
                resultDesc.textContent = "天尊笑而不答。象徵所稟事項未夠具體、機緣未至，或心中已明知何為，請凝神沉澱後再求。";
            } else {
                // 【陰杯】：兩陰朝上（兩凸朝上）
                shengCount = 0;
                resetDots();
                if (combinationDesc) combinationDesc.innerHTML = `<span style="color:#E74C3C; font-weight:bold;">【雙陰朝上 ➔ 兩凸朝上】</span>`;
                resultTitle.textContent = "🔴【陰 杯】(不允或需再思量)";
                resultTitle.className = "result-badge-text yin";
                resultDesc.textContent = "天尊示警不可。當前時機尚不適宜，或方向有誤，切莫逞強躁進，宜反省退守。";
            }

            isTossing = false;
            btnToss.disabled = false;
        }, 1100);
    });

    btnReset?.addEventListener('click', () => {
        shengCount = 0;
        resetDots();
        if (combinationDesc) combinationDesc.textContent = "【初始示範杯型：一陰一陽】";
        resultTitle.textContent = "請誠心默念後按下【請示擲筊】";
        resultTitle.className = "result-badge-text";
        resultDesc.textContent = "誠心稟明：姓名、農曆生辰、現居地址與所求事宜";
    });

    function resetDots() {
        dotRecords.forEach(d => d.classList.remove('active'));
    }
}

// -------------------------------------------------------------
// 7. 線上求籤解籤系統 (全套六十甲子籤)
// -------------------------------------------------------------
function initQianSystem() {
    let currentDrawnQian = null;
    let askingTopic = "";

    const stage1 = document.getElementById('qian-stage-1');
    const stage2 = document.getElementById('qian-stage-2');
    const stage3 = document.getElementById('qian-stage-3');
    const stage4 = document.getElementById('qian-stage-4');

    const ind1 = document.getElementById('ind-step-1');
    const ind2 = document.getElementById('ind-step-2');
    const ind3 = document.getElementById('ind-step-3');
    const ind4 = document.getElementById('ind-step-4');

    function goToStage(num) {
        [stage1, stage2, stage3, stage4].forEach(s => s?.classList.remove('active'));
        [ind1, ind2, ind3, ind4].forEach(i => i?.classList.remove('active'));

        if (num === 1) { stage1?.classList.add('active'); ind1?.classList.add('active'); }
        if (num === 2) { stage2?.classList.add('active'); ind2?.classList.add('active'); }
        if (num === 3) { stage3?.classList.add('active'); ind3?.classList.add('active'); }
        if (num === 4) { stage4?.classList.add('active'); ind4?.classList.add('active'); }
    }

    // Step 1: 稟報所求事項
    const btnStartDraw = document.getElementById('btn-start-draw');
    btnStartDraw?.addEventListener('click', () => {
        const name = document.getElementById('qian-user-name')?.value.trim();
        askingTopic = document.getElementById('qian-user-topic')?.value || '綜合指引';

        if (!name) {
            alert('請填寫信士姓名，以稟報神明知悉。');
            return;
        }

        document.getElementById('qian-display-user').textContent = name;
        document.getElementById('qian-display-topic').textContent = askingTopic;
        goToStage(2);
    });

    // Step 2: 抽籤筒
    const cylinderBox = document.getElementById('qian-cylinder-box');
    const stickPop = document.getElementById('qian-stick-pop');
    let isDrawing = false;

    cylinderBox?.addEventListener('click', () => {
        if (isDrawing) return;
        isDrawing = true;

        templeAudio.playStickShake();
        cylinderBox.classList.add('shaking');

        setTimeout(() => {
            cylinderBox.classList.remove('shaking');
            
            // 隨機自 36 籤庫中抽取一首
            const randomIndex = Math.floor(Math.random() * window.QIAN_DATABASE.length);
            currentDrawnQian = window.QIAN_DATABASE[randomIndex];

            // 籤枝浮起
            stickPop.textContent = `第${currentDrawnQian.id}籤 ${currentDrawnQian.name}`;
            stickPop.style.transform = 'translateY(-30px)';

            setTimeout(() => {
                // 進入第 3 階段：擲筊請示
                document.getElementById('drawn-qian-badge').textContent = `第 ${currentDrawnQian.id} 籤【${currentDrawnQian.name}】`;
                goToStage(3);
                isDrawing = false;
                stickPop.style.transform = 'translateY(0)';
            }, 900);
        }, 1200);
    });

    // Step 3: 請示擲筊確認
    const btnConfirmBiao = document.getElementById('btn-confirm-biao');
    const qianBiaoLeft = document.getElementById('qian-biao-left');
    const qianBiaoRight = document.getElementById('qian-biao-right');
    const qianBiaoLeftLabel = document.getElementById('qian-biao-left-label');
    const qianBiaoRightLabel = document.getElementById('qian-biao-right-label');
    const qianBiaoResult = document.getElementById('qian-biao-result');

    btnConfirmBiao?.addEventListener('click', () => {
        btnConfirmBiao.disabled = true;
        templeAudio.playBiaoSound();
        qianBiaoResult.textContent = "擲筊請示雷祖恩准中...";

        setTimeout(() => {
            // 擲筊邏輯：為提升線上參拜流暢度，聖杯機率設定約 65%
            const isSheng = Math.random() < 0.65;
            
            if (isSheng) {
                // 聖杯：一平一凸
                qianBiaoLeft.innerHTML = `<img src="images/biao_round.svg" alt="凸" />`;
                qianBiaoRight.innerHTML = `<img src="images/biao_flat.svg" alt="平" style="transform: scaleX(-1);" />`;
                if (qianBiaoLeftLabel) { qianBiaoLeftLabel.textContent = "左：陰面(凸)"; qianBiaoLeftLabel.className = "biao-state-pill round"; }
                if (qianBiaoRightLabel) { qianBiaoRightLabel.textContent = "右：陽面(平)"; qianBiaoRightLabel.className = "biao-state-pill flat"; }

                templeAudio.playChime();
                qianBiaoResult.innerHTML = "<span style='color:#2ECC71;'>【🟢 一平一凸 ➔ 聖杯！】天尊開恩准允，此籤確為賜示！即刻解籤！</span>";

                setTimeout(() => {
                    renderQianResult(currentDrawnQian);
                    goToStage(4);
                    btnConfirmBiao.disabled = false;
                }, 1200);
            } else {
                // 笑杯或陰杯，需重抽
                const isXiao = Math.random() < 0.5;
                if (isXiao) {
                    qianBiaoLeft.innerHTML = `<img src="images/biao_flat.svg" alt="平" />`;
                    qianBiaoRight.innerHTML = `<img src="images/biao_flat.svg" alt="平" style="transform: scaleX(-1);" />`;
                    if (qianBiaoLeftLabel) { qianBiaoLeftLabel.textContent = "左：陽面(平)"; qianBiaoLeftLabel.className = "biao-state-pill flat"; }
                    if (qianBiaoRightLabel) { qianBiaoRightLabel.textContent = "右：陽面(平)"; qianBiaoRightLabel.className = "biao-state-pill flat"; }
                    qianBiaoResult.innerHTML = "<span style='color:#F1C40F;'>【🟡 雙平朝上 ➔ 笑杯】天尊笑而不答，此籤非所賜之籤，請重新搖筒抽籤。</span>";
                } else {
                    qianBiaoLeft.innerHTML = `<img src="images/biao_round.svg" alt="凸" />`;
                    qianBiaoRight.innerHTML = `<img src="images/biao_round.svg" alt="凸" style="transform: scaleX(-1);" />`;
                    if (qianBiaoLeftLabel) { qianBiaoLeftLabel.textContent = "左：陰面(凸)"; qianBiaoLeftLabel.className = "biao-state-pill round"; }
                    if (qianBiaoRightLabel) { qianBiaoRightLabel.textContent = "右：陰面(凸)"; qianBiaoRightLabel.className = "biao-state-pill round"; }
                    qianBiaoResult.innerHTML = "<span style='color:#E74C3C;'>【🔴 雙凸朝上 ➔ 陰杯】天尊示警不可，此籤非所賜之籤，請重新搖筒抽籤。</span>";
                }

                setTimeout(() => {
                    goToStage(2);
                    btnConfirmBiao.disabled = false;
                }, 1800);
            }
        }, 1000);
    });

    // Step 4: 渲染籤詩結果
    function renderQianResult(qian) {
        document.getElementById('res-qian-number').textContent = `九元宮三十六天罡靈籤 第 ${qian.id} 首 【${qian.name}】`;
        document.getElementById('res-qian-gua').textContent = `神尊冠首：${qian.acrostic}`;
        document.getElementById('res-qian-auspicious').textContent = `籤運：${qian.auspicious}`;
        document.getElementById('res-qian-title').textContent = `籤別：${qian.numberTitle}`;

        const poemBox = document.getElementById('res-qian-poem-box');
        // 直排詩句，並將首字（藏頭神尊）標記純紅字
        poemBox.innerHTML = qian.poem.map(line => {
            const head = line.slice(0, 1);
            const rest = line.slice(1);
            return `<div class="qian-poem-line"><span class="luan-char-highlight" style="color: #E74C3C; font-weight: bold;">${head}</span>${rest}</div>`;
        }).join('');

        const storyBox = document.getElementById('res-qian-story');
        if (storyBox) {
            storyBox.textContent = `本籤冠首藏頭為【${qian.acrostic}】，為雷部仙真開示之天罡靈應玉律。`;
        }

        const expBox = document.getElementById('res-qian-exp');
        if (expBox) {
            if (qian.summary) {
                expBox.innerHTML = `<span style="font-size: 1.05rem; font-weight: bold; color: #8B0000;">${qian.summary}</span><br/><span style="color: #666; font-size: 0.9rem; margin-top: 4px; display: inline-block;">此籤降示：世人行事當遵天道、順天時，秉持正念修福，神明自當護佑化解。</span>`;
            } else {
                expBox.textContent = `此籤為【${qian.auspicious}】，神明垂示：目前所問之事，當修心向善、廣行功德。遵循神聖指引，順應天心而為，諸事自能漸入佳境、逢凶化吉。`;
            }
        }

        // 動態渲染各項指引
        const detailsGrid = document.querySelector('.qian-details-grid');
        if (detailsGrid) {
            if (qian.details && qian.details.length > 0) {
                detailsGrid.style.display = 'grid';
                detailsGrid.innerHTML = qian.details.map(det => `
                    <div class="qian-detail-item">
                        <strong>【${det.label}】</strong>
                        <span>${det.value}</span>
                    </div>
                `).join('');
            } else if (qian.summary) {
                detailsGrid.style.display = 'block';
                detailsGrid.innerHTML = `
                    <div style="background: rgba(192, 57, 43, 0.06); border: 1px solid rgba(192, 57, 43, 0.25); border-radius: 6px; padding: 1.25rem; text-align: center; font-size: 1.15rem; color: #8B0000; font-weight: bold; line-height: 1.8;">
                        🙏 聖真開示：${qian.summary}
                    </div>
                `;
            }
        }
    }

    // 重新求籤按鈕
    document.getElementById('btn-redraw-qian')?.addEventListener('click', () => {
        goToStage(1);
    });

    // 複製籤詩
    document.getElementById('btn-copy-qian')?.addEventListener('click', () => {
        if (!currentDrawnQian) return;
        const detailsText = currentDrawnQian.details && currentDrawnQian.details.length > 0
            ? currentDrawnQian.details.map(d => `【${d.label}】${d.value}`).join('\n')
            : `【聖真開示】\n${currentDrawnQian.summary}`;
        const text = `【台中烏日九元宮 三十六天罡靈籤】\n第 ${currentDrawnQian.id} 籤【${currentDrawnQian.name}】 - ${currentDrawnQian.auspicious}\n冠首神尊：${currentDrawnQian.acrostic}\n籤別：${currentDrawnQian.numberTitle}\n\n詩曰：\n${currentDrawnQian.poem.join('\n')}\n\n${detailsText}`;
        navigator.clipboard.writeText(text).then(() => {
            window.godCursor?.showToast("籤詩已成功複製至剪貼簿！");
        });
    });

    // 列印籤詩
    document.getElementById('btn-print-qian')?.addEventListener('click', () => {
        window.print();
    });
}

// -------------------------------------------------------------
// 8. 各項科儀活動登記系統 (支援 Google 試算表雲端即時同步)
// -------------------------------------------------------------
// 【廟方 Google 試算表 API 接收網址設定】
// 請將您從 Google 試算表 Apps Script 部署取得的網址貼在此處：
const GOOGLE_SHEET_WEBAPP_URL = ""; 

function initRegistration() {
    const ceremonyOptions = document.querySelectorAll('.ceremony-option');
    const selectedField = document.getElementById('selected-ceremony-name');
    const regForm = document.getElementById('ceremony-reg-form');
    const modal = document.getElementById('certificate-modal');
    const closeModalBtn = document.getElementById('btn-close-certificate');

    ceremonyOptions.forEach(opt => {
        opt.addEventListener('click', () => {
            ceremonyOptions.forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');
            const name = opt.getAttribute('data-name');
            if (selectedField) selectedField.value = name;
        });
    });

    regForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const ceremony = selectedField.value;
        const name = document.getElementById('reg-name').value.trim();
        const gender = document.getElementById('reg-gender').value;
        const birth = document.getElementById('reg-birth').value.trim();
        const hour = document.getElementById('reg-hour').value;
        const phone = document.getElementById('reg-phone').value.trim();
        const address = document.getElementById('reg-address').value.trim();
        const wish = document.getElementById('reg-wish').value.trim() || '祈求闔家平安、風調雨順、萬事如意';

        if (!ceremony) {
            alert('請選擇您要登記的科儀項目');
            return;
        }

        // 生成祈福編號
        const randomCode = 'JY-' + new Date().getFullYear() + '-' + Math.floor(100000 + Math.random() * 900000);
        const submitDate = new Date().toLocaleString('zh-TW');

        const submitBtn = regForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn ? submitBtn.innerHTML : '確認呈遞登記';
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '⚡ 稟報神尊並同步寫入雲端名冊中...';
        }

        // 如果已設定 Google 試算表 WebApp 網址，則透過背景非同步送出
        if (GOOGLE_SHEET_WEBAPP_URL && GOOGLE_SHEET_WEBAPP_URL.startsWith('http')) {
            try {
                const payload = {
                    code: randomCode,
                    time: submitDate,
                    ceremony: ceremony,
                    name: name,
                    gender: gender,
                    birth: birth,
                    hour: hour,
                    phone: phone,
                    address: address,
                    wish: wish
                };

                await fetch(GOOGLE_SHEET_WEBAPP_URL, {
                    method: 'POST',
                    mode: 'no-cors', // 允許跨網域寫入 Google Apps Script
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
            } catch (err) {
                console.warn('Google 試算表寫入略過或連線異常：', err);
            }
        }

        // 填入疏文憑證
        document.getElementById('cert-code').textContent = randomCode;
        document.getElementById('cert-ceremony').textContent = ceremony;
        document.getElementById('cert-name').textContent = `${name} (${gender})`;
        document.getElementById('cert-birth').textContent = `${birth} 【${hour}】`;
        document.getElementById('cert-address').textContent = address;
        document.getElementById('cert-wish').textContent = wish;
        document.getElementById('cert-date').textContent = submitDate;

        templeAudio.playChime();
        modal?.classList.add('active');
        
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }

        window.godCursor?.showToast('祈福登記成功！名冊已同步送達！');
    });

    closeModalBtn?.addEventListener('click', () => {
        modal?.classList.remove('active');
    });

    document.getElementById('btn-print-certificate')?.addEventListener('click', () => {
        window.print();
    });
}
