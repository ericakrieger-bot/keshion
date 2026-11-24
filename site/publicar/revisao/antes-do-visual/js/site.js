/* Pontos únicos de troca. O HTML contém os mesmos valores como alternativa sem JS. */
var NOME_PRODUTO = "O Assistente Inteligente";
var NOMES_NIVEIS = ["Essencial", "Avançado", "Completo"];
var WHATSAPP_NUMERO = "554137900181";
var WHATSAPP_TEXTO = "Olá! Quero agendar o diagnóstico grátis da Keshion";
(function () {
  "use strict";
  var all = function (selector, root) { return Array.prototype.slice.call((root || document).querySelectorAll(selector)); };
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  all(".np").forEach(function (el) { el.textContent = NOME_PRODUTO; });
  all("[data-nivel]").forEach(function (el) { var name = NOMES_NIVEIS[Number(el.dataset.nivel)]; el.textContent = el.hasAttribute("data-minusculo") ? name.toLocaleLowerCase("pt-BR") : name; });
  var number = WHATSAPP_NUMERO.replace(/\D/g, "");
  var formatted = number.replace(/^55(\d{2})(\d{4,5})(\d{4})$/, "($1) $2-$3");
  all("a[data-wa]").forEach(function (a) { a.href = "https://wa.me/" + number + "?text=" + encodeURIComponent(WHATSAPP_TEXTO); });
  all("[data-wa-texto]").forEach(function (el) { el.textContent = formatted; });
  all("[data-ano]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  var canObserve = "IntersectionObserver" in window;
  function observe(elements, callback, threshold) {
    if (!canObserve || reduced.matches) { elements.forEach(callback); return; }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { if (entry.isIntersecting) { callback(entry.target); observer.unobserve(entry.target); } });
    }, { threshold: threshold || 0.1 });
    elements.forEach(function (el) { observer.observe(el); });
  }
  all(".grid, .reason-list").forEach(function (grid) {
    all(":scope > .reveal", grid).forEach(function (el, i) { el.style.setProperty("--delay", Math.min(i, 4) * 90 + "ms"); });
  });
  observe(all(".reveal, .recovery-panel"), function (el) { el.classList.add("in-view"); });
  var chats = all("[data-chat]");
  function cancel(phone) { phone._sequence = (phone._sequence || 0) + 1; all(".typing", phone).forEach(function (el) { el.remove(); }); phone.querySelector("[data-status]").textContent = "online"; }
  function showAll(phone) { cancel(phone); all(".chat-panel", phone).forEach(function (panel) { panel.classList.remove("is-animating"); all("[data-message]", panel).forEach(function (message) { message.classList.add("shown"); }); }); }
  function animate(phone, panel) {
    cancel(phone);
    var sequence = phone._sequence;
    var scroller = phone.querySelector(".chat-scroll");
    var status = phone.querySelector("[data-status]");
    var messages = all("[data-message]", panel);
    messages.forEach(function (message) { message.classList.remove("shown"); });
    panel.classList.remove("is-animating");
    scroller.scrollTop = 0;
    if (reduced.matches) { showAll(phone); return; }
    panel.classList.add("is-animating");
    var typing = document.createElement("div");
    typing.className = "message clinic typing";
    typing.setAttribute("aria-hidden", "true");
    typing.innerHTML = "<i></i><i></i><i></i>";
    function wait(ms) { return new Promise(function (resolve) { window.setTimeout(function () { resolve(phone._sequence === sequence && !reduced.matches); }, ms); }); }
    function scrollBottom() { if (!phone._readingHistory) scroller.scrollTop = scroller.scrollHeight; }
    (async function () {
      for (var i = 0; i < messages.length; i++) {
        var message = messages[i];
        if (!await wait(message.classList.contains("clinic") ? 350 : 850)) return;
        if (message.classList.contains("clinic")) {
          status.textContent = "digitando...";
          panel.insertBefore(typing, message);
          scrollBottom();
          var duration = Math.min(2000, Math.max(1000, message.querySelector(".message-text").textContent.length * 12));
          if (!await wait(duration)) return;
          typing.remove();
          status.textContent = "online";
        }
        message.classList.add("shown");
        scrollBottom();
      }
      panel.classList.remove("is-animating");
    })().catch(function () { showAll(phone); });
  }
  chats.forEach(function (phone) {
    var scroller = phone.querySelector(".chat-scroll");
    scroller.addEventListener("wheel", function (event) { phone._readingHistory = event.deltaY < 0; }, { passive: true });
    scroller.addEventListener("touchstart", function () { phone._readingHistory = true; }, { passive: true });
  });
  var hero = document.querySelector('[data-chat="hero"]');
  if (hero) observe([hero], function (phone) { animate(phone, phone.querySelector(".chat-panel")); }, 0.2);
  var demo = document.querySelector('[data-chat="demo"]');
  if (demo) {
    var tabs = all('[role="tab"]');
    var panels = all(".chat-panel", demo);
    var contexts = all("[data-context]");
    var started = false;
    var active = 0;
    function select(index, focus) {
      active = index;
      cancel(demo);
      tabs.forEach(function (tab, i) { tab.setAttribute("aria-selected", String(i === index)); tab.tabIndex = i === index ? 0 : -1; });
      panels.forEach(function (panel, i) { panel.hidden = i !== index; });
      contexts.forEach(function (context, i) { context.hidden = i !== index; });
      demo.querySelector(".status-hour").textContent = ["21:07", "10:15", "17:00", "20:40"][index];
      demo._readingHistory = false;
      if (focus) tabs[index].focus();
      if (started) animate(demo, panels[index]);
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { started = true; select(i, false); });
      tab.addEventListener("keydown", function (event) {
        var index;
        if (event.key === "ArrowRight" || event.key === "ArrowDown") index = (i + 1) % tabs.length;
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") index = (i + tabs.length - 1) % tabs.length;
        if (event.key === "Home") index = 0;
        if (event.key === "End") index = tabs.length - 1;
        if (index !== undefined) { event.preventDefault(); started = true; select(index, true); }
      });
    });
    select(0, false);
    observe([demo], function () { if (!started) { started = true; animate(demo, panels[active]); } }, 0.2);
  }
  reduced.addEventListener("change", function () {
    if (reduced.matches) {
      all(".reveal, .recovery-panel").forEach(function (el) { el.classList.add("in-view"); });
      chats.forEach(showAll);
    }
  });
  document.documentElement.classList.add("js");
})();
