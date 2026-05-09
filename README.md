# School Financial Approval Project

ระบบจัดการงบประมาณและอนุมัติโครงการสำหรับสถานศึกษา พร้อมระบบจัดการ TOR (Terms of Reference)

## โครงสร้างโปรเจกต์

```
school-financial-approval/
│
├── 📁 assets/                          # ทรัพยากรสำหรับ UI (Frontend Resources)
│   ├── 📁 css/                         # Stylesheets (ถ้ามีไฟล์ CSS แยก)
│   ├── 📁 js/                          # JavaScript รวม (ถ้ามีไฟล์ JS แยก)
│   └── 📁 images/                      # รูปภาพทั้งหมด
│       ├── 📁 logos/                   # Logo ระบบ, โลโก้หน่วยงาน, Favicon
│       ├── 📁 icons/                   # Icons สำหรับ UI (SVG, PNG)
│       ├── 📁 backgrounds/             # พื้นหลัง, Hero images, Banners
│       └── 📁 uploads/                 # รูปภาพ UI (avatar, placeholder, etc.)
│
├── 📁 src/                             # Source Code ทั้งหมด
│   ├── 📁 backend/                     # Backend API (Python)
│   │   ├── 📁 api/                     # API endpoints (Flask/FastAPI routes)
│   │   ├── 📁 config/                  # การตั้งค่าและ Secrets
│   │   │   ├── .env.local              # ตัวแปรสภาพแวดล้อม (ไม่ push ขึ้น Git)
│   │   │   └── service-account.json    # Google Service Account Key (secret!)
│   │   ├── 📁 scripts/                 # Scripts สำหรับรัน/Setup
│   │   │   ├── tor-api.py              # API Server (CRUD Google Sheet)
│   │   │   ├── setup-tor-config.py     # Script setup ข้อมูลเริ่มต้น
│   │   │   └── gsheet-code.md          # ตัวอย่างโค้ดเชื่อมต่อ Google Sheet
│   │   └── 📁 utils/                   # Helper functions (reusable)
│   │
│   └── 📁 frontend/                    # Frontend Web Application
│       ├── 📁 pages/                   # HTML Pages (แยกตามหน้า)
│       │   ├── school-financial-approval.html  # 🏠 หน้าหลัก (Dashboard)
│       │   ├── tor-manager-claude.html         # 📋 TOR Manager (Claude Design)
│       │   └── tor-management.html             # 📋 TOR Manager (Legacy)
│       ├── 📁 components/              # UI Components ที่ใช้ซ้ำได้
│       └── 📁 services/                # API Service Callers (JavaScript)
│
├── 📁 data/                            # ข้อมูลระบบ (ไม่ใช่ code)
│   ├── 📁 database/                    # Database files (ถ้ามี local DB)
│   ├── 📁 exports/                     # ไฟล์ Export จากระบบ (CSV, PDF, Excel)
│   └── 📁 backups/                     # ข้อมูลสำรอง
│
├── 📁 docs/                            # เอกสารโครงการ
│   ├── AGENTS.md                       # คำแนะนำสำหรับ AI Agent
│   ├── 📁 architecture/                # เอกสารออกแบบระบบ
│   │   ├── ClaudeDesign.md             # Design System (Claude.com style)
│   │   ├── Design-Guide.md             # Dashboard Design Guide
│   │   └── TOR_Management_System_Architecture.md  # เอกสารสถาปัตยกรรม
│   ├── 📁 tor/                         # TOR Templates และตัวอย่าง
│   └── 📁 guides/                      # คู่มือการใช้งาน (User Guide)
│
├── 📁 uploads/                         # ไฟล์ที่ผู้ใช้ (User) อัปโหลด
│   ├── 📁 documents/                   # เอกสารแนบ (PDF, DOCX, XLSX)
│   ├── 📁 images/                      # รูปภาพแนบประกอบ TOR/โครงการ
│   ├── 📁 tor/                         # ไฟล์ TOR ที่อัปโหลด (PDF, DOCX)
│   └── 📁 temp/                        # ไฟล์ชั่วคราว (ห้าม commit ขึ้น Git)
│
├── 📁 tests/                           # ไฟล์ทดสอบ
│   ├── 📁 unit/                        # Unit Tests
│   └── 📁 integration/                 # Integration Tests
│       ├── test-gsheet-api.js          # Test Google Sheet (Node.js)
│       └── test-gsheet-api.py          # Test Google Sheet (Python)
│
├── 📁 .logs/                           # Log files (ไม่ push ขึ้น Git)
│
├── 📄 start-tor-system.sh              # 🚀 Launcher script (รัน API + เปิด Web)
├── 📄 package.json                     # Node.js dependencies (ถ้ามี)
├── 📄 .gitignore                       # กฎการ ignore ไฟล์
└── 📄 README.md                        # คำอธิบายโปรเจกต์ (ไฟล์นี้)
```

