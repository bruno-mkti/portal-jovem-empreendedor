/*!
 * Envia uma CÓPIA dos leads do #lead-form para a planilha (Google Apps Script).
 * Não altera nem bloqueia o envio original do site: só observa o formulário.
 */
(function () {
  'use strict';

  var SHEETS_URL = 'https://script.google.com/macros/s/AKfycbwQNCc8JDOBit3AzchEU1rexc9erBmtbXQWDo-UfS-6yDNkpv0rlk3BSE0Zh80CPbcO0A/exec';
  var TOKEN      = 'd9f97e934bafe98bfb8aa320a25e7146e482c728';   // mesmo valor do Apps Script

  var form = document.getElementById('lead-form');
  if (!form) return;

  var lastKey = '', lastAt = 0;

  function val(id) {
    var el = document.getElementById(id);
    return el ? String(el.value || '').trim() : '';
  }

  function courseTitle() {
    try {
      return JSON.parse(document.getElementById('lp-course-config').textContent).course_title || '';
    } catch (e) { return ''; }
  }

  function sendLead() {
    try {
      var nome  = val('lead_nome');
      var email = val('lead_email');
      var tel   = val('lead_telefone').replace(/\D/g, '');

      // dados inválidos: não envia
      if (nome.length < 2 || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || tel.length < 10) return;

      // evita duplicidade (clique + submit, duplo clique)
      var key = email + '|' + val('lead_curso_id');
      if (key === lastKey && Date.now() - lastAt < 15000) return;
      lastKey = key; lastAt = Date.now();

      var q = new URLSearchParams(window.location.search);
      var data = new URLSearchParams({
        token: TOKEN,
        nome: nome,
        email: email,
        telefone: tel,
        curso: courseTitle(),
        curso_id: val('lead_curso_id'),
        origem: val('lead_origem'),
        cidade: val('lead_cidade'),
        pagina: window.location.origin + window.location.pathname,
        utm_source: q.get('utm_source') || '',
        utm_medium: q.get('utm_medium') || '',
        utm_campaign: q.get('utm_campaign') || '',
        utm_content: q.get('utm_content') || '',
        utm_term: q.get('utm_term') || ''
      });

      // keepalive: o envio termina mesmo se a página redirecionar para o checkout
      fetch(SHEETS_URL, { method: 'POST', mode: 'no-cors', body: data, keepalive: true })
        .catch(function () {});

      // evento para o GTM (sem dados pessoais)
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'lead_enviado',
        curso_nome: courseTitle(),
        curso_id: val('lead_curso_id'),
        plano_origem: val('lead_origem')
      });
    } catch (e) { /* nunca atrapalhar o fluxo do site */ }
  }

  form.addEventListener('submit', sendLead, true);

  var btn = document.getElementById('lead-submit');
  if (btn) btn.addEventListener('click', sendLead, true);
})();
