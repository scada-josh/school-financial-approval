Dashboard Design Guide

คู่มือการออกแบบ Dashboard แบบ Bento Box Layout

ใช้เป็นแนวทางสร้าง Dashboard สำหรับข้อมูลและธุรกิจประเภทอื่นๆ ตาม Template นี้
 
 
1. Color System (โทนสี)

Primary Theme Colors
--bg-dark: #0f1419;          /* พื้นหลังหลัก - สีเทาเข้มมืด */
 
--bg-card: #1a1f2e;          /* พื้นหลัง Card */
 
--bg-card-hover: #242b3d;    /* พื้นหลัง Card เมื่อ hover */
 
--accent-primary: #c9a96e;   /* สีทองหลัก - ใช้ highlight */
 
--accent-secondary: #8b7355;  /* สีทองเข้ม */
Text Colors
--text-primary: #ffffff;      /* สีข้อความหลัก */
 
--text-secondary: #94a3b8;   /* สีข้อความรอง */
 
--text-muted: #64748b;       /* สีข้อความจาง */
Semantic Colors
--success: #10b981;           /* เขียว - ค่าบวก/เพิ่มขึ้น */
 
--warning: #f59e0b;          /* เหลือง - เตือน/ระวัง */
 
--danger: #ef4444;           /* แดง - ค่าลบ/ลดลง */
 
--info: #3b82f6;             /* น้ำเงิน - ข้อมูลทั่วไป */
Chart Category Colors
--coffee: #c9a96e;           /* สีกาแฟ - category หลัก */
 
--tea: #a3e635;              /* สีเขียวอ่อน */
 
--bakery: #fbbf24;           /* สีเหลืองทอง */
 
--soda: #06b6d4;             /* สีฟ้า */
Dark Theme Card Gradient (Revenue Highlight)
background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
 
/* ใช้สำหรับ Card เด่น - หลีกเลี่ยงใน Card ปกติ */
 
 
2. Layout System (ระบบ Layout)

Grid System
.bento-grid {
 
   display: grid;
 
   grid-template-columns: repeat(12, 1fr);  /* 12-column grid */
 
   gap: 12px;                              /* ช่องว่างระหว่าง card */
 
}
Spanning Classes (การกำหนดขนาด Card)
.span-2  { grid-column: span 2; }   /* 2/12 = 16.67% */
 
.span-3  { grid-column: span 3; }   /* 3/12 = 25% */
 
.span-4  { grid-column: span 4; }   /* 4/12 = 33.33% */
 
.span-5  { grid-column: span 5; }   /* 5/12 = 41.67% */
 
.span-6  { grid-column: span 6; }   /* 6/12 = 50% */
 
.span-7  { grid-column: span 7; }   /* 7/12 = 58.33% */
 
.span-8  { grid-column: span 8; }   /* 8/12 = 66.67% */
 
.span-12 { grid-column: span 12; }  /* 12/12 = 100% */
Common Layout Patterns
Pattern 1: Summary Bar (12 columns)
 
┌──────────────────────────────────────────────────────────────┐
 
│  [icon] Label    Value   [icon] Label    Value   [icon] ...  │
 
└──────────────────────────────────────────────────────────────┘
 
- ใช้ span-12 wrapper ภายนอก
- ภายในใช้ flexbox หรือ grid
- ทั่วไปใส่ 4-6 items
 
Pattern 2: KPI Cards Row (12 columns)
 
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
 
│ span-4  │ span-2  │ span-2  │ span-2  │ span-2  │         │
 
│  KPI 1  │  KPI 2  │  KPI 3  │  KPI 4  │  KPI 5  │         │
 
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
 
- การ combination ที่นิยม: 4+2+2+2+2 = 12
- หรือ: 3+3+3+3 = 12
- หรือ: 6+6 = 12
 
Pattern 3: Chart + Stats Split (12 columns)
 
┌───────────────────────────────┬───────────────────────────────┐
 
│          span-6               │           span-6              │
 
│         Chart                 │     KPIs / List / Details    │
 
