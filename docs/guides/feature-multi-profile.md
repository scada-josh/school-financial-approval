# Feature: Multi Profile

## 1. ภาพรวมของ Feature นี้

**Multi Profile** คือ ระบบที่ช่วยให้ผู้ใช้สามารถสร้าง "โปรไฟล์การเชื่อมต่อ" (Connection Profiles) หลายชุดได้ โดยแต่ละโปรไฟล์สามารถเก็บค่าการตั้งค่าของ Connectors (เช่น n8n Workflow) ที่แตกต่างกัน

ในระบบ **School Financial Approval Project** ฟีเจอร์นี้ช่วยให้ผู้ใช้สามารถ:
- สร้างโปรไฟล์หลายอันสำหรับสภาพแวดล้อมที่ต่างกัน (เช่น Production, Testing, Development)
- สลับเปลี่ยนโปรไฟล์ได้ง่าย ๆ ผ่าน dropdown
- แก้ไขชื่อโปรไฟล์ได้
- ลบโปรไฟล์ที่ไม่ต้องการได้ (ยกเว้นโปรไฟล์ Default)
- ข้อมูลทั้งหมดถูกเก็บใน **Google Sheet** (แท็บ Settings)

---

## 2. อธิบายแบบเด็กมัธยมเข้าใจ

ลองนึกถึง **แฟ้มสี** ที่ใช้เก็บเอกสารในโรงเรียน:

- แฟ้มสีฟ้า = เอกสารเรียน
- แฟ้มสีแดง = เอกสารงานกลุ่ม
- แฟ้มสีเขียว = เอกสารทดลอง

**Multi Profile** ก็เหมือนกัน เป็นการแยก "แฟ้ม" สำหรับเก็บค่าการตั้งค่าต่าง ๆ ของระบบ:

- **โปรไฟล์ "Production"** = ใช้งานจริง เชื่อมต่อกับระบบจริง
- **โปรไฟล์ "Testing"** = ใช้ทดสอบ เชื่อมต่อกับระบบทดสอบ
- **โปรไฟล์ "Default"** = โปรไฟล์เริ่มต้นที่ระบบสร้างให้

เมื่อเลือกแฟ้มไหน ระบบก็จะใช้ค่าการตั้งค่าจากแฟ้มนั้น ๆ ทำให้ไม่ต้องมานั่งกรอก URL หรือ API Key ใหม่ทุกครั้งที่เปลี่ยนสภาพแวดล้อมการใช้งาน

---

## 3. ปัญหาก่อนมี Feature นี้

**ถ้าไม่มี Multi Profile จะเกิดปัญหาอะไร?**

1. **ข้อมูลปนกัน** - ถ้ามีหลายคนใช้ระบบร่วมกัน หรือต้องทดสอบหลายสภาพแวดล้อม ค่าการตั้งค่าจะทับซ้อนกัน
2. **ยุ่งยากในการเปลี่ยน** - ทุกครั้งที่ต้องเปลี่ยนจากระบบทดสอบเป็นระบบจริง ต้องมานั่งกรอก Webhook URL, API Key ใหม่ทั้งหมด
3. **เสี่ยงผิดพลาด** - อาจส่งข้อมูลไปผิดระบบ เพราะลืมเปลี่ยนค่าการตั้งค่า
4. **ไม่มีการแยกบริบท** - ไม่รู้ว่าตอนนี้กำลังใช้งานระบบไหนอยู่

---

## 4. สิ่งที่พบในโค้ดปัจจุบัน

ตารางสรุปไฟล์และโค้ดที่เกี่ยวข้อง:

| ส่วนที่พบ | ไฟล์/โฟลเดอร์ | หน้าที่ |
|---|---|---|
| **Backend API** | `src/backend/scripts/tor-api.py` | จัดการข้อมูล Profiles ทั้งหมด รวมถึง CRUD และ sync กับ Google Sheet |
| **Frontend UI** | `index.html` | หน้า Settings Modal → Tab Connectors → ส่วนจัดการ Profiles |
| **ฐานข้อมูล** | Google Sheet (แท็บ Settings) | เก็บรายชื่อ Profiles, Active Profile, และ Config ของแต่ละ Profile |
| **State Management** | `index.html` (JavaScript) | ใช้ตัวแปร `currentProfiles`, `activeProfile`, `profileConfigs` |
| **API Endpoints** | `tor-api.py` | รองรับ GET, POST, PUT, DELETE สำหรับ Profiles |
| **Loading UI** | `index.html` (CSS/JS) | Spinner animation ขณะโหลดข้อมูล |

