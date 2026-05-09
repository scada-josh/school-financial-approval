# TOR MANAGEMENT SYSTEM (TMS) - Enterprise Architecture Document
## ระบบบริหารและตรวจสอบ TOR ภาครัฐ

**Version:** 1.0  
**Date:** 2026-05-09  
**Classification:** Internal - Government Enterprise Architecture  

---

## 1. SYSTEM OVERVIEW

### 1.1 ภาพรวมระบบ

TMS (TOR Management System) เป็นระบบ Web Application สำหรับจัดทำ ตรวจสอบ และบริหารจัดการ TOR (Terms of Reference) สำหรับโครงการภาครัฐ ระบบรองรับการ Config รูปแบบโครงการหลายประเภท ตรวจสอบความครบถ้วนของ TOR อัตโนมัติ วิเคราะห์ช่องว่าง (Gap Analysis) และใช้ AI ช่วยแนะนำ Requirement ที่เหมาะสม

### 1.2 เป้าหมายระบบ (System Goals)

| Goal ID | เป้าหมาย | Metric |
|---------|---------|--------|
| G-001 | ลดความผิดพลาดในการเขียน TOR | Error Rate < 5% |
| G-002 | ลดเวลาในการจัดทำ TOR | ลดเวลา 50% |
| G-003 | เพิ่มมาตรฐาน TOR ขององค์กร | Compliance Score > 90% |
| G-004 | ลดความเสี่ยงด้านกฎหมายและ Compliance | Risk Score < 3 (1-5 scale) |
| G-005 | เพิ่มความสามารถในการตรวจสอบย้อนหลัง | Audit Trail 100% |
| G-006 | วิเคราะห์คุณภาพ TOR เชิง Data-driven | Dashboard Coverage 100% |

### 1.3 User Persona

| Persona | Role | Goal | Pain Point |
|---------|------|------|------------|
| **เจ้าหน้าที่จัดซื้อ** | จัดทำ TOR | เขียน TOR ได้รวดเร็ว ถูกต้อง | ไม่รู้ว่าต้องใส่อะไรบ้าง |
| **ผู้ตรวจสอบ TOR** | ตรวจสอบความครบถ้วน | ตรวจสอบได้รวดเร็ว | ต้องเช็คมือทีละข้อ |
| **ฝ่ายกฎหมาย** | ตรวจสอบกฎหมาย | มั่นใจว่าถูกกฎหมาย | ไม่รู้ว่าอะไรขาด |
| **ผู้บริหาร** | อนุมัติ TOR | เห็นภาพรวม | ไม่มี Dashboard |
| **IT Governance** | ตรวจสอบ IT Security | ตรวจสอบ Cybersecurity | ไม่มี Checklist |
| **AI Assistant** | ช่วยวิเคราะห์ | แนะนำอัตโนมัติ | ไม่มีข้อมูลเทรน |

### 1.4 Workflow การทำงาน

```
[เริ่มต้น]
    ↓
[เลือกประเภทโครงการ]
    ↓
[ระบบ Load Template ตามประเภท]
    ↓
[แสดง Mandatory/Optional Fields]
    ↓
[ผู้ใช้กรอกข้อมูล TOR]
    ↓
[AI วิเคราะห์ความครบถ้วน]
    ↓
[ระบบตรวจสอบ Compliance]
    ↓
[แสดง Gap Analysis]
    ↓
[ผู้ใช้แก้ไขตามคำแนะนำ]
    ↓
[บันทึก Draft]
    ↓
[ส่งตรวจสอบ]
    ↓
[ผู้ตรวจสอบ Review]
    ↓
[อนุมัติ/ส่งกลับแก้ไข]
    ↓
[Export PDF/DOCX]
    ↓
[Archive]
```

---

## 2. FUNCTIONAL REQUIREMENTS

### 2.1 Module Breakdown

#### M-01: TOR Template Management
- **ใช้ทำอะไร:** จัดการ Template TOR ตามประเภทโครงการ
- **ผู้ใช้งาน:** Admin, เจ้าหน้าที่จัดซื้อ
- **ประโยชน์ทางธุรกิจ:** ลดเวลาเริ่มต้น ลดความผิดพลาด
- **Features:**
  - CRUD Template
  - Clone Template
  - Version Control
  - Template Preview
  - Import/Export Template

#### M-02: Project Type Configuration
- **ใช้ทำอะไร:** Config ประเภทโครงการและกฎเกณฑ์
- **ผู้ใช้งาน:** Admin
- **ประโยชน์ทางธุรกิจ:** รองรับโครงการใหม่ได้ไม่จำกัด
- **Features:**
  - เพิ่ม/แก้ไขประเภทโครงการ
  - กำหนด Mandatory Fields
  - กำหนด Validation Rules
  - กำหนด Compliance Rules
  - Scoring Weight Configuration

#### M-03: Dynamic Form Builder
- **ใช้ทำอะไร:** สร้างฟอร์ม TOR แบบ Dynamic
- **ผู้ใช้งาน:** เจ้าหน้าที่จัดซื้อ
- **ประโยชน์ทางธุรกิจ:** ใช้งานง่าย ไม่ต้องเขียน Code
- **Features:**
  - Drag & Drop Form Builder
  - Field Types: Text, Number, Date, Select, Multi-select, File Upload
  - Conditional Logic
  - Section Management
  - Auto-save Draft

#### M-04: Requirement Validation Engine
- **ใช้ทำอะไร:** ตรวจสอบความครบถ้วนของ TOR อัตโนมัติ
- **ผู้ใช้งาน:** ระบบ (Auto), ผู้ตรวจสอบ
- **ประโยชน์ทางธุรกิจ:** ตรวจสอบได้รวดเร็ว ลดตกหล่น
- **Features:**
  - Mandatory Field Check
  - Data Type Validation
  - Range Validation
  - Cross-field Validation
  - Compliance Rule Check
  - Score Calculation

#### M-05: AI Recommendation Engine
- **ใช้ทำอะไร:** AI วิเคราะห์และแนะนำ Requirement
- **ผู้ใช้งาน:** เจ้าหน้าที่จัดซื้อ, ผู้ตรวจสอบ
- **ประโยชน์ทางธุรกิจ:** เพิ่มคุณภาพ TOR ลดช่องโหว่
- **Features:**
  - Missing Requirement Detection
  - Similar Project Suggestion
  - Risk Analysis
  - Compliance Suggestion
  - TOR Draft Generation
  - Semantic Search

#### M-06: Compliance Checker
- **ใช้ทำอะไร:** ตรวจสอบ Compliance อัตโนมัติ
- **ผู้ใช้งาน:** ฝ่ายกฎหมาย, IT Governance
- **ประโยชน์ทางธุรกิจ:** ลดความเสี่ยงกฎหมาย
- **Features:**
  - พ.ร.บ. จัดซื้อจัดจ้าง Check
  - PDPA Compliance Check
  - Cybersecurity Requirement Check
  - Financial Regulation Check
  - Environmental Regulation Check
  - Compliance Score Calculation

#### M-07: PDPA / Cybersecurity Validation
- **ใช้ทำอะไร:** ตรวจสอบเฉพาะด้าน PDPA และ Cybersecurity
- **ผู้ใช้งาน:** IT Governance, DPO
- **ประโยชน์ทางธุรกิจ:** ป้องกันความเสี่ยงด้านข้อมูล
- **Features:**
  - Personal Data Classification
  - Consent Requirement Check
  - Data Retention Policy Check
  - Security Control Checklist
  - Risk Assessment Matrix
  - DPIA (Data Protection Impact Assessment)

#### M-08: Approval Workflow
- **ใช้ทำอะไร:** จัดการ Workflow การอนุมัติ TOR
- **ผู้ใช้งาน:** ทุก Role
- **ประโยชน์ทางธุรกิจ:** ควบคุมกระบวนการ มี Audit Trail
- **Features:**
  - Multi-level Approval
  - Parallel Approval
  - Conditional Routing
  - Escalation Rule
  - Delegation
  - Approval History

#### M-09: Version Control
- **ใช้ทำอะไร:** จัดการเวอร์ชันของ TOR
- **ผู้ใช้งาน:** ทุก Role
- **ประโยชน์ทางธุรกิจ:** ตรวจสอบย้อนหลังได้
- **Features:**
  - Version History
  - Diff View
  - Rollback
  - Branch Management
  - Compare Versions

#### M-10: Dashboard & Analytics
- **ใช้ทำอะไร:** แสดงผลวิเคราะห์เชิงบริหาร
- **ผู้ใช้งาน:** ผู้บริหาร, ผู้ตรวจสอบ
- **ประโยชน์ทางธุรกิจ:** ตัดสินใจเชิง Data-driven
- **Features:**
  - KPI Dashboard
  - Compliance Heatmap
  - Risk Analysis Chart
  - Project Type Comparison
  - Trend Analysis
  - Custom Report Builder

