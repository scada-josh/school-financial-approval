const { google } = require('googleapis');

// Service Account credentials from env.local
const SPREADSHEET_ID = '1Plh_0AodTomKLyP8zrBp9FOriHXVm_uGYIO4TVHSozg';
const SERVICE_ACCOUNT_EMAIL = 'opencode-gsheet@gen-lang-client-0476777034.iam.gserviceaccount.com';
const PRIVATE_KEY = `-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDTzchAmB0EWrI/
L6g6VC5mXJOKecjEOLkFyVvmj8f+XP5M2uAHzb7Qu6UEwxEvCXBOnSfItfUH8nmV
R+i/vk0ILkb4nyuu831P9G7vfV07DGMUec4/v6nU2mEM9UC5L+vfEwyqJeWzXt9U
iIOCEjzmCoj9vE/PIzdMtX0dsPRAb39611oAONg4XGqug0hfaPT7h/V4jSRoOhnJ
Pe6LeRcTR5SXTAh8tEqWTcJhAVCU4ALhrslbHx+7zuSvm4PBG3deD2coVKkb4Mdz
K/c81mgK6detxjMAHbmC3LUCeqmiDbuyXLyzFNit0LBNCZdzzCb01BvpttQuALzH
EIYg4E37AgMBAAECggEADHi6iOssEjyQ8F2LB1w7mzVqTqYbJ0q7wlZ3/dyLhzPM
mZPtyyfXS40xC1W9Jkrk/QwN8qicNAqYFC02zEuVV5z5+tvMg7G8uD+JZLq6CacS
EnuVpHVRt8HgIxYx6HWk6u7BOSegHe7BMcYUEE2onlcSd/ZlsKm/MNoi8uOfjken
BNQ9DCswbGoko62VCyU2K5CcArJihgIayBA1gcEIBZOAHQnRpt9SRcFD11uemLqD
+qnXIgbOuOplzldzpq0bKOZRCYbf3Ysd1Sp7iYsY46ZzlEzThYvdSGl0bCpT7KUO
gOprKb5LpuQ7gV0I1H/mnly9JW398eAiV9ezmJ9MAQKBgQDyop+kNORj4+ZfVhDN
R6wHyg0bTzJ33uwO/rTyVhNJvPK12kJaEOYZuz8cklw8ibuAbEIhGME88mhpru33
VuDQ2xX37TzUACIEf76rN812wmeDr7uXQKQSl986lfpp3j7x7WV3d+n5umHqboNP
R0I9YNAwhSypXVKZQ4oawAuf+wKBgQDfeGhpJXfXAF9rWVx5lcObFMUc8auGoYsF
aBbpXvTGuru3GUCySgp7nTGzf3j3XLs/+cgVyvYmNHZrkCad2n1l1M3rsS5thsAQ
N2clrKFLDk7Elcv/Kh8tgBHr40NpKXCC6/piE91chGPM/oe6gYk9voO4TQv3el5i
q2Q53kiqAQKBgF+cZ64MTadzKdeNkadiw8559zo4thl4Var/AYyxEH6xHy8754OY
PyQKni8DGaedWq6bel+SYqtClpR2oz0hFgwXGQwOhza/Kqh9MkREBAn1R1ckC5bp
mP3erM9oRDotor4wnxg5v5Bxup3nmITH/rkzCjbkc5n1tVPBwo0R+kK7AoGAC/VS
iQXjQtMXSBRRGYSFIiBbZ/AawKqWWOS4DSbyrEvDzcmBJ8lEhFbmGPfiTkJdFtBT
/66Lu4GlMJ5XIq1VdoSLvGgP1vaWAogkceSqAO00E9r8PpxPbMzkqJ3RtqfsCGV+
UY9EkjXXbVnVg4p5AJ/YRp2A3W5j7J3FUD9v3gECgYEA8AEzeuGoVHuRZ+HYRR1G
QJTVxzqaN2uT/cDNONJ+TD9Zq7zqsuw9lqikd5YEImYYGBxnoQFwjl/TfcyktfwC
4et9x5oKFofdddFex4mi/IWeaJmTd4H4A14iuxtOkKOOmBZlkTMRcunpOir7FzBL
4eX0b6M7PahsY3PfB4DNaqU=
-----END PRIVATE KEY-----`;

