document.addEventListener('DOMContentLoaded', async () => {
        function logout() { localStorage.clear(); window.location.href = '/'; }

        // ── Lee el id_equipo desde localStorage (guardado en login como 'idEquipo') ──
        function obtenerIdEquipo() {
            const claves = ['idEquipo', 'id_equipo', 'usuarioIdEquipo', 'ID_EQUIPO'];
            for (const clave of claves) {
                const val = localStorage.getItem(clave);
                if (val !== null && val !== '') {
                    const num = Number(val);
                    if (Number.isInteger(num) && num > 0) return num;
                }
            }
            return null;
        }

        async function apiJson(url, options = {}) {
            const res = await fetch(url, {
                headers: { 'Accept': 'application/json', ...(options.headers || {}) },
                ...options
            });
            const contentType = res.headers.get('content-type') || '';
            const data = contentType.includes('application/json')
                ? await res.json().catch(() => null)
                : await res.text().catch(() => '');
            if (!res.ok) {
                const msg = (data && (data.detail || data.message || data.error)) || `Error ${res.status}`;
                throw new Error(msg);
            }
            return data;
        }

        function normalizarInformes(payload) {
            if (Array.isArray(payload)) return payload;
            if (payload && Array.isArray(payload.informes)) return payload.informes;
            if (payload && Array.isArray(payload.data)) return payload.data;
            return [];
        }

        function formatearFecha(fecha, options) {
            const d = new Date(fecha);
            if (Number.isNaN(d.getTime())) return '—';
            return d.toLocaleDateString('es-ES', options);
        }

        function calcularResumenInforme(inf) {
            const labels = Array.isArray(inf.labels) ? inf.labels : [];
            const can = inf.canterano?.valores || [];
            const pro = inf.profesional?.valores || [];
            const totalMetricas = labels.length;
            const ganadas = labels.filter((_, i) => (can[i] ?? 0) > (pro[i] ?? 0)).length;
            const pct = totalMetricas > 0 ? Math.round((ganadas / totalMetricas) * 100) : 0;
            return { totalMetricas, ganadas, pct };
        }

        async function cargarInformesGuardados() {
            
            const grid = document.getElementById('grid-informes-guardados');
            const idEquipo = obtenerIdEquipo();

            if (!idEquipo) {
                grid.innerHTML = `
                    <div class="informes-vacio" style="grid-column:1/-1;">
                        <div class="vacio-icono">⚠️</div>
                        <p>Sesión no encontrada</p>
                        <small>Vuelve a <a href="/" style="color:#ffd700">iniciar sesión</a></small>
                    </div>`;
                return;
            }

            try {
                const payload = await apiJson(`/listar_informes?id_equipo=${idEquipo}`);
                const informes = normalizarInformes(payload);

                if (informes.length === 0) {
                    grid.innerHTML = `
                        <div class="informes-vacio" style="grid-column:1/-1;">
                            <div class="vacio-icono">📊</div>
                            <p>No hay informes guardados todavía</p>
                            <small>Compara jugadores y guarda el análisis desde <strong style="color:#ffd700">Comparar Jugadores</strong></small>
                        </div>`;
                    return;
                }

                grid.innerHTML = '';

                informes.forEach(inf => {
                    const { totalMetricas, ganadas, pct } = calcularResumenInforme(inf);
                    const fecha = formatearFecha(inf.fecha, { day: '2-digit', month: 'short', year: 'numeric' });
                    const nombreCan = inf.canterano?.nombre || '—';
                    const nombrePro = inf.profesional?.nombre || '—';
                    const primerNombre = nombreCan.split(' ')[0];

                    const card = document.createElement('div');
                    card.className = 'tarjeta-informe';
                    card.innerHTML = `
                        <div class="informe-tipo">⚽ Comparación</div>
                        <div class="informe-nombres">
                            <div class="informe-nombre-can">${nombreCan}</div>
                            <div class="informe-vs">vs</div>
                            <div class="informe-nombre-pro">${nombrePro}</div>
                        </div>
                        <div class="informe-meta">
                            <div class="informe-badge">
                                <span class="informe-badge-label">Temporada</span>
                                <span class="informe-badge-valor">${inf.temporada || '—'}</span>
                            </div>
                            <div class="informe-badge">
                                <span class="informe-badge-label">Fecha</span>
                                <span class="informe-badge-valor">${fecha}</span>
                            </div>
                            <div class="informe-badge">
                                <span class="informe-badge-label">Resultado</span>
                                <span class="informe-badge-valor">${ganadas}/${totalMetricas} ✓</span>
                            </div>
                        </div>
                        <div class="informe-barra-wrap">
                            <div class="informe-barra-label">
                                <span>${primerNombre}</span>
                                <span>${pct}%</span>
                            </div>
                            <div class="informe-barra">
                                <div class="informe-barra-fill" style="width:${pct}%"></div>
                            </div>
                        </div>
                        <div class="informe-acciones">
                            <button class="btn-informe-accion btn-inf-pdf">⬇️ PDF</button>
                            <button class="btn-informe-accion btn-inf-eliminar">🗑️ Eliminar</button>
                        </div>`;

                    card.querySelector('.btn-inf-pdf').addEventListener('click', () => exportarInformePDF(inf));
                    card.querySelector('.btn-inf-eliminar').addEventListener('click', () => eliminarInforme(inf.id));

                    grid.appendChild(card);
                });
            } catch (err) {
                console.error('Error cargando informes:', err);
                grid.innerHTML = `
                    <div class="informes-vacio" style="grid-column:1/-1;">
                        <div class="vacio-icono">❌</div>
                        <p>No se pudieron cargar los informes</p>
                        <small>${err.message}</small>
                    </div>`;
            }
        }

        async function eliminarInforme(id) {
            const idEquipo = obtenerIdEquipo();
            if (!idEquipo) { mostrarToast('⚠️ No se pudo identificar el equipo'); return; }
            try {
                await apiJson(`/borrar_informe/${encodeURIComponent(id)}?id_equipo=${idEquipo}`, { method: 'DELETE' });
                await cargarInformesGuardados();
                mostrarToast('🗑️ Informe eliminado');
            } catch (err) {
                mostrarToast(`❌ ${err.message}`);
            }
        }

        // Recibe el objeto informe directamente (ya normalizado), sin volver a hacer fetch
        async function exportarInformePDF(inf) {
            try {
                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
                const W = 210, H = 297, M = 14, CW = W - M * 2;
                const data = inf;
                const fecha = new Date(inf.fecha).toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' });
                const club = (localStorage.getItem('usuarioClub') || 'Club').toUpperCase();
                const temporadaSeleccionada = inf.temporada || '—';

                // ── Render gráficos ocultos en el DOM ──
                let contenedor = document.getElementById('_pdf-graficos-temp');
                if (!contenedor) {
                    contenedor = document.createElement('div');
                    contenedor.id = '_pdf-graficos-temp';
                    contenedor.style.cssText = 'position:fixed;left:-9999px;top:0;width:860px;background:#0f172a;z-index:-1;';
                    document.body.appendChild(contenedor);
                }
                contenedor.innerHTML = `
                    <div id="_pdf-radar" style="width:860px;height:500px;"></div>
                    <div id="_pdf-barras" style="width:860px;height:420px;"></div>
                `;

                const valCan = [], valProf = [];
                data.labels.forEach((_, i) => {
                    const vC = data.canterano.valores[i], vP = data.profesional.valores[i];
                    const max = Math.max(vC, vP);
                    valCan.push(max > 0 ? (vC / max) * 100 : 0);
                    valProf.push(max > 0 ? (vP / max) * 100 : 0);
                });

                await Plotly.newPlot('_pdf-radar', [
                    { type: 'scatterpolar', r: valCan, theta: data.labels, fill: 'toself', name: data.canterano.nombre, line: { color: '#3b82f6', width: 3 }, fillcolor: 'rgba(59,130,246,0.3)' },
                    { type: 'scatterpolar', r: valProf, theta: data.labels, fill: 'toself', name: data.profesional.nombre, line: { color: '#800020', width: 3 }, fillcolor: 'rgba(128,0,32,0.3)' }
                ], { polar: { radialaxis: { visible: true, showticklabels: false, gridcolor: 'rgba(255,255,255,0.1)', range: [0, 105] }, angularaxis: { gridcolor: '#334155', color: 'white', tickfont: { size: 12 }, rotation: 90 }, bgcolor: 'rgba(30,41,59,0.5)' }, paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: { color: 'white' }, showlegend: true, legend: { orientation: 'h', y: -0.2, x: 0.5, xanchor: 'center' }, margin: { t: 40, b: 40, l: 80, r: 80 } }, { staticPlot: true });

                await Plotly.newPlot('_pdf-barras', [
                    { type: 'bar', orientation: 'h', name: data.canterano.nombre, x: data.canterano.valores, y: data.labels, marker: { color: 'rgba(59,130,246,0.85)' } },
                    { type: 'bar', orientation: 'h', name: data.profesional.nombre, x: data.profesional.valores, y: data.labels, marker: { color: 'rgba(128,0,32,0.85)' } }
                ], { barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: { color: 'white', size: 12 }, xaxis: { gridcolor: 'rgba(255,255,255,0.08)', color: 'white', zeroline: false }, yaxis: { color: 'white', automargin: true, tickfont: { size: 13 } }, legend: { orientation: 'h', y: -0.18, x: 0.5, xanchor: 'center' }, margin: { t: 20, b: 60, l: 140, r: 30 } }, { staticPlot: true });

                // Espera a que Plotly renderice
                await new Promise(r => setTimeout(r, 600));

                // ─── PÁGINA 1 ───────────────────────────────
                pdf.setFillColor(8, 12, 30); pdf.rect(0, 0, W, H, 'F');
                pdf.setFillColor(100, 0, 25); pdf.rect(0, 0, W, 42, 'F');
                pdf.setFillColor(128, 0, 32); pdf.rect(0, 0, W * 0.5, 42, 'F');
                pdf.setFillColor(255, 215, 0); pdf.rect(0, 42, W, 1.5, 'F');

                pdf.setFillColor(165, 0, 68); pdf.circle(M + 11, 21, 9, 'F');
                pdf.setDrawColor(255, 215, 0); pdf.setLineWidth(0.8); pdf.circle(M + 11, 21, 9, 'S');
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(10); pdf.setFont('helvetica', 'bold');
                pdf.text('MG', M + 11, 24, { align: 'center' });

                pdf.setTextColor(255, 255, 255); pdf.setFontSize(18); pdf.setFont('helvetica', 'bold');
                pdf.text('METRICGOAL', M + 25, 18);
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(7); pdf.setFont('helvetica', 'normal');
                pdf.text('PLATAFORMA DE ANALISIS DE CANTERA PROFESIONAL', M + 25, 25);

                pdf.setTextColor(200, 200, 220); pdf.setFontSize(7.5);
                pdf.text(fecha, W - M, 16, { align: 'right' });
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(8.5); pdf.setFont('helvetica', 'bold');
                pdf.text(club, W - M, 26, { align: 'right' });
                pdf.setTextColor(180, 180, 200); pdf.setFontSize(6.5); pdf.setFont('helvetica', 'normal');
                pdf.text(`Temporada ${temporadaSeleccionada}`, W - M, 34, { align: 'right' });

                let y = 58;
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(7.5); pdf.setFont('helvetica', 'bold');
                pdf.text('> INFORME COMPARATIVO', M, y);

                y += 9;
                pdf.setTextColor(100, 160, 255); pdf.setFontSize(18); pdf.setFont('helvetica', 'bold');
                const w1 = pdf.getTextWidth(data.canterano.nombre);
                pdf.text(data.canterano.nombre, M, y);
                pdf.setTextColor(120, 120, 150); pdf.setFontSize(11); pdf.setFont('helvetica', 'normal');
                pdf.text(' vs ', M + w1 + 1, y);
                const wVs = pdf.getTextWidth(' vs ');
                pdf.setTextColor(220, 80, 110); pdf.setFontSize(18); pdf.setFont('helvetica', 'bold');
                pdf.text(data.profesional.nombre, M + w1 + wVs + 1, y);

                y += 4;
                pdf.setDrawColor(255, 215, 0); pdf.setLineWidth(0.5);
                pdf.line(M, y, W - M, y);

                y += 10;
                const cW3 = (CW - 10) / 3;
                const ganadasCan = data.labels.filter((_, i) => data.canterano.valores[i] > data.profesional.valores[i]).length;

                const drawCard = (x, cy, titulo, valor, colorValor) => {
                    pdf.setFillColor(15, 22, 50); pdf.roundedRect(x, cy, cW3, 24, 3, 3, 'F');
                    pdf.setDrawColor(255, 215, 0); pdf.setLineWidth(0.25); pdf.roundedRect(x, cy, cW3, 24, 3, 3, 'S');
                    pdf.setTextColor(120, 130, 160); pdf.setFontSize(6); pdf.setFont('helvetica', 'bold');
                    pdf.text(titulo, x + cW3 / 2, cy + 8, { align: 'center' });
                    pdf.setTextColor(...colorValor); pdf.setFontSize(13); pdf.setFont('helvetica', 'bold');
                    pdf.text(valor, x + cW3 / 2, cy + 18, { align: 'center' });
                };

                drawCard(M,              y, 'TEMPORADA',           temporadaSeleccionada,              [255, 215, 0]);
                drawCard(M + cW3 + 5,   y, 'METRICAS ANALIZADAS', `${data.labels.length}`,            [200, 220, 255]);
                drawCard(M + (cW3+5)*2, y, 'GANADAS (CANTERANO)', `${ganadasCan} / ${data.labels.length}`, [100, 200, 120]);

                y += 34;
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(8); pdf.setFont('helvetica', 'bold');
                pdf.text('> TABLA COMPARATIVA DE METRICAS', M, y);
                y += 6;

                const colW = [52, 34, 28, 34, 34];
                const cols = ['METRICA', data.canterano.nombre.substring(0,16).toUpperCase(), 'DIFER.', data.profesional.nombre.substring(0,16).toUpperCase(), 'VENTAJA'];
                pdf.setFillColor(128, 0, 32); pdf.roundedRect(M, y, CW, 9, 2, 2, 'F');
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(6.5); pdf.setFont('helvetica', 'bold');
                let cx = M + 3;
                cols.forEach((col, i) => { pdf.text(col, cx, y + 6); cx += colW[i]; });
                y += 9;

                data.labels.forEach((label, i) => {
                    const vC = data.canterano.valores[i], vP = data.profesional.valores[i];
                    const diff = vC - vP, diffAbs = Math.abs(diff);
                    if (i % 2 === 0) { pdf.setFillColor(14, 20, 46); pdf.rect(M, y, CW, 8, 'F'); }
                    cx = M + 3;
                    pdf.setFont('helvetica', 'normal'); pdf.setTextColor(180, 190, 210); pdf.setFontSize(7);
                    pdf.text(label, cx, y + 5.5); cx += colW[0];
                    pdf.setTextColor(diff > 0 ? 100 : 180, diff > 0 ? 170 : 200, diff > 0 ? 255 : 220);
                    if (diff > 0) pdf.setFont('helvetica', 'bold');
                    pdf.text(`${vC}`, cx, y + 5.5); cx += colW[1];
                    pdf.setFont('helvetica', 'bold');
                    if (diff === 0) { pdf.setTextColor(120,130,160); pdf.text('=', cx, y + 5.5); }
                    else if (diff > 0) { pdf.setTextColor(80,150,255); pdf.text(`+${diffAbs}`, cx, y + 5.5); }
                    else { pdf.setTextColor(210,70,90); pdf.text(`-${diffAbs}`, cx, y + 5.5); }
                    cx += colW[2];
                    pdf.setFont(diff < 0 ? 'bold' : 'normal', 'normal');
                    pdf.setTextColor(diff < 0 ? 220 : 180, diff < 0 ? 80 : 200, diff < 0 ? 100 : 220);
                    pdf.text(`${vP}`, cx, y + 5.5); cx += colW[3];
                    pdf.setFont('helvetica', 'bold');
                    if (diff > 0) { pdf.setTextColor(80,150,255); pdf.text('>> ' + data.canterano.nombre.split(' ')[0], cx, y + 5.5); }
                    else if (diff < 0) { pdf.setTextColor(210,70,90); pdf.text('>> ' + data.profesional.nombre.split(' ')[0], cx, y + 5.5); }
                    else { pdf.setTextColor(120,130,160); pdf.text('Empate', cx, y + 5.5); }
                    y += 8;
                });

                pdf.setDrawColor(255, 215, 0); pdf.setLineWidth(0.3); pdf.line(M, y, W - M, y);

                // Footer pág 1
                pdf.setFillColor(15, 10, 30); pdf.rect(0, H - 14, W, 14, 'F');
                pdf.setDrawColor(255, 215, 0); pdf.setLineWidth(0.3); pdf.line(M, H - 14, W - M, H - 14);
                pdf.setTextColor(100, 110, 140); pdf.setFontSize(6.5); pdf.setFont('helvetica', 'normal');
                pdf.text(`METRICGOAL · Sistema de Analisis de Cantera · ${new Date().getFullYear()}`, W / 2, H - 6, { align: 'center' });
                pdf.setTextColor(255, 215, 0); pdf.text('1', W - M, H - 6, { align: 'right' });

                // ─── PÁGINA 2: Gráficos ────────────────────
                pdf.addPage();
                pdf.setFillColor(8, 12, 30); pdf.rect(0, 0, W, H, 'F');
                pdf.setFillColor(100, 0, 25); pdf.rect(0, 0, W, 20, 'F');
                pdf.setFillColor(255, 215, 0); pdf.rect(0, 20, W, 1, 'F');

                pdf.setFillColor(165, 0, 68); pdf.circle(M + 7, 10, 5.5, 'F');
                pdf.setDrawColor(255, 215, 0); pdf.setLineWidth(0.5); pdf.circle(M + 7, 10, 5.5, 'S');
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(6); pdf.setFont('helvetica', 'bold');
                pdf.text('MG', M + 7, 12, { align: 'center' });
                pdf.setTextColor(255, 255, 255); pdf.setFontSize(10);
                pdf.text('METRICGOAL', M + 17, 9);
                pdf.setTextColor(200, 200, 220); pdf.setFontSize(6.5); pdf.setFont('helvetica', 'normal');
                pdf.text(`${data.canterano.nombre} vs ${data.profesional.nombre} · ${temporadaSeleccionada}`, M + 17, 15.5);
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(7);
                pdf.text('2', W - M, 13, { align: 'right' });

                y = 30;
                pdf.setTextColor(255, 215, 0); pdf.setFontSize(8); pdf.setFont('helvetica', 'bold');
                pdf.text('> ANALISIS RADAR MULTIDIMENSIONAL', M, y);
                y += 4;

                const radarCanvas = await html2canvas(document.getElementById('_pdf-radar'), { backgroundColor: '#0f172a', scale: window.devicePixelRatio > 1 ? 1 : 2, useCORS: true, logging: false });
                const radarImg = radarCanvas.toDataURL('image/png');
                const rH = Math.min((radarCanvas.height / radarCanvas.width) * CW, 105);
                pdf.addImage(radarImg, 'PNG', M, y, CW, rH);
                y += rH + 12;

                pdf.setTextColor(255, 215, 0); pdf.setFontSize(8);
                pdf.text('> COMPARATIVA POR METRICA', M, y);
                y += 4;

                const barrasCanvas = await html2canvas(document.getElementById('_pdf-barras'), { backgroundColor: '#0f172a', scale: window.devicePixelRatio > 1 ? 1 : 2, useCORS: true, logging: false });
                const barrasImg = barrasCanvas.toDataURL('image/png');
                const bH = Math.min((barrasCanvas.height / barrasCanvas.width) * CW, 95);
                pdf.addImage(barrasImg, 'PNG', M, y, CW, bH);
                y += bH + 12;

                if (y < H - 55) {
                    const perdidas = data.labels.filter((_, i) => data.canterano.valores[i] < data.profesional.valores[i]).length;
                    const pct = Math.round((ganadasCan / data.labels.length) * 100);
                    pdf.setFillColor(12, 18, 42); pdf.roundedRect(M, y, CW, 38, 4, 4, 'F');
                    pdf.setDrawColor(255, 215, 0); pdf.setLineWidth(0.35); pdf.roundedRect(M, y, CW, 38, 4, 4, 'S');
                    pdf.setFillColor(255, 215, 0); pdf.roundedRect(M, y, 3, 38, 2, 2, 'F');
                    pdf.setTextColor(255, 215, 0); pdf.setFontSize(8); pdf.setFont('helvetica', 'bold');
                    pdf.text('CONCLUSION DEL ANALISIS', M + 8, y + 10);
                    pdf.setTextColor(180, 190, 215); pdf.setFontSize(7); pdf.setFont('helvetica', 'normal');
                    const txt = `${data.canterano.nombre} supera a ${data.profesional.nombre} en ${ganadasCan} de ${data.labels.length} metricas (${pct}%). El profesional de referencia aventaja en ${perdidas} categorias. Este informe ha sido generado automaticamente por METRICGOAL para el seguimiento y desarrollo de la cantera del ${club}.`;
                    pdf.text(pdf.splitTextToSize(txt, CW - 16), M + 8, y + 19);
                }

                // Footer pág 2
                pdf.setFillColor(15, 10, 30); pdf.rect(0, H - 14, W, 14, 'F');
                pdf.setDrawColor(255, 215, 0); pdf.setLineWidth(0.3); pdf.line(M, H - 14, W - M, H - 14);
                pdf.setTextColor(100, 110, 140); pdf.setFontSize(6.5); pdf.setFont('helvetica', 'normal');
                pdf.text(`METRICGOAL · Sistema de Analisis de Cantera · ${new Date().getFullYear()}`, W / 2, H - 6, { align: 'center' });

                const fname = `MG_${data.canterano.nombre.replace(/\s+/g,'_')}_vs_${data.profesional.nombre.replace(/\s+/g,'_')}_${temporadaSeleccionada.replace('/','_')}.pdf`;
                pdf.save(fname);

                // Limpieza
                contenedor.innerHTML = '';

            } catch (err) {
                console.error('Error exportando PDF:', err);
                mostrarToast(`Error al generar PDF: ${err.message}`);
            }
        }

        function mostrarToast(msg) {
            const t = document.getElementById('toast-informes');
            t.textContent = msg;
            t.style.display = 'block';
            setTimeout(() => t.classList.add('activo'), 10);
            setTimeout(() => { t.classList.remove('activo'); setTimeout(() => t.style.display = 'none', 400); }, 3000);
        }

        window.onload = () => cargarInformesGuardados();

        /* ── Cierra dropdowns al hacer click fuera ── */
document.addEventListener('click', (e) => {
    if (!e.target.closest('.tarjeta-informe')) {
        document.querySelectorAll('.informe-dropdown.abierto').forEach(d => d.classList.remove('abierto'));
    }
});
 
/* ── Genera la tarjeta DOM ── */
function crearTarjetaInforme(inf) {
    const { totalMetricas, ganadas, pct } = calcularResumenInforme(inf);
    const fecha = formatearFecha(inf.fecha, { day: '2-digit', month: 'short', year: 'numeric' });
    const nombreCan = inf.canterano?.nombre || '—';
    const nombrePro = inf.profesional?.nombre || '—';
    const primerNombre = nombreCan.split(' ')[0];
 
    const card = document.createElement('div');
    card.className = 'tarjeta-informe';
    card.innerHTML = `
        <!-- Menú 3 puntos -->
        <button class="btn-informe-menu" title="Opciones" aria-label="Opciones">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <circle cx="8" cy="2.5" r="1.4"/>
                <circle cx="8" cy="8"   r="1.4"/>
                <circle cx="8" cy="13.5" r="1.4"/>
            </svg>
        </button>
        <div class="informe-dropdown" role="menu">
            <button class="btn-dd-pdf" role="menuitem">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                Exportar PDF
            </button>
            <div class="informe-dropdown-sep"></div>
            <button class="btn-dd-eliminar danger" role="menuitem">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
                Eliminar
            </button>
        </div>
 
        <!-- Cabecera -->
        <div class="informe-tipo" style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#475569;font-weight:700;margin-bottom:10px;">⚽ Comparación · ${inf.temporada || '—'}</div>
        <div class="informe-nombres">
            <div class="informe-nombre-can">${nombreCan}</div>
            <div class="informe-vs">vs</div>
            <div class="informe-nombre-pro">${nombrePro}</div>
        </div>
 
        <!-- Meta -->
        <div class="informe-meta" style="margin-top:12px;">
            <div class="informe-badge">
                <span class="informe-badge-label">Fecha</span>
                <span class="informe-badge-valor">${fecha}</span>
            </div>
            <div class="informe-badge">
                <span class="informe-badge-label">Resultado</span>
                <span class="informe-badge-valor">${ganadas}/${totalMetricas} ✓</span>
            </div>
        </div>
 
        <!-- Barra -->
        <div class="informe-barra-wrap" style="margin-top:12px;">
            <div class="informe-barra-label">
                <span>${primerNombre}</span>
                <span>${pct}%</span>
            </div>
            <div class="informe-barra">
                <div class="informe-barra-fill" style="width:${pct}%"></div>
            </div>
        </div>
 
        <!-- Botón Abrir -->
        <button class="btn-inf-abrir">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <rect x="3" y="3" width="18" height="18" rx="3"/>
                <line x1="9" y1="12" x2="15" y2="12"/>
                <line x1="12" y1="9" x2="15" y2="12"/>
                <line x1="12" y1="15" x2="15" y2="12"/>
            </svg>
            Abrir informe
        </button>
    `;
 
    /* Eventos */
    const menuBtn = card.querySelector('.btn-informe-menu');
    const dropdown = card.querySelector('.informe-dropdown');
 
    menuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        /* Cierra otros */
        document.querySelectorAll('.informe-dropdown.abierto').forEach(d => {
            if (d !== dropdown) d.classList.remove('abierto');
        });
        dropdown.classList.toggle('abierto');
    });
 
    card.querySelector('.btn-dd-pdf').addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.remove('abierto');
        exportarInformePDF(inf);
    });
 
    card.querySelector('.btn-dd-eliminar').addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.remove('abierto');
        eliminarInforme(inf.id);
    });
 
    card.querySelector('.btn-inf-abrir').addEventListener('click', () => {
        abrirModalInforme(inf);
    });
 
    return card;
}
 
