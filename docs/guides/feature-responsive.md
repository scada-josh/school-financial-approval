# คู่มือ: ทำให้เว็บไซต์รองรับมือถือ (Responsive Design)

> สำหรับ: เด็กมัธยมที่เพิ่งหัดทำเว็บ  
> อ่านเวลา: 15 นาที  
> ระดับ: ง่าย-ปานกลาง

---

## 1. ปัญหาที่เจอคืออะไร?

### ภาพที่ 1: เมนูบน Navbar หายไปบนมือถือ
เมื่อเปิดเว็บไซต์บนมือถือ (หน้าจอเล็กกว่า 768px) เมนู **หน้าหลัก / TOR Manager / ติดตามสถานะ** ที่อยู่บนแถบด้านบน (Navbar) **หายไปเลย** ทำให้ผู้ใช้ไม่สามารถเปลี่ยนหน้าได้

**สาเหตุ:** โค้ดเดิมซ่อนเมนูไว้ด้วยคำสั่ง `display: none` เมื่อหน้าจอเล็ก แต่ไม่มีตัวเลือกอื่นให้ผู้ใช้กดแทน

```css
@media (max-width: 768px) {
    .nav-menu { display: none; }  /* ← ซ่อนเมนู */
}
```

### ภาพที่ 2: ตัวเลขสถิติ (Stats) แสดงไม่เรียบร้อย
ตัวเลขสถิติต่างๆ เช่น จำนวนโครงการ, อนุมัติแล้ว, รอดำเนินการ แสดงซ้อนกัน กระจัดกระจาย ไม่เป็นระเบียบ บางส่วนหายไป

**สาเหตุ:** การจัดวาง (Layout) ใช้ `flex` แบบเรียงในแถวเดียว ซึ่งบนหน้าจอมือถือที่แคบ ทำให้เนื้อหาไม่พอใส่

---

## 2. แก้ปัญหาอย่างไร? (Step-by-Step)

### ขั้นตอนที่ 1: เพิ่มปุ่ม Hamburger Menu (☰)

**Hamburger Menu คืออะไร?**  
คือปุ่มสามขีด (☰) ที่เห็นบนแอปมือถือทั่วไป กดแล้วจะเปิดเมนูขึ้นมา

**ทำอะไร:**
1. เพิ่มปุ่ม Hamburger เข้าไปใน Navbar (แถบด้านบน)
2. ปุ่มนี้จะ **แสดงเฉพาะบนมือถือ** (ซ่อนบนคอม)

```html
<!-- เพิ่มปุ่มนี้ต่อท้าย nav-menu -->
<button class="nav-hamburger" onclick="toggleMobileNav()">
    ☰
</button>
```

```css
.nav-hamburger {
    display: none;  /* ซ่อนบนคอม */
}

@media (max-width: 768px) {
    .nav-hamburger {
        display: flex;  /* แสดงบนมือถือ */
    }
}
```

### ขั้นตอนที่ 2: สร้างเมนูมือถือแบบ Slide จากขวา

**ทำอะไร:**
1. สร้าง Overlay (พื้นหลังมืด) ทับหน้าจอทั้งหมด
2. สร้าง Sidebar (แถบด้านข้าง) สไลด์เข้ามาจากขวามือ
3. ใส่เมนูทั้งหมดลงไปใน Sidebar

```html
<!-- Overlay + Sidebar -->
<div class="mobile-nav-overlay" id="mobile-nav-overlay" onclick="closeMobileNav()">
    <div class="mobile-nav" onclick="event.stopPropagation()">
        <div class="mobile-nav-header">
            <div>Menu</div>
            <button onclick="closeMobileNav()">✕</button>
        </div>
        <div class="mobile-nav-menu">
            <button onclick="navigateTo('home'); closeMobileNav();">หน้าหลัก</button>
            <button onclick="navigateTo('tor'); closeMobileNav();">TOR Manager</button>
            <button onclick="navigateTo('tracker'); closeMobileNav();">ติดตามสถานะ</button>
        </div>
    </div>
</div>
```