async function testGoogleSheetAPI() {
  try {
    console.log('🚀 Starting Google Sheet API Test...\n');
    
    // 1. Authenticate with Service Account
    console.log('1️⃣ Authenticating with Service Account...');
    const auth = new google.auth.GoogleAuth({
      credentials: {
        client_email: SERVICE_ACCOUNT_EMAIL,
        private_key: PRIVATE_KEY,
      },
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });
    
    const authClient = await auth.getClient();
    console.log('✅ Authentication successful!\n');
    
    // 2. Get spreadsheet info
    console.log('2️⃣ Reading spreadsheet info...');
    const sheets = google.sheets({ version: 'v4', auth: authClient });
    
    const spreadsheetInfo = await sheets.spreadsheets.get({
      spreadsheetId: SPREADSHEET_ID,
    });
    
    console.log('📊 Spreadsheet Title:', spreadsheetInfo.data.properties.title);
    console.log('📑 Total Sheets:', spreadsheetInfo.data.sheets.length);
    console.log('Sheet Names:');
    spreadsheetInfo.data.sheets.forEach((sheet, i) => {
      console.log(`  ${i + 1}. ${sheet.properties.title}`);
    });
    console.log('');
    
    // 3. Read data from existing sheet
    console.log('3️⃣ Reading data from first sheet...');
    const firstSheetName = spreadsheetInfo.data.sheets[0].properties.title;
    
    const readResponse = await sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET_ID,
      range: `${firstSheetName}!A1:E20`,
    });
    
    console.log('📖 Data from first sheet:');
    if (readResponse.data.values) {
      readResponse.data.values.forEach((row, i) => {
        console.log(`  Row ${i + 1}:`, row.join(' | '));
      });
    } else {
      console.log('  (No data found)');
    }
    console.log('');
    
    // 4. Create new sheet for TMS data
    console.log('4️⃣ Creating new sheet: TMS_Config...');
    
    try {
      const addSheetResponse = await sheets.spreadsheets.batchUpdate({
        spreadsheetId: SPREADSHEET_ID,
        requestBody: {
          requests: [
            {
              addSheet: {
                properties: {
                  title: 'TMS_Config',
                },
              },
            },
          ],
        },
      });
      
      const newSheetId = addSheetResponse.data.replies[0].addSheet.properties.sheetId;
      console.log('✅ New sheet created! Sheet ID:', newSheetId);
    } catch (err) {
      if (err.message.includes('already exists')) {
        console.log('ℹ️ Sheet "TMS_Config" already exists, will overwrite data');
      } else {
        throw err;
      }
    }
    console.log('');
    
    // 5. Write data to new sheet
    console.log('5️⃣ Writing TMS configuration data...');
    
    const configData = [
      ['TOR Management System - Configuration'],
      ['Generated:', new Date().toISOString()],
      [''],
      ['=== PROJECT TYPES ==='],
      ['Code', 'Name (TH)', 'Name (EN)', 'Category', 'Active'],
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
      ['RESEARCH', 'Research & Innovation', 'Research & Innovation', 'R&D', 'TRUE'],
      [''],
      ['=== COMPLIANCE RULES ==='],
      ['Project Type', 'Rule Name', 'Regulation', 'Mandatory', 'Weight'],
      ['PROCUREMENT', 'TOR_Completeness', 'พ.ร.บ. จัดซื้อจัดจ้าง 2560', 'TRUE', '20'],
      ['IT_DIGITAL', 'PDPA_Check', 'PDPA 2562', 'TRUE', '25'],
      ['IT_DIGITAL', 'Security_Check', 'พ.ร.บ. ไซเบอร์ 2562', 'TRUE', '25'],
      ['CLOUD', 'Data_Residency', 'PDPA 2562', 'TRUE', '30'],
      ['AI_BIGDATA', 'AI_Ethics', 'จริยธรรม AI', 'TRUE', '20'],
      ['CYBERSECURITY', 'Incident_Response', 'พ.ร.บ. ไซเบอร์ 2562', 'TRUE', '30'],
      [''],
      ['=== SCORING WEIGHTS ==='],
      ['Category', 'Weight', 'Description'],
      ['Completeness', '30', 'ความครบถ้วน'],
      ['Compliance', '40', 'ความถูกต้องตามกฎหมาย'],
      ['Risk', '20', 'ความเสี่ยง'],
      ['Quality', '10', 'คุณภาพ'],
      [''],
      ['=== SYSTEM CONFIG ==='],
      ['Key', 'Value', 'Description'],
      ['APP_NAME', 'TOR Management System', 'ชื่อระบบ'],
      ['VERSION', '1.0.0', 'เวอร์ชัน'],
      ['DEFAULT_LANG', 'th', 'ภาษาเริ่มต้น'],
      ['SESSION_TIMEOUT', '1800', 'เวลา Session (วินาที)'],
      ['MAX_FILE_SIZE', '10485760', 'ขนาดไฟล์สูงสุด (ไบต์)'],
    ];
    
    const writeResponse = await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: 'TMS_Config!A1',
      valueInputOption: 'RAW',
      requestBody: {
        values: configData,
      },
    });
    
    console.log('✅ Data written successfully!');
    console.log('📊 Updated cells:', writeResponse.data.updatedCells);
    console.log('📊 Updated range:', writeResponse.data.updatedRange);
    console.log('');
    
    // 6. Format the header
    console.log('6️⃣ Formatting sheet...');
    
    // Get sheet ID for TMS_Config
    const sheetInfo = await sheets.spreadsheets.get({
      spreadsheetId: SPREADSHEET_ID,
    });
    
    const tmsSheet = sheetInfo.data.sheets.find(
      s => s.properties.title === 'TMS_Config'
    );
    
    if (tmsSheet) {
      const sheetId = tmsSheet.properties.sheetId;
      
      await sheets.spreadsheets.batchUpdate({
        spreadsheetId: SPREADSHEET_ID,
        requestBody: {
          requests: [
            {
              repeatCell: {
                range: {
                  sheetId: sheetId,
                  startRowIndex: 0,
                  endRowIndex: 1,
                },
                cell: {
                  userEnteredFormat: {
                    backgroundColor: { red: 0.2, green: 0.4, blue: 0.8 },
                    textFormat: {
                      bold: true,
                      foregroundColor: { red: 1, green: 1, blue: 1 },
                    },
                  },
                },
                fields: 'userEnteredFormat(backgroundColor,textFormat)',
              },
            },
            {
              autoResizeDimensions: {
                dimensions: {
                  sheetId: sheetId,
                  dimension: 'COLUMNS',
                  startIndex: 0,
                  endIndex: 5,
                },
              },
            },
          ],
        },
      });
      
      console.log('✅ Formatting applied!\n');
    }
    
    // 7. Verify written data
    console.log('7️⃣ Verifying written data...');
    const verifyResponse = await sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET_ID,
      range: 'TMS_Config!A1:E10',
    });
    
    console.log('📖 First 10 rows of TMS_Config:');
    verifyResponse.data.values.forEach((row, i) => {
      console.log(`  Row ${i + 1}:`, row.join(' | '));
    });
    console.log('');
    
    // Summary
    console.log('═══════════════════════════════════════════');
    console.log('✅ GOOGLE SHEET API TEST COMPLETE');
    console.log('═══════════════════════════════════════════');
    console.log('');
    console.log('📊 Test Results:');
    console.log('  ✅ Authentication: SUCCESS');
    console.log('  ✅ Read Spreadsheet: SUCCESS');
    console.log('  ✅ Read Existing Data: SUCCESS');
    console.log('  ✅ Create New Sheet: SUCCESS');
    console.log('  ✅ Write Data: SUCCESS');
    console.log('  ✅ Format Sheet: SUCCESS');
    console.log('  ✅ Verify Data: SUCCESS');
    console.log('');
    console.log('📋 Spreadsheet URL:');
    console.log(`  https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/edit`);
    console.log('');
    console.log('📝 New Sheet Created: TMS_Config');
    console.log('   - 15 Project Types');
    console.log('   - 6 Compliance Rules');
    console.log('   - 4 Scoring Weights');
    console.log('   - 5 System Configurations');
    console.log('');
    console.log('🎉 All operations completed successfully!');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.response) {
      console.error('Response:', error.response.data);
    }
    process.exit(1);
  }
}

testGoogleSheetAPI();