/* ══════════════════════════════════════════
   MODAL — abrir
   ══════════════════════════════════════════ */
function abrirModalInforme(inf) {
    const modal = document.getElementById('modal-informe');
    const panel = document.getElementById('modal-panel-inner');
 
    const nombreCan = inf.canterano?.nombre || '—';
    const nombrePro = inf.profesional?.nombre || '—';
    const labels    = Array.isArray(inf.labels) ? inf.labels : [];
    const valCan    = inf.canterano?.valores || [];
    const valPro    = inf.profesional?.valores || [];
 
    const ganadas  = labels.filter((_, i) => (valCan[i] ?? 0) > (valPro[i] ?? 0)).length;
    const perdidas = labels.filter((_, i) => (valCan[i] ?? 0) < (valPro[i] ?? 0)).length;
    const empates  = labels.length - ganadas - perdidas;
    const pct      = labels.length > 0 ? Math.round((ganadas / labels.length) * 100) : 0;
    const fecha    = formatearFecha(inf.fecha, { day: '2-digit', month: 'long', year: 'numeric' });
 
    /* ── Filas de tabla ── */
    const filas = labels.map((label, i) => {
        const vC = valCan[i] ?? 0;
        const vP = valPro[i] ?? 0;
        const maxV = Math.max(vC, vP, 1);
        const pctC = Math.round((vC / maxV) * 100);
        const pctP = Math.round((vP / maxV) * 100);
        const diff = vC - vP;
 
        const ventajaHtml = diff > 0
            ? `<span class="ventaja-pill ventaja-can">▲ ${nombreCan.split(' ')[0]}</span>`
            : diff < 0
                ? `<span class="ventaja-pill ventaja-pro">▲ ${nombrePro.split(' ')[0]}</span>`
                : `<span class="ventaja-pill ventaja-tie">= Empate</span>`;
 
        const diffHtml = diff === 0
            ? `<span style="color:#475569;font-weight:600">—</span>`
            : diff > 0
                ? `<span style="color:#60a5fa;font-weight:700">+${Math.abs(diff)}</span>`
                : `<span style="color:#fca5a5;font-weight:700">−${Math.abs(diff)}</span>`;
 
        return `<tr>
            <td>${label}</td>
            <td class="t-center">
                <div class="barra-mini-wrap">
                    <div class="barra-mini"><div class="barra-mini-fill" style="width:${pctC}%;background:#3b82f6;"></div></div>
                    <span class="barra-mini-val" style="color:#60a5fa">${vC}</span>
                </div>
            </td>
            <td class="t-center">${diffHtml}</td>
            <td class="t-center">
                <div class="barra-mini-wrap">
                    <div class="barra-mini"><div class="barra-mini-fill" style="width:${pctP}%;background:#800020;"></div></div>
                    <span class="barra-mini-val" style="color:#fca5a5">${vP}</span>
                </div>
            </td>
            <td class="t-center">${ventajaHtml}</td>
        </tr>`;
    }).join('');
 
    /* ── Color KPI victorias ── */
    const kpiColor = pct >= 60 ? '#4ade80' : pct >= 40 ? '#fbbf24' : '#f87171';
 
    panel.innerHTML = `
        <!-- Header -->
        <div class="modal-header">
            <div class="modal-header-left">
                <div class="modal-badge-top">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                    Informe · ${inf.temporada || '—'}
                </div>
                <div class="modal-titulo-nombres">
                    <span class="modal-nombre-can">${nombreCan}</span>
                    <span class="modal-vs">vs</span>
                    <span class="modal-nombre-pro">${nombrePro}</span>
                </div>
                <div class="modal-meta-row">
                    <div class="modal-meta-pill">
                        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        <span>${fecha}</span>
                    </div>
                    <div class="modal-meta-pill">
                        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                        <span>${labels.length} métricas</span>
                    </div>
                </div>
            </div>
            <button class="btn-modal-cerrar" onclick="cerrarModalInforme()" aria-label="Cerrar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
        </div>
 
        <!-- KPIs -->
        <div class="modal-kpi-row">
            <div class="modal-kpi">
                <div class="modal-kpi-label">Victorias</div>
                <div class="modal-kpi-value" style="color:${kpiColor}">${pct}%</div>
                <div class="modal-kpi-sub">${ganadas} de ${labels.length}</div>
            </div>
            <div class="modal-kpi">
                <div class="modal-kpi-label">Ganadas</div>
                <div class="modal-kpi-value" style="color:#60a5fa">${ganadas}</div>
                <div class="modal-kpi-sub">métricas</div>
            </div>
            <div class="modal-kpi">
                <div class="modal-kpi-label">Empates</div>
                <div class="modal-kpi-value" style="color:#94a3b8">${empates}</div>
                <div class="modal-kpi-sub">métricas</div>
            </div>
            <div class="modal-kpi">
                <div class="modal-kpi-label">Por debajo</div>
                <div class="modal-kpi-value" style="color:#fca5a5">${perdidas}</div>
                <div class="modal-kpi-sub">métricas</div>
            </div>
        </div>
 
        <!-- Tabla comparativa -->
        <div class="modal-section" style="margin-top:18px;">
            <div class="modal-section-title">Tabla comparativa</div>
            <table class="modal-tabla">
                <thead>
                    <tr>
                        <th style="text-align:left">Métrica</th>
                        <th style="color:#60a5fa">${nombreCan.split(' ')[0].toUpperCase()}</th>
                        <th>DIFER.</th>
                        <th style="color:#fca5a5">${nombrePro.split(' ')[0].toUpperCase()}</th>
                        <th>VENTAJA</th>
                    </tr>
                </thead>
                <tbody>${filas}</tbody>
            </table>
        </div>
 
        <!-- Radar -->
        <div class="modal-radar-wrap" style="margin-top:20px;">
            <div class="modal-section-title">Análisis radar</div>
            <div class="modal-radar-canvas-container">
                <canvas id="modal-radar-canvas"></canvas>
                <div class="modal-leyenda">
                    <div class="modal-leyenda-item">
                        <div class="modal-leyenda-dot" style="background:#3b82f6"></div>
                        ${nombreCan}
                    </div>
                    <div class="modal-leyenda-item">
                        <div class="modal-leyenda-dot" style="background:#800020"></div>
                        ${nombrePro}
                    </div>
                </div>
            </div>
        </div>
 
        <!-- Conclusión -->
        <div class="modal-conclusion">
            <div class="modal-conclusion-title">📋 Conclusión del análisis</div>
            <div class="modal-conclusion-text">
                <strong>${nombreCan}</strong> supera a <strong>${nombrePro}</strong> en
                <strong style="color:#60a5fa">${ganadas} de ${labels.length} métricas</strong> (${pct}%).
                ${perdidas > 0 ? `El profesional de referencia aventaja en <strong style="color:#fca5a5">${perdidas} ${perdidas === 1 ? 'categoría' : 'categorías'}</strong>.` : ''}
                ${empates > 0 ? `Registran <strong>${empates} empate${empates > 1 ? 's' : ''}</strong>.` : ''}
                Informe generado por <strong>METRICGOAL</strong> · Temporada ${inf.temporada || '—'}.
            </div>
        </div>
    `;
 
    modal.classList.add('visible');
    document.body.style.overflow = 'hidden';
 
    /* Dibuja radar con Chart.js */
    requestAnimationFrame(() => {
        dibujarRadarModal(labels, valCan, valPro, nombreCan, nombrePro);
    });
}
 
