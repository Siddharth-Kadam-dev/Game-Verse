// /* GameVerse BGMI Compatibility Checker: front-end. Talks to the Django JSON API (/api/...). */
// (() => {
//   'use strict';
//   const $ = (s, r = document) => r.querySelector(s);
//   const fmt = (n) => Number(n).toLocaleString('en-US');
//   const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
//   const MAX_SCORE = 10000000;
//   const BAR_SCALE = 1800000;


// /* --------- Data access --------- */
//   const API_BRANDS = '/checker/api/brands';
//   const API_DEVICES = '/checker/api/devices';
//   const API_VERSIONS = '/checker/api/versions';
//   const API_CHECK = '/checker/api/check/device/';
//   const API_SCORE = '/checker/api/check/score';

//   const serverApi = {
//     async get(url) {
//       const res = await fetch(url);
//       const data = await res.json().catch(() => ({}));
//       if (!res.ok) throw new Error(data.error || 'Request failed. Please try again.');
//       return data;
//     },
//     brands: () => serverApi.get(API_BRANDS),
//     devices: (id) => serverApi.get(`${API_DEVICES}?brand_id=${encodeURIComponent(id)}`),
//     versions: () => serverApi.get(API_VERSIONS),
//     checkDevice: (id) => serverApi.get(`${API_CHECK}${encodeURIComponent(id)}`),
//     checkScore: (score) => serverApi.get(`${API_SCORE}?antutu=${encodeURIComponent(score)}`),
//   };

//   const api = serverApi;

//   /* ---------- Rendering ---------- */
//   const resultsEl = $('#results');

//   function tableHtml(versions, { idle }) {
//     const rows = versions.map((v) => {
//       const cls = idle ? '' : v.isBest ? 'best' : v.supported ? 'ok' : 'locked';
//       const width = Math.max(4, Math.min(100, (v.min_antutu / BAR_SCALE) * 100));
//       let action = '';
//       if (!idle && v.supported) {
//         action = `<a class="btn small ${v.isBest ? 'primary' : ''} dl" href="${esc(v.download_url || '#')}" data-version="${esc(v.version)}">Download</a>`;
//       } else if (!idle) {
//         action = `<span class="gap">Needs +${fmt(v.min_antutu - v.score)}</span>`;
//       }
//       return `<tr class="${cls}">
//         <td class="v">BGMI ${esc(v.version)}</td>
//         <td><span class="need">${fmt(v.min_antutu)}+</span><span class="bar"><i style="width:${width}%"></i></span></td>
//         <td>${esc(v.fps_label)}</td>
//         <td class="act">${action}</td>
//       </tr>`;
//     }).join('');
//     return `<div class="table-scroll ${idle ? 'idle' : ''}"><table>
//       <caption>${idle ? 'BGMI version requirements' : 'All BGMI versions'}</caption>
//       <thead><tr><th scope="col">Version</th><th scope="col">Needs AnTuTu v10</th><th scope="col">Target frame rate</th><th scope="col"><span class="sr">Download</span></th></tr></thead>
//       <tbody>${rows}</tbody></table></div>`;
//   }

//   function renderIdle(versions) {
//     resultsEl.innerHTML = `
//       <h2 class="title">Your result appears here</h2>
//       <p class="sub">Check a phone or enter a score on the left. Until then, this is what each BGMI version asks for.</p>
//       ${tableHtml(versions, { idle: true })}`;
//   }

//   function renderResult(r) {
//     const best = r.recommended;
//     const versions = r.versions.map((v) => ({ ...v, score: r.antutu, isBest: best && v.version === best.version }));
//     const who = r.device ? `${esc(r.device.brand)} ${esc(r.device.model)}` : `AnTuTu score ${fmt(r.antutu)}`;
//     const facts = r.device
//       ? `<p class="facts"><span>Chipset <b>${esc(r.device.chipset)}</b></span><span>AnTuTu v10 <b>${fmt(r.antutu)}</b></span></p>`
//       : '<p class="facts"></p>';

