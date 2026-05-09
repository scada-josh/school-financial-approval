// ========== Fetch Function ========== function fetchSheet(gid) { return new Promise((resolve, reject) => { const cb = '_gviz' + gid + '_' + Date.now(); const timer = setTimeout(() => { cleanup(); reject(new Error('Request timeout (20s)')); }, 20000);
 
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
 
 // แปลงข้อมูลเป็น Array of Objects
 
 const cols = resp.table.cols.map(c => (c.label || c.id || '').trim());
 
 const rows = (resp.table.rows || []).map(r =>
 
   Object.fromEntries(cols.map((h, i) => {
 
     const cell = r.c ? r.c[i] : null;
 
     const val = (cell && cell.v !== null && cell.v !== undefined)
 
                ? String(cell.v) : '';
 
     return [h, val.trim()];
 
   }))
 
 );
 
 resolve(rows);
 
};
 
// สร้าง script tag
 
const s = document.createElement('script');
 
s.id = '__gs_' + cb;
 
s.src = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?gid=${gid}&tqx=responseHandler:${cb}`;
 
s.onerror = () => { clearTimeout(timer); cleanup(); reject(new Error('Script load failed')); };
 
document.head.appendChild(s);
 
}); }
 
// ========== ใช้งาน ========== async function loadData() { try { const [rows1, rows2] = await Promise.all([ fetchSheet(SHEETS.sheet1), fetchSheet(SHEETS.sheet2), ]); console.log('Data:', rows1, rows2); } catch (err) { console.error('Error:', err.message); } }