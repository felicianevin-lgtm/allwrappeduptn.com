/**
 * All Wrapped Up — quote form handler (Google Apps Script, bound to the leads sheet).
 *
 * What it does on every form submission:
 *   1. Appends a row to the sheet this script is attached to (creates the header row if empty).
 *   2. Emails the lead to NOTIFY_TO (Amiebeth) from the Google account that deployed the script,
 *      with an "Email [Name]" button that starts a clean new message to the lead (nothing quoted).
 *      Reply-To is also set to the lead's email, but a plain Reply quotes this email back to them,
 *      so the body carries only the lead's own answers, no internal notes.
 *   3. Nothing to click, ever. No activation, no forwarding confirmation.
 *   4. Drops spam (see spamReasons) onto a 'Spam' tab of the sheet instead of emailing it.
 *
 * Setup (once, in the team@norcaladmin.com Google account):
 *   1. Create a Google Sheet called "All Wrapped Up Leads".
 *   2. Extensions → Apps Script. Delete the sample code, paste this whole file, click Save.
 *   3. Deploy → New deployment → type "Web app". Execute as: Me. Who has access: Anyone. Deploy.
 *      Authorize when asked (Advanced → Go to project). Copy the Web app URL.
 *   4. Put that URL in FORM_ENDPOINT at the top of build.py, rebuild, push.
 *   To change who gets the email later: edit NOTIFY_TO / CC below, then Deploy → Manage deployments → edit → New version.
 */

var NOTIFY_TO = 'abthearp@gmail.com';      // Amiebeth: receives every lead
var CC        = 'team@norcaladmin.com';    // hub copy; set to '' for none
var SITE      = 'https://allwrappeduptn.com';

var COLUMNS = [
  ['Received',          function (p) { return new Date(); }],
  ['Name',              'name'],
  ['Company',           'company'],
  ['Email',             'email'],
  ['Phone',             'phone'],
  ['Wrapping for',      'client_type'],
  ['Gift count',        'gift_count'],
  ['Needed by',         'needed_by'],
  ['City',              'city'],
  ['Pickup / delivery', 'pickup'],
  ['Best way to reach', 'preferred_contact'],
  ['Message',           'message'],
  ['Page',              'page'],
  ['Status',            function () { return 'New'; }]
];

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};
    if (!p.name && !p.email && !p.message) return redirect();
    var reasons = spamReasons(p);
    if (reasons.length) { logSpam(p, reasons); return redirect(); }   // caught: kept on the Spam tab, no email

    var row = COLUMNS.map(function (c) { return typeof c[1] === 'function' ? c[1](p) : (p[c[1]] || ''); });
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(COLUMNS.map(function (c) { return c[0]; }));
      sheet.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold');
      sheet.setFrozenRows(1);
    }
    sheet.appendRow(row);

    var who = p.name || 'Someone';
    var kind = ({corporate: 'corporate', family: 'family holiday', wedding: 'wedding', shower: 'shower', birthday: 'birthday / anniversary', question: 'question', other: ''})[p.client_type] || '';
    var subject = 'New Gift Wrapping Website Lead Inquiry Received' + (who !== 'Someone' ? ' — ' + who : '') + (kind ? ' (' + kind + ')' : '');
    var lines = COLUMNS.slice(1, -1).map(function (c) {
      var v = typeof c[1] === 'function' ? '' : (p[c[1]] || '');
      return v ? '<tr><td style="padding:6px 12px 6px 0;color:#857a7d;white-space:nowrap;vertical-align:top">' + c[0] + '</td><td style="padding:6px 0">' + esc(v).replace(/\n/g, '<br>') + '</td></tr>' : '';
    }).join('');
    var validEmail = p.email && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(p.email);
    // The button starts a blank new message to the lead, so nothing from this email is quoted back to them.
    var button = '';
    if (validEmail) {
      var mailto = 'mailto:' + encodeURIComponent(p.email).replace(/%40/g, '@') +
        '?subject=' + encodeURIComponent('Your gift wrapping quote - All Wrapped Up') +
        '&body=' + encodeURIComponent('Hi ' + (who !== 'Someone' ? who.split(' ')[0] : 'there') + ',\n\n');
      button = '<p style="margin:20px 0 0"><a href="' + esc(mailto) + '" style="display:inline-block;background:#221b1d;color:#ffffff;text-decoration:none;padding:10px 18px;border-radius:6px;font-weight:bold">Email ' + esc(who !== 'Someone' ? who : 'this lead') + '</a></p>';
    }
    // Keep internal notes out of this body: a plain Reply quotes all of it to the lead.
    var html = '<div style="font-family:Arial,sans-serif;font-size:15px;color:#221b1d;max-width:620px">' +
      '<p style="font-size:18px;margin:0 0 14px"><b>New Gift Wrapping Website Lead Inquiry Received</b></p>' +
      '<table style="border-collapse:collapse">' + lines + '</table>' + button + '</div>';
    var opts = { htmlBody: html, name: 'All Wrapped Up website' };
    if (validEmail) opts.replyTo = p.email;
    if (CC) opts.cc = CC;
    MailApp.sendEmail(NOTIFY_TO, subject, 'New website lead. Open in an HTML email client to see the details.', opts);
  } catch (err) {
    try { MailApp.sendEmail(CC || NOTIFY_TO, 'Quote form error', String(err) + '\n\n' + JSON.stringify((e && e.parameter) || {})); } catch (ignore) {}
  }
  return redirect();
}

