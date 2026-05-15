document.addEventListener('DOMContentLoaded', async () => {
    console.log(typeof TomSelect);

    let buscador;
    let temporadaSeleccionada = null;
    let datosComparacion = null;

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

    const elCanterano = document.querySelector('#select-canterano');
    if (elCanterano?.tomselect) {
        elCanterano.tomselect.destroy();
    }

    buscador = new TomSelect(elCanterano, {
        create: false,
        valueField: 'value',
        labelField: 'text',
        searchField: 'text',
        sortField: { field: 'text', direction: 'asc' },
        placeholder: 'Selecciona un canterano',
        onChange: async function(value) {
            if (!value) {
                document.getElementById('selector-temporada-wrapper').style.display = 'none';
                temporadaSeleccionada = null;
                return;
            }
            await cargarTemporadasCanterano(value);
        }
    });

    new TomSelect("#select-profesional", {
        maxItems: 1,
        hideSelected: true,
        allowEmptyOption: true,
        valueField: 'player',
        labelField: 'display_name',
        searchField: 'player',
        plugins: ['remove_button'],
        load: async function(query, callback) {
            if (query.length < 3) return callback();
            try {
                const res = await fetch(`/buscar_profesionales?nombre=${encodeURIComponent(query)}`);
                const data = await res.json();
                callback(data.map(p => ({
                    player: p.player,
                    display_name: `${p.player} (${p.team})`
                })));
            } catch {
                callback();
            }
        },
        render: {
            option: (item, escape) => `
                <div class="py-2">
                    <div style="font-weight:bold;color:white;">${escape(item.player)}</div>
                    <small style="color:#94a3b8;">${escape(item.display_name)}</small>
                </div>`,
            item: (item, escape) => `<div style="color:white;">${escape(item.display_name)}</div>`
        },
        onItemAdd: function() {
            this.blur();
        }
    });

    async function cargarJugadoresSelect() {
        const idEquipo = obtenerIdEquipo();
        if (!idEquipo) return;

        try {
            const response = await fetch(`/obtener_jugadores?id_equipo=${idEquipo}`);
            const jugadores = await response.json();

            buscador.clearOptions();

            jugadores.forEach(j => {
                buscador.addOption({
                    value: j.id_jugador,
                    text: `${j.nombre} ${j.apellidos || ''} (${j.posicion})`
                });
            });

            buscador.refreshOptions(false);
        } catch (error) {
            console.error("Error al cargar jugadores:", error);
        }
    }

    async function cargarTemporadasCanterano(idJugador) {
        const temporadas = ['2023/24', '2024/25', '2025/26'];
        const disponibles = [];

        for (const temp of temporadas) {
            try {
                const res = await fetch(`/obtener_stats?id_jugador=${idJugador}&temporada=${encodeURIComponent(temp)}`);
                const data = await res.json();
                if (data) disponibles.push(temp);
            } catch {}
        }

        const wrapper = document.getElementById('selector-temporada-wrapper');
        const tabsContainer = document.getElementById('temporada-tabs');
        tabsContainer.innerHTML = '';

        if (disponibles.length === 0) {
            wrapper.style.display = 'none';
            temporadaSeleccionada = null;
            return;
        }

        temporadaSeleccionada = disponibles[disponibles.length - 1];

        disponibles.forEach(temp => {
            const btn = document.createElement('button');
            btn.className = 'tab-temporada' + (temp === temporadaSeleccionada ? ' tab-activa' : '');
            btn.textContent = temp;
            btn.onclick = () => {
                temporadaSeleccionada = temp;
                document.querySelectorAll('.tab-temporada').forEach(b => b.classList.remove('tab-activa'));
                btn.classList.add('tab-activa');
            };
            tabsContainer.appendChild(btn);
        });

        wrapper.style.display = 'block';
    }

    async function realizarComparacion() {
        const idCanterano = document.getElementById('select-canterano').value;
        const nombreProfesional = document.getElementById('select-profesional').value;

        if (!idCanterano || !nombreProfesional) {
            alert("Por favor, selecciona ambos jugadores");
            return;
        }

        if (!temporadaSeleccionada) {
            const t = document.getElementById('toast-sin-stats');
            t.textContent = '⚠️ Aún no has introducido estadísticas para este jugador. Ve a Mi Equipo y selecciona al jugador para introducirlas.';
            t.style.display = 'block';
            setTimeout(() => t.classList.add('activo'), 17);
            setTimeout(() => {
                t.classList.remove('activo');
                setTimeout(() => t.style.display = 'none', 700);
            }, 4000);
            return;
        }

        try {
            const response = await fetch(
                `/api/comparar_jugadores?id_canterano=${idCanterano}&nombre_profesional=${encodeURIComponent(nombreProfesional)}&temporada=${encodeURIComponent(temporadaSeleccionada)}`
            );
            const data = await response.json();

            if (data.error) {
                const t = document.getElementById('toast-sin-stats');
                t.textContent = '⚠️ Aún no has introducido estadísticas para este jugador. Ve a Mi Equipo y selecciona al jugador para introducirlas.';
                t.style.display = 'block';
                setTimeout(() => t.classList.add('activo'), 17);
                setTimeout(() => {
                    t.classList.remove('activo');
                    setTimeout(() => t.style.display = 'none', 700);
                }, 4000);
                return;
            }

            datosComparacion = data;

            document.getElementById('seccion-metricas').style.display = 'flex';
            document.getElementById('barra-exportar').style.display = 'flex';
            document.getElementById('th-canterano').textContent = data.canterano.nombre;
            document.getElementById('th-profesional').textContent = data.profesional.nombre;

            const valCan = [];
            const valProf = [];

            data.labels.forEach((_, i) => {
                const vC = data.canterano.valores[i];
                const vP = data.profesional.valores[i];
                const max = Math.max(vC, vP);
                valCan.push(max > 0 ? (vC / max) * 100 : 0);
                valProf.push(max > 0 ? (vP / max) * 100 : 0);
            });

            Plotly.newPlot('grafico-radar', [
                {
                    type: 'scatterpolar',
                    r: valCan,
                    theta: data.labels,
                    fill: 'toself',
                    name: data.canterano.nombre,
                    customdata: data.canterano.valores,
                    hovertemplate: `<b>${data.canterano.nombre}</b><br>%{theta}: <b>%{customdata}</b><extra></extra>`,
                    line: { color: '#3b82f6', width: 3 },
                    fillcolor: 'rgba(59,130,246,0.3)'
                },
                {
                    type: 'scatterpolar',
                    r: valProf,
                    theta: data.labels,
                    fill: 'toself',
                    name: data.profesional.nombre,
                    customdata: data.profesional.valores,
                    hovertemplate: `<b>${data.profesional.nombre}</b><br>%{theta}: <b>%{customdata}</b><extra></extra>`,
                    line: { color: '#800020', width: 3 },
                    fillcolor: 'rgba(128,0,32,0.3)'
                }
            ], {
                polar: {
                    radialaxis: {
                        visible: true,
                        showticklabels: false,
                        gridcolor: "rgba(255,255,255,0.1)",
                        range: [0, 105]
                    },
                    angularaxis: {
                        gridcolor: "#334155",
                        color: "white",
                        tickfont: { size: 12 },
                        rotation: 90
                    },
                    bgcolor: "rgba(30,41,59,0.5)"
                },
                hovermode: 'closest',
                paper_bgcolor: "rgba(0,0,0,0)",
                plot_bgcolor: "rgba(0,0,0,0)",
                font: { color: "white" },
                showlegend: true,
                legend: {
                    orientation: "h",
                    y: -0.2,
                    x: 0.5,
                    xanchor: "center"
                },
                margin: { t: 40, b: 40, l: 80, r: 80 }
            }, { responsive: true });

            Plotly.newPlot('grafico-barras', [
                {
                    type: 'bar',
                    orientation: 'h',
                    name: data.canterano.nombre,
                    x: data.canterano.valores,
                    y: data.labels,
                    marker: {
                        color: 'rgba(59,130,246,0.85)',
                        line: { color: '#3b82f6', width: 1.5 }
                    },
                    hovertemplate: `<b>${data.canterano.nombre}</b>: %{x}<extra></extra>`
                },
                {
                    type: 'bar',
                    orientation: 'h',
                    name: data.profesional.nombre,
                    x: data.profesional.valores,
                    y: data.labels,
                    marker: {
                        color: 'rgba(128,0,32,0.85)',
                        line: { color: '#800020', width: 1.5 }
                    },
                    hovertemplate: `<b>${data.profesional.nombre}</b>: %{x}<extra></extra>`
                }
            ], {
                barmode: 'group',
                paper_bgcolor: "rgba(0,0,0,0)",
                plot_bgcolor: "rgba(0,0,0,0)",
                font: { color: "white", size: 12 },
                xaxis: { gridcolor: "rgba(255,255,255,0.08)", color: "white", zeroline: false },
                yaxis: { color: "white", automargin: true, tickfont: { size: 13 } },
                legend: { orientation: "h", y: -0.18, x: 0.5, xanchor: "center" },
                margin: { t: 20, b: 60, l: 140, r: 30 }
            }, { responsive: true });

            const tbody = document.getElementById('tabla-body');
            tbody.innerHTML = '';

            data.labels.forEach((label, i) => {
                const vC = data.canterano.valores[i];
                const vP = data.profesional.valores[i];
                const diff = vC - vP;
                const diffAbs = Math.abs(diff);

                let diffClass, diffText, tdCanClass = '', tdProfClass = '';

                if (diff === 0) {
                    diffClass = 'diff-empate';
                    diffText = '=';
                } else if (diff > 0) {
                    diffClass = 'diff-canton-gana';
                    diffText = `+${diffAbs}`;
                    tdCanClass = 'celda-ganador';
                } else {
                    diffClass = 'diff-prof-gana';
                    diffText = `-${diffAbs}`;
                    tdProfClass = 'celda-ganador';
                }

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="label-metrica">${label}</td>
                    <td class="${tdCanClass}">${vC}</td>
                    <td class="celda-diff ${diffClass}">${diffText}</td>
                    <td class="${tdProfClass}">${vP}</td>
                `;
                tbody.appendChild(tr);
            });

        } catch (error) {
            console.error("Error:", error);
            alert("No se pudo cargar el gráfico.");
        }
    }

    async function exportarPDF() {
        if (!datosComparacion) return;

        const btn = document.querySelector('.btn-pdf');
        const orig = btn.innerHTML;
        btn.innerHTML = '<span class="icono">⏳</span> Generando...';
        btn.disabled = true;

        try {
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
            const W = 210, H = 297, M = 14, CW = W - M * 2;
            const data = datosComparacion;
            const fecha = new Date().toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' });
            const club = (localStorage.getItem('usuarioClub') || 'Club').toUpperCase();

            pdf.setFillColor(8, 12, 30);
            pdf.rect(0, 0, W, H, 'F');

            pdf.setFillColor(100, 0, 25);
            pdf.rect(0, 0, W, 42, 'F');
            pdf.setFillColor(128, 0, 32);
            pdf.rect(0, 0, W * 0.5, 42, 'F');

            pdf.setFillColor(255, 215, 0);
            pdf.rect(0, 42, W, 1.5, 'F');

            pdf.setFillColor(165, 0, 68);
            pdf.circle(M + 11, 21, 9, 'F');
            pdf.setDrawColor(255, 215, 0);
            pdf.setLineWidth(0.8);
            pdf.circle(M + 11, 21, 9, 'S');
            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(10);
            pdf.setFont('helvetica', 'bold');
            pdf.text('MG', M + 11, 24, { align: 'center' });

            pdf.setTextColor(255, 255, 255);
            pdf.setFontSize(18);
            pdf.setFont('helvetica', 'bold');
            pdf.text('METRICGOAL', M + 25, 18);
            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(7);
            pdf.setFont('helvetica', 'normal');
            pdf.text('PLATAFORMA DE ANALISIS DE CANTERA PROFESIONAL', M + 25, 25);

            pdf.setTextColor(200, 200, 220);
            pdf.setFontSize(7.5);
            pdf.text(fecha, W - M, 16, { align: 'right' });
            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(8.5);
            pdf.setFont('helvetica', 'bold');
            pdf.text(club, W - M, 26, { align: 'right' });
            pdf.setTextColor(180, 180, 200);
            pdf.setFontSize(6.5);
            pdf.setFont('helvetica', 'normal');
            pdf.text(`Temporada ${temporadaSeleccionada}`, W - M, 34, { align: 'right' });

            let y = 58;
            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(7.5);
            pdf.setFont('helvetica', 'bold');
            pdf.text('> INFORME COMPARATIVO', M, y);

            y += 9;
            pdf.setTextColor(100, 160, 255);
            pdf.setFontSize(18);
            pdf.setFont('helvetica', 'bold');
            const w1 = pdf.getTextWidth(data.canterano.nombre);
            pdf.text(data.canterano.nombre, M, y);
            pdf.setTextColor(120, 120, 150);
            pdf.setFontSize(11);
            pdf.setFont('helvetica', 'normal');
            pdf.text(' vs ', M + w1 + 1, y);
            const wVs = pdf.getTextWidth(' vs ');
            pdf.setTextColor(220, 80, 110);
            pdf.setFontSize(18);
            pdf.setFont('helvetica', 'bold');
            pdf.text(data.profesional.nombre, M + w1 + wVs + 1, y);

            y += 4;
            pdf.setDrawColor(255, 215, 0);
            pdf.setLineWidth(0.5);
            pdf.line(M, y, W - M, y);

            y += 10;
            const cW = (CW - 10) / 3;

            const drawCard = (x, cy, titulo, valor, colorValor) => {
                pdf.setFillColor(15, 22, 50);
                pdf.roundedRect(x, cy, cW, 24, 3, 3, 'F');
                pdf.setDrawColor(255, 215, 0);
                pdf.setLineWidth(0.25);
                pdf.roundedRect(x, cy, cW, 24, 3, 3, 'S');
                pdf.setTextColor(120, 130, 160);
                pdf.setFontSize(6);
                pdf.setFont('helvetica', 'bold');
                pdf.text(titulo, x + cW / 2, cy + 8, { align: 'center' });
                pdf.setTextColor(...colorValor);
                pdf.setFontSize(13);
                pdf.setFont('helvetica', 'bold');
                pdf.text(valor, x + cW / 2, cy + 18, { align: 'center' });
            };

            const ganadasCan = data.labels.filter((_, i) => data.canterano.valores[i] > data.profesional.valores[i]).length;
            drawCard(M, y, 'TEMPORADA', temporadaSeleccionada || '—', [255, 215, 0]);
            drawCard(M + cW + 5, y, 'MÉTRICAS ANALIZADAS', `${data.labels.length}`, [200, 220, 255]);
            drawCard(M + (cW + 5) * 2, y, 'GANADAS (CANTERANO)', `${ganadasCan} / ${data.labels.length}`, [100, 200, 120]);

            y += 34;
            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(8);
            pdf.setFont('helvetica', 'bold');
            pdf.text('> TABLA COMPARATIVA DE MÉTRICAS', M, y);
            y += 6;

            const colW = [52, 34, 28, 34, 34];
            const nomCan = data.canterano.nombre.substring(0, 16).toUpperCase();
            const nomPro = data.profesional.nombre.substring(0, 16).toUpperCase();
            const cols = ['METRICA', nomCan, 'DIFER.', nomPro, 'VENTAJA'];

            pdf.setFillColor(128, 0, 32);
            pdf.roundedRect(M, y, CW, 9, 2, 2, 'F');
            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(6.5);
            pdf.setFont('helvetica', 'bold');
            let cx = M + 3;
            cols.forEach((col, i) => {
                pdf.text(col, cx, y + 6);
                cx += colW[i];
            });
            y += 9;

            data.labels.forEach((label, i) => {
                const vC = data.canterano.valores[i];
                const vP = data.profesional.valores[i];
                const diff = vC - vP;
                const diffAbs = Math.abs(diff);

                if (i % 2 === 0) {
                    pdf.setFillColor(14, 20, 46);
                    pdf.rect(M, y, CW, 8, 'F');
                }

                cx = M + 3;
                pdf.setFont('helvetica', 'normal');
                pdf.setTextColor(180, 190, 210);
                pdf.setFontSize(7);
                pdf.text(label, cx, y + 5.5);
                cx += colW[0];

                pdf.setTextColor(diff > 0 ? 100 : 180, diff > 0 ? 170 : 200, diff > 0 ? 255 : 220);
                if (diff > 0) pdf.setFont('helvetica', 'bold');
                pdf.text(`${vC}`, cx, y + 5.5);
                cx += colW[1];

                pdf.setFont('helvetica', 'bold');
                if (diff === 0) {
                    pdf.setTextColor(120, 130, 160);
                    pdf.text('=', cx, y + 5.5);
                } else if (diff > 0) {
                    pdf.setTextColor(80, 150, 255);
                    pdf.text(`+${diffAbs}`, cx, y + 5.5);
                } else {
                    pdf.setTextColor(210, 70, 90);
                    pdf.text(`-${diffAbs}`, cx, y + 5.5);
                }
                cx += colW[2];

                pdf.setFont(diff < 0 ? 'bold' : 'normal', 'normal');
                pdf.setTextColor(diff < 0 ? 220 : 180, diff < 0 ? 80 : 200, diff < 0 ? 100 : 220);
                pdf.text(`${vP}`, cx, y + 5.5);
                cx += colW[3];

                pdf.setFont('helvetica', 'bold');
                if (diff > 0) {
                    pdf.setTextColor(80, 150, 255);
                    pdf.text('>> ' + data.canterano.nombre.split(' ')[0], cx, y + 5.5);
                } else if (diff < 0) {
                    pdf.setTextColor(210, 70, 90);
                    pdf.text('>> ' + data.profesional.nombre.split(' ')[0], cx, y + 5.5);
                } else {
                    pdf.setTextColor(120, 130, 160);
                    pdf.text('Empate', cx, y + 5.5);
                }

                y += 8;
            });

            pdf.setDrawColor(255, 215, 0);
            pdf.setLineWidth(0.3);
            pdf.line(M, y, W - M, y);

            pdf.setFillColor(15, 10, 30);
            pdf.rect(0, H - 14, W, 14, 'F');
            pdf.setDrawColor(255, 215, 0);
            pdf.setLineWidth(0.3);
            pdf.line(M, H - 14, W - M, H - 14);
            pdf.setTextColor(100, 110, 140);
            pdf.setFontSize(6.5);
            pdf.setFont('helvetica', 'normal');
            pdf.text(`METRICGOAL · Sistema de Análisis de Cantera · ${new Date().getFullYear()}`, W / 2, H - 6, { align: 'center' });

            pdf.addPage();
            pdf.setFillColor(8, 12, 30);
            pdf.rect(0, 0, W, H, 'F');

            pdf.setFillColor(100, 0, 25);
            pdf.rect(0, 0, W, 20, 'F');
            pdf.setFillColor(255, 215, 0);
            pdf.rect(0, 20, W, 1, 'F');

            pdf.setFillColor(165, 0, 68);
            pdf.circle(M + 7, 10, 5.5, 'F');
            pdf.setDrawColor(255, 215, 0);
            pdf.setLineWidth(0.5);
            pdf.circle(M + 7, 10, 5.5, 'S');
            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(6);
            pdf.setFont('helvetica', 'bold');
            pdf.text('MG', M + 7, 12, { align: 'center' });

            pdf.setTextColor(255, 255, 255);
            pdf.setFontSize(10);
            pdf.text('METRICGOAL', M + 17, 9);
            pdf.setTextColor(200, 200, 220);
            pdf.setFontSize(6.5);
            pdf.setFont('helvetica', 'normal');
            pdf.text(`${data.canterano.nombre} vs ${data.profesional.nombre} · ${temporadaSeleccionada}`, M + 17, 15.5);
            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(7);
            pdf.text('2', W - M, 13, { align: 'right' });

            let y2 = 30;

            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(8);
            pdf.setFont('helvetica', 'bold');
            pdf.text('> ANALISIS RADAR MULTIDIMENSIONAL', M, y2);
            y2 += 4;

            const radarEl = document.getElementById('grafico-radar');
            const radarCanvas = await html2canvas(radarEl, { backgroundColor: '#0f172a', scale: 2, useCORS: true, logging: false });
            const radarImg = radarCanvas.toDataURL('image/png');
            const rH = Math.min((radarCanvas.height / radarCanvas.width) * CW, 105);
            pdf.addImage(radarImg, 'PNG', M, y2, CW, rH);
            y2 += rH + 12;

            pdf.setTextColor(255, 215, 0);
            pdf.setFontSize(8);
            pdf.text('> COMPARATIVA POR MÉTRICA', M, y2);
            y2 += 4;

            const barrasEl = document.getElementById('grafico-barras');
            const barrasCanvas = await html2canvas(barrasEl, { backgroundColor: '#0f172a', scale: 2, useCORS: true, logging: false });
            const barrasImg = barrasCanvas.toDataURL('image/png');
            const bH = Math.min((barrasCanvas.height / barrasCanvas.width) * CW, 95);
            pdf.addImage(barrasImg, 'PNG', M, y2, CW, bH);
            y2 += bH + 12;

            if (y2 < H - 55) {
                const perdidas = data.labels.filter((_, i) => data.canterano.valores[i] < data.profesional.valores[i]).length;
                const pct = Math.round((ganadasCan / data.labels.length) * 100);

                pdf.setFillColor(12, 18, 42);
                pdf.roundedRect(M, y2, CW, 38, 4, 4, 'F');
                pdf.setDrawColor(255, 215, 0);
                pdf.setLineWidth(0.35);
                pdf.roundedRect(M, y2, CW, 38, 4, 4, 'S');
                pdf.setFillColor(255, 215, 0);
                pdf.roundedRect(M, y2, 3, 38, 2, 2, 'F');

                pdf.setTextColor(255, 215, 0);
                pdf.setFontSize(8);
                pdf.setFont('helvetica', 'bold');
                pdf.text('CONCLUSION DEL ANÁLISIS', M + 8, y2 + 10);

                pdf.setTextColor(180, 190, 215);
                pdf.setFontSize(7);
                pdf.setFont('helvetica', 'normal');
                const txt = `${data.canterano.nombre} supera a ${data.profesional.nombre} en ${ganadasCan} de ${data.labels.length} metricas (${pct}%). El profesional de referencia aventaja en ${perdidas} categorías. Este informe ha sido generado automáticamente por METRICGOAL para el seguimiento y desarrollo de la cantera del ${club}.`;
                const lines = pdf.splitTextToSize(txt, CW - 16);
                pdf.text(lines, M + 8, y2 + 19);
            }

            pdf.setFillColor(15, 10, 30);
            pdf.rect(0, H - 14, W, 14, 'F');
            pdf.setDrawColor(255, 215, 0);
            pdf.setLineWidth(0.3);
            pdf.line(M, H - 14, W - M, H - 14);
            pdf.setTextColor(100, 110, 140);
            pdf.setFontSize(6.5);
            pdf.setFont('helvetica', 'normal');
            pdf.text(`METRICGOAL · Sistema de Análisis de Cantera · ${new Date().getFullYear()}`, W / 2, H - 6, { align: 'center' });

            const fname = `MG_${data.canterano.nombre.replace(/\s+/g, '_')}_vs_${data.profesional.nombre.replace(/\s+/g, '_')}_${(temporadaSeleccionada || '').replace('/', '_')}.pdf`;
            pdf.save(fname);

        } catch (err) {
            console.error('Error PDF:', err);
            alert('Error al generar el PDF.');
        } finally {
            btn.innerHTML = orig;
            btn.disabled = false;
        }
    }

    async function guardarEnInformes() {
        if (!datosComparacion) return;

        const idEquipo = obtenerIdEquipo();
        const btn = document.querySelector('.btn-guardar-informe');

        if (!idEquipo) {
            mostrarToast('❌ No se pudo identificar el equipo');
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<span class="icono">⏳</span> Guardando...';

        try {
            const response = await fetch(`/guardar_informe?id_equipo=${idEquipo}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    fecha: new Date().toISOString(),
                    temporada: temporadaSeleccionada,
                    canterano: datosComparacion.canterano.nombre,
                    profesional: datosComparacion.profesional.nombre,
                    datos: datosComparacion
                })
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                mostrarToast('✅ Informe guardado correctamente');
            } else {
                mostrarToast(`❌ ${result.detail || result.message || 'Error al guardar el informe'}`);
            }
        } catch (e) {
            console.error('Error guardando informe:', e);
            mostrarToast('❌ Error de conexión');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<span class="icono">📁</span> Guardar en Informes';
        }
    }

    function mostrarToast(msg) {
        const t = document.getElementById('toast-informe');
        t.textContent = msg;
        t.style.display = 'block';
        setTimeout(() => t.classList.add('activo'), 10);
        setTimeout(() => {
            t.classList.remove('activo');
            setTimeout(() => t.style.display = 'none', 400);
        }, 3200);
    }

    function logout() {
        localStorage.clear();
        window.location.href = '/';
    }

    window.realizarComparacion = realizarComparacion;
    window.guardarEnInformes = guardarEnInformes;
    window.exportarPDF = exportarPDF;
    window.logout = logout;

    await cargarJugadoresSelect();
});