//     let pick, next = '';
//     if (best) {
//       pick = `<div class="pick">
//         <div><span class="tag">Best match</span><h3>BGMI ${esc(best.version)}</h3><p class="fps">${esc(best.fps_label)}</p></div>
//         <a class="btn primary dl" href="${esc(best.download_url || '#')}" data-version="${esc(best.version)}">Download BGMI ${esc(best.version)}</a>
//       </div>`;
//       next = r.next_upgrade
//         ? `<p class="next">Next up is <b>BGMI ${esc(r.next_upgrade.version)}</b>, which needs ${fmt(r.next_upgrade.min_antutu)}+. You are ${fmt(r.next_upgrade.gap)} points short.</p>`
//         : '<p class="next">This is the newest BGMI version in our list, and your score clears it.</p>';
//     } else {
//       const first = r.versions[0];
//       pick = `<div class="pick"><div><h3>No supported BGMI version</h3></div></div>`;
//       next = `<p class="next">The oldest version, <b>BGMI ${esc(first.version)}</b>, needs ${fmt(first.min_antutu)}+. Your score is ${fmt(first.min_antutu - r.antutu)} points short.</p>`;
//     }

//     resultsEl.innerHTML = `
//       <div class="verdict ${best ? '' : 'none'}">
//         <p class="who">${who}</p>${facts}${pick}${next}
//       </div>
//       ${tableHtml(versions, { idle: false })}`;

//     if (window.matchMedia('(max-width: 900px)').matches) {
//       const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
//       resultsEl.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
//     }
//   }

//   /* ---------- Toast for placeholder download links ---------- */
//   const toastEl = $('#toast');
//   let toastTimer;
//   function toast(msg) {
//     toastEl.textContent = msg;
//     toastEl.hidden = false;
//     clearTimeout(toastTimer);
//     toastTimer = setTimeout(() => { toastEl.hidden = true; }, 3200);
//   }
//   document.addEventListener('click', (e) => {
//     const a = e.target.closest('a.dl');
//     if (!a) return;
//     const href = a.getAttribute('href');
//     if (!href || href === '#') {
//       e.preventDefault();
//       toast(`The download link for BGMI ${a.dataset.version} has not been added yet.`);
//     }
//   });

//   /* ---------- Tabs ---------- */
//   const tabs = [$('#tab-device'), $('#tab-score')];
//   function selectTab(tab, focus) {
//     tabs.forEach((t) => {
//       const on = t === tab;
//       t.setAttribute('aria-selected', on);
//       t.tabIndex = on ? 0 : -1;
//       $('#' + t.getAttribute('aria-controls')).hidden = !on;
//     });
//     if (focus) tab.focus();
//   }
//   tabs.forEach((t, i) => {
//     t.addEventListener('click', () => selectTab(t));
//     t.addEventListener('keydown', (e) => {
//       if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
//         e.preventDefault();
//         selectTab(tabs[(i + 1) % tabs.length], true);
//       }
//     });
//   });

//   /* ---------- Mode 1: pick a phone ---------- */
//   const brandSel = $('#brand');
//   const modelSel = $('#model');
//   const errDevice = $('#err-device');
//   const showErr = (el, msg) => { el.textContent = msg; el.hidden = !msg; };

//   brandSel.addEventListener('change', async () => {
//     showErr(errDevice, '');
//     if (!brandSel.value) {
//       modelSel.innerHTML = '<option value="">Choose a brand first</option>';
//       modelSel.disabled = true;
//       return;
//     }
//     modelSel.disabled = true;
//     modelSel.innerHTML = '<option value="">Loading models...</option>';
//     try {
//       const devices = await api.devices(brandSel.value);
//       modelSel.innerHTML = '<option value="">Select your phone</option>' +
//         devices.map((d) => `<option value="${d.device_id}">${esc(d.model)} (${esc(d.segment)})</option>`).join('');
//       modelSel.disabled = false;
//     } catch (err) {
//       modelSel.innerHTML = '<option value="">Could not load models</option>';
//       showErr(errDevice, err.message);
//     }
//   });

//   $('#pane-device').addEventListener('submit', async (e) => {
//     e.preventDefault();
//     showErr(errDevice, '');
//     if (!brandSel.value) return showErr(errDevice, 'Choose a brand to continue.');
//     if (!modelSel.value) return showErr(errDevice, 'Select your phone model to continue.');
//     try { renderResult(await api.checkDevice(modelSel.value)); }
//     catch (err) { showErr(errDevice, err.message); }
//   });

//   /* ---------- Mode 2: AnTuTu score ---------- */
//   const scoreInput = $('#score');
//   const errScore = $('#err-score');

//   $('#pane-score').addEventListener('submit', async (e) => {
//     e.preventDefault();
//     showErr(errScore, '');
//     const raw = scoreInput.value.replace(/[,\s]/g, '');
//     if (!/^\d+$/.test(raw)) return showErr(errScore, 'Enter your score as a whole number, for example 650000.');
//     const n = Number(raw);
//     if (n < 1 || n > MAX_SCORE) return showErr(errScore, `Enter a score between 1 and ${fmt(MAX_SCORE)}.`);
//     try { renderResult(await api.checkScore(n)); }
//     catch (err) { showErr(errScore, err.message); }
//   });