#### M-11: Google Sheet Integration
- **ใช้ทำอะไร:** เชื่อมต่อข้อมูลจาก Google Sheet
- **ผู้ใช้งาน:** ระบบ (Auto), Admin
- **ประโยชน์ทางธุรกิจ:** ใช้ข้อมูล Master จาก Sheet
- **Features:**
  - Sync Project Type Matrix
  - Sync Compliance Rules
  - Import Historical Data
  - Export Report to Sheet
  - Real-time Sync
  - Conflict Resolution

#### M-12: Export PDF / DOCX
- **ใช้ทำอะไร:** Export TOR เป็นเอกสาร
- **ผู้ใช้งาน:** เจ้าหน้าที่จัดซื้อ
- **ประโยชน์ทางธุรกิจ:** ใช้งานร่วมกับระบบอื่น
- **Features:**
  - Export PDF
  - Export DOCX
  - Export Excel
  - Custom Template
  - Digital Signature
  - Watermark

#### M-13: Audit Log
- **ใช้ทำอะไร:** บันทึกการกระทำทั้งหมด
- **ผู้ใช้งาน:** Admin, ผู้บริหาร
- **ประโยชน์ทางธุรกิจ:** ตรวจสอบย้อนหลัง รองรับ Audit
- **Features:**
  - Action Log
  - Change Log
  - Access Log
  - Export Log
  - Log Retention Policy

---

## 3. NON-FUNCTIONAL REQUIREMENTS

### 3.1 Security

| Requirement | Specification | Standard |
|-------------|---------------|----------|
| Authentication | SSO / LDAP / MFA | SAML 2.0, OAuth 2.0 |
| Authorization | RBAC + ABAC | NIST SP 800-53 |
| Data Encryption | AES-256 (at rest), TLS 1.3 (in transit) | - |
| API Security | OAuth 2.0 + JWT + Rate Limiting | OWASP API Security |
| Password Policy | Min 12 chars, Complexity, Expiry 90 days | NIST 800-63B |
| Session Management | Timeout 30 min, Secure Cookie, HttpOnly | OWASP |

### 3.2 Scalability

| Requirement | Specification |
|-------------|---------------|
| Concurrent Users | 1,000+ concurrent |
| Document Storage | 10TB+ |
| API Throughput | 10,000 req/min |
| Database | Support 10M+ records |
| Horizontal Scaling | Kubernetes Auto-scaling |

### 3.3 Performance

| Requirement | Specification |
|-------------|---------------|
| Page Load Time | < 2 seconds |
| API Response Time | < 500ms (P95) |
| Report Generation | < 10 seconds |
| AI Analysis | < 30 seconds |
| Database Query | < 100ms |

### 3.4 Availability

| Requirement | Specification |
|-------------|---------------|
| Uptime | 99.9% (8.76 hours downtime/year) |
| RTO | 4 hours |
| RPO | 1 hour |
| Maintenance Window | Sunday 00:00-04:00 |

### 3.5 Logging & Monitoring

| Requirement | Specification |
|-------------|---------------|
| Log Retention | 7 years (Audit Log) |
| Application Log | 1 year |
| Log Format | JSON (ELK Stack) |
| Monitoring | Prometheus + Grafana |
| Alerting | PagerDuty / Slack |

### 3.6 Backup & Disaster Recovery

| Requirement | Specification |
|-------------|---------------|
| Backup Frequency | Daily (Full), Hourly (Incremental) |
| Backup Storage | 3 copies (Local, Remote, Cloud) |
| DR Site | Active-Passive |
| DR Testing | Quarterly |

---

## 4. DATABASE DESIGN

### 4.1 ER Diagram

```
[users] 1---* [user_roles] *---1 [roles]
  |
  1---* [tor_documents]
  |       |
  |       1---* [tor_versions]
  |       |
  |       1---* [tor_sections]
  |       |       |
  |       |       1---* [tor_fields]
  |       |               |
  |       |               1---* [field_values]
  |       |
  |       1---* [approval_workflows]
  |       |
  |       1---* [audit_logs]
  |
  1---* [compliance_checks]

[project_types] 1---* [project_type_rules]
  |
  1---* [tor_documents]
  |
  1---* [compliance_rules]

[ai_models] 1---* [ai_predictions]
  |
  1---* [ai_training_data]

[dashboards] 1---* [dashboard_widgets]
  |
  1---* [kpi_definitions]
```

### 4.2 Master Tables

#### 4.2.1 project_types (ประเภทโครงการ)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| code | VARCHAR(50) | รหัสประเภทโครงการ |
| name_th | VARCHAR(255) | ชื่อภาษาไทย |
| name_en | VARCHAR(255) | ชื่อภาษาอังกฤษ |
| description | TEXT | รายละเอียด |
| category | VARCHAR(100) | หมวดหมู่ |
| is_active | BOOLEAN | สถานะ |
| created_at | TIMESTAMP | วันที่สร้าง |
| updated_at | TIMESTAMP | วันที่แก้ไข |

#### 4.2.2 compliance_rules (กฎ Compliance)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| project_type_id | UUID (FK) | อ้างอิงประเภทโครงการ |
| rule_name | VARCHAR(255) | ชื่อกฎ |
| regulation | VARCHAR(255) | กฎหมาย/ระเบียบ |
| description | TEXT | รายละเอียด |
| is_mandatory | BOOLEAN | บังคับหรือไม่ |
| weight | DECIMAL(5,2) | น้ำหนักคะแนน |
| validation_logic | JSONB | เงื่อนไขการตรวจสอบ |
| created_at | TIMESTAMP | วันที่สร้าง |

#### 4.2.3 roles (บทบาท)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| role_name | VARCHAR(100) | ชื่อ Role |
| role_code | VARCHAR(50) | รหัส Role |
| permissions | JSONB | สิทธิ์ |
| description | TEXT | รายละเอียด |

### 4.3 Transaction Tables

#### 4.3.1 tor_documents (เอกสาร TOR)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| project_type_id | UUID (FK) | ประเภทโครงการ |
| document_no | VARCHAR(50) | เลขที่เอกสาร |
| title | VARCHAR(500) | ชื่อโครงการ |
| description | TEXT | รายละเอียด |
| status | VARCHAR(50) | สถานะ (draft, review, approved, rejected) |
| version | INT | เวอร์ชัน |
| created_by | UUID (FK) | ผู้สร้าง |
| created_at | TIMESTAMP | วันที่สร้าง |
| updated_at | TIMESTAMP | วันที่แก้ไข |
| submitted_at | TIMESTAMP | วันที่ส่ง |
| approved_at | TIMESTAMP | วันที่อนุมัติ |
| compliance_score | DECIMAL(5,2) | คะแนน Compliance |
| risk_score | DECIMAL(5,2) | คะแนนความเสี่ยง |
| completeness_pct | DECIMAL(5,2) | เปอร์เซ็นต์ความครบถ้วน |

#### 4.3.2 tor_sections (Section ของ TOR)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| tor_id | UUID (FK) | อ้างอิง TOR |
| section_no | VARCHAR(20) | หมายเลข Section |
| title | VARCHAR(255) | ชื่อ Section |
| description | TEXT | รายละเอียด |
| order_index | INT | ลำดับ |
| is_mandatory | BOOLEAN | บังคับหรือไม่ |

#### 4.3.3 field_values (ค่าของ Fields)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| tor_id | UUID (FK) | อ้างอิง TOR |
| section_id | UUID (FK) | อ้างอิง Section |
| field_name | VARCHAR(255) | ชื่อ Field |
| field_type | VARCHAR(50) | ประเภท Field |
| value | TEXT | ค่า |
| is_valid | BOOLEAN | ผ่าน Validation |
| validation_message | TEXT | ข้อความ Validation |

#### 4.3.4 approval_workflows (Workflow การอนุมัติ)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| tor_id | UUID (FK) | อ้างอิง TOR |
| approver_id | UUID (FK) | ผู้อนุมัติ |
| level | INT | ระดับ |
| status | VARCHAR(50) | สถานะ |
| comments | TEXT | ความคิดเห็น |
| action_at | TIMESTAMP | วันที่ดำเนินการ |

### 4.4 Configuration Tables

#### 4.4.1 validation_rules (กฎ Validation)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| project_type_id | UUID (FK) | ประเภทโครงการ |
| field_name | VARCHAR(255) | ชื่อ Field |
| rule_type | VARCHAR(50) | ประเภทกฎ |
| rule_config | JSONB | การตั้งค่ากฎ |
| error_message | TEXT | ข้อความ Error |

