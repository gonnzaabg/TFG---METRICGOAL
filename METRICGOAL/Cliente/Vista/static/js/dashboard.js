document.addEventListener('DOMContentLoaded', () => {
    window.onload = function() {
        const nombre = localStorage.getItem('usuarioNombre');
        if (!nombre) { window.location.href = '/'; return; }
        document.getElementById('clubDisplay').textContent = localStorage.getItem('usuarioClub')?.toUpperCase() || "CLUB NO ASIGNADO";
        document.getElementById('coachDisplay').textContent = nombre.replace("Bienvenido, ", "") + " — " + (localStorage.getItem('usuarioEquipo') || "Sin equipo");
        cargarJugadores();
    };

    const carruseles = {
        Delantero: { jugadores: [], pagina: 0 },
        Mediocentro: { jugadores: [], pagina: 0 },
        Defensa: { jugadores: [], pagina: 0 },
        Portero: { jugadores: [], pagina: 0 }
    };

    const getPorPagina = () => window.innerWidth <= 768 ? 2 : 3;

    async function cargarJugadores() {
        try {
            const idEquipo = localStorage.getItem('idEquipo');
            if (!idEquipo || idEquipo === "null") return;
            const response = await fetch(`/obtener_jugadores?id_equipo=${idEquipo}`);
            const jugadores = await response.json();
            Object.keys(carruseles).forEach(pos => { carruseles[pos].jugadores = []; carruseles[pos].pagina = 0; });
            jugadores.forEach(j => { if (carruseles[j.posicion]) carruseles[j.posicion].jugadores.push(j); });
            Object.keys(carruseles).forEach(pos => renderCarrusel(pos));
        } catch (error) { console.error("Error cargando jugadores:", error); }
    }

    function crearCajaJugador(j) {
        const caja = document.createElement('div');
        caja.className = 'caja-jugador';
        caja.innerHTML = `
            <div class="menu-jugador">
                <button class="btn-menu" onclick="toggleMenu(event, this)">⋮</button>
                <div class="menu-dropdown">
                    <button onclick="confirmarEliminarJugador(event, ${j.id_jugador})">
                        <span>🗑️</span> Eliminar
                    </button>
                </div>
            </div>
            <strong>${j.nombre} ${j.apellidos || j.apellido}</strong>
            <span style="
                font-size: 0.68rem; font-weight: 600;
                color: rgba(255,215,0,0.55);
                text-transform: uppercase; letter-spacing: 1px;
            ">${j.posicion}${j.edad ? ' · ' + j.edad + ' años' : ''}</span>
        `;
        caja.onclick = (e) => {
            if (!e.target.classList.contains('btn-menu')) {
                abrirModalStats(j.id_jugador, `${j.nombre} ${j.apellidos || j.apellido}`);
            }
        };
        return caja;
    }

    function renderCarrusel(pos, direccion = null) {
        const estado = carruseles[pos];
        const seccion = document.getElementById(`seccion-${pos}`);
        const track = document.getElementById(`track-${pos}`);
        const dotsContainer = document.getElementById(`dots-${pos}`);
        const fila = document.getElementById(`fila-${pos}`);

        if (seccion) seccion.style.display = 'block';

        if (estado.jugadores.length === 0) {
            track.innerHTML = `
                <div style="
                    width: 100%;
                    min-height: 110px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                    text-align: center;
                    flex: 1;
                ">
                    <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; 
                        letter-spacing: 1.2px; color: rgba(255,255,255,0.2);">
                        Sin jugadores en esta posición
                    <div style="
                        font-size: 0.72rem; font-weight: 700;
                        color: #ffd700;
                        cursor: pointer;
                        letter-spacing: 1px;
                        text-shadow: 0 0 8px rgba(255,215,0,0.6), 0 0 16px rgba(255,215,0,0.3);
                        animation: pulseGold 2s ease-in-out infinite;
                    " onclick="abrirModal()">
                        Añadir jugador
                    </div>
                </div>`;
            dotsContainer.innerHTML = '';
            fila.querySelector('.flecha-izq').classList.add('flecha-disabled');
            fila.querySelector('.flecha-der').classList.add('flecha-disabled');
            return;
        }

        const pp = getPorPagina();
        const totalPaginas = Math.ceil(estado.jugadores.length / pp) || 1;
        const inicio = estado.pagina * pp;
        const slice = estado.jugadores.slice(inicio, inicio + pp);

        track.classList.remove('slide-right', 'slide-left');
        void track.offsetWidth;
        if (direccion === 1)  track.classList.add('slide-right');
        if (direccion === -1) track.classList.add('slide-left');

        track.innerHTML = '';
        slice.forEach(j => track.appendChild(crearCajaJugador(j)));

        dotsContainer.innerHTML = '';
        if (totalPaginas > 1) {
            for (let i = 0; i < totalPaginas; i++) {
                const dot = document.createElement('span');
                dot.className = 'dot' + (i === estado.pagina ? ' active' : '');
                dot.onclick = () => irAPagina(pos, i);
                dotsContainer.appendChild(dot);
            }
        }

        const flechaIzq = fila.querySelector('.flecha-izq');
        const flechaDer = fila.querySelector('.flecha-der');
        flechaIzq.classList.toggle('flecha-disabled', estado.pagina === 0);
        flechaDer.classList.toggle('flecha-disabled', estado.pagina >= totalPaginas - 1);
    }

    function moverCarrusel(pos, dir) {
        const estado = carruseles[pos];
        const totalPaginas = Math.ceil(estado.jugadores.length / getPorPagina()) || 1;
        const nuevaPagina = estado.pagina + dir;
        if (nuevaPagina < 0 || nuevaPagina >= totalPaginas) return;
        estado.pagina = nuevaPagina;
        renderCarrusel(pos, dir);
    }

    function irAPagina(pos, pagina) {
        const dir = pagina > carruseles[pos].pagina ? 1 : -1;
        carruseles[pos].pagina = pagina;
        renderCarrusel(pos, dir);
    }

    window.addEventListener('resize', () => {
        Object.keys(carruseles).forEach(pos => { carruseles[pos].pagina = 0; renderCarrusel(pos); });
    });

    document.getElementById('formJugador').onsubmit = async function(e) {
        e.preventDefault();
        const idEquipo = localStorage.getItem('idEquipo');
        const datosJugador = {
            nombre: document.getElementById('nombreJ').value,
            apellidos: document.getElementById('apellidoJ').value,
            edad: parseInt(document.getElementById('edadJ').value),
            posicion: document.getElementById('posicionJ').value
        };
        try {
            const response = await fetch(`/registrar_jugador?id_equipo=${idEquipo}`, {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(datosJugador)
            });
            if (response.ok) { cerrarModal(); cargarJugadores(); }
            else { const err = await response.json(); alert("Error: " + (err.detail || "Error desconocido")); }
        } catch (err) { alert("Error de conexión"); }
    };

    function abrirModal() { document.getElementById('modalJugador').style.display = 'flex'; }
    function cerrarModal() { document.getElementById('modalJugador').style.display = 'none'; document.getElementById('formJugador').reset(); }
    function logout() { localStorage.clear(); window.location.href = '/'; }

    function abrirModalStats(id, nombreCompleto) {
        document.getElementById('idJugadorStats').value = id;
        document.getElementById('statsTitulo').textContent = `Estadísticas: ${nombreCompleto}`;
        document.getElementById('modalEstadisticas').style.display = 'flex';
        consultarStats();
    }

    function cerrarModalStats() {
        document.getElementById('modalEstadisticas').style.display = 'none';
        ['goles','asist','amarillas','rojas','pj','min','pases'].forEach(id => {
            const el = document.getElementById(id); if (el) el.value = '';
        });
        document.getElementById('idJugadorStats').value = '';
    }

    async function consultarStats() {
        const idJugador = document.getElementById('idJugadorStats').value;
        const temp = document.getElementById('temporada').value;

        if (!idJugador || !temp) {
            console.warn("Faltan parámetros:", { idJugador, temp });
            return;
        }

        try {
            const response = await fetch(`/obtener_stats?id_jugador=${idJugador}&temporada=${temp}`);
            if (response.ok) {
                const data = await response.json();
                if (data) {
                    document.getElementById('goles').value = data.goles;
                    document.getElementById('asist').value = data.asistencias;
                    document.getElementById('amarillas').value = data.tarj_amarillas;
                    document.getElementById('rojas').value = data.tarj_rojas;
                    document.getElementById('pj').value = data.partidos_jugados;
                    document.getElementById('min').value = data.minutos_jugados;
                    document.getElementById('pases').value = data.pases_clave;
                } else { resetearInputsStats(); }
            }
        } catch (err) { console.error("Error al consultar stats:", err); }
    }

    function toggleMenu(event, element) {
        event.stopPropagation();
        document.querySelectorAll('.menu-dropdown').forEach(m => m.classList.remove('show-menu'));
        element.nextElementSibling.classList.toggle('show-menu');
    }

    let idJugadorAEliminar = null;
    function confirmarEliminarJugador(event, id) {
        event.stopPropagation();
        idJugadorAEliminar = id;
        document.getElementById('modalConfirmar').style.display = 'flex';
    }
    function cerrarConfirmar() {
        document.getElementById('modalConfirmar').style.display = 'none';
        idJugadorAEliminar = null;
    }

    document.addEventListener('click', async (e) => {
        if (e.target && e.target.id === 'btnConfirmarEliminar') {
            if (!idJugadorAEliminar) return;
            try {
                const response = await fetch(`/eliminar_jugador/${idJugadorAEliminar}`, { method: 'DELETE' });
                if (response.ok) {
                    cerrarConfirmar();
                    mostrarNotificacion("🗑️ Jugador eliminado");
                    setTimeout(() => cargarJugadores(), 300);
                } else { mostrarNotificacion("❌ Error al eliminar"); }
            } catch (error) { mostrarNotificacion("❌ Error de conexión"); }
        }
    });

    window.addEventListener('click', () => {
        document.querySelectorAll('.menu-dropdown').forEach(m => m.classList.remove('show-menu'));
    });

    function resetearInputsStats() {
        ['goles','asist','amarillas','rojas','pj','min','pases'].forEach(id => {
            const el = document.getElementById(id); if (el) el.value = '';
        });
    }

    document.getElementById('formEstadisticas').onsubmit = async function(e) {
        e.preventDefault();
        const btn = e.target.querySelector('.btn-guardar');
        const orig = btn.textContent;
        btn.textContent = "Guardando..."; btn.disabled = true;
        const idJugador = document.getElementById('idJugadorStats').value;
        const stats = {
            temporada: document.getElementById('temporada').value,
            goles: parseInt(document.getElementById('goles').value),
            asistencias: parseInt(document.getElementById('asist').value),
            tarj_amarillas: parseInt(document.getElementById('amarillas').value),
            tarj_rojas: parseInt(document.getElementById('rojas').value),
            partidos_jugados: parseInt(document.getElementById('pj').value),
            minutos_jugados: parseInt(document.getElementById('min').value),
            pases_clave: parseInt(document.getElementById('pases').value)
        };
        try {
            const response = await fetch(`/registrar_estadisticas?id_jugador=${idJugador}`, {
                method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(stats)
            });
            if (response.ok) {
                cerrarModalStats();
                mostrarNotificacion("✅ Estadísticas actualizadas");
            } else {
                const errorData = await response.json();
                console.error("❌ Error del servidor:", errorData);
                mostrarNotificacion("❌ Error al actualizar: " + (errorData.detail || "Error desconocido"));
            }
        } catch (err) { alert("❌ Error de conexión: " + err); }
        finally { btn.textContent = orig; btn.disabled = false; }
    };

    function mostrarNotificacion(mensaje) {
        const toast = document.getElementById('toast');
        if (!toast) return;
        toast.textContent = mensaje;
        toast.style.display = 'block';
        setTimeout(() => toast.classList.add('toast-active'), 10);
        setTimeout(() => {
            toast.classList.remove('toast-active');
            setTimeout(() => toast.style.display = 'none', 500);
        }, 3000);
    }

    window.logout = logout;
    window.abrirModal = abrirModal;
    window.cerrarModal = cerrarModal;
    window.moverCarrusel = moverCarrusel;
    window.abrirModalStats = abrirModalStats;
    window.cerrarModalStats = cerrarModalStats;
    window.consultarStats = consultarStats;
    window.toggleMenu = toggleMenu;
    window.confirmarEliminarJugador = confirmarEliminarJugador;
    window.cerrarConfirmar = cerrarConfirmar;
});