function cerrarModalInforme() {
    const modal = document.getElementById('modal-informe');
    modal.classList.remove('visible');
    document.body.style.overflow = '';
    if (window._modalRadarChart) {
        window._modalRadarChart.destroy();
        window._modalRadarChart = null;
    }
}

window.cerrarModalInforme = cerrarModalInforme;
 
/* Cierra al click fuera del panel */
document.getElementById('modal-informe').addEventListener('click', (e) => {
    if (e.target === document.getElementById('modal-informe')) cerrarModalInforme();
});
 
/* Cierra con Escape */
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') cerrarModalInforme();
});
 
/* ── Radar con Chart.js (CDN) ── */
function dibujarRadarModal(labels, valCan, valPro, nombreCan, nombrePro) {
    const canvas = document.getElementById('modal-radar-canvas');
    if (!canvas) return;
 
    /* Normaliza a 0-100 */
    const normalized = (arr) => labels.map((_, i) => {
        const maxV = Math.max(valCan[i] ?? 0, valPro[i] ?? 0);
        return maxV > 0 ? Math.round(((arr[i] ?? 0) / maxV) * 100) : 0;
    });
 
    const cargar = () => {
        if (window._modalRadarChart) window._modalRadarChart.destroy();
        const ctx = canvas.getContext('2d');
        window._modalRadarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels,
                datasets: [
                    {
                        label: nombreCan,
                        data: normalized(valCan),
                        backgroundColor: 'rgba(59,130,246,0.2)',
                        borderColor: '#3b82f6',
                        borderWidth: 2.5,
                        pointBackgroundColor: '#3b82f6',
                        pointRadius: 4,
                        pointHoverRadius: 6,
                    },
                    {
                        label: nombrePro,
                        data: normalized(valPro),
                        backgroundColor: 'rgba(128,0,32,0.2)',
                        borderColor: '#800020',
                        borderWidth: 2.5,
                        pointBackgroundColor: '#800020',
                        pointRadius: 4,
                        pointHoverRadius: 6,
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    r: {
                        min: 0, max: 105,
                        ticks: { display: false, stepSize: 25 },
                        grid: { color: 'rgba(255,255,255,0.08)' },
                        angleLines: { color: 'rgba(255,255,255,0.08)' },
                        pointLabels: {
                            color: '#94a3b8',
                            font: { size: 12, weight: '600' }
                        }
                    }
                }
            }
        });
    };
 
    if (window.Chart) {
        cargar();
    } else {
        const s = document.createElement('script');
        s.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js';
        s.onload = cargar;
        document.head.appendChild(s);
    }
}