**CSS สำคัญ:**
```css
.mobile-nav-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.5);  /* พื้นหลังมืด */
    display: none;  /* ซ่อนไว้ก่อน */
}

.mobile-nav-overlay.active {
    display: flex;  /* แสดงเมื่อเปิด */
}

.mobile-nav {
    position: fixed;
    top: 0; right: 0; bottom: 0;
    width: 280px;
    background: white;
    transform: translateX(100%);  /* ซ่อนไว้นอกจอขวา */
    transition: transform 0.3s;   /* เอฟเฟกต์สไลด์ */
}

.mobile-nav-overlay.active .mobile-nav {
    transform: translateX(0);     /* สไลด์เข้ามา */
}
```

### ขั้นตอนที่ 3: เขียน JavaScript ควบคุมการเปิด-ปิด

```javascript
function toggleMobileNav() {
    document.getElementById('mobile-nav-overlay').classList.toggle('active');
}

function closeMobileNav() {
    document.getElementById('mobile-nav-overlay').classList.remove('active');
}
```

**ทำงานยังไง:**
- กด Hamburger → เพิ่ม class `active` → Overlay แสดง + Sidebar สไลด์เข้า
- กดปุ่ม ✕ หรือพื้นหลังมืด → ลบ class `active` → ปิด

### ขั้นตอนที่ 4: แก้ Stats Dashboard ให้สวยบนมือถือ

**ปัญหาเดิม:** ตัวเลข 4 ชุด เรียงแถวเดียว บีบกันแน่น

**วิธีแก้:** ใช้ CSS Grid + Flexbox ให้ปรับตัวอัตโนมัติ

```css
.stats-dashboard {
    display: flex;
    justify-content: center;
    gap: 0;
}

/* บนมือถือ: แสดง 2 คู่ (2 คอลัมน์) */
@media (max-width: 768px) {
    .stats-dashboard {
        flex-wrap: wrap;           /* ขึ้นบรรทัดใหม่ได้ */
        gap: 16px;
        justify-content: center;
    }
    
    .stat-card {
        flex: 1 1 45%;            /* กว้างประมาณครึ่งจอ */
        min-width: 140px;
        justify-content: center;
    }
    
    .stat-value {
        font-size: 28px;          /* ลดขนาดตัวเลข */
    }
    
    .stat-label {
        font-size: 13px;          /* ลดขนาดตัวอักษร */
    }
}

/* บนมือถือจอเล็กมาก: แสดงเรียงต่อกัน */
@media (max-width: 480px) {
    .stats-dashboard {
        flex-direction: column;    /* เรียงต่อกันแนวตั้ง */
        align-items: stretch;
    }
    
    .stat-card {
        flex: 1 1 100%;           /* กว้างเต็มที่ */
    }
}
```

### ขั้นตอนที่ 5: ปรับส่วนอื่นๆ ให้ Responsive

#### 5.1 Table (ตารางข้อมูล)
**ปัญหา:** ตารางมีหลายคอลัมน์ บนมือถือมองไม่ครบ

**แก้:** ทำให้ตารางเลื่อนซ้าย-ขวาได้ (Horizontal Scroll)

```css
@media (max-width: 768px) {
    .table-container {
        overflow-x: auto;          /* เลื่อนได้ */
        -webkit-overflow-scrolling: touch;  /* เลื่อนลื่นบน iOS */
    }
    
    .project-table {
        min-width: 800px;          /* บังคับความกว้างขั้นต่ำ */
    }
}
```

#### 5.2 Filter Bar (แถบกรองข้อมูล)
**ปัญหา:** ช่องกรองหลายอัน เรียงแถวเดียวไม่พอ

**แก้:** ให้เรียงซ้อนกันแนวตั้ง

