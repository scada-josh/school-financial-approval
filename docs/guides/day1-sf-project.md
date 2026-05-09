# Day 1 - School Financial Approval Project Guide

> คู่มือ step-by-step สำหรับนักเรียนมัธยม เรียนรู้การสร้างโปรเจกต์เว็บไซต์ระบบอนุมัติโครงการของโรงเรียน ตั้งแต่การตั้งค่า Git จนถึงการแก้ไขหน้าเว็บจริง

---

## สารบัญ

1. [ภาพรวมโปรเจกต์](#1-ภาพรวมโปรเจกต์)
2. [เครื่องมือที่ใช้](#2-เครื่องมือที่ใช้)
3. [โครงสร้างโฟลเดอร์](#3-โครงสร้างโฟลเดอร์)
4. [Step 1: สร้าง Git Repository](#step-1-สร้าง-git-repository)
5. [Step 2: สร้างไฟล์ .gitignore](#step-2-สร้างไฟล์-gitignore)
6. [Step 3: สร้างหน้าเว็บหลัก index.html](#step-3-สร้างหน้าเว็บหลัก-indexhtml)
7. [Step 4: เพิ่ม Our Team Section](#step-4-เพิ่ม-our-team-section)
8. [Step 5: เพิ่มสมาชิกทีมคนที่ 5](#step-5-เพิ่มสมาชิกทีมคนที่-5)
9. [Step 6: เปลี่ยนตำแหน่งและรูปภาพสมาชิก](#step-6-เปลี่ยนตำแหน่งและรูปภาพสมาชิก)
10. [สรุปสิ่งที่เรียนรู้](#สรุปสิ่งที่เรียนรู้)

---

## 1. ภาพรวมโปรเจกต์

**School Financial Approval Project** คือระบบเว็บไซต์สำหรับโรงเรียน ช่วยจัดการ:
- การอนุมัติโครงการต่าง ๆ
- การตรวจสอบ TOR (Terms of Reference)
- การติดตามสถานะโครงการ
- การรายงานสถิติ

เว็บไซต์นี้เป็น **Single Page Application (SPA)** ที่เขียนด้วย HTML + CSS + JavaScript ทั้งหมดอยู่ในไฟล์เดียว (`index.html`)

---

## 2. เครื่องมือที่ใช้

| เครื่องมือ | หน้าที่ |
|---|---|
| **OpenCode (AI Assistant)** | ช่วยเขียนโค้ด แก้ไข และจัดการไฟล์ |
| **Git** | บันทึกประวัติการเปลี่ยนแปลงของโค้ด |
| **GitHub** | เก็บโค้ดออนไลน์ (Remote Repository) |
| **เทอร์มินัล (Terminal)** | พิมพ์คำสั่งระบบ |
| **เบราว์เซอร์** | ดูผลลัพธ์ของเว็บไซต์ |

---

## 3. โครงสร้างโฟลเดอร์

```
ai-assistance-approve/
├── index.html                          ← ไฟล์เว็บหลัก (ที่เราแก้ไข)
├── .gitignore                          ← บอก Git ว่าไฟล์ไหนไม่ต้องอัปโหลด
├── assets/
│   └── images/
│       ├── logos/
│       │   ├── logo.png                ← โลโก้โปรเจกต์
│       │   └── logo-01.png
│       └── team/                       ← รูปภาพสมาชิกทีม
│           ├── DevJosh.jpg
│           ├── Meoww.JPG
│           ├── Meowww.JPG
│           ├── reeniizz.jpg
│           ├── santiketa.jpg
│           └── เหมันต์.jpg
├── docs/
│   ├── guides/                         ← คู่มือต่าง ๆ (ไฟล์นี้อยู่ที่นี่)
│   └── architecture/                   ← เอกสารสถาปัตยกรรมระบบ
├── src/
│   ├── frontend/pages/                 ← หน้าเว็บเพิ่มเติม
│   └── backend/scripts/                ← สคริปต์ Python
└── data/
    ├── backups/.gitkeep
    └── exports/.gitkeep
```

---

## Step 1: สร้าง Git Repository

### ทำอะไร
สร้างที่เก็บโค้ด (Repository) บนเครื่องและเชื่อมกับ GitHub

### Prompt ที่ใช้กับ AI
> "สร้าง git repository สำหรับโปรเจกต์ School Financial Approval Project และเชื่อมกับ GitHub"

### คำสั่งที่รัน
```bash
# เริ่มต้นสร้าง git repo
git init

# เพิ่มไฟล์ทั้งหมด
git add .

# บันทึก (commit) ครั้งแรก
git commit -m "Initial commit: School Financial Approval Project"

# เชื่อมกับ GitHub
git remote add origin https://github.com/ชื่อผู้ใช้/ai-assistance-approve.git
git push -u origin main
```

### คำอธิบาย
- `git init` = เริ่มต้นสร้างที่เก็บโค้ดใหม่ในโฟลเดอร์นี้
- `git add .` = เพิ่มไฟล์ทั้งหมดเข้าสู่ระบบ tracking
- `git commit -m "..."` = บันทึกสถานะปัจจุบัน พร้อมข้อความอธิบาย
- `git remote add origin` = เชื่อมโยงกับ repo บน GitHub
- `git push` = อัปโหลดโค้ดขึ้น GitHub

---

## Step 2: สร้างไฟล์ .gitignore

### ทำอะไร
บอก Git ว่าไฟล์ไหน **ไม่ควร** อัปโหลดขึ้น GitHub (เช่น รหัสผ่าน, ไฟล์ชั่วคราว)

### Prompt ที่ใช้กับ AI
> "เพิ่ม .gitignore เพื่อป้องกันไม่ให้อัปโหลดไฟล์ลับ"

### ไฟล์ .gitignore ตัวอย่าง
```gitignore
# ไฟล์รหัสผ่านและ key
*.json
.env
env.local

# ไฟล์ระบบ macOS
.DS_Store

# โฟลเดอร์ไฟล์ชั่วคราว
node_modules/
temp/
```

### คำสั่งที่รัน
```bash
git add .gitignore
git commit -m "chore: strengthen .gitignore rules for secrets"
```

### คำอธิบาย
- `.gitignore` = ไฟล์พิเศษที่ Git จะอ่านแล้วข้ามไฟล์ที่ตรงกับเงื่อนไข
- `chore:` = คำนำหน้า commit message บอกว่าเป็นงานบำรุงรักษา
- สำคัญมาก: **ห้ามอัปโหลดไฟล์รหัสผ่านขึ้น GitHub เด็ดขาด!**

---

## Step 3: สร้างหน้าเว็บหลัก index.html

### ทำอะไร
สร้างไฟล์ HTML หลักของเว็บไซต์ ประกอบด้วย 3 หน้า:
1. **หน้าหลัก (Home)** - แสดงข้อมูลภาพรวม สถิติ ฟีเจอร์ และทีม
2. **TOR Manager** - จัดการประเภทโครงการและหัวข้อ TOR
3. **ติดตามสถานะ (Tracker)** - ตารางติดตามสถานะโครงการ

### โครงสร้าง HTML แบบภาพรวม

```html
<!DOCTYPE html>
<html lang="th">
<head>
    <!-- ส่วนตั้งค่า: ภาษา, ฟอนต์, CSS -->
    <style>
        /* CSS Variables = สีที่ใช้ทั้งเว็บ */
        :root {
            --primary: #cc785c;        /* สีหลัก ส้มอบ */
            --canvas: #faf9f5;          /* สีพื้นหลัง */
            --ink: #141413;             /* สีตัวหนังสือ */
            /* ... อีกหลายตัว */
        }

        /* CSS สำหรับแต่ละส่วน */
        .nav { ... }           /* แถบเมนูด้านบน */
        .hero { ... }          /* ส่วนหัวข้อเรื่อง */
        .stats-bar { ... }     /* แถบสถิติ */
        .feature-grid { ... }  /* กริดฟีเจอร์ */
        .team-section { ... }  /* ส่วนทีม */
        .team-grid { ... }     /* กริดสมาชิกทีม */

        /* Responsive = ทำให้แสดงผลได้ทุกขนาดจอ */
        @media (max-width: 1024px) { ... }  /* แท็บเล็ต */
        @media (max-width: 768px) { ... }   /* มือถือ */
    </style>
</head>
<body>
    <nav>...</nav>           <!-- เมนูด้านบน -->
    <main>
        <div id="page-home">...</div>      <!-- หน้าหลัก -->
        <div id="page-tor">...</div>        <!-- หน้า TOR -->
        <div id="page-tracker">...</div>    <!-- หน้า Tracker -->
    </main>
    <script>
        /* JavaScript ควบคุมการสลับหน้า โหลดข้อมูล ฯลฯ */
    </script>
</body>
</html>
```

### แนวคิดสำคัญที่ใช้

#### CSS Grid (ตารางกริด)
```css
.team-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);  /* แบ่งเป็น 5 คอลัมน์เท่ากัน */
    gap: 24px;                               /* ระยะห่างระหว่างช่อง */
}
```
- `repeat(5, 1fr)` = สร้าง 5 คอลัมน์ แต่ละคอลัมน์กว้างเท่ากัน (1 fraction)
- `gap` = ระยะห่างระหว่างช่อง

#### CSS Variables (ตัวแปร CSS)
```css
:root {
    --primary: #cc785c;
}
.team-avatar {
    border: 3px solid var(--primary);  /* ใช้ตัวแปรแทนเขียนสีตรง */
}
```
- ข้อดี: เปลี่ยนสีที่เดียว ทั้งเว็บเปลี่ยนตาม

#### Responsive Design (ออกแบบตอบสนอง)
```css
/* จอขนาดปกติ (Desktop) */
.team-grid { grid-template-columns: repeat(5, 1fr); }

/* จอขนาดกลาง (Tablet - กว้างไม่เกิน 1024px) */
@media (max-width: 1024px) {
    .team-grid { grid-template-columns: repeat(3, 1fr); }
}

/* จอเล็ก (มือถือ - กว้างไม่เกิน 768px) */
@media (max-width: 768px) {
    .team-grid { grid-template-columns: repeat(2, 1fr); }
}
```

---

## Step 4: เพิ่ม Our Team Section

### ทำอะไร
เพิ่มส่วน "Our Team" ลงในหน้าแรก แสดงสมาชิกทีม 4 คน

### Prompt ที่ใช้กับ AI
> "เพิ่ม section 'Our Team' ลงในหน้า home แสดงสมาชิกทีม 4 คน พร้อมรูปภาพ ชื่อ และตำแหน่ง"

### โค้ดที่เพิ่ม

#### CSS (ใน `<style>`)
```css
/* Team Section */
.team-section {
    margin: 64px 0;           /* ระยะห่างด้านบน-ล่าง */
    text-align: center;        /* จัดกึ่งกลาง */
}
.team-section-title {
    font-size: 36px;
    margin-bottom: 16px;
}
.team-section-subtitle {
    color: var(--muted);
    font-size: 18px;
    margin-bottom: 32px;
}
.team-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);  /* 4 คอลัมน์สำหรับ 4 คน */
    gap: 32px;
    margin-top: 32px;
}
.team-member {
    display: flex;
    flex-direction: column;    /* เรียงแนวตั้ง: รูป → ชื่อ → ตำแหน่ง */
    align-items: center;
}
.team-avatar {
    width: 140px;
    height: 140px;
    border-radius: 50%;        /* ทำให้รูปเป็นวงกลม */
    object-fit: cover;         /* ครอบภาพให้พอดี */
    margin-bottom: 16px;
    border: 3px solid var(--hairline);
    transition: all 0.3s;      /* ลูกเล่นเมื่อ hover */
}
.team-member:hover .team-avatar {
    border-color: var(--primary);
    transform: scale(1.05);    /* ขยายเล็กน้อยเมื่อเอาเมาส์ชี้ */
}
.team-name {
    font-size: 18px;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 4px;
}
.team-role {
    font-size: 14px;
    color: var(--muted);
}
```

#### HTML (ใน `<div id="page-home">`)
```html
<!-- Our Team Section -->
<section class="team-section">
    <h2 class="font-display team-section-title">Our Team</h2>
    <p class="team-section-subtitle">ทีมพัฒนาระบบ School Financial Approval Project</p>
    <div class="team-grid">
        <div class="team-member">
            <img src="assets/images/team/DevJosh.jpg" alt="DevJosh" class="team-avatar">
            <div class="team-name">DevJosh</div>
            <div class="team-role">Lead Developer</div>
        </div>
        <div class="team-member">
            <img src="assets/images/team/Meoww.jpg" alt="Meoww" class="team-avatar">
            <div class="team-name">Meoww</div>
            <div class="team-role">UX/UI Designer</div>
        </div>
        <div class="team-member">
            <img src="assets/images/team/reeniizz.jpg" alt="reeniizz" class="team-avatar">
            <div class="team-name">reeniizz</div>
            <div class="team-role">Project Manager</div>
        </div>
        <div class="team-member">
            <img src="assets/images/team/santiketa.jpg" alt="santiketa" class="team-avatar">
            <div class="team-name">santiketa</div>
            <div class="team-role">Backend Developer</div>
        </div>
    </div>
</section>
```

### คำสั่ง Git
```bash
git add index.html
git commit -m "feat: add Our Team section to homepage"
```

### คำอธิบาย
- `feat:` = คำนำหน้า commit message บอกว่าเป็นการเพิ่มฟีเจอร์ใหม่
- `border-radius: 50%` = ทำให้รูปภาพเป็นทรงกลม
- `object-fit: cover` = ทำให้รูปไม่บิดเบี้ยว ครอบคลุมพื้นที่ทั้งหมด

---

## Step 5: เพิ่มสมาชิกทีมคนที่ 5

### ทำอะไร
เพิ่ม "เหมันต์" (Product Owner) เป็นสมาชิกคนที่ 5 และปรับ grid ให้รองรับ

### Prompt ที่ใช้กับ AI
> "เพิ่มสมาชิกทีมคนที่ 5 ชื่อ เหมันต์ ตำแหน่ง Product Owner รูป assets/images/team/เหมันต์.jpg"

### สิ่งที่ต้องแก้ไข (3 จุด)

#### 5.1 เพิ่ม HTML สมาชิกคนใหม่
```html
<div class="team-member">
    <img src="assets/images/team/เหมันต์.jpg" alt="เหมันต์" class="team-avatar">
    <div class="team-name">เหมันต์</div>
    <div class="team-role">Product Owner</div>
</div>
```
เพิ่มใน `<div class="team-grid">` หลังสมาชิกคนสุดท้าย

#### 5.2 เปลี่ยน Grid จาก 4 เป็น 5 คอลัมน์
```css
/* ก่อน */
.team-grid { grid-template-columns: repeat(4, 1fr); }

/* หลัง */
.team-grid { grid-template-columns: repeat(5, 1fr); }
```

#### 5.3 เพิ่ม Responsive สำหรับ Tablet
```css
@media (max-width: 1024px) {
    /* เพิ่มบรรทัดนี้เข้าไป */
    .team-grid { grid-template-columns: repeat(3, 1fr); }
}
```
ทำไมต้องเป็น 3? เพราะ 5 คน บนแท็บเล็ตแบ่งเป็น 3+2 ดูสวยกว่า 5 แถวยาว

### คำสั่ง Git
```bash
git add index.html assets/images/team/เหมันต์.jpg
git commit -m "feat: add team member เหมันต์ (Product Owner)"
```

---

## Step 6: เปลี่ยนตำแหน่งและรูปภาพสมาชิก

### ทำอะไร
1. เปลี่ยนรูปภาพของ Meoww จาก `Meoww.jpg` เป็น `Meowww.JPG`
2. เปลี่ยนตำแหน่งของสมาชิก 3 คน

### Prompt ที่ใช้กับ AI
> "เปลี่ยนภาพของ Meoww ใช้ภาพ assets/images/team/Meowww.JPG แทน และเปลี่ยนตำแหน่งจาก UX/UI Designer เป็น Project Manager, Backend Developer เป็น AI Engineer, Project Manager เป็น Intelligent Automation Specialist"

### สิ่งที่เปลี่ยน (4 จุด)

#### 6.1 เปลี่ยนรูป Meoww
```html
<!-- ก่อน -->
<img src="assets/images/team/Meoww.jpg" alt="Meoww" class="team-avatar">

<!-- หลัง -->
<img src="assets/images/team/Meowww.JPG" alt="Meoww" class="team-avatar">
```
**หมายเหตุ**: ชื่อไฟล์ต้องตรงกับไฟล์จริงในโฟลเดอร์ รวมถึงตัวพิมพ์ใหญ่-เล็ก (.JPG ไม่ใช่ .jpg)

#### 6.2 เปลี่ยนตำแหน่ง Meoww
```html
<!-- ก่อน -->
<div class="team-role">UX/UI Designer</div>

<!-- หลัง -->
<div class="team-role">Project Manager</div>
```

#### 6.3 เปลี่ยนตำแหน่ง reeniizz
```html
<!-- ก่อน -->
<div class="team-role">Project Manager</div>

<!-- หลัง -->
<div class="team-role">Intelligent Automation Specialist</div>
```

#### 6.4 เปลี่ยนตำแหน่ง santiketa
```html
<!-- ก่อน -->
<div class="team-role">Backend Developer</div>

<!-- หลัง -->
<div class="team-role">AI Engineer</div>
```

### ตารางสมาชิกทีมหลังเปลี่ยนแปลง

| ชื่อ | ตำแหน่งเดิม | ตำแหน่งใหม่ |
|---|---|---|
| DevJosh | Lead Developer | Lead Developer (ไม่เปลี่ยน) |
| Meoww | UX/UI Designer | Project Manager |
| reeniizz | Project Manager | Intelligent Automation Specialist |
| santiketa | Backend Developer | AI Engineer |
| เหมันต์ | Product Owner | Product Owner (ไม่เปลี่ยน) |

---

## สรุปสิ่งที่เรียนรู้

### Git Commands ที่ใช้
| คำสั่ง | หน้าที่ |
|---|---|
| `git init` | สร้าง repository ใหม่ |
| `git add .` | เพิ่มไฟล์ทั้งหมด |
| `git add ชื่อไฟล์` | เพิ่มไฟล์ที่ระบุ |
| `git commit -m "ข้อความ"` | บันทึกพร้อมข้อความ |
| `git push` | อัปโหลดขึ้น GitHub |

### Commit Message Format
```
ประเภท: คำอธิบายสั้น ๆ
```
- `feat:` = เพิ่มฟีเจอร์ใหม่
- `chore:` = งานบำรุงรักษา
- `fix:` = แก้บั๊ก
- `docs:` = เอกสาร

### CSS ที่สำคัญ
| คำสั่ง | หน้าที่ |
|---|---|
| `display: grid` | สร้างตารางกริด |
| `grid-template-columns: repeat(N, 1fr)` | แบ่ง N คอลัมน์เท่ากัน |
| `border-radius: 50%` | ทำให้เป็นวงกลม |
| `object-fit: cover` | ครอบภาพพอดี |
| `@media (max-width: Npx)` | CSS สำหรับจอขนาดไม่เกิน N px |
| `transition: all 0.3s` | ลูกเล่นเคลื่อนไหว |

### เทคนิคการ Prompt AI
1. **บอกให้ชัดเจน**: ระบุไฟล์, ชื่อ, ตำแหน่ง, ที่อยู่ไฟล์รูป
2. **ทีละอย่าง**: ถ้าต้องเปลี่ยนหลายจุด พิมพ์รวมในข้อความเดียว
3. **ตรวจสอบผล**: เปิดไฟล์ดูว่า AI แก้ถูกไหม

---

## ประวัติ Commit ทั้งหมด (Git Log)

```
178ae4d Initial commit: School Financial Approval Project
fc49152 chore: strengthen .gitignore rules for secrets
616021c feat: add Our Team section to homepage
e289b99 feat: add team member เหมันต์ (Product Owner)
```

---

> สร้างโดย OpenCode AI Assistant | วันที่ 9 พฤษภาคม 2569