### 4.1 Backend (`src/backend/scripts/tor-api.py`)

**คลาส `GoogleSheetsClient`** มี methods สำหรับจัดการ Profiles:

- `get_profiles()` - ดึงรายชื่อ Profiles ทั้งหมด และ Profile ที่กำลังใช้งานอยู่
- `get_profile(name)` - ดึงค่า Config ของ Profile ที่ระบุ
- `save_profile(name, config)` - สร้างหรือบันทึก Profile พร้อม Config
- `delete_profile(name)` - ลบ Profile (ห้ามลบ Default)
- `set_active_profile(name)` - ตั้งค่า Profile ที่จะใช้งาน
- `rename_profile(old_name, new_name)` - เปลี่ยนชื่อ Profile
- `_update_settings_from_dict()` - Sync ข้อมูลกับ Google Sheet โดยลบแถวที่ไม่มีอยู่จริง

### 4.2 Frontend (`index.html`)

**ตัวแปร State:**
```javascript
let currentProfiles = [];      // เก็บรายชื่อ Profiles ทั้งหมด
let activeProfile = 'Default'; // Profile ที่กำลังใช้งานอยู่
let profileConfigs = {};       // เก็บ Config ของแต่ละ Profile
let profileModalMode = 'add';  // โหมดของ Modal (add/edit)
let isUpdatingSelector = false; // ป้องกัน trigger onchange ขณะอัปเดต UI
```

**ฟังก์ชันหลัก:**
- `loadSettings()` - โหลด Settings และ Profiles พร้อมกัน
- `updateProfileSelector()` - อัปเดต dropdown แสดงรายชื่อ Profiles
- `loadProfileConfig()` - โหลดค่า Config ของ Profile ที่เลือก
- `applyProfileConfig()` - นำค่า Config ไปแสดงในฟอร์ม
- `onProfileChange()` - เมื่อผู้ใช้เปลี่ยน Profile จาก dropdown
- `saveCurrentProfileConfig()` - บันทึกค่า Config ปัจจุบัน
- `openProfileModal()`, `saveProfile()`, `deleteProfile()` - จัดการ Modal เพิ่ม/แก้ไข/ลบ
- `setProfileLoading()` - แสดง/ซ่อน Spinner ขณะโหลด

---

## 5. Flow การทำงานแบบ Step-by-Step

### 5.1 การสร้าง Profile

1. ผู้ใช้กดปุ่ม **+** (เพิ่มโปรไฟล์) ที่อยู่ข้าง ๆ ช่องเลือก Profile
2. ระบบแสดง **Modal** (หน้าต่างเล็ก) พร้อมช่องให้กรอกชื่อ Profile
3. ผู้ใช้กรอกชื่อ เช่น "Production" หรือ "Testing"
4. ระบบตรวจสอบว่า:
   - ชื่อต้องไม่ว่าง
   - ชื่อต้องไม่ซ้ำกับที่มีอยู่
5. ระบบสร้าง Profile ใหม่ โดยใช้ค่า Config จากหน้าจอปัจจุบัน
6. ระบบบันทึกลง **Google Sheet** (แท็บ Settings)
7. ระบบอัปเดต dropdown ให้แสดง Profile ใหม่
8. ระบบเลือก Profile ใหม่เป็น Active Profile ทันที

### 5.2 การเลือก Profile

1. ผู้ใช้คลิกที่ **dropdown** เลือก Profile
2. ระบบแสดง **Spinner Loading** (วงกลมหมุน)
3. ระบบบันทึกค่า Config ของ Profile ปัจจุบันก่อน
4. ระบบส่งคำขอไป Backend เพื่อตั้งค่า Active Profile
5. ระบบโหลดค่า Config ของ Profile ใหม่จาก Google Sheet
6. ระบบอัปเดตหน้าจอให้แสดงค่า Config ของ Profile ที่เลือก
7. ระบบซ่อน Spinner และแสดงข้อความ "เปลี่ยนโปรไฟล์สำเร็จ"