#### 4.4.2 scoring_weights (น้ำหนักคะแนน)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| project_type_id | UUID (FK) | ประเภทโครงการ |
| category | VARCHAR(100) | หมวดหมู่ |
| weight | DECIMAL(5,2) | น้ำหนัก |
| description | TEXT | รายละเอียด |

### 4.5 Audit Tables

#### 4.5.1 audit_logs

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| table_name | VARCHAR(100) | ชื่อ Table |
| record_id | UUID | ID ของ Record |
| action | VARCHAR(50) | การกระทำ |
| old_values | JSONB | ค่าเก่า |
| new_values | JSONB | ค่าใหม่ |
| user_id | UUID (FK) | ผู้ใช้ |
| ip_address | VARCHAR(45) | IP Address |
| user_agent | TEXT | User Agent |
| created_at | TIMESTAMP | วันที่ |

### 4.6 AI Tables

#### 4.6.1 ai_models

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| model_name | VARCHAR(255) | ชื่อ Model |
| model_version | VARCHAR(50) | เวอร์ชัน |
| model_type | VARCHAR(100) | ประเภท |
| status | VARCHAR(50) | สถานะ |
| accuracy | DECIMAL(5,2) | ความแม่นยำ |
| training_date | TIMESTAMP | วันที่เทรน |

#### 4.6.2 ai_predictions

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Primary Key |
| model_id | UUID (FK) | Model |
| tor_id | UUID (FK) | TOR |
| prediction_type | VARCHAR(100) | ประเภท |
| input_data | JSONB | Input |
| output_data | JSONB | Output |
| confidence | DECIMAL(5,2) | ความมั่นใจ |
| created_at | TIMESTAMP | วันที่ |

---

## 5. DASHBOARD & KPI DESIGN

### 5.1 Dashboard สำหรับผู้บริหาร (Executive Dashboard)

**วัตถุประสงค์:** ดูภาพรวมคุณภาพ TOR และความเสี่ยง

| Widget | Type | Metric |
|--------|------|--------|
| TOR Quality Score | Gauge | คะแนนเฉลี่ย TOR |
| Compliance Rate | Percentage | % TOR ผ่าน Compliance |
| Risk Distribution | Pie Chart | การกระจายความเสี่ยง |
| Monthly Trend | Line Chart | เทรนด์คุณภาพรายเดือน |
| Top Risk Projects | Table | โครงการเสี่ยงสูงสุด |
| Project Type Comparison | Bar Chart | เปรียบเทียบประเภท |

**การใช้ตัดสินใจ:**
- ตัดสินใจอนุมัติงบประมาณ
- กำหนดนโยบายการจัดทำ TOR
- ประเมินประสิทธิภาพหน่วยงาน

### 5.2 Dashboard สำหรับเจ้าหน้าที่จัดซื้อ (Procurement Dashboard)

**วัตถุประสงค์:** ติดตามสถานะ TOR และงานของตน

| Widget | Type | Metric |
|--------|------|--------|
| My TOR Status | Kanban | สถานะ TOR ของฉัน |
| Draft Completion | Progress Bar | % ความสมบูรณ์ |
| AI Suggestions | List | คำแนะนำ AI |
| Compliance Issues | Alert List | ปัญหา Compliance |
| Template Usage | Bar Chart | การใช้ Template |

**การใช้ตัดสินใจ:**
- จัดลำดับความสำคัญงาน
- แก้ไข TOR ตามคำแนะนำ
- ติดตาม Deadline

### 5.3 Dashboard สำหรับผู้ตรวจสอบ TOR (Reviewer Dashboard)

**วัตถุประสงค์:** ตรวจสอบ TOR ได้รวดเร็ว

| Widget | Type | Metric |
|--------|------|--------|
| Pending Review | Counter | รอตรวจสอบ |
| Compliance Heatmap | Heatmap | ความครบถ้วนตามหมวด |
| Gap Analysis | Radar Chart | ช่องว่างรายด้าน |
| Risk Score | Gauge | คะแนนความเสี่ยง |
| Comparison View | Side-by-side | เทียบเวอร์ชัน |

**การใช้ตัดสินใจ:**
- อนุมัติ/ส่งกลับแก้ไข
- ระบุปัญหาที่ต้องแก้
- ประเมินความพร้อม

### 5.4 Dashboard สำหรับฝ่ายกฎหมาย (Legal Dashboard)

**วัตถุประสงค์:** ตรวจสอบความถูกต้องทางกฎหมาย

| Widget | Type | Metric |
|--------|------|--------|
| Legal Compliance Rate | Gauge | % ผ่านกฎหมาย |
| Regulation Checklist | Checklist | รายการกฎหมาย |
| High Risk Clauses | Alert List | เงื่อนไขเสี่ยง |
| PDPA Status | Status Indicator | สถานะ PDPA |
| Approval History | Timeline | ประวัติการอนุมัติ |

**การใช้ตัดสินใจ:**
- ยืนยันความถูกต้องกฎหมาย
- ระบุความเสี่ยงทางกฎหมาย
- ให้คำปรึกษา

### 5.5 Dashboard สำหรับ IT Governance (IT Dashboard)

**วัตถุประสงค์:** ตรวจสอบ Security และ IT Requirements

| Widget | Type | Metric |
|--------|------|--------|
| Security Checklist | Checklist | รายการ Security |
| Cybersecurity Score | Gauge | คะแนน Security |
| Data Classification | Pie Chart | การจำแนกข้อมูล |
| Technical Requirements | Table | ความต้องการทางเทคนิค |
| Risk Matrix | Matrix | ตารางความเสี่ยง |

### 5.6 KPI Definitions

| KPI ID | Name | Formula | Target | Frequency |
|--------|------|---------|--------|-----------|
| KPI-001 | TOR Completeness % | (Complete Fields / Total Fields) * 100 | > 95% | Per TOR |
| KPI-002 | Compliance Score | Weighted Average of Compliance Checks | > 90% | Per TOR |
| KPI-003 | Risk Score | Calculated Risk Matrix Score | < 3 (1-5) | Per TOR |
| KPI-004 | Approval Time | Average Days from Submit to Approve | < 5 days | Monthly |
| KPI-005 | Revision Count | Average Number of Revisions | < 2 | Monthly |
| KPI-006 | AI Accuracy | (Correct Predictions / Total) * 100 | > 85% | Monthly |
| KPI-007 | User Satisfaction | Survey Score (1-5) | > 4.0 | Quarterly |
| KPI-008 | System Uptime | (Available Time / Total Time) * 100 | > 99.9% | Monthly |

---

## 6. AI CAPABILITY DESIGN

### 6.1 AI วิเคราะห์ TOR (TOR Analyzer)

| Component | Description |
|-----------|-------------|
| **Input** | TOR Document (Structured Data + Text) |
| **Process** | NLP Analysis + Rule Engine + Pattern Matching |
| **Output** | Analysis Report, Missing Items, Risk Flags |
| **Business Value** | ลดเวลาตรวจสอบ 80% |

**Technical Stack:**
- LLM: GPT-4 / Claude / Llama 3 (Self-hosted option)
- Framework: LangChain / LangGraph
- Vector DB: Pinecone / Weaviate / PGVector
- Embedding: text-embedding-3-large

### 6.2 AI ตรวจ Missing Requirement

| Component | Description |
|-----------|-------------|
| **Input** | Current TOR Fields, Project Type |
| **Process** | Compare with Master Template + Similar Projects |
| **Output** | List of Missing Requirements with Priority |
| **Business Value** | ลดช่องโหว่ Requirement |

**Process Flow:**
1. Extract current TOR structure
2. Query Vector DB for similar projects
3. Compare with Master Template
4. Generate missing items list
5. Score priority based on impact

### 6.3 AI แนะนำหัวข้อ (Topic Suggester)

| Component | Description |
|-----------|-------------|
| **Input** | Project Type, Keywords, Existing Sections |
| **Process** | Semantic Search + Content Generation |
| **Output** | Suggested Topics with Descriptions |
| **Business Value** | เพิ่มความครบถ้วน |

### 6.4 AI วิเคราะห์ความเสี่ยง (Risk Analyzer)

| Component | Description |
|-----------|-------------|
| **Input** | TOR Content, Project Type, Budget |
| **Process** | Risk Classification + Historical Analysis |
| **Output** | Risk Score, Risk Items, Mitigation Suggestions |
| **Business Value** | ลดความเสี่ยงโครงการ |

**Risk Categories:**
- Legal Risk (กฎหมาย)
- Technical Risk (เทคนิค)
- Financial Risk (การเงิน)
- Schedule Risk (กำหนดเวลา)
- Compliance Risk (Compliance)

### 6.5 AI Suggest Compliance

| Component | Description |
|-----------|-------------|
| **Input** | Project Type, Scope, Data Types |
| **Process** | Regulation Mapping + Compliance Checklist |
| **Output** | Required Regulations, Checklist Items |
| **Business Value** | มั่นใจว่าถูกกฎหมาย |