async function cargarStatsEquipo() {
    const idEquipo = obtenerIdEquipo();
    if (!idEquipo) return;
    try {
        const data = await apiJson(`/stats_equipo?id_equipo=${idEquipo}`);
        document.getElementById('stat-jugadores').querySelector('.stat-global-valor').textContent = data.total_jugadores ?? '—';
        document.getElementById('stat-partidos').querySelector('.stat-global-valor').textContent = data.total_partidos ?? '—';
        document.getElementById('stat-goles').querySelector('.stat-global-valor').textContent = data.total_goles ?? '—';
        document.getElementById('stat-asistencias').querySelector('.stat-global-valor').textContent = data.total_asistencias ?? '—';
        document.getElementById('stat-pases').querySelector('.stat-global-valor').textContent = data.total_pases_clave ?? '—';
    } catch (err) {
        console.error('Error cargando stats globales:', err);
    }
}
 
async function cargarInformesGuardados() {
    const grid = document.getElementById('grid-informes-guardados');
    const idEquipo = obtenerIdEquipo();
 
    if (!idEquipo) {
        grid.innerHTML = `
            <div class="informes-vacio" style="grid-column:1/-1;">
                <div class="vacio-icono">⚠️</div>
                <p>Sesión no encontrada</p>
                <small>Vuelve a <a href="/" style="color:#ffd700">iniciar sesión</a></small>
            </div>`;
        return;
    }
 
    try {
        const payload = await apiJson(`/listar_informes?id_equipo=${idEquipo}`);
        const informes = normalizarInformes(payload);
 
        if (informes.length === 0) {
            grid.innerHTML = `
                <div class="informes-vacio" style="grid-column:1/-1;">
                    <div class="vacio-icono">📊</div>
                    <p>No hay informes guardados todavía</p>
                    <small>Compara jugadores y guarda el análisis desde <strong style="color:#ffd700">Comparar Jugadores</strong></small>
                </div>`;
            return;
        }
 
        grid.innerHTML = '';
        informes.forEach(inf => grid.appendChild(crearTarjetaInforme(inf)));
 
    } catch (err) {
        console.error('Error cargando informes:', err);
        grid.innerHTML = `
            <div class="informes-vacio" style="grid-column:1/-1;">
                <div class="vacio-icono">❌</div>
                <p>No se pudieron cargar los informes</p>
                <small>${err.message}</small>
            </div>`;
    }
}