### 5.3 การแก้ไขชื่อ Profile

1. ผู้ใช้เลือก Profile ที่ต้องการแก้ไขจาก dropdown
2. ผู้ใช้กดปุ่ม **✎** (แก้ไขโปรไฟล์)
3. ระบบแสดง Modal พร้อมชื่อปัจจุบัน
4. ผู้ใช้แก้ไขชื่อแล้วกดบันทึก
5. ระบบตรวจสอบว่าชื่อไม่ซ้ำและไม่ว่าง
6. ระบบส่งคำขอ rename ไป Backend
7. Backend อัปเดตชื่อใน Google Sheet และย้าย Config ไปชื่อใหม่
8. ระบบอัปเดต dropdown และเลือกชื่อใหม่

### 5.4 การลบ Profile

1. ผู้ใช้เลือก Profile ที่ต้องการลบจาก dropdown
2. ผู้ใช้กดปุ่ม **🗑** (ลบโปรไฟล์)
3. ระบบแสดงข้อความยืนยัน "คุณต้องการลบโปรไฟล์นี้ใช่หรือไม่?"
4. ผู้ใช้กด "ตกลง"
5. ระบบแสดง **Spinner Loading**
6. ระบบส่งคำขอลบไป Backend
7. Backend ลบข้อมูลออกจาก Google Sheet จริง ๆ
8. ระบบเปลี่ยนกลับไปใช้ **Default** Profile
9. ระบบอัปเดต dropdown ให้ไม่แสดง Profile ที่ถูกลบ
10. ระบบซ่อน Spinner และแสดงข้อความ "ลบโปรไฟล์สำเร็จ"

**หมายเหตุ:** ไม่สามารถลบ **Default** Profile ได้

---

## 6. โครงสร้างข้อมูลของ Profile

ข้อมูล Profiles ถูกเก็บใน **Google Sheet** (แท็บ Settings) ในรูปแบบ Key-Value:

| Category | Key | ตัวอย่างค่า | ความหมาย |
|---|---|---|---|
| Profiles | PROFILE_LIST | `["Default","Production"]` | รายชื่อ Profiles ทั้งหมด |
| Profiles | ACTIVE_PROFILE | Production | Profile ที่กำลังใช้งานอยู่ |
| Profile_Default | N8N_ENABLED | false | เปิด/ปิด n8n สำหรับ Default |
| Profile_Default | N8N_WEBHOOK_URL | https://... | URL สำหรับ Default |
| Profile_Default | N8N_API_KEY | key123 | API Key สำหรับ Default |
| Profile_Default | N8N_WORKFLOW_ID | wf-001 | Workflow ID สำหรับ Default |
| Profile_Production | N8N_ENABLED | true | เปิด/ปิด n8n สำหรับ Production |
| Profile_Production | N8N_WEBHOOK_URL | https://prod... | URL สำหรับ Production |

**หมายเหตุ:** โครงสร้างนี้ใช้ระบบ Key-Value ใน Google Sheet ไม่ใช่ Database Table แบบ Relational แบบดั้งเดิม

---

## 7. API ที่เกี่ยวข้อง

| Method | Path | หน้าที่ | สถานะ |
|---|---|---|---|
| GET | `/api/profiles` | ดึงรายชื่อ Profiles ทั้งหมดและ Active Profile | **ทำแล้ว** |
| GET | `/api/profiles/{name}` | ดึงค่า Config ของ Profile ที่ระบุ | **ทำแล้ว** |
| POST | `/api/profiles` | สร้าง Profile ใหม่พร้อม Config | **ทำแล้ว** |
| POST | `/api/profiles/rename` | เปลี่ยนชื่อ Profile (old_name → new_name) | **ทำแล้ว** |
| PUT | `/api/profiles/{name}` | อัปเดตค่า Config ของ Profile | **ทำแล้ว** |
| PUT | `/api/profiles/active/{name}` | ตั้งค่า Active Profile | **ทำแล้ว** |
| DELETE | `/api/profiles/{name}` | ลบ Profile (ห้ามลบ Default) | **ทำแล้ว** |