### 6.6 AI Generate TOR Draft

| Component | Description |
|-----------|-------------|
| **Input** | Project Type, Basic Info, Keywords |
| **Process** | Template Filling + Content Generation |
| **Output** | Complete TOR Draft |
| **Business Value** | ลดเวลาเริ่มต้น 70% |

### 6.7 AI Semantic Search

| Component | Description |
|-----------|-------------|
| **Input** | Search Query (Natural Language) |
| **Process** | Vector Search + Reranking |
| **Output** | Relevant TORs, Sections, Clauses |
| **Business Value** | ค้นหาได้เร็ว แม่นยำ |

### 6.8 AI Similar Project Recommendation

| Component | Description |
|-----------|-------------|
| **Input** | Current Project Description |
| **Process** | Similarity Matching + Collaborative Filtering |
| **Output** | Similar Projects with Lessons Learned |
| **Business Value** | เรียนรู้จากโครงการอื่น |

---

## 7. PROJECT CONFIGURATION ENGINE

### 7.1 Configuration Architecture

```
[Project Type Config]
    ├── Basic Info
    ├── Mandatory Fields
    ├── Optional Fields
    ├── Validation Rules
    ├── Compliance Rules
    ├── Scoring Weights
    ├── Workflow Definition
    └── AI Model Config
```

### 7.2 Dynamic Configuration Model

| Config Level | Description | Example |
|--------------|-------------|---------|
| **Organization** | ค่าเริ่มต้นองค์กร | Logo, Address, Default Approver |
| **Project Type** | ค่าเฉพาะประเภทโครงการ | IT Project has Security Section |
| **Template** | ค่า Template | Standard IT TOR Template |
| **Document** | ค่าเฉพาะเอกสาร | Custom Fields for Project X |

### 7.3 Field Configuration

```json
{
  "field_id": "project_budget",
  "field_name": "งบประมาณโครงการ",
  "field_type": "number",
  "is_mandatory": true,
  "validation_rules": [
    {
      "rule_type": "min_value",
      "value": 0,
      "error_message": "งบประมาณต้องมากกว่า 0"
    },
    {
      "rule_type": "max_value",
      "value": 100000000,
      "error_message": "งบประมาณเกินลิมิต"
    }
  ],
  "visibility_rules": [
    {
      "condition": "project_type == 'construction'",
      "show": true
    }
  ],
  "ai_analysis": {
    "risk_threshold": 50000000,
    "risk_level": "high"
  }
}
```

### 7.4 Workflow Configuration

```json
{
  "workflow_id": "it_project_approval",
  "project_type": "it_digital",
  "steps": [
    {
      "step": 1,
      "name": "Procurement Review",
      "approver_role": "procurement_officer",
      "action": "review",
      "timeout_days": 3
    },
    {
      "step": 2,
      "name": "IT Governance Review",
      "approver_role": "it_governance",
      "action": "review",
      "condition": "has_it_component == true"
    },
    {
      "step": 3,
      "name": "Legal Review",
      "approver_role": "legal_officer",
      "action": "review",
      "condition": "budget > 10000000"
    },
    {
      "step": 4,
      "name": "Executive Approval",
      "approver_role": "director",
      "action": "approve",
      "condition": "budget > 50000000"
    }
  ],
  "escalation_rules": {
    "timeout_action": "escalate_to_manager",
    "reminder_interval": 24
  }
}
```

### 7.5 Scoring Configuration

```json
{
  "scoring_id": "it_project_scoring",
  "categories": [
    {
      "name": "Completeness",
      "weight": 0.3,
      "max_score": 100
    },
    {
      "name": "Compliance",
      "weight": 0.4,
      "max_score": 100
    },
    {
      "name": "Risk",
      "weight": 0.2,
      "max_score": 100
    },
    {
      "name": "Quality",
      "weight": 0.1,
      "max_score": 100
    }
  ],
  "thresholds": {
    "pass": 80,
    "warning": 60,
    "fail": 0
  }
}
```

### 7.6 Adding New Project Type

**Process:**
1. Admin เพิ่ม Project Type ใหม่
2. กำหนด Mandatory/Optional Fields
3. กำหนด Validation Rules
4. กำหนด Compliance Rules
5. กำหนด Workflow
6. กำหนด Scoring Weights
7. Train AI Model สำหรับประเภทใหม่
8. Test Configuration
9. Publish

---

## 8. INTEGRATION DESIGN

### 8.1 Integration Architecture

```
[TMS Application]
    ├── [Google Sheet API] ←→ Project Matrix Data
    ├── [SSO/LDAP] ←→ Authentication
    ├── [e-Signature API] ←→ Digital Signature
    ├── [DMS API] ←→ Document Storage
    ├── [Email Service] ←→ Notifications
    ├── [LINE API] ←→ Mobile Notifications
    ├── [AI/LLM API] ←→ AI Features
    └── [Reporting API] ←→ External Reports
```

### 8.2 Google Sheet Integration

**Use Cases:**
1. Import Project Type Matrix from Sheet
2. Sync Compliance Rules
3. Export Analytics Report
4. Backup Configuration

**Technical Details:**
- API: Google Sheets API v4
- Auth: OAuth 2.0 (Service Account)
- Sync Mode: Push (TMS → Sheet) + Pull (Sheet → TMS)
- Frequency: Real-time (Webhook) or Scheduled (Cron)
- Conflict Resolution: Last-write-wins with Audit Log

**Data Mapping:**
| Sheet Tab | TMS Table | Sync Direction |
|-----------|-----------|----------------|
| TOR_Matrix | project_types, compliance_rules | Bidirectional |
| Users | users | Import |
| Audit | audit_logs | Export |

### 8.3 SSO / LDAP Integration

**Protocol:** SAML 2.0 / OAuth 2.0 / OpenID Connect
**Identity Providers:**
- Active Directory
- Google Workspace
- Government SSO (if available)

**Flow:**
1. User → TMS → Identity Provider
2. Identity Provider → Authentication → SAML Response
3. TMS → Validate SAML → Create Session
4. RBAC Mapping from LDAP Groups

### 8.4 e-Signature Integration

**Providers:**
- Thai Digital Signature (CA)
- Docusign
- Adobe Sign

**Flow:**
1. TOR Approved → Trigger e-Sign Request
2. Send to Signers
3. Collect Signatures
4. Store Signed Document
5. Update Status

### 8.5 DMS Integration

**Protocol:** CMIS / REST API
**Systems:**
- Alfresco
- Microsoft SharePoint
- OpenText

**Features:**
- Store TOR Documents
- Version Control
- Document Linking
- Full-text Search

### 8.6 Notification Integration

**Channels:**
| Channel | Use Case | Provider |
|---------|----------|----------|
| Email | Formal notifications, Reports | SMTP / SendGrid |
| LINE | Urgent alerts, Mobile | LINE Messaging API |
| SMS | Critical alerts | Thai SMS Gateway |
| In-app | Real-time updates | WebSocket |

**Events:**
- TOR Submitted
- Approval Required
- Approval Completed
- Revision Requested
- Deadline Approaching

---

## 9. TECHNOLOGY STACK

### 9.1 Frontend

| Layer | Technology | Reason |
|-------|-----------|--------|
| Framework | React 18 / Next.js 14 | SSR, Performance, SEO |
| UI Library | Ant Design / Material-UI | Enterprise Components |
| State Management | Zustand / Redux Toolkit | Scalable |
| Form Management | React Hook Form | Performance |
| Data Fetching | TanStack Query | Caching, Sync |
| Charts | Apache ECharts / Recharts | Rich Visualization |
| PDF Generation | React-PDF / jsPDF | Client-side PDF |
| Build Tool | Vite | Fast Build |

### 9.2 Backend

| Layer | Technology | Reason |
|-------|-----------|--------|
| Language | TypeScript (Node.js) / Python | Type Safety, AI Ecosystem |
| Framework | NestJS (Node) / FastAPI (Python) | Enterprise, OpenAPI |
| API | GraphQL + REST | Flexibility |
| Authentication | Passport.js / FastAPI Security | Multiple Strategies |
| Authorization | CASL / Oso | RBAC + ABAC |
| Validation | Zod / Pydantic | Type-safe |
| Documentation | Swagger / OpenAPI | Auto-generated |

### 9.3 Database

| Type | Technology | Use Case |
|------|-----------|----------|
| Primary DB | PostgreSQL 16 | ACID, JSONB, Full-text |
| Cache | Redis | Session, Cache, Queue |
| Vector DB | pgvector / Pinecone | AI Embeddings |
| Search | Elasticsearch / Meilisearch | Full-text Search |
| Time-series | TimescaleDB | Analytics, Metrics |