└───────────────────────────────┴───────────────────────────────┘
 
- ใช้เมื่อต้องการแสดงกราฟพร้อมข้อมูลสรุป
 
 
3. Widgets & Components

3.1 Card Widget (พื้นฐาน)
HTML Structure:
 
<div class="card span-3">
 
   <div class="card-label">
 
       Label Name
 
       <span class="material-symbols-outlined info-tooltip" title="คำอธิบาย">info</span>
 
   </div>
 
   <div class="card-value-sm">Value</div>
 
   <div class="card-subtitle">Subtitle</div>
 
</div>
 
CSS:
 
.card {
 
   background: var(--bg-card);
 
   border-radius: 12px;
 
   padding: 14px;
 
   border: 1px solid var(--border);
 
   transition: all 0.2s;
 
}
 
.card:hover {
 
   background: var(--bg-card-hover);
 
   border-color: var(--accent-primary);
 
}
 
.card-label {
 
   font-size: 0.65rem;
 
   font-weight: 600;
 
   color: var(--text-muted);
 
   text-transform: uppercase;
 
   letter-spacing: 0.05em;
 
   margin-bottom: 4px;
 
   display: flex;
 
   align-items: center;
 
   gap: 4px;
 
}
 
.card-value { font-size: 1.5rem; font-weight: 700; }
 
.card-value-sm { font-size: 1.15rem; font-weight: 600; }
 
.card-subtitle { font-size: 0.6rem; color: var(--text-muted); margin-top: 4px; }
 
Variants:
 
Highlight Card (Revenue):
 
.revenue-card {
 
   background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
 
   border: none;
 
}
 
.revenue-card .card-value { font-size: 1.75rem; color: var(--bg-dark); }
 
Status Card Colors:
 
.card-value-sm.success { color: var(--success); }
 
.card-value-sm.warning { color: var(--warning); }
 
.card-value-sm.danger  { color: var(--danger); }
 
.card-value-sm.info    { color: var(--info); }
3.2 Bar Chart Widget
HTML Structure:
 
<div class="bar-chart" id="chartId">
 
   <!-- Bar rows will be injected by JS -->
 
</div>
 
CSS:
 
.bar-chart {
 
   flex: 1;
 
   display: flex;
 
   flex-direction: column;
 
   justify-content: space-around;
 
}
 
.bar-row {
 
   display: flex;
 
   align-items: center;
 
   gap: 8px;
 
}
 
.bar-label {
 
   width: 60px;
 
   font-size: 0.65rem;
 
   color: var(--text-secondary);
 
   text-align: right;
 
}
 
.bar-track {
 
   flex: 1;
 
   height: 16px;
 
   background: var(--border);
 
   border-radius: 3px;
 
   overflow: hidden;
 
}
 
.bar-fill {
 
   height: 100%;
 
   border-radius: 3px;
 
   transition: width 0.5s ease;
 
}
 
.bar-fill.coffee { background: var(--coffee); }
 
.bar-fill.tea { background: var(--tea); color: var(--bg-dark); }
 
.bar-fill.bakery { background: var(--bakery); color: var(--bg-dark); }
 