---

## 8. ส่วนของ Frontend/UI

สรุปจากโค้ดใน `index.html`:

### 8.1 ส่วนเลือก Profile
- **Dropdown** (`<select id="profile-select">`) - แสดงรายชื่อ Profiles ทั้งหมด
- **ปุ่ม +** (`onclick="openProfileModal('add')"`) - สร้าง Profile ใหม่
- **ปุ่ม ✎** (`onclick="openProfileModal('edit')"`) - แก้ไขชื่อ Profile
- **ปุ่ม 🗑** (`onclick="deleteProfile()"`) - ลบ Profile (disabled เมื่อเป็น Default)

### 8.2 Modal จัดการ Profile
- **Title** - แสดง "เพิ่มโปรไฟล์" หรือ "แก้ไขโปรไฟล์"
- **Input** - ช่องกรอกชื่อ Profile
- **ปุ่มยกเลิก** - ปิด Modal
- **ปุ่มบันทึก** - บันทึก Profile

### 8.3 Loading Overlay
- **วงกลมหมุน** (Spinner) แบบ Modern พร้อม backdrop-filter blur
- **ข้อความ** "กำลังโหลด..."
- แสดงเมื่อ:
  - เปลี่ยน Profile
  - ลบ Profile

### 8.4 ส่วนแสดง Config
- **Webhook URL** - แสดงค่าตาม Profile ที่เลือก
- **API Key** - แสดงค่าตาม Profile ที่เลือก
- **Workflow ID** - แสดงค่าตาม Profile ที่เลือก
- **ปุ่มเปิด/ปิด n8n** - สถานะตาม Profile ที่เลือก

---

## 9. การตรวจสอบข้อมูลและ Error Handling

จากโค้ดที่ตรวจสอบได้:

### 9.1 Validation (การตรวจสอบ)

| สิ่งที่ตรวจสอบ | ไฟล์ | ผลถ้าไม่ผ่าน |
|---|---|---|
| ชื่อ Profile ห้ามว่าง | `index.html` | แสดง Toast "กรุณาระบุชื่อโปรไฟล์" |
| ชื่อ Profile ห้ามซ้ำ | `index.html` + `tor-api.py` | แสดง Toast "โปรไฟล์นี้มีอยู่แล้ว" |
| ห้ามลบ Default | `tor-api.py` | แสดง Toast "ไม่สามารถลบโปรไฟล์ Default ได้" |
| ห้ามแก้ไขชื่อเป็น Default | `tor-api.py` | Error: "Cannot rename Default profile" |
| Profile ต้องมีอยู่จริง | `tor-api.py` | Error: "Profile 'xxx' not found" |

### 9.2 Error Handling (การจัดการข้อผิดพลาด)

- **ถ้า API ไม่ตอบสนอง** - แสดง Toast "ไม่สามารถ...ได้" และ log error ใน Console
- **ถ้าโหลด Config ไม่สำเร็จ** - ใช้ค่าเริ่มต้น (N8N_ENABLED=false, ค่าอื่นว่าง)
- **ถ้าลบแล้วโหลด Default ไม่สำเร็จ** - แสดง Warning ใน Console แต่ไม่ crash
- **Spinner จะซ่อนเสมอ** - ใช้ `try...finally` เพื่อป้องกัน Spinner ค้าง

---

## 10. ตัวอย่างการใช้งาน

### ตัวอย่าง 1: นักเรียนแยก Profile สำหรับงานต่าง ๆ

**สถานการณ์:** นักเรียนต้องส่งงานโครงการให้อาจารย์หลายวิชา

- **โปรไฟล์ "วิชา IT"** - Webhook ส่งไปยังระบบของอาจารย์ IT
- **โปรไฟล์ "วิชาบัญชี"** - Webhook ส่งไปยังระบบของอาจารย์บัญชี
- **โปรไฟล์ "Default"** - ไม่ส่งไปไหน (ใช้ทดสอบ)

**ผลลัพธ์:** เมื่อเลือกโปรไฟล์ไหน ข้อมูลก็จะส่งไปยังอาจารย์ท่านนั้นโดยอัตโนมัติ

