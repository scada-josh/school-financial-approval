# คู่มือ Deploy โปรเจคขึ้น Render.com (แบบ Step-by-Step)

> **สำหรับใคร?** เด็กมัธยมหรือมือใหม่ที่อยากเอาเว็บไซต์ + API ตัวเองขึ้น Hosting ฟรี แบบไม่ต้องเช่า Server แพงๆ
>
> **ระดับความยาก:** ⭐⭐⭐ (ปานกลาง)  
> **เวลาที่ใช้:** ประมาณ 30-45 นาที

---

## 1. เรา Deploy อะไร?

โปรเจคนี้คือระบบ **School Financial Approval** ที่มี:

- **Frontend:** หน้าเว็บ HTML/CSS/JavaScript (ไฟล์ `index.html`)
- **Backend:** Python API Server (ไฟล์ `tor-api.py`) ที่คุยกับ Google Sheets
- **Database:** ใช้ Google Sheets เป็นฐานข้อมูลแทน (ไม่ต้องตั้ง MySQL/PostgreSQL)

### สิ่งที่ต้องการจาก Render.com

Render.com คือ Platform ที่ให้เรา Run เว็บไซต์ได้ฟรี (มีข้อจำกัดนิดหน่อย) โดยเราไม่ต้องเช่า Server เอง

**สิ่งที่ Render ทำให้เรา:**
1. ให้ Domain ฟรี (เช่น `https://school-financial-approval.onrender.com`)
2. Run Python Server ให้ 24 ชั่วโมง
3. Auto-deploy เมื่อเรา Push โค้ดใหม่

---

## 2. เตรียมโปรเจคให้พร้อม Deploy

ก่อน Deploy ต้องแก้ไขโค้ดให้รองรับการ Run บน Server จริง ไม่ใช่แค่เครื่องตัวเอง

### 2.1 สร้างไฟล์ `requirements.txt`

ไฟล์นี้บอก Render ว่าโปรเจคเราใช้ Library อะไรบ้าง

```txt
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
```

**ทำไมต้องมี?**  
Render ต้องรู้ว่าต้องติดตั้ง Python Library อะไรบ้างก่อน Run โปรเจคเรา

### 2.2 แก้ไข Backend (`tor-api.py`)

ต้องแก้หลายจุดเพื่อรองรับ Render:

#### ✅ จุดที่ 1: รับ PORT จาก Environment Variable

เดิม: Run ที่ port 8765 บนเครื่องตัวเอง
```python
server = HTTPServer(('localhost', 8765), APIHandler)
```

แก้เป็น: รับ PORT ที่ Render กำหนดให้
```python
port = int(os.environ.get('PORT', 8765))
host = os.environ.get('HOST', '0.0.0.0')
server = HTTPServer((host, port), APIHandler)
```

**ทำไม?** Render จะบอกว่าให้ใช้ Port ไหน (มักเป็น 10000 ขึ้นไป) เราต้องยอมรับค่านั้น

#### ✅ จุดที่ 2: Serve Static Files

เดิม: Backend รับเฉพาะ API (`/api/...`) ไฟล์ HTML ต้องเปิดแยก

แก้เป็น: Backend ต้องส่งไฟล์ HTML, CSS, รูปภาพ ให้ด้วย
```python
def _serve_static(self, path):
    # ส่งไฟล์ index.html, assets/, uploads/ ให้ Browser
    # ตรวจสอบความปลอดภัยก่อน (ไม่ให้อ่านไฟล์นอกโฟลเดอร์)
```

**ทำไม?** บน Render เรามีแค่ 1 Service ต้องให้ Backend จัดการทั้ง API และ Static Files

#### ✅ จุดที่ 3: โหลด Google Credentials จาก Environment Variables

เดิม: ใส่ Private Key ตรงๆ ในโค้ด (อันตราย!)
```python
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----"""
```

แก้เป็น: อ่านจาก Environment Variable
```python
PRIVATE_KEY = os.environ.get('GOOGLE_PRIVATE_KEY')
SERVICE_ACCOUNT_EMAIL = os.environ.get('GOOGLE_CLIENT_EMAIL')
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
```

**ทำไม?** ถ้าใส่ Key ในโค้ด แล้ว Push ขึ้น GitHub (Public) คนอื่นเอา Key ไปใช้ได้!

### 2.3 สร้างไฟล์ `render.yaml`

ไฟล์นี้เป็น "แผนผัง" บอก Render ว่าจะสร้าง Service ยังไง:

```yaml
services:
  - type: web
    name: school-financial-approval
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python src/backend/scripts/tor-api.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

### 2.4 สร้างไฟล์ `.env.example`

ไฟล์ตัวอย่างที่บอกว่าต้องตั้งค่าอะไรบ้าง แต่ไม่ใส่ค่าจริง:

```bash
# Google Sheets
SPREADSHEET_ID=ใส่_ID_ที่นี่
GOOGLE_SERVICE_ACCOUNT_JSON=ใส่_JSON_ทั้งหมดที่นี่
```

---

## 3. ขั้นตอน Deploy บน Render.com

### Step 1: Push โค้ดขึ้น GitHub

```bash
git add .
git commit -m "build: prepare for Render deployment"
git push origin feature/multi-profile-settings
```

**⚠️ สำคัญมาก:** อย่า Push ไฟล์ Secrets! (`.env`, `service-account.json`)  
ตรวจสอบว่ามีใน `.gitignore` แล้ว:
```gitignore
.env
*.json.key
service-account*.json
```

### Step 2: สมัครและเชื่อมต่อ Render กับ GitHub

1. ไปที่ [render.com](https://render.com)
2. สมัครด้วย GitHub Account
3. กด **New +** > **Blueprint**
4. เลือก Repository ของโปรเจค
5. กด **Apply**

### Step 3: ตั้งค่า Environment Variables

ไปที่ Dashboard > โปรเจค > **Environment** > เพิ่มตัวแปร:

| ชื่อตัวแปร | ค่าที่ใส่ | เอามาจากไหน |
|---|---|---|
| `SPREADSHEET_ID` | `1Plh_0AodTomKLyP8zrBp9FOriHXVm_uGYIO4TVHSozg` | URL Google Sheet |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | `{ "type": "service_account", ... }` | ไฟล์ `service-account.json` ที่โหลดจาก Google Cloud |

**วิธีเอา JSON:**
```bash
# ในเครื่องตัวเอง เปิดไฟล์แล้ว Copy ทั้งหมด
cat src/backend/config/gen-lang-client-0476777034-d38efeabd270.json
```

แล้ว Paste ทั้งหมดในช่อง Value (จะยาวๆ หน่อย แต่ใช้ได้)

### Step 4: Deploy!

Render จะ:
1. โหลดโค้ดจาก GitHub
2. รัน `pip install -r requirements.txt`
3. รัน `python src/backend/scripts/tor-api.py`
4. เปิดเว็บที่ URL แบบ `https://school-financial-approval.onrender.com`

---

## 4. ปัญหาที่เจอ + วิธีแก้ไข

### ❌ ปัญหา 1: `IndentationError: unexpected indent`

**อาการ:**
```
File "tor-api.py", line 52
    if not PRIVATE_KEY:
IndentationError: unexpected indent
```

**สาเหตุ:** แก้โค้ดแล้วเว้นวรรค (Indent) ผิด ใน Python ต้องเรียงแถวให้ตรงกัน

**วิธีแก้:**
```python
# ผิด ❌
PRIVATE_KEY = os.environ.get('GOOGLE_PRIVATE_KEY')
        if not PRIVATE_KEY:  # ย่อหน้าเกินไป!
            PRIVATE_KEY = ''

# ถูก ✅
PRIVATE_KEY = os.environ.get('GOOGLE_PRIVATE_KEY')
if not PRIVATE_KEY:
    PRIVATE_KEY = ''
```

---

### ❌ ปัญหา 2: API เรียก `localhost:8765` บน Render ไม่ได้

**อาการ:** หน้าเว็บโหลดไม่ได้ ขึ้น Error:
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
localhost:8765/api/tor/projects
```

**สาเหตุ:** ใน JavaScript ระบุ API URL เป็น `http://localhost:8765` ซึ่งเป็นเครื่องตัวเอง บน Render ไม่มี localhost

**วิธีแก้:**

แก้จาก:
```javascript
const API_BASE = 'http://localhost:8765';
```

เป็น:
```javascript
const API_BASE = '';  // หรือ '/' ก็ได้
```

แล้วใช้ Path สัมพันธ์ (Relative Path):
```javascript
fetch(`${API_BASE}/api/tor/projects`)
// กลายเป็น: /api/tor/projects
// Browser จะต่อ Domain เอง: https://xxx.onrender.com/api/tor/projects
```

**ต้องแก้ทุกไฟล์ HTML:**
- `index.html`
- `src/frontend/pages/tor-manager-claude.html`
- `src/frontend/pages/project-tracker.html`
- `src/frontend/pages/school-financial-approval.html`

---

### ❌ ปัญหา 3: รูปทีมงานโหลดไม่ได้ (404)

**อาการ:**
```
Failed to load resource: the server responded with a status of 404
เหมันต์.jpg
```

**สาเหตุ:**
1. ชื่อไฟล์เป็นภาษาไทย (`เหมันต์.jpg`) บาง Server อ่านไม่ค่อยดี
2. URL Encode แล้วยาวเกินไปหรือผิด

**วิธีแก้:**