```css
@media (max-width: 768px) {
    .filter-bar {
        flex-direction: column;    /* เรียงแนวตั้ง */
        align-items: stretch;       /* กว้างเต็มที่ */
    }
    
    .filter-select {
        width: 100%;               /* เต็มความกว้าง */
        min-width: auto;
    }
}
```

#### 5.3 Modal (หน้าต่าง Popup)
**ปัญหา:** Modal กว้างเกินไป บนมือถือเกินขอบจอ

**แก้:** ลด Padding และจำกัดความกว้าง

```css
@media (max-width: 768px) {
    .modal {
        padding: 24px;             /* ลดระยะห่าง */
        max-width: 95vw;           /* ไม่เกิน 95% ของจอ */
        margin: 16px;
    }
    
    .modal-title {
        font-size: 22px;           /* ลดขนาดหัวข้อ */
    }
    
    .form-actions {
        flex-direction: column-reverse;  /* ปุ่มเรียงต่อกัน */
    }
    
    .form-actions .btn {
        width: 100%;               /* ปุ่มกว้างเต็มที่ */
    }
}
```

#### 5.4 Team Section (ส่วนทีมงาน)
**ปัญหา:** รูปทีมงาน 5 คน เรียงแถวเดียว บีบกันเล็กมาก

**แก้:** ลดจำนวนคอลัมน์ตามขนาดจอ

```css
.team-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);  /* คอม: 5 คอลัมน์ */
}

@media (max-width: 1024px) {
    .team-grid {
        grid-template-columns: repeat(3, 1fr);  /* แท็บเล็ต: 3 คอลัมน์ */
    }
}

@media (max-width: 768px) {
    .team-grid {
        grid-template-columns: repeat(2, 1fr);  /* มือถือ: 2 คอลัมน์ */
        gap: 24px;
    }
    
    .team-avatar {
        width: 90px;               /* ลดขนาดรูป */
        height: 90px;
    }
}
```

---

## 3. สรุป Breakpoints ที่ใช้

**Breakpoint คืออะไร?**  
คือ "จุดเปลี่ยน" ขนาดหน้าจอ ที่ CSS จะเปลี่ยนการแสดงผล

| ขนาดจอ | ชื่อเรียก | สิ่งที่เปลี่ยน |
|---------|----------|---------------|
| > 1024px | Desktop | แสดงปกติทุกอย่าง |
| 768px - 1024px | Tablet | ลดคอลัมน์ Grid, ปรับขนาดตัวอักษร |
| < 768px | Mobile | แสดง Hamburger Menu, ซ่อนเมนูเดิม |
| < 480px | Small Mobile | เรียงแนวตั้งทั้งหมด, ขนาดเล็กลง |

---

## 4. ผลลัพธ์หลังแก้ไข

### ✅ ก่อนแก้ไข
- [ ] เปิดบนมือถือ → เมนูหายไป เลื่อนหน้าไม่ได้
- [ ] ตัวเลขสถิติซ้อนกัน อ่านไม่ออก
- [ ] ตารางข้อมูลล้นจอ
- [ ] ปุ่มกดเล็กเกินไป

### ✅ หลังแก้ไข
- [x] มี Hamburger Menu กดเปลี่ยนหน้าได้
- [x] Stats แสดงเป็นระเบียบ 2 คอลัมน์ หรือเรียงต่อกัน
- [x] ตารางเลื่อนซ้าย-ขวาได้
- [x] ทุกปุ่มกดง่าย ขนาดพอดีนิ้ว
- [x] รูปทีมงานไม่บีบ แสดงสวยงาม

---

## 5. เทคนิคสำคัญที่ได้เรียนรู้

### 5.1 Mobile-First vs Desktop-First
- โปรเจกต์นี้ใช้ **Desktop-First** (เขียน CSS สำหรับคอมก่อน แล้วใช้ `@media` ปรับสำหรับมือถือ)
- แต่แนะนำให้ฝึก **Mobile-First** (เขียนสำหรับมือถือก่อน แล้วขยายสำหรับคอม) เพราะง่ายต่อการดูแล

