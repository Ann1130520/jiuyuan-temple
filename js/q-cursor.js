/**
 * 台中烏日九元宮 - 神明 Q 圖游標與靈光特效管理器
 * 
 * 功能說明：
 * 1. 打開網頁時會「隨機」挑選一尊神明 Q 圖取代滑鼠游標
 * 2. 滑鼠移動時帶有古典宮廷金光星塵拖尾特效
 * 3. 滑鼠點擊時擴散祥雲金光波紋
 * 4. 提供切換選單供信眾隨時挑選喜愛的守護神
 * 
 * 【換圖指南】
 * 若未來有自家的專屬神明 Q 版原畫（PNG/SVG/WebP），
 * 只要放入 images/q_gods/ 目錄，並在下方 GOD_CURSORS 陣列修改路徑即可！
 */

const GOD_CURSORS = [
    {
        id: 'leizu',
        name: '九天應元雷聲普化天尊 (主祀)',
        title: '雷部至尊．消災伏魔',
        icon: 'images/q_gods/q_leizu.svg'
    },
    {
        id: 'leigong',
        name: '雷公天君',
        title: '號令雷霆．巡視善惡',
        icon: 'images/q_gods/q_leigong.svg'
    },
    {
        id: 'dianmu',
        name: '電母娘娘',
        title: '寶鏡昭明．分辨是非',
        icon: 'images/q_gods/q_dianmu.svg'
    },
    {
        id: 'tiger',
        name: '招財金虎爺將軍',
        title: '虎嘯生風．招財納福',
        icon: 'images/q_gods/q_tiger.svg'
    },
    {
        id: 'prince',
        name: '中壇元帥三太子',
        title: '乾坤合道．護童保安',
        icon: 'images/q_gods/q_prince.svg'
    }
];

class GodCursorManager {
    constructor() {
        this.currentGod = null;
        this.cursorElement = null;
        this.canvas = null;
        this.ctx = null;
        this.particles = [];
        this.mouse = { x: -100, y: -100, prevX: -100, prevY: -100, speed: 0 };
        this.isActive = true;
    }

    init() {
        // 隨機挑選一尊神明
        const randomIndex = Math.floor(Math.random() * GOD_CURSORS.length);
        this.setGod(GOD_CURSORS[randomIndex]);

        this.createCursorDOM();
        this.createCanvas();
        this.bindEvents();
        this.animate();
        this.renderSelectorWidget();
    }

    setGod(god) {
        this.currentGod = god;
        
        // 替換系統原生游標（兼顧相容性與無縫備援）
        document.documentElement.style.cursor = `url('${god.icon}') 4 4, auto`;
        
        // 更新自訂跟隨游標小精靈
        if (this.cursorElement) {
            const img = this.cursorElement.querySelector('img');
            if (img) img.src = god.icon;
            const label = this.cursorElement.querySelector('.god-name-tag');
            if (label) label.textContent = god.name;
        }

        // 更新頂部顯示的守護神通知
        const widgetBadge = document.getElementById('current-god-name');
        if (widgetBadge) {
            widgetBadge.textContent = god.name;
        }
    }

    createCursorDOM() {
        // 建立浮動神明 Q 圖小跟隨精靈
        this.cursorElement = document.createElement('div');
        this.cursorElement.className = 'custom-god-cursor';
        this.cursorElement.innerHTML = `
            <img src="${this.currentGod.icon}" alt="${this.currentGod.name}" draggable="false" />
            <div class="god-name-tag">${this.currentGod.name}</div>
        `;
        document.body.appendChild(this.cursorElement);
    }

    createCanvas() {
        // 金色星塵與祥雲粒子軌跡 Canvas
        this.canvas = document.createElement('canvas');
        this.canvas.className = 'god-cursor-canvas';
        this.ctx = this.canvas.getContext('2d');
        document.body.appendChild(this.canvas);
        this.resizeCanvas();
    }

    resizeCanvas() {
        if (!this.canvas) return;
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    bindEvents() {
        window.addEventListener('resize', () => this.resizeCanvas());

        window.addEventListener('mousemove', (e) => {
            const dx = e.clientX - this.mouse.x;
            const dy = e.clientY - this.mouse.y;
            this.mouse.speed = Math.sqrt(dx * dx + dy * dy);
            this.mouse.prevX = this.mouse.x;
            this.mouse.prevY = this.mouse.y;
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;

            // 游標 DOM 定位更新 (微延遲彈性動態)
            if (this.cursorElement) {
                this.cursorElement.style.transform = `translate3d(${e.clientX + 14}px, ${e.clientY + 14}px, 0)`;
            }

            // 移動時生成微金光星塵粒子
            if (this.mouse.speed > 2) {
                const count = Math.min(3, Math.floor(this.mouse.speed / 10) + 1);
                for (let i = 0; i < count; i++) {
                    this.particles.push({
                        x: e.clientX + (Math.random() - 0.5) * 12,
                        y: e.clientY + (Math.random() - 0.5) * 12,
                        vx: (Math.random() - 0.5) * 1.5,
                        vy: (Math.random() - 0.5) * 1.5 + 0.5,
                        size: Math.random() * 3 + 1.5,
                        alpha: 0.85,
                        color: Math.random() > 0.4 ? '#FFD700' : '#FFF2A8',
                        life: 1
                    });
                }
            }
        });

        // 點擊滑鼠時生成金光祥雲衝擊波
        window.addEventListener('click', (e) => {
            this.createClickRipple(e.clientX, e.clientY);
        });

        // 離開視窗時隱藏
        document.addEventListener('mouseleave', () => {
            if (this.cursorElement) this.cursorElement.style.opacity = '0';
        });
        document.addEventListener('mouseenter', () => {
            if (this.cursorElement) this.cursorElement.style.opacity = '1';
        });
    }

    createClickRipple(x, y) {
        // 點擊產生 12 顆四散金光與外擴光環
        for (let i = 0; i < 12; i++) {
            const angle = (Math.PI * 2 / 12) * i;
            const speed = Math.random() * 3 + 2;
            this.particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                size: Math.random() * 4 + 2,
                alpha: 1,
                color: '#FFDF00',
                isSpark: true,
                life: 1
            });
        }