### 9.4 AI/LLM

| Component | Technology | Reason |
|-----------|-----------|--------|
| LLM | GPT-4 / Claude 3 / Llama 3 | Performance / Cost / Privacy |
| Framework | LangChain / LangGraph | Orchestration |
| Vector Store | pgvector / Weaviate | RAG |
| Embedding | OpenAI / Ollama | Semantic Search |
| Model Serving | vLLM / TGI | Performance |
| Training | Hugging Face / MLflow | MLOps |

### 9.5 Cloud Architecture

| Provider | Services |
|----------|----------|
| **AWS** | EKS, RDS, S3, Lambda, CloudFront |
| **Azure** | AKS, Azure SQL, Blob, Functions |
| **GCP** | GKE, Cloud SQL, Cloud Storage |
| **Thai Cloud** | C-sky, True IDC (Data Residency) |

**Architecture Pattern:**
- Microservices (Kubernetes)
- API Gateway (Kong / AWS API Gateway)
- Service Mesh (Istio - optional)
- CDN (CloudFront / CloudFlare)
- WAF (AWS WAF / CloudFlare)

### 9.6 DevOps / CI-CD

| Tool | Purpose |
|------|---------|
| Git | Version Control |
| GitHub / GitLab | Repository, CI/CD |
| Docker | Containerization |
| Kubernetes | Orchestration |
| Helm | Package Management |
| ArgoCD | GitOps |
| Prometheus | Monitoring |
| Grafana | Visualization |
| ELK Stack | Logging |
| Jaeger | Tracing |

**CI/CD Pipeline:**
```
[Developer Push]
    ↓
[Unit Test]
    ↓
[Lint / Format]
    ↓
[Build Docker Image]
    ↓
[Integration Test]
    ↓
[Security Scan]
    ↓
[Deploy to Staging]
    ↓
[E2E Test]
    ↓
[Deploy to Production]
    ↓
[Smoke Test]
```

---

## 10. SECURITY & COMPLIANCE

### 10.1 PDPA Compliance

| Requirement | Implementation |
|-------------|----------------|
| Consent Management | Consent Form + Audit Trail |
| Data Minimization | Collect only necessary data |
| Purpose Limitation | Clear data usage policy |
| Data Subject Rights | Access, Rectify, Delete, Portability |
| Data Protection Officer | DPO Contact + Process |
| DPIA | Automated Risk Assessment |
| Data Breach Notification | 72-hour notification process |
| Cross-border Transfer | Standard Contractual Clauses |

### 10.2 Cybersecurity

| Control | Implementation |
|---------|----------------|
| Network Security | VPC, Security Groups, NACL |
| Application Security | OWASP Top 10 Protection |
| Data Security | Encryption at rest + in transit |
| Identity Security | MFA, Password Policy |
| Endpoint Security | API Security, Input Validation |
| Monitoring | SIEM, Intrusion Detection |
| Incident Response | Playbook, Escalation |
| Vulnerability Management | Monthly Scan, Patch Management |

### 10.3 Audit Trail

| Requirement | Implementation |
|-------------|----------------|
| Log Everything | All CRUD operations |
| Immutable Logs | Write-once storage |
| Log Integrity | Digital Signature |
| Log Retention | 7 years |
| Log Access | RBAC for log viewing |
| Real-time Alert | Anomaly Detection |

### 10.4 Access Control

**RBAC Model:**
```
[User] → [Role] → [Permission] → [Resource]
```

**Roles:**
| Role | Permissions |
|------|-------------|
| System Admin | Full Access |
| Procurement Manager | Manage TOR, Reports |
| Procurement Officer | Create/Edit TOR |
| TOR Reviewer | Review, Comment |
| Legal Officer | Legal Review |
| IT Governance | Security Review |
| Executive | Approve, Dashboard |
| Auditor | View Only, Audit Log |

**ABAC (Attribute-Based):**
- Department-based access
- Project-type based access
- Classification-based access
- Time-based restrictions

### 10.5 Data Retention

| Data Type | Retention Period | Action After |
|-----------|-----------------|--------------|
| Active TOR | 7 years | Archive |
| Draft TOR | 1 year | Delete |
| Audit Log | 7 years | Archive |
| AI Training Data | 3 years | Anonymize |
| Session Log | 90 days | Delete |
| Backup | 1 year | Delete |

### 10.6 Encryption

| Layer | Method |
|-------|--------|
| Database | AES-256 (TDE) |
| Files | AES-256 (Client-side) |
| API | TLS 1.3 |
| Password | bcrypt / Argon2 |
| Secrets | HashiCorp Vault |
| Backup | AES-256 |

### 10.7 Zero Trust Architecture

**Principles:**
1. Never Trust, Always Verify
2. Assume Breach
3. Verify Explicitly
4. Use Least Privilege Access

**Implementation:**
- Micro-segmentation
- Continuous Authentication
- Device Trust
- Real-time Risk Assessment

### 10.8 OWASP Compliance

| Threat | Mitigation |
|--------|-----------|
| Injection | Parameterized Queries |
| Broken Auth | MFA, Session Mgmt |
| Sensitive Data Exposure | Encryption |
| XXE | Disable XML External Entities |
| Broken Access Control | RBAC + ABAC |
| Security Misconfiguration | Hardening Guide |
| XSS | Content Security Policy |
| Insecure Deserialization | Input Validation |
| Known Vulnerabilities | Dependency Scan |
| Insufficient Logging | Comprehensive Audit |

---

## 11. UX/UI DESIGN

### 11.1 Design Principles

1. **Simplicity** - ลดขั้นตอน ลดความซับซ้อน
2. **Clarity** - ชัดเจน ไม่คลุมเครือ
3. **Efficiency** - ทำงานได้เร็ว ลดคลิก
4. **Consistency** - รูปแบบสม่ำเสมอ
5. **Accessibility** - รองรับทุกคน

### 11.2 Page Designs

#### 11.2.1 Dashboard Page

**Layout:**
```
┌─────────────────────────────────────┐
│  Header (Logo, User, Notification)  │
├──────────┬──────────────────────────┤
│          │                          │
│ Sidebar  │   KPI Cards (4 boxes)    │
│          │                          │
│ - Dashboard├─────────────────────────┤
│ - My TORs│   Charts (2 columns)     │
│ - Review │                          │
│ - Admin  │   Data Tables            │
│          │                          │
└──────────┴──────────────────────────┘
```

**Features:**
- Drag & Drop Widgets
- Customize Layout
- Real-time Updates
- Export to PDF/Excel

#### 11.2.2 TOR Builder Page

**Layout:**
```
┌─────────────────────────────────────┐
│  Progress Bar (Step 1 of 5)         │
├─────────────────────────────────────┤
│                                     │
│  [Section Selector]  [Form Area]    │
│                                     │
│  - Section 1        [Field 1    ]   │
│  - Section 2        [Field 2    ]   │
│  - Section 3        [Field 3    ]   │
│  ✓ Section 4        [Field 4    ]   │
│    Section 5                        │
│                                     │
│  [AI Suggestions Panel]             │
│  - Suggestion 1                     │
│  - Suggestion 2                     │
│                                     │
├─────────────────────────────────────┤
│  [Save Draft] [Preview] [Submit]    │
└─────────────────────────────────────┘
```

**Features:**
- Step-by-step Wizard
- Section Navigation
- AI Suggestions Sidebar
- Real-time Validation
- Auto-save Draft
- Progress Indicator

#### 11.2.3 Compliance Checker Page

