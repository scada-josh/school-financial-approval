# Day 2 - School Financial Approval Project Guide

> คู่มือ step-by-step สำหรับนักเรียนมัธยม วันที่ 2: การเพิ่มฟอร์ม Submit TOR, ปรับแต่งดีไซน์ Hero Section, และเพิ่มระบบ Icons

---

## สารบัญ

1. [สรุปสิ่งที่ทำในวันที่ 2](#1-สรุปสิ่งที่ทำในวันที่-2)
2. [Step 1: ปรับแต่ง Quote ให้ดู Modern](#step-1-ปรับแต่ง-quote-ให้ดู-modern)
3. [Step 2: สร้างปุ่ม Submit TOR และ Modal Form](#step-2-สร้างปุ่ม-submit-tor-และ-modal-form)
4. [Step 3: เพิ่มระบบเลือกโครงการและอัพโหลดไฟล์](#step-3-เพิ่มระบบเลือกโครงการและอัพโหลดไฟล์)
5. [Step 4: เพิ่ม Backend API สำหรับรับข้อมูล TOR](#step-4-เพิ่ม-backend-api-สำหรับรับข้อมูล-tor)
6. [Step 5: ปรับแต่ง Hero Section ให้เต็มจอ](#step-5-ปรับแต่ง-hero-section-ให้เต็มจอ)
7. [Step 6: สร้าง Stats Dashboard](#step-6-สร้าง-stats-dashboard)
8. [Step 7: เปลี่ยน Background Color และฟอนต์ภาษาไทย](#step-7-เปลี่ยน-background-color-และฟอนต์ภาษาไทย)
9. [Step 8: เพิ่ม Lucide Icons แทน Emoji](#step-8-เพิ่ม-lucide-icons-แทน-emoji)
10. [Step 9: ปรับแต่ง Navigation Bar](#step-9-ปรับแต่ง-navigation-bar)
11. [Step 10: Commit การเปลี่ยนแปลง](#step-10-commit-การเปลี่ยนแปลง)
12. [สรุปสิ่งที่เรียนรู้](#สรุปสิ่งที่เรียนรู้)

---

## 1. สรุปสิ่งที่ทำในวันที่ 2

ในวันที่ 2 เราได้พัฒนาเว็บไซต์ให้มีความสวยงามและใช้งานได้จริงมากขึ้น โดยมีการเปลี่ยนแปลงหลัก ๆ ดังนี้:

- **ปรับแต่ง Quote** ให้ดู minimal และ modern
- **สร้างฟอร์ม Submit TOR** พร้อมระบบอัพโหลดไฟล์ PDF/DOCX
- **เพิ่มระบบเลือกโครงการ** แบบ dropdown พร้อมเพิ่มโครงการใหม่ได้
- **สร้าง Backend API** รับข้อมูลและบันทึกลง Google Sheets
- **ปรับ Hero Section** ให้เป็นหน้าเต็มจอ (Full Screen)
- **สร้าง Stats Dashboard** แสดงสถิติโครงการ
- **เปลี่ยน Background Color** เป็นโทนครีมอุ่น
- **เพิ่ม Lucide Icons** แทน emoji ทั้งหมด
- **ปรับ Navigation Bar** ให้มีสีส้มเมื่อ active

---

## Step 1: ปรับแต่ง Quote ให้ดู Modern

### ทำอะไร
ปรับแต่งข้อความ Quote "เพิ่มประสิทธิภาพการดำเนินงานด้วย AI และระบบอัตโนมัติ (Automation)" ให้ดูเรียบง่าย ไม่ดูเด่นจนเกินไป

### Prompt ที่ใช้กับ AI
> "เอาข้อความออกจาก hero-subtitle และทำเป็น Quote เน้นๆ"

### สิ่งที่เปลี่ยน

#### ก่อน (เดิม)
```html
<p class="hero-subtitle">
    ระบบบริหารงบประมาณ...<br>
    และเพิ่มประสิทธิภาพการดำเนินงานด้วย AI และระบบอัตโนมัติ (Automation)
</p>
```

#### หลัง (แยกออกมาเป็น Quote)
```html
<p class="hero-subtitle">ระบบบริหารงบประมาณ...</p>
<div class="hero-quote">
    <blockquote>"เพิ่มประสิทธิภาพการดำเนินงานด้วย AI และระบบอัตโนมัติ (Automation)"</blockquote>
</div>
```

#### CSS ที่ใช้
```css
.hero-quote { margin: var(--space-xl) auto; max-width: 640px; }
.hero-quote blockquote {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 500;
    color: var(--muted);
    text-align: center;
    letter-spacing: 0.02em;
    line-height: 1.6;
}
```

### คำอธิบาย
- **แยกข้อความออกมา** จาก subtitle มาเป็นบล็อกใหม่
- **ใช้ฟอนต์ Inter** แทน Cormorant Garamond (serif)
- **ลดขนาด** จาก 28px เป็น 15px
- **เอา italic และเครื่องหมายคำพูดใหญ่ออก**
- **เปลี่ยนเป็นสีเทาอ่อน** แทนสีส้ม

---

## Step 2: สร้างปุ่ม Submit TOR และ Modal Form

### ทำอะไร
สร้างปุ่ม "Submit TOR" ที่เมื่อกดจะเปิดหน้าต่าง Modal (ฟอร์ม) เต็มจอ ให้ผู้ใช้กรอกข้อมูลและอัพโหลดไฟล์ TOR

### Prompt ที่ใช้กับ AI
> "อยากให้มีปุ่ม Submit TOR เพื่อเปิด pop up form แบบ fullscreen และให้กรอก ชื่อ สกุล email และอัพโหลดไฟล์ TOR (pdf, docx)"

### โครงสร้างที่สร้าง

#### 2.1 ปุ่ม Submit TOR (ใน Hero Section)
```html
<button class="btn-open-submit" onclick="openSubmitTorModal()">
    <span>📄</span> Submit TOR
</button>
```

#### 2.2 CSS สำหรับปุ่ม
```css
.btn-open-submit {
    background: linear-gradient(135deg, var(--primary), var(--primary-active));
    color: white;
    border: none;
    border-radius: 50px;
    padding: 28px 80px;
    font-size: 24px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 8px 28px rgba(204, 120, 92, 0.4);
}
```

#### 2.3 Modal Overlay (พื้นหลังมืด)
```css
.submit-tor-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(24, 23, 21, 0.75);
    backdrop-filter: blur(8px);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 2500;
}
.submit-tor-overlay.active { display: flex; }
```

#### 2.4 Modal Form (ฟอร์มกรอกข้อมูล)
```html
<div class="submit-tor-overlay" id="submit-tor-overlay">
    <div class="submit-tor-modal">
        <div class="submit-tor-header">
            <h2>Submit TOR</h2>
            <p>กรอกข้อมูลและแนบไฟล์ TOR เพื่อส่งตรวจสอบ</p>
        </div>
        <form id="submit-tor-form">
            <!-- ชื่อ -->
            <div class="form-row">
                <div class="form-group">
                    <label>ชื่อ *</label>
                    <input type="text" id="submit-tor-firstname" required>
                </div>
                <div class="form-group">
                    <label>นามสกุล *</label>
                    <input type="text" id="submit-tor-lastname" required>
                </div>
            </div>
            <!-- อีเมล -->
            <div class="form-group">
                <label>อีเมล *</label>
                <input type="email" id="submit-tor-email" required>
            </div>
            <!-- ไฟล์ -->
            <div class="form-group">
                <label>ไฟล์ TOR *</label>
                <div class="file-drop-zone">
                    <div>คลิกหรือลากไฟล์มาวางที่นี่</div>
                    <input type="file" id="submit-tor-file" accept=".pdf,.docx">
                </div>
            </div>
            <button type="submit" class="btn-submit-tor">Submit TOR</button>
        </form>
    </div>
</div>
```

#### 2.5 JavaScript เปิด/ปิด Modal
```javascript
function openSubmitTorModal() {
    document.getElementById('submit-tor-overlay').classList.add('active');
    document.body.style.overflow = 'hidden'; // ปิดการ scroll
}

function closeSubmitTorModal() {
    document.getElementById('submit-tor-overlay').classList.remove('active');
    document.body.style.overflow = '';
}
```

### คำอธิบาย
- **Modal** = หน้าต่างที่ลอยขึ้นมาทับเนื้อหาเดิม
- **Overlay** = พื้นหลังสีมืด คลิกแล้วปิดได้ (ก่อนหน้านี้ แต่ตอนหลังเอาออก)
- **backdrop-filter: blur** = ทำให้พื้นหลังเบลอ
- **Drag & Drop** = ลากไฟล์มาวางได้เลย

---

## Step 3: เพิ่มระบบเลือกโครงการและอัพโหลดไฟล์

### ทำอะไร
เพิ่ม dropdown ให้เลือกโครงการที่มีอยู่แล้ว หรือเพิ่มโครงการใหม่ พร้อมกรอกรายละเอียด

### Prompt ที่ใช้กับ AI
> "ในฟอร์มอัพโหลดให้เพิ่มการเลือกชื่อโครงการ ถ้าไม่มีให้สามารถกดเพิ่มโครงการได้เลย"

### สิ่งที่เพิ่ม

#### 3.1 Dropdown เลือกโครงการ
```html
<div class="form-group">
    <label>โครงการ *</label>
    <select class="form-select" id="submit-tor-project" onchange="handleProjectSelect(this)">
        <option value="">เลือกโครงการ</option>
        <!-- รายการโครงการจะถูกโหลดจาก API -->
        <option value="__NEW__">+ เพิ่มโครงการใหม่</option>
    </select>
</div>
```

#### 3.2 ฟิลด์สำหรับโครงการใหม่ (แสดงเมื่อเลือก "เพิ่มใหม่")
```html
<div id="new-project-fields" style="display: none;">
    <input type="text" id="submit-tor-new-project" placeholder="ชื่อโครงการ">
    <select id="submit-tor-new-project-type">
        <option value="">เลือกประเภท</option>
        <option value="จัดซื้อจัดจ้างทั่วไป">จัดซื้อจัดจ้างทั่วไป</option>
        <option value="IT / Digital Transformation">IT / Digital Transformation</option>
        <option value="AI / Big Data">AI / Big Data</option>
    </select>
    <select id="submit-tor-new-project-year">
        <option value="">เลือกปี</option>
        <option value="ปีงบประมาณ 2568">ปีงบประมาณ 2568</option>
    </select>
    <textarea id="submit-tor-new-project-desc" placeholder="รายละเอียดโครงการ"></textarea>
</div>
```

#### 3.3 โหลดรายชื่อโครงการจาก API
```javascript
async function loadProjectNames() {
    const res = await fetch(`${API_BASE}/api/tor/project-names`);
    const data = await res.json();
    
    const select = document.getElementById('submit-tor-project');
    data.data.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        select.appendChild(option);
    });
}
```

### คำอธิบาย
- **Dropdown** ดึงข้อมูลจาก Google Sheets (Projects sheet) อัตโนมัติ
- **เลือก "+ เพิ่มโครงการใหม่"** จะแสดงฟิลด์เพิ่มเติม
- **ประเภทโครงการ** ดึงจาก TOR_Config sheet

---

## Step 4: เพิ่ม Backend API สำหรับรับข้อมูล TOR

### ทำอะไร
เพิ่มระบบรับข้อมูลจากฟอร์ม บันทึกไฟล์ และเก็บข้อมูลลง Google Sheets

### Prompt ที่ใช้กับ AI
> "เพิ่ม backend endpoint POST /api/tor/submit และให้เก็บไฟล์ไว้ที่ uploads/documents"

### ไฟล์ที่แก้ไข
`src/backend/scripts/tor-api.py`

### สิ่งที่เพิ่ม

#### 4.1 Endpoint รับข้อมูล
```python
elif path == '/api/tor/submit':
    body = self._read_body()
    first_name = body.get('firstName', '').strip()
    last_name = body.get('lastName', '').strip()
    email = body.get('email', '').strip()
    project_name = body.get('projectName', '').strip()
    file_data = body.get('fileData', '')
    
    # บันทึกไฟล์
    file_bytes = base64.b64decode(file_data)
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, 'wb') as f:
        f.write(file_bytes)
    
    # บันทึกลง Google Sheets
    sheets_client.add_tor_submission({
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'projectName': project_name,
        'fileName': unique_filename,
        'status': 'รอตรวจสอบ'
    })
```

#### 4.2 สร้าง Sheet TOR_Submissions อัตโนมัติ
```python
def ensure_tor_submissions_sheet(self):
    # ตรวจสอบว่ามี sheet หรือยัง ถ้าไม่มีให้สร้าง
    # เพิ่ม headers: ID, วันที่ส่ง, ชื่อ, นามสกุล, อีเมล, ชื่อโครงการ, ชื่อไฟล์, สถานะ
```

#### 4.3 ถ้าเป็นโครงการใหม่ เพิ่มลง Projects Sheet
```python
if is_new_project:
    sheets_client.add_new_project_to_sheet(
        project_name,
        project_type=project_type,
        project_description=project_description,
        budget_year=budget_year
    )
```

### คำอธิบาย
- **Base64** = วิธีแปลงไฟล์เป็นข้อความเพื่อส่งผ่าน JSON
- **UPLOAD_DIR** = โฟลเดอร์ `uploads/documents/`
- **TOR_Submissions** = Sheet ใหม่ใน Google Sheets เก็บประวัติการส่ง

---

## Step 5: ปรับแต่ง Hero Section ให้เต็มจอ

### ทำอะไร
ทำให้ Hero Section (ส่วนหัวเว็บ) สูงเต็มหน้าจอ (Full Screen)

### Prompt ที่ใช้กับ AI
> "ช่วยใส่ background ใน hero section ด้วยภาพนี้" และ "ให้ภาพขยายกว้างเต็มพื้นที่"

### สิ่งที่เปลี่ยน

#### 5.1 เพิ่ม Background Image
```css
.hero {
    background-image: url('assets/images/backgrounds/bg-hero.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
```

#### 5.2 ทำให้เต็มจอ
```css
.hero-wrapper {
    width: 100vw;
    height: calc(100vh - 64px);  /* สูงเต็มจอ ลบ nav bar */
    position: relative;
    left: 50%;
    transform: translateX(-50%);
}
```

#### 5.3 ย้าย Stats Dashboard เข้า Hero
```html
<div class="hero-wrapper">
    <section class="hero">
        <!-- เนื้อหาเดิม (Logo, Title, Button) -->
        
        <!-- Stats Dashboard ย้ายมาอยู่ในนี้ -->
        <div class="stats-dashboard">
            <!-- 4 cards -->
        </div>
    </section>
</div>
```

### คำอธิบาย
- **100vw** = กว้างเต็ม viewport width
- **calc(100vh - 64px)** = สูงเต็มจอ ลบความสูงของ nav bar (64px)
- **transform: translateX(-50%)** = จัดกลางเมื่อใช้ left: 50%

---

## Step 6: สร้าง Stats Dashboard

### ทำอะไร
สร้างแถบแสดงสถิติ 4 รายการ พร้อมไอคอนและเส้นคั่น

### สิ่งที่สร้าง

#### 6.1 HTML Structure
```html
<div class="stats-dashboard">
    <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
            <div class="stat-value" id="home-stat-total">-</div>
            <div class="stat-label">โครงการทั้งหมด</div>
        </div>
    </div>
    <!-- อีก 3 cards -->
</div>
```

#### 6.2 CSS (แบบไม่มีกรอบ มีเส้นคั่น)
```css
.stats-dashboard {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    padding: 0 0 var(--space-xl) 0;
}
.stat-card {
    background: transparent;
    padding: 0 var(--space-xxl);
    display: flex;
    align-items: center;
    gap: var(--space-md);
    border-right: 1px solid rgba(204, 120, 92, 0.2);
}
.stat-card:last-child { border-right: none; }
.stat-icon {
    font-size: 32px;
    color: var(--primary);  /* สีส้ม */
}
.stat-value {
    font-size: 36px;
    font-weight: 700;
    color: var(--primary);
}
```

### คำอธิบาย
- **ไม่มีกรอบ/พื้นหลัง** (transparent)
- **ไอคอนสีส้ม** ไม่มีวงกลมพื้นหลัง
- **เส้นแนวตั้ง** คั่นระหว่างแต่ละ stat
- **ตัวเลขสีส้ม** ขนาดใหญ่

---

## Step 7: เปลี่ยน Background Color และฟอนต์ภาษาไทย

### ทำอะไร
1. เปลี่ยนสีพื้นหลังเว็บไซต์
2. เพิ่มฟอนต์ภาษาไทยที่อ่านง่าย

### สิ่งที่เปลี่ยน

#### 7.1 สีพื้นหลัง
```css
/* ก่อน */
--canvas: #faf9f5;  /* ขาวนวล */

/* หลัง */
--canvas: #FFF8F0;  /* ครีมอุ่น */
```

#### 7.2 เพิ่มฟอนต์ Sarabun
```html
<link href="https://fonts.googleapis.com/css2?family=...&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

#### 7.3 ใช้ฟอนต์ภาษาไทย
```css
body {
    font-family: 'Sarabun', 'Inter', sans-serif;
}
.font-thai {
    font-family: 'Sarabun', sans-serif;
}
```

### คำอธิบาย
- **Sarabun** = ฟอนต์ไทยจาก Google Fonts อ่านง่าย ทันสมัย
- **#FFF8F0** = สีครีมอุ่น สบายตา

---

## Step 8: เพิ่ม Lucide Icons แทน Emoji

### ทำอะไร
เปลี่ยน emoji (📋, ✅, ⏳ ฯลฯ) เป็น SVG Icons แบบ Lucide ทั้งหมด

### ตัวอย่างการเปลี่ยน

#### ก่อน (Emoji)
```html
<div class="stat-icon">📋</div>
<div class="feature-icon">📊</div>
<button>✕</button>
```

#### หลัง (Lucide SVG)
```html
<!-- โครงการทั้งหมด - Clipboard List -->
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <rect width="8" height="4" x="8" y="2" rx="1"/>
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
    <path d="M12 11h4"/><path d="M12 16h4"/>
    <path d="M8 11h.01"/><path d="M8 16h.01"/>
</svg>

<!-- อนุมัติแล้ว - Check Circle -->
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
    <polyline points="22 4 12 14.01 9 11.01"/>
</svg>

<!-- รอดำเนินการ - Clock -->
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="12" cy="12" r="10"/>
    <polyline points="12 6 12 12 16 14"/>
</svg>

<!-- ประเภทโครงการ - Layers -->
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <polygon points="12 2 2 7 12 12 22 7 12 2"/>
    <polyline points="2 17 12 22 22 17"/>
    <polyline points="2 12 12 17 22 12"/>
</svg>
```

### Icons ที่ใช้แทน

| ส่วน | Emoji เดิม | Lucide Icon |
|---|---|---|
| โครงการทั้งหมด | 📋 | `clipboard-list` |
| อนุมัติแล้ว | ✅ | `check-circle` |
| รอดำเนินการ | ⏳ | `clock` |
| ประเภทโครงการ | 📊 | `layers` |
| ไฟล์อัพโหลด | 📎 | `paperclip` |
| ลบไฟล์ | ✕ | `x` |
| ลบโครงการ | 🗑 | `trash-2` |
| แก้ไข | ✎ | `pencil` |
| ลูกศร | → | `arrow-right` |

### คำอธิบาย
- **Lucide Icons** = ชุดไอคอน SVG ฟรี สไตล์เรียบง่าย
- **SVG** = ภาพเวกเตอร์ ขยายได้ไม่แตก
- **stroke="currentColor"** = ใช้สีตาม parent element

---

## Step 9: ปรับแต่ง Navigation Bar

### ทำอะไร
1. เปลี่ยนสีปุ่ม Active เป็นสีส้ม
2. เพิ่มปุ่ม Settings

### Prompt ที่ใช้กับ AI
> "เมนู nav bar เมื่อปุ่ม Active อยากให้เป็นสีส้มอ่อนๆ และอยากให้เพิ่มปุ่ม Setting ที่มีเส้นขอบสีส้ม"

### สิ่งที่เปลี่ยน

#### 9.1 ปุ่ม Active สีส้ม
```css
.nav-item.active {
    color: var(--primary);  /* สีส้ม */
    background: rgba(204, 120, 92, 0.1);  /* พื้นหลังส้มอ่อน 10% */
}
```

#### 9.2 ปุ่ม Settings
```css
.nav-btn-settings {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    color: var(--primary);
    border: 1.5px solid var(--primary);
    background: transparent;
    border-radius: var(--radius-md);
}
```

#### 9.3 HTML
```html
<button class="nav-btn-settings">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18..."/>
        <circle cx="12" cy="12" r="3"/>
    </svg>
    Settings
</button>
```

### คำอธิบาย
- **ปุ่ม Active** = สีส้มอ่อน ไม่ใช่สีเทาเหมือนเดิม
- **ปุ่ม Settings** = มีเส้นขอบสีส้ม พื้นหลังโปร่งใส

---

## Step 10: Commit การเปลี่ยนแปลง

### Commit ครั้งที่ 1: Submit TOR Form
```bash
git add index.html src/backend/scripts/tor-api.py
git commit -m "feat: add Submit TOR form with modal, file upload, and Google Sheets integration

- Add fullscreen Submit TOR modal to index.html
- Add backend endpoint POST /api/tor/submit to tor-api.py
- Handle base64 file uploads to uploads/documents/
- Save metadata to TOR_Submissions Google Sheet
- Support creating new projects in Projects sheet
- Add GET /api/tor/project-names endpoint"
```

### Commit ครั้งที่ 2: Redesign Homepage
```bash
git add index.html src/frontend/pages/
git add assets/images/backgrounds/ assets/images/icons/
git add "assets/images/team/เหมันต์.jpg"
git commit -m "feat: redesign homepage hero section with full-screen background and dashboard stats

- Make hero section full viewport height (100vh)
- Add Sarabun Thai font for modern typography
- Redesign stats dashboard with orange-themed icons
- Add Submit TOR button with custom icon
- Change global background color to warm cream (#FFF8F0)
- Add Settings button with orange border to navbar
- Change active nav item to orange highlight
- Add responsive styles for mobile and tablet"
```

### คำอธิบาย
- แบ่ง commit เป็น 2 ครั้งตามลักษณะงาน
- Commit แรก = ฟีเจอร์ Submit TOR
- Commit ที่สอง = การปรับแต่งดีไซน์

---

## สรุปสิ่งที่เรียนรู้

### HTML/CSS เทคนิคใหม่

| เทคนิค | คำอธิบาย |
|---|---|
| **Modal/Overlay** | หน้าต่างลอยที่มีพื้นหลังมืด |
| **backdrop-filter: blur** | ทำให้พื้นหลังเบลอ |
| **100vw / 100vh** | กว้าง/สูงเต็ม viewport |
| **calc()** | คำนวณค่า CSS (เช่น calc(100vh - 64px)) |
| **transform: translateX(-50%)** | เลื่อนตำแหน่งเพื่อจัดกลาง |
| **flex: 1** | ขยายเต็มพื้นที่ที่เหลือ |
| **SVG inline** | ใส่โค้ด SVG ตรงใน HTML |
| **Base64** | แปลงไฟล์เป็นข้อความเพื่อส่งผ่าน API |

### JavaScript ที่ใช้

| ฟังก์ชัน | หน้าที่ |
|---|---|
| `fetch()` | ส่ง/รับข้อมูลจาก API |
| `FileReader` | อ่านไฟล์ในเบราว์เซอร์ |
| `FormData` | เก็บข้อมูลฟอร์ม |
| `classList.add/remove` | เปลี่ยน class ของ element |

### Git Commands เพิ่มเติม

| คำสั่ง | หน้าที่ |
|---|---|
| `git diff --stat` | ดูสรุปการเปลี่ยนแปลง |
| `git log --oneline` | ดูประวัติ commit แบบสั้น |

### Icons ที่ใช้ (Lucide)

| ชื่อ | ความหมาย |
|---|---|
| `clipboard-list` | รายการเอกสาร |
| `check-circle` | ติ๊กถูกในวงกลม |
| `clock` | นาฬิกา (รอ) |
| `layers` | ชั้นซ้อน (หมวดหมู่) |
| `file-up` | อัพโหลดไฟล์ |
| `trash-2` | ถังขยะ (ลบ) |
| `pencil` | ดินสอ (แก้ไข) |
| `x` | ปิด/ยกเลิก |
| `arrow-right` | ลูกศรขวา |
| `settings` | ฟันเฟือง (ตั้งค่า) |
| `paperclip` | คลิปหนีบกระดาษ (แนบไฟล์) |

---

## ประวัติ Commit ทั้งหมด (Git Log)

```
53529e5 feat: redesign homepage hero section with full-screen background and dashboard stats
dc6c2b7 feat: add Submit TOR form with modal, file upload, and Google Sheets integration
1bfa2c2 feat: update team roles and add day1 guide
e289b99 feat: add team member เหมันต์ (Product Owner)
616021c feat: add Our Team section to homepage
fc49152 chore: strengthen .gitignore rules for secrets
178ae4d Initial commit: School Financial Approval Project
```

---

> สร้างโดย OpenCode AI Assistant | วันที่ 10 พฤษภาคม 2569
> คู่มือนี้บันทึกทุกขั้นตอนการพัฒนาเว็บไซต์ School Financial Approval Project วันที่ 2