function doGet() { return redirect(); }

// ---- Spam filter -------------------------------------------------------------
// The website's JavaScript stamps every real submission with the page path, the time the page
// loaded (t) and a checksum of it (k). Bots that post straight to this URL send none of that.
function spamReasons(p) {
  var hard = [], soft = [];
  if (p.website) hard.push('honeypot field filled');
  if (!p.t || !p.k || String(checksum(p.t)) !== String(p.k)) hard.push('posted without the website form (no page token)');
  else if (Date.now() - Number(p.t) < 3000) hard.push('submitted less than 3 seconds after the page loaded');
  var text = [p.name, p.company, p.message].join(' ');
  if (/https?:\/\/|www\.|\.(ru|cn|xyz|top|club|site)\b/i.test(text)) soft.push('link in message');
  if (/[Ѐ-ӿ一-鿿؀-ۿ]/.test(text)) soft.push('non-Latin text');
  if (p.needed_by && /^\d{4}-\d{2}-\d{2}$/.test(p.needed_by) && new Date(p.needed_by) < new Date(Date.now() - 864e5)) soft.push('needed-by date is in the past');
  var digits = (p.phone || '').replace(/\D/g, '');
  if (digits && !(digits.length === 10 || (digits.length === 11 && digits.charAt(0) === '1'))) soft.push('phone is not a US number');
  if (p.name && !/[aeiouy]/i.test(p.name)) soft.push('name has no vowels');
  if (p.email && /^no-?reply|\d{5,}@/i.test(p.email)) soft.push('email looks generated');
  if (p.client_type && !/^(corporate|family|wedding|shower|birthday|question|other)$/.test(p.client_type)) soft.push('invalid form value');
  return hard.length ? hard.concat(soft) : (soft.length >= 2 ? soft : []);
}
function checksum(t) { var h = 0, s = String(t); for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 1000003; return h; }
function logSpam(p, reasons) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('Spam') || ss.insertSheet('Spam');
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(COLUMNS.map(function (c) { return c[0]; }).slice(0, -1).concat(['Why it was caught']));
      sheet.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold'); sheet.setFrozenRows(1);
    }
    var row = COLUMNS.slice(0, -1).map(function (c) { return typeof c[1] === 'function' ? c[1](p) : (p[c[1]] || ''); });
    sheet.appendRow(row.concat([reasons.join('; ')]));
  } catch (ignore) {}
}

// Non-JavaScript fallback: the browser lands here after a plain form post, so send it on to the thank-you page.
function redirect() {
  return HtmlService.createHtmlOutput('<!doctype html><meta http-equiv="refresh" content="0;url=' + SITE + '/thank-you/"><script>window.top.location.replace("' + SITE + '/thank-you/")</script>Thank you.')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]; }); }