**Layout:**
```
┌─────────────────────────────────────┐
│  TOR Title: [Project X]             │
├─────────────────────────────────────┤
│                                     │
│  Compliance Score: [85%] 🟡         │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Checklist                   │    │
│  │ ✓ Item 1 (Legal)           │    │
│  │ ✓ Item 2 (PDPA)            │    │
│  │ ⚠ Item 3 (Security)        │    │
│  │ ✗ Item 4 (Financial)       │    │
│  │ ✓ Item 5 (Technical)       │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Gap Analysis                │    │
│  │ Missing: Data Retention     │    │
│  │ Missing: Risk Assessment    │    │
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

#### 11.2.4 AI Assistant Page

**Layout:**
```
┌─────────────────────────────────────┐
│  🤖 AI Assistant                    │
├─────────────────────────────────────┤
│                                     │
│  [Chat Interface]                   │
│                                     │
│  User: Analyze this TOR            │
│  AI: I've analyzed your TOR...     │
│       - Risk Score: Medium          │
│       - Missing: Security Section   │
│       - Suggestion: Add...          │
│                                     │
│  [Quick Actions]                    │
│  [Analyze] [Suggest] [Compare]     │
│                                     │
└─────────────────────────────────────┘
```

### 11.3 Mobile Responsiveness

**Breakpoints:**
| Device | Width | Layout |
|--------|-------|--------|
| Desktop | > 1200px | Full sidebar + content |
| Tablet | 768-1200px | Collapsed sidebar |
| Mobile | < 768px | Bottom navigation |

**Mobile Features:**
- Touch-friendly buttons
- Swipe navigation
- Offline mode (PWA)
- Push notifications
- Camera integration (scan documents)

### 11.4 Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|-------------|----------------|
| Keyboard Navigation | Tab order, Shortcuts |
| Screen Reader | ARIA labels, Alt text |
| Color Contrast | Ratio >= 4.5:1 |
| Font Size | Adjustable 100-200% |
| Focus Indicator | Visible focus ring |
| Error Identification | Clear error messages |

---

## 12. OUTPUT FORMAT & DELIVERABLES

### 12.1 Architecture Diagram (Text-based)

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Web App │  │ Mobile   │  │  Tablet  │  │  Admin   │   │
│  │ (React)  │  │ (PWA)    │  │ (Responsive)│  (Panel) │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼────────────┼────────────┼────────────┼──────────┘
        │            │            │            │
        └────────────┴─────┬──────┴────────────┘
                           │ HTTPS/TLS 1.3
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY                             │
│                    (Kong / AWS API GW)                       │
│  - Rate Limiting                                             │
│  - Authentication (JWT)                                      │
│  - Request Routing                                           │
│  - Load Balancing                                            │
└───────┬───────────────────────────────┬─────────────────────┘
        │                               │
        ▼                               ▼
┌───────────────┐            ┌───────────────────────┐
│   GRAPHQL     │            │      REST API         │
│   SERVER      │            │      (NestJS)         │
│  (Apollo)     │            │                       │
└───────┬───────┘            └───────────┬───────────┘
        │                                │
        ▼                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   MICROSERVICES LAYER                        │
│                                                              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │  TOR    │ │  AI     │ │Compliance│ │  User   │           │
│  │ Service │ │ Service │ │ Service  │ │ Service │           │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘           │
│       │           │           │           │                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ Approval│ │Dashboard│ │  Audit  │ │Notification│        │
│  │ Service │ │ Service │ │ Service │ │  Service  │          │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘           │
│       │           │           │           │                 │
└───────┼───────────┼───────────┼───────────┼─────────────────┘
        │           │           │           │
        └───────────┴─────┬─────┴───────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │PostgreSQL│  │  Redis   │  │pgvector  │  │Elasticsearch│ │
│  │(Primary) │  │ (Cache)  │  │(Vector)  │  │ (Search)  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │   S3     │  │  Kafka   │  │TimescaleDB│                 │
│  │(Storage) │  │ (Queue)  │  │(Metrics) │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                 EXTERNAL INTEGRATIONS                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Google  │  │   SSO    │  │e-Signature│  │   DMS    │   │
│  │  Sheet   │  │ / LDAP   │  │          │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Email   │  │   LINE   │  │  AI/LLM  │                  │
│  │ Service  │  │  Notify  │  │   API    │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### 12.2 API Design

#### REST API Endpoints

**TOR Management:**
```
POST   /api/v1/tors              # Create TOR
GET    /api/v1/tors              # List TORs
GET    /api/v1/tors/:id          # Get TOR Detail
PUT    /api/v1/tors/:id          # Update TOR
DELETE /api/v1/tors/:id          # Delete TOR (Soft)
POST   /api/v1/tors/:id/submit   # Submit TOR
POST   /api/v1/tors/:id/approve  # Approve TOR
POST   /api/v1/tors/:id/reject   # Reject TOR
GET    /api/v1/tors/:id/versions # Get Versions
POST   /api/v1/tors/:id/clone    # Clone TOR
```

**Project Type Configuration:**
```
GET    /api/v1/project-types              # List Project Types
POST   /api/v1/project-types              # Create Project Type
GET    /api/v1/project-types/:id          # Get Project Type
PUT    /api/v1/project-types/:id          # Update Project Type
DELETE /api/v1/project-types/:id          # Delete Project Type
GET    /api/v1/project-types/:id/rules    # Get Rules
POST   /api/v1/project-types/:id/rules    # Add Rule
```

**AI Services:**
```
POST   /api/v1/ai/analyze          # Analyze TOR
POST   /api/v1/ai/suggest          # Get Suggestions
POST   /api/v1/ai/generate         # Generate Draft
POST   /api/v1/ai/search           # Semantic Search
POST   /api/v1/ai/risk-assessment  # Risk Assessment
```

**Compliance:**
```
POST   /api/v1/compliance/check    # Check Compliance
GET    /api/v1/compliance/rules    # Get Compliance Rules
GET    /api/v1/compliance/score/:torId  # Get Score
```

**Dashboard:**
```
GET    /api/v1/dashboard/kpi       # Get KPI Data
GET    /api/v1/dashboard/analytics # Get Analytics
GET    /api/v1/dashboard/reports   # Get Reports
```

#### GraphQL Schema

```graphql
type TOR {
  id: ID!
  projectType: ProjectType!
  documentNo: String!
  title: String!
  status: TORStatus!
  version: Int!
  sections: [TORSection!]!
  complianceScore: Float
  riskScore: Float
  completenessPct: Float
  createdBy: User!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type ProjectType {
  id: ID!
  code: String!
  nameTh: String!
  nameEn: String!
  category: String!
  rules: [ComplianceRule!]!
  isActive: Boolean!
}

type ComplianceRule {
  id: ID!
  ruleName: String!
  regulation: String!
  isMandatory: Boolean!
  weight: Float!
}

type Query {
  tors(filter: TORFilterInput, pagination: PaginationInput): TORConnection!
  tor(id: ID!): TOR
  projectTypes: [ProjectType!]!
  projectType(id: ID!): ProjectType
  dashboardKPIs: DashboardKPI!
  complianceScore(torId: ID!): ComplianceResult!
}

type Mutation {
  createTOR(input: CreateTORInput!): TOR!
  updateTOR(id: ID!, input: UpdateTORInput!): TOR!
  submitTOR(id: ID!): TOR!
  approveTOR(id: ID!, input: ApprovalInput!): TOR!
  analyzeTOR(id: ID!): AIAnalysisResult!
}
```

### 12.3 User Flow Diagrams

#### Flow 1: Create TOR

```
[User Login]
    ↓
[Select Project Type]
    ↓
[System Load Template]
    ↓
[Fill Basic Info]
    ↓
[Fill Sections]
    ├── Auto-save Draft
    └── Real-time Validation
    ↓
[AI Analysis]
    ├── Check Completeness
    ├── Check Compliance
    └── Generate Suggestions
    ↓
[Review Suggestions]
    ├── Accept
    └── Ignore
    ↓
[Preview TOR]
    ↓
[Submit for Review]
    ↓
[Notification to Reviewer]
```

#### Flow 2: Review & Approve

```
[Reviewer Login]
    ↓
[View Pending TORs]
    ↓
[Open TOR]
    ├── View Details
    ├── View Compliance Score
    └── View AI Analysis
    ↓
[Review]
    ├── Approve
    │   └── [Next Level / Final]
    └── Reject
        └── [Add Comments]
        └── [Return to Owner]
    ↓
[Notification]
```

#### Flow 3: AI-Assisted TOR Creation

```
[Enter Keywords / Description]
    ↓
[AI Generate Draft]
    ├── Analyze Requirements
    ├── Match Similar Projects
    └── Generate Content
    ↓
[Review AI Draft]
    ├── Edit Content
    ├── Add Sections
    └── Remove Sections
    ↓
[Run Compliance Check]
    ↓
[Finalize]
```

### 12.4 Module Breakdown Matrix

| Module | Sub-modules | Complexity | Priority | Team Size | Duration |
|--------|------------|------------|----------|-----------|----------|
| **Core** | | | | | |
 | User Management | Auth, RBAC, Profile | Medium | P0 | 2 | 2 weeks |
 | TOR Builder | Form Builder, Sections | High | P0 | 3 | 4 weeks |
 | Template Mgmt | CRUD, Version, Clone | Medium | P0 | 2 | 2 weeks |
| **AI** | | | | | |
 | AI Analyzer | NLP, Analysis | High | P1 | 3 | 6 weeks |
 | AI Suggester | Semantic Search | High | P1 | 2 | 4 weeks |
 | AI Generator | Content Gen | High | P2 | 2 | 4 weeks |
| **Compliance** | | | | | |
 | Compliance Checker | Rules Engine | High | P0 | 2 | 3 weeks |
 | PDPA Validator | PDPA Rules | Medium | P1 | 1 | 2 weeks |
 | Security Checker | Security Rules | Medium | P1 | 1 | 2 weeks |
| **Workflow** | | | | | |
 | Approval Workflow | Multi-level | High | P0 | 2 | 3 weeks |
 | Notification | Email, LINE | Low | P1 | 1 | 1 week |
| **Integration** | | | | | |
 | Google Sheet | Sync, Import | Medium | P1 | 2 | 2 weeks |
 | SSO/LDAP | Auth Integration | Medium | P1 | 1 | 1 week |
 | Export | PDF, DOCX | Low | P2 | 1 | 1 week |
| **Dashboard** | | | | | |
 | Executive Dashboard | KPI, Charts | Medium | P1 | 2 | 2 weeks |
 | Operational Dashboard | Kanban, Lists | Low | P2 | 1 | 1 week |
| **Infrastructure** | | | | | |
 | CI/CD | Pipeline | Medium | P0 | 1 | 2 weeks |
 | Monitoring | Logging, Alert | Medium | P1 | 1 | 1 week |

### 12.5 Risk Matrix

| Risk ID | Risk | Impact | Likelihood | Mitigation | Owner |
|---------|------|--------|------------|------------|-------|
| R-001 | AI Model Bias | High | Medium | Diverse Training Data, Human Review | AI Team |
| R-002 | Data Breach | Critical | Low | Encryption, Access Control, Audit | Security Team |
| R-003 | Regulatory Change | High | High | Flexible Config, Regular Updates | Legal Team |
| R-004 | Performance Issue | Medium | Medium | Caching, CDN, Optimization | DevOps Team |
| R-005 | User Adoption | High | Medium | Training, UX Design, Support | Product Team |
| R-006 | Integration Failure | Medium | Medium | Fallback Mechanism, Retry Logic | Integration Team |
| R-007 | Scope Creep | Medium | High | Change Control, MVP First | PM |
| R-008 | Vendor Lock-in | Medium | Low | Open Standards, Multi-cloud | Architect |

### 12.6 KPI Matrix

| KPI | Measurement | Frequency | Target | Responsible |
|-----|------------|-----------|--------|-------------|
| **Efficiency** | | | | |
| TOR Creation Time | Average hours | Monthly | < 8 hours | Procurement |
| Review Cycle Time | Average days | Monthly | < 3 days | Reviewer |
| Revision Count | Average per TOR | Monthly | < 2 | Procurement |
| **Quality** | | | | |
| Compliance Rate | % Pass | Monthly | > 95% | Compliance |
| AI Accuracy | % Correct | Monthly | > 85% | AI Team |
| Error Rate | % Rejected | Monthly | < 5% | Quality Team |
| **System** | | | | |
| Uptime | % Available | Monthly | > 99.9% | DevOps |
| Response Time | P95 ms | Daily | < 500ms | DevOps |
| User Satisfaction | Score 1-5 | Quarterly | > 4.0 | Product |
| **Business** | | | | |
| Cost Savings | % Reduced | Quarterly | > 30% | Finance |
| Risk Reduction | % Reduced | Quarterly | > 40% | Risk Team |
| Adoption Rate | % Active Users | Monthly | > 80% | Product |

### 12.7 Implementation Roadmap

#### Phase 1: MVP (Months 1-3)
**Goal:** Core TOR Management
- [ ] User Management & Authentication
- [ ] Project Type Configuration
- [ ] TOR Builder (Basic)
- [ ] Template Management
- [ ] Approval Workflow (Simple)
- [ ] Basic Dashboard

#### Phase 2: Intelligence (Months 4-6)
**Goal:** AI & Compliance
- [ ] AI Analyzer (Basic)
- [ ] Compliance Checker
- [ ] PDPA Validator
- [ ] Advanced Dashboard
- [ ] Export PDF/DOCX
- [ ] Google Sheet Integration

#### Phase 3: Enterprise (Months 7-9)
**Goal:** Scale & Integration
- [ ] AI Generator
- [ ] Semantic Search
- [ ] Advanced Workflow
- [ ] SSO/LDAP Integration
- [ ] e-Signature Integration
- [ ] DMS Integration

#### Phase 4: Optimization (Months 10-12)
**Goal:** Performance & AI Maturity
- [ ] Advanced AI Models
- [ ] Predictive Analytics
- [ ] Advanced Dashboard
- [ ] Performance Optimization
- [ ] Disaster Recovery
- [ ] Security Hardening

**Timeline:**
```
Month:  1   2   3   4   5   6   7   8   9   10  11  12
        ├─────── MVP ───────┤
                            ├─── Intelligence ───┤
                                                ├─── Enterprise ───┤
                                                                    ├── Optimization ─┤
        ├─────────────────────────── V1.0 Release ───────────────────────────────┤
```

---

## APPENDIX A: GOOGLE SHEET DATA STRUCTURE

### Sheet Tabs for Import

#### A.1 project_types
| code | name_th | name_en | category | is_active |
|------|---------|---------|----------|-----------|
| PROCUREMENT | จัดซื้อจัดจ้างทั่วไป | General Procurement | General | TRUE |
| IT_DIGITAL | IT / Digital Transformation | IT/Digital Transformation | IT | TRUE |
| CLOUD | Cloud / Data Center | Cloud/Data Center | IT | TRUE |
| AI_BIGDATA | AI / Big Data | AI/Big Data | IT | TRUE |
| CYBERSECURITY | Cybersecurity | Cybersecurity | IT | TRUE |
| SMART_CITY | Smart City / IoT | Smart City/IoT | IT | TRUE |
| ERP | ERP / Financial | ERP/Financial | Finance | TRUE |
| OPEN_DATA | Open Data | Open Data | Data | TRUE |
| DATA_EXCHANGE | Data Exchange | Data Exchange | Data | TRUE |
| TELECOM | Telecommunications | Telecommunications | Infrastructure | TRUE |
| HEALTHCARE | Healthcare | Healthcare | Social | TRUE |
| EDUCATION | Education | Education | Social | TRUE |
| CONSTRUCTION | Construction | Construction | Infrastructure | TRUE |
| CONSULTING | Consulting | Consulting | Service | TRUE |
| RESEARCH | Research & Innovation | Research & Innovation | R&D | TRUE |

#### A.2 compliance_rules
| project_type_code | rule_name | regulation | is_mandatory | weight | description |
|-------------------|-----------|------------|--------------|--------|-------------|
| PROCUREMENT | TOR_C completeness | พ.ร.บ. จัดซื้อจัดจ้าง 2560 | TRUE | 20 | ต้องมี TOR ครบถ้วน |
| IT_DIGITAL | PDPA_Check | PDPA 2562 | TRUE | 25 | ตรวจสอบ PDPA |
| IT_DIGITAL | Security_Check | พ.ร.บ. ไซเบอร์ 2562 | TRUE | 25 | ตรวจสอบ Security |
| CLOUD | Data_Residency | PDPA 2562 | TRUE | 30 | ตรวจสอบ Data Residency |
| AI_BIGDATA | AI_Ethics | จริยธรรม AI | TRUE | 20 | ตรวจสอบ AI Ethics |

#### A.3 validation_rules
| project_type_code | field_name | rule_type | rule_config | error_message |
|-------------------|------------|-----------|-------------|---------------|
| PROCUREMENT | budget | min_value | {"value": 0} | งบประมาณต้องมากกว่า 0 |
| PROCUREMENT | budget | max_value | {"value": 100000000} | งบประมาณเกินลิมิต |
| IT_DIGITAL | has_security_plan | required | {} | ต้องมี Security Plan |

#### A.4 scoring_weights
| project_type_code | category | weight | description |
|-------------------|----------|--------|-------------|
| PROCUREMENT | completeness | 30 | ความครบถ้วน |
| PROCUREMENT | compliance | 40 | ความถูกต้องตามกฎหมาย |
| PROCUREMENT | risk | 20 | ความเสี่ยง |
| PROCUREMENT | quality | 10 | คุณภาพ |

#### A.5 kpi_definitions
| kpi_id | name | formula | target | frequency |
|--------|------|---------|--------|-----------|
| KPI-001 | TOR Completeness % | (Complete/Total)*100 | 95 | per_tor |
| KPI-002 | Compliance Score | Weighted Average | 90 | per_tor |
| KPI-003 | Risk Score | Calculated | 3 | per_tor |
| KPI-004 | Approval Time | AVG(days) | 5 | monthly |
| KPI-005 | Revision Count | AVG(count) | 2 | monthly |

---

## APPENDIX B: GOOGLE APPS SCRIPT FOR SHEET CREATION

```javascript
/**
 * สคริปต์นี้ใช้สร้าง Sheet ใหม่และนำเข้าข้อมูล Configuration
 * 
 * วิธีใช้:
 * 1. เปิด Google Sheet (https://docs.google.com/spreadsheets/d/1Plh_0AodTomKLyP8zrBp9FOriHXVm_uGYIO4TVHSozg)
 * 2. เมนู Extensions > Apps Script
 * 3. วางโค้ดนี้ลงไป
 * 4. กด Run
 */

function setupTORManagementSheets() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  
  // สร้าง Sheet: project_types
  const ptSheet = spreadsheet.getSheetByName('project_types') || spreadsheet.insertSheet('project_types');
  ptSheet.clear();
  ptSheet.getRange(1, 1, 1, 5).setValues([['code', 'name_th', 'name_en', 'category', 'is_active']]);
  ptSheet.getRange(2, 1, 15, 5).setValues([
    ['PROCUREMENT', 'จัดซื้อจัดจ้างทั่วไป', 'General Procurement', 'General', 'TRUE'],
    ['IT_DIGITAL', 'IT / Digital Transformation', 'IT/Digital Transformation', 'IT', 'TRUE'],
    ['CLOUD', 'Cloud / Data Center', 'Cloud/Data Center', 'IT', 'TRUE'],
    ['AI_BIGDATA', 'AI / Big Data', 'AI/Big Data', 'IT', 'TRUE'],
    ['CYBERSECURITY', 'Cybersecurity', 'Cybersecurity', 'IT', 'TRUE'],
    ['SMART_CITY', 'Smart City / IoT', 'Smart City/IoT', 'IT', 'TRUE'],
    ['ERP', 'ERP / Financial', 'ERP/Financial', 'Finance', 'TRUE'],
    ['OPEN_DATA', 'Open Data', 'Open Data', 'Data', 'TRUE'],
    ['DATA_EXCHANGE', 'Data Exchange', 'Data Exchange', 'Data', 'TRUE'],
    ['TELECOM', 'Telecommunications', 'Telecommunications', 'Infrastructure', 'TRUE'],
    ['HEALTHCARE', 'Healthcare', 'Healthcare', 'Social', 'TRUE'],
    ['EDUCATION', 'Education', 'Education', 'Social', 'TRUE'],
    ['CONSTRUCTION', 'Construction', 'Construction', 'Infrastructure', 'TRUE'],
    ['CONSULTING', 'Consulting', 'Consulting', 'Service', 'TRUE'],
    ['RESEARCH', 'Research & Innovation', 'Research & Innovation', 'R&D', 'TRUE']
  ]);
  
  // สร้าง Sheet: compliance_rules
  const crSheet = spreadsheet.getSheetByName('compliance_rules') || spreadsheet.insertSheet('compliance_rules');
  crSheet.clear();
  crSheet.getRange(1, 1, 1, 6).setValues([['project_type_code', 'rule_name', 'regulation', 'is_mandatory', 'weight', 'description']]);
  crSheet.getRange(2, 1, 5, 6).setValues([
    ['PROCUREMENT', 'TOR_Completeness', 'พ.ร.บ. จัดซื้อจัดจ้าง 2560', 'TRUE', '20', 'ต้องมี TOR ครบถ้วน'],
    ['IT_DIGITAL', 'PDPA_Check', 'PDPA 2562', 'TRUE', '25', 'ตรวจสอบ PDPA'],
    ['IT_DIGITAL', 'Security_Check', 'พ.ร.บ. ไซเบอร์ 2562', 'TRUE', '25', 'ตรวจสอบ Security'],
    ['CLOUD', 'Data_Residency', 'PDPA 2562', 'TRUE', '30', 'ตรวจสอบ Data Residency'],
    ['AI_BIGDATA', 'AI_Ethics', 'จริยธรรม AI', 'TRUE', '20', 'ตรวจสอบ AI Ethics']
  ]);
  
  // สร้าง Sheet: validation_rules
  const vrSheet = spreadsheet.getSheetByName('validation_rules') || spreadsheet.insertSheet('validation_rules');
  vrSheet.clear();
  vrSheet.getRange(1, 1, 1, 5).setValues([['project_type_code', 'field_name', 'rule_type', 'rule_config', 'error_message']]);
  vrSheet.getRange(2, 1, 3, 5).setValues([
    ['PROCUREMENT', 'budget', 'min_value', '{"value": 0}', 'งบประมาณต้องมากกว่า 0'],
    ['PROCUREMENT', 'budget', 'max_value', '{"value": 100000000}', 'งบประมาณเกินลิมิต'],
    ['IT_DIGITAL', 'has_security_plan', 'required', '{}', 'ต้องมี Security Plan']
  ]);
  
  // สร้าง Sheet: scoring_weights
  const swSheet = spreadsheet.getSheetByName('scoring_weights') || spreadsheet.insertSheet('scoring_weights');
  swSheet.clear();
  swSheet.getRange(1, 1, 1, 4).setValues([['project_type_code', 'category', 'weight', 'description']]);
  swSheet.getRange(2, 1, 4, 4).setValues([
    ['PROCUREMENT', 'completeness', '30', 'ความครบถ้วน'],
    ['PROCUREMENT', 'compliance', '40', 'ความถูกต้องตามกฎหมาย'],
    ['PROCUREMENT', 'risk', '20', 'ความเสี่ยง'],
    ['PROCUREMENT', 'quality', '10', 'คุณภาพ']
  ]);
  
  // สร้าง Sheet: kpi_definitions
  const kpiSheet = spreadsheet.getSheetByName('kpi_definitions') || spreadsheet.insertSheet('kpi_definitions');
  kpiSheet.clear();
  kpiSheet.getRange(1, 1, 1, 5).setValues([['kpi_id', 'name', 'formula', 'target', 'frequency']]);
  kpiSheet.getRange(2, 1, 5, 5).setValues([
    ['KPI-001', 'TOR Completeness %', '(Complete/Total)*100', '95', 'per_tor'],
    ['KPI-002', 'Compliance Score', 'Weighted Average', '90', 'per_tor'],
    ['KPI-003', 'Risk Score', 'Calculated', '3', 'per_tor'],
    ['KPI-004', 'Approval Time', 'AVG(days)', '5', 'monthly'],
    ['KPI-005', 'Revision Count', 'AVG(count)', '2', 'monthly']
  ]);
  
  // สร้าง Sheet: system_config
  const configSheet = spreadsheet.getSheetByName('system_config') || spreadsheet.insertSheet('system_config');
  configSheet.clear();
  configSheet.getRange(1, 1, 1, 3).setValues([['config_key', 'config_value', 'description']]);
  configSheet.getRange(2, 1, 5, 3).setValues([
    ['APP_NAME', 'TOR Management System', 'ชื่อระบบ'],
    ['VERSION', '1.0.0', 'เวอร์ชัน'],
    ['DEFAULT_LANG', 'th', 'ภาษาเริ่มต้น'],
    ['SESSION_TIMEOUT', '1800', 'เวลา Session (วินาที)'],
    ['MAX_FILE_SIZE', '10485760', 'ขนาดไฟล์สูงสุด (ไบต์)']
  ]);
  
  Logger.log('Setup completed successfully!');
}