async function cargarDestacados() {
    const idEquipo = obtenerIdEquipo();
    if (!idEquipo) return;

    try {
        const data = await apiJson(`/stats_destacados?id_equipo=${idEquipo}`);

        const cardGoleador = document.getElementById('card-goleador');
        if (data.goleador) {
            cardGoleador.querySelector('.nombre-jugador').textContent = 
                `${data.goleador.nombre} ${data.goleador.apellidos}`;
            cardGoleador.querySelector('.dato-estadistico').textContent = 
                `${data.goleador.goles} goles`;
        } else {
            cardGoleador.querySelector('.nombre-jugador').textContent = 'Sin datos';
            cardGoleador.querySelector('.dato-estadistico').textContent = '—';
        }

        const cardAsistente = document.getElementById('card-asistente');
        if (data.asistente) {
            cardAsistente.querySelector('.nombre-jugador').textContent = 
                `${data.asistente.nombre} ${data.asistente.apellidos}`;
            cardAsistente.querySelector('.dato-estadistico').textContent = 
                `${data.asistente.asistencias} asistencias`;
        } else {
            cardAsistente.querySelector('.nombre-jugador').textContent = 'Sin datos';
            cardAsistente.querySelector('.dato-estadistico').textContent = '—';
        }

    } catch (err) {
        console.error('Error cargando destacados:', err);
    }
}

window.onload = () => {
    cargarInformesGuardados();
    cargarDestacados();
    cargarStatsEquipo();
};

window.logout = logout;

});