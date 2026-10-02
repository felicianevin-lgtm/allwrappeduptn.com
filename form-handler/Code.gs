/**
 * All Wrapped Up — quote form handler (Google Apps Script, bound to the leads sheet).
 *
 * What it does on every form submission:
 *   1. Appends a row to the sheet this script is attached to (creates the header row if empty).
 *   2. Emails the lead to NOTIFY_TO (Amiebeth) from the Google account that deployed the script,
 *      with Reply-To set to the lead's own email so she can reply directly.
 *   3. Nothing to click, ever. No activation, no forwarding confirmation.
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
    if (p.website) return redirect();                       // honeypot filled: a bot, drop silently
    if (!p.name && !p.email && !p.message) return redirect();

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
    var html = '<div style="font-family:Arial,sans-serif;font-size:15px;color:#221b1d;max-width:620px">' +
      '<p style="font-size:18px;margin:0 0 14px"><b>New Gift Wrapping Website Lead Inquiry Received</b></p>' +
      '<table style="border-collapse:collapse">' + lines + '</table>' +
      '<p style="margin:18px 0 0">Reply to this email to answer ' + esc(who) + ' directly' + (p.preferred_contact ? ' (they prefer ' + esc(p.preferred_contact).toLowerCase() + ')' : '') + '.</p>' +
      '<p style="color:#857a7d;font-size:13px;margin-top:22px">Sent automatically by the quote form at ' + SITE + '. Every lead is also logged in the "All Wrapped Up Leads" Google Sheet.</p></div>';
    var opts = { htmlBody: html, name: 'All Wrapped Up website' };
    if (p.email && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(p.email)) opts.replyTo = p.email;
    if (CC) opts.cc = CC;
    MailApp.sendEmail(NOTIFY_TO, subject, 'New lead from ' + SITE + '. Open in an HTML email client to see the details.', opts);
  } catch (err) {
    try { MailApp.sendEmail(CC || NOTIFY_TO, 'Quote form error', String(err) + '\n\n' + JSON.stringify((e && e.parameter) || {})); } catch (ignore) {}
  }
  return redirect();
}

function doGet() { return redirect(); }

// Non-JavaScript fallback: the browser lands here after a plain form post, so send it on to the thank-you page.
function redirect() {
  return HtmlService.createHtmlOutput('<!doctype html><meta http-equiv="refresh" content="0;url=' + SITE + '/thank-you/"><script>window.top.location.replace("' + SITE + '/thank-you/")</script>Thank you.')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]; }); }