.bar-fill.hot { background: #ef4444; }
 
.bar-fill.iced { background: #3b82f6; }
 
.bar-value {
 
   font-size: 0.6rem;
 
   font-weight: 600;
 
   color: var(--bg-dark);
 
}
3.3 Progress Bar Widget
HTML Structure:
 
<div style="display: flex; justify-content: space-between;">
 
   <span>Label</span>
 
   <span>80%</span>
 
</div>
 
<div class="progress-track">
 
   <div class="progress-fill" style="width: 80%; background: var(--success);"></div>
 
</div>
 
CSS:
 
.progress-track {
 
   width: 100%;
 
   height: 6px;
 
   background: var(--border);
 
   border-radius: 3px;
 
   overflow: hidden;
 
   margin-top: 6px;
 
}
 
.progress-fill {
 
   height: 100%;
 
   border-radius: 3px;
 
}
3.4 List Item Widget (Ranking)
CSS:
 
.list-item {
 
   display: flex;
 
   align-items: center;
 
   justify-content: space-between;
 
   padding: 8px 0;
 
   border-bottom: 1px solid var(--border);
 
}
 
.list-item:last-child { border-bottom: none; }
 
.list-item-left { display: flex; align-items: center; gap: 8px; }
 
.list-rank {
 
   width: 20px;
 
   height: 20px;
 
   border-radius: 5px;
 
   display: flex;
 
   align-items: center;
 
   justify-content: center;
 
   font-size: 0.65rem;
 
   font-weight: 600;
 
}
 
.list-rank.gold   { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: var(--bg-dark); }
 
.list-rank.silver { background: linear-gradient(135deg, #94a3b8, #64748b); color: var(--bg-dark); }
 
.list-rank.bronze { background: linear-gradient(135deg, #d97706, #92400e); color: white; }
 
.list-value { font-weight: 600; }
3.5 Staff/Avatar Grid
CSS:
 
.staff-grid {
 
   display: grid;
 
   grid-template-columns: repeat(3, 1fr);
 
   gap: 8px;
 
}
 
.staff-card {
 
   background: var(--bg-dark);
 
   border-radius: 10px;
 
   padding: 12px;
 
   text-align: center;
 
}
 
.staff-avatar {
 
   width: 36px;
 
   height: 36px;
 
   border-radius: 50%;
 
   margin: 0 auto 8px;
 
   display: flex;
 
   align-items: center;
 
   justify-content: center;
 
   font-weight: 700;
 
   font-size: 0.75rem;
 
}
 
.staff-avatar.s1 { background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)); color: var(--bg-dark); }
 
.staff-avatar.s2 { background: linear-gradient(135deg, var(--info), #1d4ed8); }
 
.staff-avatar.s3 { background: linear-gradient(135deg, var(--success), #059669); }
3.6 Weather/Icon Grid
CSS:
 
.weather-grid {
 
   display: grid;
 
   grid-template-columns: repeat(4, 1fr);
 
   gap: 10px;
 
}
 
.weather-card {
 
   background: var(--bg-dark);
 
   border-radius: 10px;
 
   padding: 12px;
 
   text-align: center;
 
}
 
.weather-icon { font-size: 1.5rem; margin-bottom: 4px; }
 
.weather-label { font-size: 0.65rem; color: var(--text-muted); }
 
.weather-value { font-size: 1rem; font-weight: 700; margin-top: 2px; }
 
 
4. Section Structure

4.1 Section Header
<section id="sectionId" class="section">
 
   <div class="section-header">
 
       <h2 class="section-title">📊 Section Title</h2>
 
       <span class="section-badge">Label</span>
 
   </div>
 
   <div class="bento-grid">
 
       <!-- Widgets here -->
 
   </div>
 
</section>
 
CSS:
 
.section { margin-bottom: 20px; scroll-margin-top: 68px; }
 
.section-header {
 
   display: flex;
 
   align-items: center;
 
   gap: 10px;
 
   margin-bottom: 12px;
 
}
 
.section-title { font-size: 0.95rem; font-weight: 600; }
 
.section-badge {
 
   padding: 2px 10px;
 
   background: var(--accent-primary);
 
   color: var(--bg-dark);
 
   border-radius: 12px;
 
   font-size: 0.65rem;
 
   font-weight: 600;
 
}
4.2 Section Order (แนะนำ)
1. Summary Bar - ภาพรวมที่ด้านบนสุด
2. Insights - ข้อมูลเชิงลึกและคำแนะนำ
3. Profitability - ตัวเลขกำไร
4. Sales - ยอดขายพร้อม Trend Chart
5. Product - สินค้า/บริการ
6. Time - การวิเคราะห์ตามเวลา
7. Channel - ช่องทางการขาย
8. Customer - ลูกค้า
9. Promo - โปรโมชั่น
10. Payment - การชำระเงิน
11. Weather - ปัจจัยภายนอก
12. Staff - พนักงาน
 
 
5. Header & Navigation

Header (Fixed)
.header {
 
   position: fixed;
 
   top: 0; left: 0; right: 0;
 
   background: rgba(15, 20, 25, 0.95);
 
   backdrop-filter: blur(10px);
 
   border-bottom: 1px solid var(--border);
 
   z-index: 1000;
 
   padding: 0 16px;
 
   height: 56px;
 
}
Navigation Menu
.nav-menu {
 
   display: flex;
 
   gap: 2px;
 
   overflow-x: auto;
 
}
 
.nav-item {
 
   display: flex;
 
   align-items: center;
 
   gap: 4px;
 
   padding: 6px 12px;
 
   border-radius: 6px;
 
   color: var(--text-secondary);
 
   text-decoration: none;
 
   font-size: 0.75rem;
 
   font-weight: 500;
 
   white-space: nowrap;
 
   transition: all 0.2s;
 
   border: 1px solid transparent;
 
}
 
.nav-item:hover { background: var(--bg-card); color: var(--text-primary); }
 
.nav-item.active { background: var(--accent-primary); color: var(--bg-dark); }
 
 
6. Loading & States

Loading Overlay
.loading-overlay {
 
   position: fixed;
 
   top: 0; left: 0; right: 0; bottom: 0;
 
   background: var(--bg-dark);
 
   display: flex;
 
   align-items: center;
 
   justify-content: center;
 
   z-index: 9999;
 
   flex-direction: column;
 
   gap: 16px;
 
}
 
.loading-spinner {
 
   width: 48px;
 
   height: 48px;
 
   border: 4px solid var(--border);
 
   border-top-color: var(--accent-primary);
 
   border-radius: 50%;
 
   animation: spin 1s linear infinite;
 
}
 
@keyframes spin { to { transform: rotate(360deg); } }
 
.loading-text {
 
   color: var(--text-secondary);
 
   font-size: 0.875rem;
 
}
Live Indicator
.live-indicator {
 
   display: flex;
 
   align-items: center;
 
   gap: 6px;
 
   padding: 4px 10px;
 
   background: rgba(16, 185, 129, 0.1);
 
   border-radius: 12px;
 
   font-size: 0.7rem;
 
   color: var(--success);
 
}
 
.live-dot {
 
   width: 6px;
 
   height: 6px;
 
   background: var(--success);
 
   border-radius: 50%;
 
   animation: pulse 2s infinite;
 
}
 
@keyframes pulse {
 
   0%, 100% { opacity: 1; }
 
   50% { opacity: 0.5; }
 
}
 
 
7. Typography

Font
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
Font Weight Usage
- 700 (Bold): ตัวเลข KPI หลัก
- 600 (SemiBold): หัวข้อ, label ที่ต้องการเน้น
- 500 (Medium): Navigation, buttons
- 400 (Regular): ข้อความปกติ
- 300 (Light): Subtitle, description ที่เป็นรอง
Font Sizes
/* Section Title: 0.95rem */
 
.section-title { font-size: 0.95rem; font-weight: 600; }
 
/* Card Label: 0.65rem uppercase */
 
.card-label { font-size: 0.65rem; text-transform: uppercase; }
 
/* Card Value: 1.15-1.75rem */
 
.card-value { font-size: 1.5rem; font-weight: 700; }
 
.card-value-sm { font-size: 1.15rem; font-weight: 600; }
 
/* Chart Labels: 0.65rem */
 
.bar-label { font-size: 0.65rem; }
 
.bar-value { font-size: 0.6rem; }
 
 
8. Responsive Breakpoints

/* Tablet */
 
@media (max-width: 1024px) {
 
   .span-2, .span-3, .span-4, .span-5, .span-6 { grid-column: span 6; }
 
   .span-7, .span-8, .span-12 { grid-column: span 12; }
 
   .weather-grid { grid-template-columns: repeat(2, 1fr); }
 
   .staff-grid { grid-template-columns: repeat(2, 1fr); }
 
}
 
/* Mobile */
 
@media (max-width: 768px) {
 
   .span-2, .span-3, .span-4, .span-5, .span-6,
 
   .span-7, .span-8, .span-12 { grid-column: span 12; }
 
   .nav-item span:last-child { display: none; }
 
   .weather-grid { grid-template-columns: repeat(2, 1fr); }
 
   .staff-grid { grid-template-columns: 1fr; }
 
}
 
/* Small Mobile */
 
@media (max-width: 600px) {
 
   .main { padding: 68px 10px 16px; }
 
   .summary-bar { gap: 16px; padding: 12px 14px; }
 
   .bento-grid { gap: 8px; }
 
}
 
 
9. Google Sheets Integration

Data Fetching Function
function fetchSheet(gid = 0) {
 
   return new Promise((resolve, reject) => {
 
       const cb = '__gviz_' + gid + '_' + Date.now();
 
       const timer = setTimeout(() => {
 
           cleanup();
 
           reject(new Error('Request timeout (20s)'));
 
       }, 20000);
 
       function cleanup() {
 
           delete window[cb];
 
           const el = document.getElementById('__gs_' + cb);
 
           if (el) el.remove();
 
       }
 
       window[cb] = function(resp) {
 
           clearTimeout(timer);
 
           cleanup();
 
           if (resp.status !== 'ok') {
 
               reject(new Error(resp.errors?.[0]?.message || 'gviz error'));
 
               return;
 
           }
 
           const cols = resp.table.cols.map(c => (c.label || c.id || '').trim());
 
           const rows = (resp.table.rows || []).map(r =>
 
               Object.fromEntries(cols.map((h, i) => {
 
                   const cell = r.c ? r.c[i] : null;
 
                   let val = (cell && cell.v !== null && cell.v !== undefined) ? String(cell.v) : '';
 
                   return [h, val.trim()];
 
               }))
 
           );
 
           resolve(rows);
 
       };
 
       const s = document.createElement('script');
 
       s.id = '__gs_' + cb;
 
       s.src = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?gid=${gid}&tqx=responseHandler:${cb}`;
 
       s.onerror = () => { clearTimeout(timer); cleanup(); reject(new Error('Script load failed')); };
 
       document.head.appendChild(s);
 
   });
 
}
Configuration
const SHEET_ID = 'YOUR_GOOGLE_SHEET_ID_HERE';
 
 
10. Animation Guidelines

/* Hover transitions */
 
.card, .nav-item { transition: all 0.2s; }
 
/* Bar chart animation */
 
.bar-fill { transition: width 0.5s ease; }
 
/* Loading spinner */
 
@keyframes spin { to { transform: rotate(360deg); } }
 
/* Live indicator pulse */
 
@keyframes pulse {
 
   0%, 100% { opacity: 1; }
 
   50% { opacity: 0.5; }
 
}
 
 
11. Checklist ก่อน Deploy

กำหนด SHEET_ID ที่ถูกต้อง
ทดสอบ Loading State
ทดสอบ Refresh Button
ทดสอบ Navigation Smooth Scroll
ตรวจสอบ Responsive ทุก Breakpoint
ตรวจสอบ Tooltips ทุก KPI
ทดสอบทุก Chart/Widget rendering
ตรวจสอบ Live Indicator animation
ตรวจสอบ Sync Time อัปเดตถูกต้อง
 
 
12. Quick Start Template

<!DOCTYPE html>
 
<html lang="th">
 
<head>
 
   <meta charset="UTF-8">
 
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
 
   <title>Your Dashboard</title>
 
   <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
 
   <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
 
   <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
 
   <style>
 
       /* Paste CSS from Section 1-9 here */
 
   </style>
 
</head>
 
<body>
 
   <!-- Paste Header from Section 5 -->
 
   <!-- Paste Summary Bar -->
 
   <!-- Paste Sections from Section 4 -->
 
   
 
   <script>
 
       const SHEET_ID = 'YOUR_SHEET_ID';
 
       // Paste fetchSheet from Section 9
 
       // Add your calculation and render logic
 
   </script>
 
</body>
 
</html>