        // 擴散光環
        this.particles.push({
            x: x,
            y: y,
            radius: 5,
            maxRadius: 40,
            alpha: 0.8,
            isRing: true,
            color: '#E5C158',
            life: 1
        });
    }

    animate() {
        if (!this.ctx) return;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];

            if (p.isRing) {
                // 環狀擴散
                p.radius += 2.5;
                p.alpha -= 0.04;
                if (p.alpha <= 0 || p.radius >= p.maxRadius) {
                    this.particles.splice(i, 1);
                    continue;
                }
                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                this.ctx.strokeStyle = `rgba(229, 193, 88, ${p.alpha})`;
                this.ctx.lineWidth = 2;
                this.ctx.stroke();
            } else {
                // 粒子運動
                p.x += p.vx;
                p.y += p.vy;
                p.alpha -= 0.025;
                p.size = Math.max(0.2, p.size * 0.96);

                if (p.alpha <= 0) {
                    this.particles.splice(i, 1);
                    continue;
                }

                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                this.ctx.fillStyle = p.color;
                this.ctx.globalAlpha = Math.max(0, p.alpha);
                this.ctx.fill();
                this.ctx.globalAlpha = 1;
            }
        }

        requestAnimationFrame(() => this.animate());
    }

    renderSelectorWidget() {
        // 在頁面右上方建立一個精巧的切換小掛飾
        const widget = document.createElement('div');
        widget.className = 'god-selector-widget';
        widget.innerHTML = `
            <div class="god-widget-inner" id="god-widget-trigger">
                <span class="widget-icon">⚡</span>
                <span class="widget-text">當前守護神游標：<strong id="current-god-name">${this.currentGod.name}</strong></span>
                <span class="widget-arrow">▼</span>
            </div>
            <div class="god-dropdown-menu" id="god-dropdown-menu">
                <div class="dropdown-header">選擇隨行守護神 (滑鼠游標)</div>
                <div class="god-list-items">
                    ${GOD_CURSORS.map(g => `
                        <div class="god-item-option ${g.id === this.currentGod.id ? 'active' : ''}" data-god-id="${g.id}">
                            <img src="${g.icon}" alt="${g.name}" />
                            <div class="god-info">
                                <div class="name">${g.name}</div>
                                <div class="title">${g.title}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="god-dropdown-footer">
                    <button id="btn-random-god" class="btn-random-god">🎲 隨機變換神尊</button>
                </div>
            </div>
        `;
        document.body.appendChild(widget);

        // 綁定選單開關
        const trigger = widget.querySelector('#god-widget-trigger');
        const menu = widget.querySelector('#god-dropdown-menu');
        
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('show');
        });

        document.addEventListener('click', (e) => {
            if (!widget.contains(e.target)) {
                menu.classList.remove('show');
            }
        });

        // 點擊選擇神尊
        const options = widget.querySelectorAll('.god-item-option');
        options.forEach(opt => {
            opt.addEventListener('click', () => {
                const id = opt.getAttribute('data-god-id');
                const selected = GOD_CURSORS.find(g => g.id === id);
                if (selected) {
                    this.setGod(selected);
                    options.forEach(o => o.classList.remove('active'));
                    opt.classList.add('active');
                    menu.classList.remove('show');
                    // 提示
                    this.showToast(`已切換為：${selected.name} 護佑！`);
                }
            });
        });

        // 隨機切換按鈕
        const btnRandom = widget.querySelector('#btn-random-god');
        btnRandom.addEventListener('click', (e) => {
            e.stopPropagation();
            let nextIndex;
            do {
                nextIndex = Math.floor(Math.random() * GOD_CURSORS.length);
            } while (GOD_CURSORS[nextIndex].id === this.currentGod.id && GOD_CURSORS.length > 1);

            const nextGod = GOD_CURSORS[nextIndex];
            this.setGod(nextGod);
            options.forEach(o => {
                if (o.getAttribute('data-god-id') === nextGod.id) o.classList.add('active');
                else o.classList.remove('active');
            });
            menu.classList.remove('show');
            this.showToast(`靈光一閃！迎請【${nextGod.name}】隨行護佑！`);
        });
    }

    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'temple-toast';
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 50);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 2500);
    }
}

// 頁面載入完成時自動啟動
document.addEventListener('DOMContentLoaded', () => {
    window.godCursor = new GodCursorManager();
    window.godCursor.init();
});