//   /* ---------- Start ---------- */
//   (async function init() {
//     try {
//       const [brands, versions] = await Promise.all([api.brands(), api.versions()]);
//       brandSel.innerHTML = '<option value="">Select a brand</option>' +
//         brands.map((b) => `<option value="${b.brand_id}">${esc(b.name)}</option>`).join('');
//       renderIdle(versions);
//     } catch (err) {
//       brandSel.innerHTML = '<option value="">Could not load brands</option>';
//       resultsEl.innerHTML = `<h2 class="title">The checker could not reach its database</h2>
//         <p class="sub">Start the server with <code>python manage.py runserver</code> and reload this page.</p>`;
//     }
//   })();
// })();




/* GameVerse BGMI Compatibility Checker: front-end */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const fmt = (n) => Number(n).toLocaleString('en-US');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const MAX_SCORE = 10000000;
  const BAR_SCALE = 1800000;

  /* ---------- Data access ---------- */
  const api = {
    async get(url) {
      const res = await fetch(url);
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || 'Request failed. Please try again.');
      return data;
    },
    brands: () => api.get('/checker/api/brands'),
    devices: (id) => api.get('/checker/api/devices?brand_id=' + encodeURIComponent(id)),
    versions: () => api.get('/checker/api/versions'),
    checkDevice: (id) => api.get('/checker/api/check/device/' + encodeURIComponent(id)),
    checkScore: (score) => api.get('/checker/api/check/score?antutu=' + encodeURIComponent(score)),
  };

  /* ---------- Rendering ---------- */
  const resultsEl = $('#results');

  function tableHtml(versions, { idle }) {
    const rows = versions.map((v) => {
      const cls = idle ? '' : v.isBest ? 'best' : v.supported ? 'ok' : 'locked';
      const width = Math.max(4, Math.min(100, (v.min_antutu / BAR_SCALE) * 100));
      let action = '';
      if (!idle && v.supported) {
        action = `<a class="btn small ${v.isBest ? 'primary' : ''} dl" href="${esc(v.download_url || '#')}" data-version="${esc(v.version)}">Download</a>`;
      } else if (!idle) {
        action = `<span class="gap">Needs +${fmt(v.min_antutu - v.score)}</span>`;
      }
      return `<tr class="${cls}">
        <td class="v">BGMI ${esc(v.version)}</td>
        <td><span class="need">${fmt(v.min_antutu)}+</span><span class="bar"><i style="width:${width}%"></i></span></td>
        <td>${esc(v.fps_label)}</td>
        <td class="act">${action}</td>
      </tr>`;
    }).join('');
    return `<div class="table-scroll ${idle ? 'idle' : ''}"><table>
      <caption>${idle ? 'BGMI version requirements' : 'All BGMI versions'}</caption>
      <thead><tr><th scope="col">Version</th><th scope="col">Needs AnTuTu v10</th><th scope="col">Target frame rate</th><th scope="col"><span class="sr">Download</span></th></tr></thead>
      <tbody>${rows}</tbody></table></div>`;
  }

  function renderIdle(versions) {
    resultsEl.innerHTML = `
      <h2 class="title">Your result appears here</h2>
      <p class="sub">Check a phone or enter a score on the left. Until then, this is what each BGMI version asks for.</p>
      ${tableHtml(versions, { idle: true })}`;
  }

  function renderResult(r) {
    const best = r.recommended;
    const versions = r.versions.map((v) => ({ ...v, score: r.antutu, isBest: best && v.version === best.version }));
    const who = r.device ? `${esc(r.device.brand)} ${esc(r.device.model)}` : `AnTuTu score ${fmt(r.antutu)}`;
    const facts = r.device
      ? `<p class="facts"><span>Chipset <b>${esc(r.device.chipset)}</b></span><span>AnTuTu v10 <b>${fmt(r.antutu)}</b></span></p>`
      : '<p class="facts"></p>';

    let pick, next = '';
    if (best) {
      pick = `<div class="pick">
        <div><span class="tag">Best match</span><h3>BGMI ${esc(best.version)}</h3><p class="fps">${esc(best.fps_label)}</p></div>
        <a class="btn primary dl" href="${esc(best.download_url || '#')}" data-version="${esc(best.version)}">Download BGMI ${esc(best.version)}</a>
      </div>`;
      next = r.next_upgrade
        ? `<p class="next">Next up is <b>BGMI ${esc(r.next_upgrade.version)}</b>, which needs ${fmt(r.next_upgrade.min_antutu)}+. You are ${fmt(r.next_upgrade.gap)} points short.</p>`
        : '<p class="next">This is the newest BGMI version in our list, and your score clears it.</p>';
    } else {
      const first = r.versions[0];
      pick = `<div class="pick"><div><h3>No supported BGMI version</h3></div></div>`;
      next = `<p class="next">The oldest version, <b>BGMI ${esc(first.version)}</b>, needs ${fmt(first.min_antutu)}+. Your score is ${fmt(first.min_antutu - r.antutu)} points short.</p>`;
    }

    resultsEl.innerHTML = `
      <div class="verdict ${best ? '' : 'none'}">
        <p class="who">${who}</p>${facts}${pick}${next}
      </div>
      ${tableHtml(versions, { idle: false })}`;

    if (window.matchMedia('(max-width: 900px)').matches) {
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      resultsEl.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }
  }

  /* ---------- Toast for placeholder download links ---------- */
  const toastEl = $('#toast');
  let toastTimer;
  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toastEl.hidden = true; }, 3200);
  }
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a.dl');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href || href === '#') {
      e.preventDefault();
      toast(`The download link for BGMI ${a.dataset.version} has not been added yet.`);
    }
  });

  /* ---------- Tabs ---------- */
  const tabs = [$('#tab-device'), $('#tab-score')];
  function selectTab(tab, focus) {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      $('#' + t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => selectTab(t));
    t.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        selectTab(tabs[(i + 1) % tabs.length], true);
      }
    });
  });

  /* ---------- Mode 1: pick a phone ---------- */
  const brandSel = $('#brand');
  const modelSel = $('#model');
  const errDevice = $('#err-device');
  const showErr = (el, msg) => { el.textContent = msg; el.hidden = !msg; };

  brandSel.addEventListener('change', async () => {
    showErr(errDevice, '');
    if (!brandSel.value) {
      modelSel.innerHTML = '<option value="">Choose a brand first</option>';
      modelSel.disabled = true;
      return;
    }
    modelSel.disabled = true;
    modelSel.innerHTML = '<option value="">Loading models...</option>';
    try {
      const devices = await api.devices(brandSel.value);
      modelSel.innerHTML = '<option value="">Select your phone</option>' +
        devices.map((d) => `<option value="${d.device_id}">${esc(d.model)} (${esc(d.segment)})</option>`).join('');
      modelSel.disabled = false;
    } catch (err) {
      modelSel.innerHTML = '<option value="">Could not load models</option>';
      showErr(errDevice, err.message);
    }
  });

  $('#pane-device').addEventListener('submit', async (e) => {
    e.preventDefault();
    showErr(errDevice, '');
    if (!brandSel.value) return showErr(errDevice, 'Choose a brand to continue.');
    if (!modelSel.value) return showErr(errDevice, 'Select your phone model to continue.');
    try { renderResult(await api.checkDevice(modelSel.value)); }
    catch (err) { showErr(errDevice, err.message); }
  });

  /* ---------- Mode 2: AnTuTu score ---------- */
  const scoreInput = $('#score');
  const errScore = $('#err-score');

  $('#pane-score').addEventListener('submit', async (e) => {
    e.preventDefault();
    showErr(errScore, '');
    const raw = scoreInput.value.replace(/[,\s]/g, '');
    if (!/^\d+$/.test(raw)) return showErr(errScore, 'Enter your score as a whole number, for example 650000.');
    const n = Number(raw);
    if (n < 1 || n > MAX_SCORE) return showErr(errScore, `Enter a score between 1 and ${fmt(MAX_SCORE)}.`);
    try { renderResult(await api.checkScore(n)); }
    catch (err) { showErr(errScore, err.message); }
  });

  /* ---------- Start ---------- */
  (async function init() {
    try {
      const [brands, versions] = await Promise.all([api.brands(), api.versions()]);
      brandSel.innerHTML = '<option value="">Select a brand</option>' +
        brands.map((b) => `<option value="${b.brand_id}">${esc(b.name)}</option>`).join('');
      renderIdle(versions);
    } catch (err) {
      brandSel.innerHTML = '<option value="">Could not load brands</option>';
      resultsEl.innerHTML = `<h2 class="title">The checker could not reach its database</h2>
        <p class="sub">Start the server with <code>python manage.py runserver</code> and reload this page.</p>`;
    }
  })();
})();