### ตัวอย่าง 2: ผู้ใช้แยก Profile สำหรับงานส่วนตัวและงานบริษัท

**สถานการณ์:** คุณใช้ระบบนี้ทั้งในโรงเรียนและในงานส่วนตัว

- **โปรไฟล์ "โรงเรียน"** - เชื่อมต่อกับระบบของโรงเรียน
- **โปรไฟล์ "งานส่วนตัว"** - เชื่อมต่อกับระบบของตัวเอง
- **โปรไฟล์ "ทดสอบ"** - เชื่อมต่อกับระบบทดสอบ (sandbox)

**ผลลัพธ์:** ไม่ต้องมานั่งลบ/กรอก URL ใหม่ทุกครั้งที่เปลี่ยนงาน

### ตัวอย่าง 3: ระบบแยกบริบทตาม Profile

**สถานการณ์:** ทีมงานมีหลายคนใช้ระบบร่วมกัน

- **โปรไฟล์ "ทีม A"** - ใช้ Webhook ของทีม A
- **โปรไฟล์ "ทีม B"** - ใช้ Webhook ของทีม B
- **โปรไฟล์ "รวม"** - ส่งไปยังระบบกลาง

**ผลลัพธ์:** แต่ละทีมใช้งานได้โดยไม่กระทบกัน

---

## 11. สรุปสิ่งที่ทำแล้ว

- **ระบบสร้าง/เพิ่ม Profile** - ผู้ใช้สามารถสร้าง Profile ใหม่ได้ พร้อมค่า Config จากหน้าจอปัจจุบัน
- **ระบบเลือก Profile** - ใช้ dropdown เลือกได้ พร้อมบันทึก Active Profile ลง Google Sheet
- **ระบบแก้ไขชื่อ Profile** - เปลี่ยนชื่อได้โดยไม่สูญเสีย Config
- **ระบบลบ Profile** - ลบได้ (ยกเว้น Default) พร้อมลบข้อมูลจริงจาก Google Sheet
- **ระบบเก็บข้อมูล** - ใช้ Google Sheet (แท็บ Settings) เก็บ Profile List, Active Profile, และ Config แยกตาม Profile
- **ระบบ Cache Management** - Clear cache ทุกครั้งที่มีการแก้ไข เพื่อป้องกันข้อมูลค้าง
- **ระบบ Sync ข้อมูล** - `_update_settings_from_dict` จะ sync ข้อมูลกับ Sheet โดยลบแถวที่ไม่มีอยู่จริง
- **Loading Spinner** - แสดงขณะเปลี่ยนหรือลบ Profile พร้อม animation แบบ Modern
- **Validation** - ตรวจสอบชื่อซ้ำ, ชื่อว่าง, ห้ามลบ Default
- **Error Handling** - จัดการข้อผิดพลาดด้วย try-catch และแสดง Toast แจ้งเตือน
- **ไอคอน House** - เพิ่มไอคอนบ้าน (Lucide) ให้ปุ่ม "หน้าหลัก" ใน navbar
- **Responsive Design** - รองรับการแสดงผลบนอุปกรณ์ต่าง ๆ

---

## 12. สิ่งที่ยังไม่พบในโค้ดปัจจุบัน

- **การจัดลำดับ (Reorder) Profiles** - ยังไม่สามารถลากเรียงลำดับ Profile ได้
- **ระบบคัดลอก (Duplicate) Profile** - ยังไม่มีปุ่มคัดลอก Profile
- **การ Import/Export Profiles** - ยังไม่สามารถสำรองหรือนำเข้า Profiles จากไฟล์ได้
- **ระบบสิทธิ์ (Permission)** - ยังไม่มีการจำกัดสิทธิ์ว่าใครสามารถแก้ไข Profile ได้
- **ประวัติการเปลี่ยน Profile** - ยังไม่มีการบันทึกประวัติว่าใครเปลี่ยน Profile เมื่อไหร่
- **ระบบ Default Config Template** - ยังไม่มี Template สำหรับสร้าง Profile แบบเร็ว
- **การตั้งค่าเริ่มต้น (Default Values)** - ยังไม่มีระบบตั้งค่าเริ่มต้นสำหรับ Profile ใหม่
- **Unit Test / Integration Test** - ยังไม่มีการทดสอบอัตโนมัติสำหรับ Feature นี้

