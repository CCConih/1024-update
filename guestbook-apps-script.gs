/**
 * HINDIA 1024 — guest book backend (Google Apps Script)
 *
 * Setup:
 *  1. Create a Google Sheet → Extensions → Apps Script → paste this file → Save.
 *  2. Deploy → New deployment → type "Web app"
 *     Execute as: Me · Who has access: Anyone → Deploy, allow access.
 *  3. Copy the Web app URL (ends in /exec) into GUESTBOOK_ENDPOINT
 *     (01b-guestbook-FOOTER-injection.html in the multi-page kit,
 *     02-hero-guestbook.html in the one-page kit).
 *  After editing this script later: Deploy → Manage deployments → edit → New version,
 *  so the same URL keeps working.
 *
 * Each signature becomes a row on the "Guest book" tab: time, name, email, language, page.
 * The page shows "Signed" only when this script answers {"ok":true}.
 */
var SHEET_NAME = "Guest book";
var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function doPost(e) {
  var p = (e && e.parameter) || {};
  // honeypot: only bots fill the hidden "website" field — answer ok so they move on, save nothing
  if (p.website) return reply(true);

  var name = String(p.name || "").trim().slice(0, 80);
  var email = String(p.email || "").trim().slice(0, 120);
  if (!name || !EMAIL_RE.test(email) || p.consent !== "yes") return reply(false);

  // two people signing at once must not both write the header row
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) sheet.appendRow(["Signed at", "Name", "Email", "Language", "Page"]);
    sheet.appendRow([new Date(), cell(name), cell(email), cell(p.lang).slice(0, 5), cell(p.source).slice(0, 200)]);
  } finally {
    lock.releaseLock();
  }
  return reply(true);
}

// text starting with = + - @ would run as a formula when the sheet is opened
function cell(v) {
  v = String(v == null ? "" : v);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function reply(ok) {
  return ContentService.createTextOutput(JSON.stringify({ ok: ok }))
    .setMimeType(ContentService.MimeType.JSON);
}