/**
 * ฟังก์ชันสำหรับ Export ข้อมูลจาก TMS มา Sheet
 */
function exportTORData(torData) {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  let torSheet = spreadsheet.getSheetByName('tor_documents');
  
  if (!torSheet) {
    torSheet = spreadsheet.insertSheet('tor_documents');
    torSheet.getRange(1, 1, 1, 8).setValues([
      ['document_no', 'title', 'project_type', 'status', 'compliance_score', 'risk_score', 'completeness_pct', 'created_at']
    ]);
  }
  
  const lastRow = torSheet.getLastRow();
  torSheet.getRange(lastRow + 1, 1, 1, 8).setValues([[
    torData.documentNo,
    torData.title,
    torData.projectType,
    torData.status,
    torData.complianceScore,
    torData.riskScore,
    torData.completenessPct,
    new Date().toISOString()
  ]]);
}

/**
 * ฟังก์ชันสำหรับ Sync ข้อมูลจาก Sheet ไป TMS
 */
function syncToTMS() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const ptSheet = spreadsheet.getSheetByName('project_types');
  
  if (!ptSheet) {
    Logger.log('project_types sheet not found');
    return;
  }
  
  const data = ptSheet.getDataRange().getValues();
  const headers = data[0];
  const rows = data.slice(1);
  
  // แปลงเป็น JSON
  const projectTypes = rows.map(row => {
    const obj = {};
    headers.forEach((header, index) => {
      obj[header] = row[index];
    });
    return obj;
  });
  
  Logger.log(JSON.stringify(projectTypes, null, 2));
  
  // TODO: ส่งไปยัง TMS API
  // const response = UrlFetchApp.fetch('https://your-tms-api.com/sync/project-types', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   payload: JSON.stringify(projectTypes)
  // });
}
```

---

**END OF DOCUMENT**

*Document Version: 1.0*  
*Classification: Internal*  
*Next Review: 2026-08-09*