### 5.2 หน่วยที่ควรใช้บนมือถือ
- **px** → ใช้กับขนาดที่แน่นอน (เช่น ขนาดปุ่ม, ความกว้าง Sidebar)
- **%** → ใช้กับความกว้างที่ยืดหยุ่น
- **vw/vh** → ใช้กับขนาดที่อิงตามหน้าจอ
- **rem/em** → ใช้กับขนาดตัวอักษร (ปรับตามตั้งค่าผู้ใช้)

### 5.3 Flexbox vs Grid
- **Flexbox** → เหมาะกับการจัดเรียงในแถวเดียว (Navbar, Stats, Filter)
- **Grid** → เหมาะกับการจัดเรียงหลายแถวหลายคอลัมน์ (Feature Cards, Team)

### 5.4 สิ่งที่ต้องเช็คเสมอ
1. **Touch Target** → ปุ่มควรมีขนาดอย่างน้อย 44x44px (นิ้วคนเรากดง่าย)
2. **Font Size** → ตัวอักษรไม่ควรเล็กกว่า 16px (อ่านสบายตา)
3. **Contrast** → สีตัวอักษรกับพื้นหลังต้องต่างกันชัดเจน
4. **Horizontal Scroll** → หน้าเว็บไม่ควรเลื่อนซ้าย-ขวา (ยกเว้นตารางที่กำหนดไว้)

---

## 6. ไฟล์ที่แก้ไขทั้งหมด

1. `index.html` → หน้าหลัก (เพิ่ม Hamburger + ปรับ Hero, Stats, Team)
2. `src/frontend/pages/school-financial-approval.html` → หน้าจัดการงบประมาณ
3. `src/frontend/pages/project-tracker.html` → หน้าติดตามสถานะ
4. `src/frontend/pages/tor-manager-claude.html` → หน้าจัดการ TOR

---

## 7. คำศัพท์ที่ใช้

| ศัพท์ | ความหมาย |
|-------|---------|
| Responsive | ปรับตัวตามขนาดหน้าจอ |
| Navbar | แถบเมนูด้านบน |
| Hamburger Menu | ปุ่มสามขีด (☰) |
| Overlay | พื้นหลังทึบทับหน้าจอ |
| Sidebar | แถบด้านข้าง |
| Breakpoint | จุดเปลี่ยนขนาดหน้าจอ |
| Flexbox | ระบบจัดวางแบบยืดหยุ่น |
| Grid | ระบบจัดวางแบบตาราง |
| Media Query | คำสั่ง CSS ที่ตรวจสอบขนาดจอ (`@media`) |
| Touch Target | พื้นที่ที่ผู้ใช้แตะบนหน้าจอ |

---

## 8. แหล่งเรียนรู้เพิ่มเติม

- [MDN: Responsive Design](https://developer.mozilla.org/th/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [CSS Tricks: A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS Tricks: A Complete Guide to Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Google: Responsive Web Design Basics](https://web.dev/responsive-web-design-basics/)

---

## 9. ทดสอบยังไง?

### บนคอมพิวเตอร์ (Chrome/Edge/Firefox)
1. กด **F12** เปิด DevTools
2. กดปุ่ม **Toggle Device Toolbar** (📱 หรือ Ctrl+Shift+M)
3. เลือกขนาดจอ เช่น iPhone 12 Pro, Samsung Galaxy
4. ลองกด Hamburger Menu, เลื่อนตาราง, ดู Stats

### บนมือถือจริง
1. เปิดเว็บไซต์บนมือถือ
2. ลองกดทุกปุ่ม
3. ลองหมุนจอแนวนอน
4. เช็คว่าอ่านง่าย กดง่าย ไม่มีส่วนไหนหาย

---

**เขียนโดย:** AI Assistant  
**วันที่:** 15 พฤษภาคม 2026  
**เวอร์ชัน:** 1.0  
**Branch:** `feature/responsive`