1. เปลี่ยนชื่อไฟล์เป็นภาษาอังกฤษ:
```bash
mv "assets/images/team/เหมันต์.jpg" assets/images/team/hemon.jpg
```

2. แก้ใน HTML:
```html
<!-- ผิด ❌ -->
<img src="assets/images/team/เหมันต์.jpg">

<!-- ถูก ✅ -->
<img src="assets/images/team/hemon.jpg">
```

**บทเรียน:** ตั้งชื่อไฟล์เป็นภาษาอังกฤษดีที่สุด ไม่มีช่องว่าง ไม่มีอักขระพิเศษ

---

### ❌ ปัญหา 4: Google Credentials ไม่ทำงาน

**อาการ:** API Error หรือข้อมูลจาก Google Sheet ไม่มา

**สาเหตุ:**
1. ลืมตั้งค่า `GOOGLE_SERVICE_ACCOUNT_JSON` ใน Render
2. ใส่ JSON ผิด (ขาด `{}` หรือมี newline ที่ผิด)

**วิธีแก้:**

1. ตรวจสอบว่าตั้งค่าใน Render Dashboard > Environment แล้ว
2. ลอง Test ในเครื่องก่อน:
```bash
export GOOGLE_SERVICE_ACCOUNT_JSON="$(cat src/backend/config/your-file.json)"
python src/backend/scripts/tor-api.py
```
3. ถ้า JSON มี `\n` ใน private_key ต้องแน่ใจว่า Render รับค่าได้ถูกต้อง (บางทีต้อง Escape)

---

## 5. สรุปไฟล์ที่สร้าง/แก้ไขทั้งหมด

| ไฟล์ | ทำอะไร | สถานะ |
|---|---|---|
| `requirements.txt` | บอก Library ที่ต้องติดตั้ง | สร้างใหม่ |
| `render.yaml` | Blueprint สำหรับ Render | สร้างใหม่ |
| `.env.example` | ตัวอย่างตัวแปรสภาพแวดล้อม | สร้างใหม่ |
| `src/backend/scripts/tor-api.py` | แก้รองรับ Render, เอา Key ออก | แก้ไข |
| `index.html` | แก้ API_BASE, แก้ชื่อรูป | แก้ไข |
| `src/frontend/pages/*.html` | แก้ API_BASE ทุกหน้า | แก้ไข |
| `assets/images/team/hemon.jpg` | เปลี่ยนชื่อจากภาษาไทย | เปลี่ยนชื่อ |

---

## 6. เช็คลิสต์ก่อน Deploy ครั้งต่อไป

- [ ] ตรวจสอบว่าไม่มี Secrets ในโค้ด (ใช้ `os.environ.get`)
- [ ] ตรวจสอบว่า `.gitignore` มี `.env` และ `*.json`
- [ ] ตรวจสอบว่า `requirements.txt` อัพเดตแล้ว
- [ ] ตรวจสอบว่า API_BASE เป็น `''` ไม่ใช่ `localhost`
- [ ] ตรวจสอบว่าชื่อไฟล์ภาษาอังกฤษทั้งหมด
- [ ] Push ขึ้น GitHub
- [ ] ตั้งค่า Environment Variables บน Render
- [ ] Deploy และเช็ค Logs

---

## 7. คำศัพท์ที่ควรรู้

| คำศัพท์ | คืออะไร |
|---|---|
| **Deploy** | เอาโค้ดจากเครื่องเราขึ้นไปรันบน Server จริง |
| **Environment Variable** | ตัวแปรที่เก็บค่าความลับ (Password, API Key) ไม่ให้อยู่ในโค้ด |
| **Static Files** | ไฟล์ที่ไม่เปลี่ยนแปลง เช่น HTML, CSS, รูปภาพ |
| **API** | ช่องทางให้ Frontend คุยกับ Backend |
| **Port** | ประตูที่ Server เปิดรอรับการเชื่อมต่อ |
| **Repository** | ที่เก็บโค้ดบน GitHub |
| **Commit** | บันทึกการเปลี่ยนแปลงโค้ด |
| **Push** | ส่ง Commit ขึ้น GitHub |
| **Pull** | โหลดโค้ดใหม่จาก GitHub |
| **Domain** | ชื่อเว็บ เช่น `google.com` |
| **Hosting** | บริการให้เช่าที่เก็บเว็บไซต์ |

---

## 8. แหล่งข้อมูลเพิ่มเติม

- [Render.com Documentation](https://render.com/docs)
- [Google Sheets API Python](https://developers.google.com/sheets/api/quickstart/python)
- [Git คืออะไร? (ภาษาไทย)](https://www.borntodev.com/2021/08/04/git-version-control/)

---

**เขียนโดย:** AI Assistant (Opencode)  
**วันที่:** 15 พฤษภาคม 2026  
**สำหรับโปรเจค:** School Financial Approval Project