---

## 13. สิ่งที่สามารถพัฒนาต่อได้

### 13.1 ฟีเจอร์เสริม
- **เพิ่มสีหรือ Avatar ให้ Profile** - ให้ผู้ใช้เลือกสีประจำ Profile เพื่อจำง่าย
- **เพิ่มคำอธิบาย (Description)** - ให้ผู้ใช้เพิ่ม note อธิบายว่า Profile นี้ใช้ทำอะไร
- **ระบบคัดลอก Profile** - ปุ่ม "คัดลอก" เพื่อสร้าง Profile ใหม่จากอันเดิม
- **ระบบ Import/Export** - ส่งออก Profiles เป็น JSON หรือนำเข้ากลับมา
- **ระบบค้นหา/กรอง** - เมื่อมี Profile มาก ๆ ให้ค้นหาได้
- **Shortcut Keys** - กด Ctrl+1, Ctrl+2 เพื่อสลับ Profile เร็ว ๆ
- **ระบบกลุ่ม (Group/Folder)** - จัดกลุ่ม Profiles เช่น "งานโรงเรียน", "งานส่วนตัว"

### 13.2 การปรับปรุงด้านเทคนิค
- **เพิ่ม Unit Test** - ทดสอบฟังก์ชัน CRUD ของ Profiles
- **เพิ่ม Integration Test** - ทดสอบการทำงานร่วมกันระหว่าง Frontend และ Backend
- **เพิ่ม Loading State ในส่วนอื่น ๆ** - เช่น ขณะบันทึก Settings
- **ปรับปรุง Error Message** - ให้ชัดเจนและเป็นมิตรมากขึ้น
- **เพิ่มระบบ Undo** - ถ้าลบผิด ให้กด Undo ได้ (เช่น ภายใน 5 วินาที)
- **เพิ่มระบบ Backup** - สำรอง Profiles ก่อนลบ

### 13.3 การพัฒนาด้าน UX/UI
- **ปรับปรุง Modal** - เพิ่ม animation เข้า/ออก
- **เพิ่ม Tooltip** - แสดงคำอธิบายเมื่อ hover ปุ่ม
- **ปรับปรุง Spinner** - เพิ่ม skeleton loading แทน spinner ในบางส่วน
- **เพิ่ม Empty State** - ถ้ายังไม่มี Profile ให้แสดงคำแนะนำ

---

## 14. สรุปสุดท้าย

**Multi Profile** คือฟีเจอร์ที่ช่วยให้ผู้ใช้สามารถจัดการ "ชุดการตั้งค่า" ได้หลายชุด โดยไม่ต้องมานั่งกรอกข้อมูลใหม่ทุกครั้งที่เปลี่ยนสภาพแวดล้อมการใช้งาน

เหมือนกับการมี **หลายแฟ้มเอกสาร** ที่แต่ละแฟ้มเก็บข้อมูลคนละชนิดกัน เมื่อต้องการใช้แฟ้มไหนก็แค่หยิบแฟ้มนั้นมา ไม่ต้องมานั่งเขียนใหม่ทั้งหมด

ในโปรเจกต์นี้ ข้อมูล Profiles ถูกเก็บใน **Google Sheet** ทำให้ไม่ต้องติดตั้ง Database แยก และสามารถดู/แก้ไขข้อมูลได้ง่ายจาก Google Sheets โดยตรง

ฟีเจอร์นี้ช่วยให้ระบบยืดหยุ่นมากขึ้น รองรับการใช้งานหลายบริบท และลดความผิดพลาดจากการตั้งค่าผิดสภาพแวดล้อม

---

**ไฟล์ที่เกี่ยวข้องหลัก:**
- `src/backend/scripts/tor-api.py` - Backend API
- `index.html` - Frontend UI และ Logic
- Google Sheet (แท็บ Settings) - ฐานข้อมูล

**Branch ที่พัฒนา:** `feature/multi-profile-settings`