---

## การใช้งานแต่ละโฟลเดอร์

| โฟลเดอร์ | ใช้เก็บอะไร | ตัวอย่างไฟล์ |
|----------|-------------|--------------|
| `assets/images/logos/` | Logo ระบบ, Favicon, Logo หน่วยงาน | `logo-sf.svg`, `favicon.ico` |
| `assets/images/icons/` | Icons สำหรับ UI | `menu-icon.svg`, `check-icon.png` |
| `assets/images/backgrounds/` | พื้นหลัง, Hero images | `hero-bg.jpg`, `banner.png` |
| `assets/images/uploads/` | รูปภาพที่ใช้ใน UI (ไม่ใช่ user upload) | `avatar-default.png`, `placeholder.jpg` |
| `src/backend/api/` | API Routes / Controllers | `projects.py`, `auth.py` |
| `src/backend/config/` | Config และ Secrets | `.env.local`, `service-account.json` |
| `src/backend/scripts/` | Scripts รัน/Setup | `tor-api.py`, `setup-tor-config.py` |
| `src/backend/utils/` | Helper Functions | `gsheet.py`, `validators.py` |
| `src/frontend/pages/` | HTML Pages | `school-financial-approval.html` |
| `src/frontend/components/` | Reusable UI Components | `modal.html`, `navbar.html` |
| `src/frontend/services/` | API Callers (JS) | `api.js`, `auth.js` |
| `data/exports/` | ไฟล์ Export จากระบบ | `report-2026-05-09.csv`, `tor-export.pdf` |
| `data/backups/` | ข้อมูลสำรอง | `backup-2026-05-09.sql` |
| `docs/tor/` | TOR Templates | `tor-template-procurement.docx` |
| `docs/guides/` | คู่มือการใช้งาน | `user-guide.pdf`, `admin-guide.md` |
| `uploads/documents/` | เอกสารแนบจากผู้ใช้ | `project-plan.pdf`, `budget.xlsx` |
| `uploads/images/` | รูปภาพแนบจากผู้ใช้ | `site-photo.jpg`, `diagram.png` |
| `uploads/tor/` | ไฟล์ TOR จากผู้ใช้ | `tor-project-a.pdf`, `tor-draft.docx` |
| `uploads/temp/` | ไฟล์ชั่วคราว | `temp-export-12345.csv` |
| `tests/unit/` | Unit Tests | `test-validators.py` |
| `tests/integration/` | Integration Tests | `test-gsheet-api.py` |
| `.logs/` | Log files | `app-2026-05-09.log`, `error.log` |

---

## วิธีใช้งาน

### 1. รันระบบทั้งหมด
```bash
./start-tor-system.sh
```

### 2. เปิดหน้าเว็บ
```bash
open src/frontend/pages/school-financial-approval.html
```

### 3. รัน Backend API อย่างเดียว
```bash
python3 src/backend/scripts/tor-api.py
```

---

## หมายเหตุสำคัญ

⚠️ **อย่า push ข้อมูลลับขึ้น Git:**
- ไฟล์ `src/backend/config/.env.local` (มี API Keys)
- ไฟล์ `src/backend/config/*.json` (Service Account Keys)
- ไฟล์ใน `uploads/` (ข้อมูลผู้ใช้)
- ไฟล์ใน `data/backups/`
- ไฟล์ใน `.logs/`

✅ **ควร push ขึ้น Git:**
- Source code ทั้งหมดใน `src/`
- เอกสารใน `docs/`
- ไฟล์ config template (ไม่มี secret)
- Tests ใน `tests/`
