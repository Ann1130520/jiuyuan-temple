/**
 * 台中烏日九元宮 - Google 試算表 (Google Sheets) 自動接收登記名冊腳本
 * 
 * 【使用步驟】：
 * 1. 打開您的 Google 雲端硬碟，建立一個空白的「Google 試算表」，命名為「烏日九元宮-信眾科儀登記名冊」
 * 2. 點擊頂部選單的「擴充功能」➔「Apps Script」
 * 3. 把此檔案的所有程式碼完整複製並覆蓋貼到 Apps Script 編輯器中
 * 4. 點擊右上角「部署」➔「新增部署」
 * 5. 齒輪選擇「網頁應用程式 (Web App)」
 *    - 說明：信眾登記接收端
 *    - 執行身分：我 (您的 Google 帳號)
 *    - 誰可以存取：所有人 (Anyone)  <-- 這點最重要！
 * 6. 點擊「部署」，授權存取後，會得到一串「網頁應用程式網址 (Web App URL)」
 * 7. 把該網址複製下來，貼到九元宮網頁 js/main.js 的 GOOGLE_SHEET_WEBAPP_URL 變數即可！
 */

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000); // 鎖定防並發衝突
  
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // 如果是第一行，自動建立標題列
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "疏文編號",
        "登記時間",
        "科儀項目",
        "信士姓名",
        "乾造/坤造",
        "出生生辰",
        "出生時辰",
        "聯絡電話",
        "通訊地址",
        "祈福心願"
      ]);
      // 美化標題列
      sheet.getRange(1, 1, 1, 10).setBackground("#8B0000").setFontColor("#FFFFFF").setFontWeight("bold");
    }
    
    var data = JSON.parse(e.postData.contents);
    
    // 將新的一筆信眾資料寫入下一行
    sheet.appendRow([
      data.code || "",
      data.time || new Date().toLocaleString("zh-TW"),
      data.ceremony || "",
      data.name || "",
      data.gender || "",
      data.birth || "",
      data.hour || "",
      data.phone || "",
      data.address || "",
      data.wish || ""
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({ result: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ result: "error", error: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}
