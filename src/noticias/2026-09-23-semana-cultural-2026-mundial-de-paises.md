---
title: "Semana Cultural 2026: ¡Bienvenidos al Mundial de la Alegría en el Colegio CSD!"
fecha: 2026-09-23
autor: "Comité Cultural y Pedagógico CSD"
categoria: "Eventos"
resumen: "Del 28 de Octubre al 02 de Noviembre vivimos el 'Mundial: Un recorrido por países'. Consulta aquí el pasaporte interactivo, los horarios por jornada y escucha la canción oficial de nuestra fiesta escolar."
portada: "/assets/logo.png"
publicado: true
---

<!-- ========================================================
     CONTENEDOR DEL PLEGABLE INTERACTIVO INSTITUCIONAL CSD
     ======================================================== -->

<div class="cultural-container">

  <!-- REPRODUCTOR OFICIAL DE AUDIO DE LA SEMANA CULTURAL -->
  <div class="audio-player-banner">
    <div class="player-left">
      <div class="sound-wave" id="sound-wave" aria-hidden="true">
        <span></span><span></span><span></span><span></span><span></span>
      </div>
      <div class="player-info">
        <span class="player-label">🎵 CANCIÓN OFICIAL SEMANA CULTURAL</span>
        <strong id="song-title">El Orgullo del CSD</strong>
      </div>
    </div>
    
    <div class="player-controls">
      <button type="button" id="btn-audio-toggle" class="btn-play-pause" onclick="toggleAudio()">
        <span id="play-icon">▶️</span>
        <span id="play-text">Escuchar Canción</span>
      </button>
      <button type="button" class="btn-switch-song" onclick="switchSong()" title="Cambiar canción">
        🔄 Cambiar Tema
      </button>
    </div>

    <audio id="cultural-audio" loop preload="metadata">
      <source src="/assets/audio/El_Orgullo_del_CSD.mp3" type="audio/mpeg">
    </audio>
  </div>

  <!-- TARJETA PRINCIPAL ESTILO HISTORIETA & INSTITUCIONAL -->
  <div class="cultural-card">

    <!-- CABECERA INSTITUCIONAL CON LOGO Y COLORES CSD -->
    <div class="cultural-header">
      <div class="header-badges">
        <span class="badge-flag">📢 Evento Institucional CSD</span>
        <span class="badge-accent">Semana Cultural 2026</span>
        <span class="badge-dates">📅 28 de Octubre al 02 de Noviembre</span>
      </div>

      <div class="header-content">
        <img src="/assets/logo.png" alt="Escudo Colegio CSD" class="header-logo">
        <div class="header-titles">
          <h1>🌍 ¡Bienvenidos al Mundial de la Alegría!</h1>
          <p class="header-subtitle">"Mundial: Un recorrido por países" · Pasaporte & Folleto Interactivo</p>
        </div>
      </div>
      <div class="header-motto">Colegio CSD · Estudio · Amor · Paz · Sede La Cumbre</div>
    </div>

    <!-- INTRODUCCIÓN PEDAGÓGICA -->
    <div class="cultural-body">
      <div class="intro-box">
        <p>
          Estimada comunidad educativa y queridas familias: nuestra institución abre sus fronteras para vivir una semana llena de color, ciencia, deporte y hermandad. Cada grado escolar representará a un país con trajes típicos, historia, gastronomía, expresiones artísticas y competencias deportivas.
        </p>
        <p>
          A continuación, presentamos el <strong>Folleto y Pasaporte Digital Interactivo</strong> con la programación día a día y los horarios oficiales para Primaria y Bachillerato.
        </p>
      </div>

      <!-- VISOR DEL PLEGABLE INTERACTIVO (DÍA A DÍA) -->
      <div class="interactive-stage">
        <div class="stage-topbar">
          <div class="stage-tag">📲 Pasaporte Interactivo Digital</div>
          <span class="stage-hint">Toca cada día para explorar la programación oficial</span>
        </div>

        <!-- Pestañas de Días -->
        <div class="day-tabs-slider" role="tablist">
          <button class="day-tab active" onclick="selectDay(1)" id="tab-d1" role="tab" aria-selected="true">
            <span class="tab-emoji">🌟</span>
            <span class="tab-day">Lun 28 Oct</span>
            <span class="tab-title">Inauguración</span>
          </button>
          <button class="day-tab" onclick="selectDay(2)" id="tab-d2" role="tab" aria-selected="false">
            <span class="tab-emoji">🎨</span>
            <span class="tab-day">Mar 29 Oct</span>
            <span class="tab-title">Cultura & Danza</span>
          </button>
          <button class="day-tab" onclick="selectDay(3)" id="tab-d3" role="tab" aria-selected="false">
            <span class="tab-emoji">⚽</span>
            <span class="tab-day">Mié 30 Oct</span>
            <span class="tab-title">Mundialito</span>
          </button>
          <button class="day-tab" onclick="selectDay(4)" id="tab-d4" role="tab" aria-selected="false">
            <span class="tab-emoji">🤝</span>
            <span class="tab-day">Jue 31 Oct</span>
            <span class="tab-title">Acción Social</span>
          </button>
          <button class="day-tab" onclick="selectDay(5)" id="tab-d5" role="tab" aria-selected="false">
            <span class="tab-emoji">🔬</span>
            <span class="tab-day">Vie 02 (Día)</span>
            <span class="tab-title">Feria Ciencia & Arte</span>
          </button>
          <button class="day-tab" onclick="selectDay(6)" id="tab-d6" role="tab" aria-selected="false">
            <span class="tab-emoji">🏮</span>
            <span class="tab-day">Vie 02 (Noche)</span>
            <span class="tab-title">Noche de Faroles</span>
          </button>
        </div>

        <!-- Paneles de Contenido de Cada Día -->
        <div class="day-panels-container">

          <!-- Día 1 -->
          <div class="day-panel active" id="panel-d1">
            <div class="panel-header">
              <div class="panel-pill">Día 1 · Lunes 28 de Octubre</div>
              <h3>🌟 Gran Apertura: Desfile de Países y Antorcha Cultural</h3>
            </div>
            <p class="panel-desc">
              Apertura solemne de la Semana Cultural 2026. Desfile inaugural con las delegaciones de cada país representadas por nuestros estudiantes, encendido de la antorcha olímpica y presentación de las muestras folclóricas de apertura.
            </p>
            <div class="panel-details-grid">
              <div class="detail-box">
                <strong>🎒 Primaria:</strong> 7:00 AM – 11:30 AM (Desfile infantil y muestras de países de América y Europa).
              </div>
              <div class="detail-box">
                <strong>🎓 Bachillerato:</strong> 1:00 PM – 6:00 PM (Inauguración mayor, protocolos y gala artística).
              </div>
            </div>
            <div class="stamp-badge">
              <span>🛂 SELLO OFICIAL DÍA 1: DESFILE INAUGURAL CSD</span>
            </div>
          </div>

          <!-- Día 2 -->
          <div class="day-panel" id="panel-d2" style="display:none;">
            <div class="panel-header">
              <div class="panel-pill">Día 2 · Martes 29 de Octubre</div>
              <h3>🎨 Muestras Culturales, Tradiciones y Expresión Artística</h3>
            </div>
            <p class="panel-desc">
              Un viaje por las tradiciones, dialectos, música y trajes típicos del mundo. Los estudiantes exponen las características más fascinantes de su país asignado a través del teatro, poesía y coreografías grupales.
            </p>
            <div class="panel-details-grid">
              <div class="detail-box">
                <strong>🎒 Primaria:</strong> 7:00 AM – 11:30 AM (Rondas tradicionales, cuentos del mundo y música infantil).
              </div>
              <div class="detail-box">
                <strong>🎓 Bachillerato:</strong> 1:00 PM – 6:00 PM (Debates culturales, danzas internacionales y dramatizados).
              </div>
            </div>
            <div class="stamp-badge">
              <span>🛂 SELLO OFICIAL DÍA 2: EXPRESIÓN ARTÍSTICA & MUNDO</span>
            </div>
          </div>

          <!-- Día 3 -->
          <div class="day-panel" id="panel-d3" style="display:none;">
            <div class="panel-header">
              <div class="panel-pill">Día 3 · Miércoles 30 de Octubre</div>
              <h3>⚽ El Mundialito Deportivo CSD: Jornada Continua</h3>
            </div>
            <p class="panel-desc">
              ¡Día de fiesta deportiva y juego limpio! Torneo relámpago interclases de microfútbol, voleibol y circuitos de agilidad. Cada equipo defiende la camiseta de su nación en un ambiente de compañerismo y respeto mutuo.
            </p>
            <div class="panel-details-grid">
              <div class="detail-box highlight-box">
                <strong>🎒 Primaria & 🎓 Bachillerato (Jornada Continua):</strong>
                <div style="font-size:1.15rem; font-weight:800; color:#B91C1C; margin-top:4px;">7:00 AM – 5:00 PM</div>
                <span>¡Ven con ropa deportiva cómoda, hidratación y la mejor energía para alentar a tu equipo!</span>
              </div>
            </div>
            <div class="stamp-badge">
              <span>🛂 SELLO OFICIAL DÍA 3: JUEGO LIMPIO & DEPORTE CSD</span>
            </div>
          </div>

          <!-- Día 4 -->
          <div class="day-panel" id="panel-d4" style="display:none;">
            <div class="panel-header">
              <div class="panel-pill">Día 4 · Jueves 31 de Octubre</div>
              <h3>🤝 Acción Social, Jornada Fraterna y Valores</h3>
            </div>
            <p class="panel-desc">
              Viviendo el pilar de <strong>Estudio, Amor y Paz</strong>. Espacios de reflexión, solidaridad comunitaria, intercambio de mensajes de gratitud y actividades lúdicas formativas que unen los lazos de amistad entre compañeros y profesores.
            </p>
            <div class="panel-details-grid">
              <div class="detail-box">
                <strong>🎒 Primaria & 🎓 Bachillerato:</strong>
                <div style="font-size:1.1rem; font-weight:800; color:#047857; margin-top:4px;">7:00 AM – 11:00 AM</div>
                <span>Jornada fraterna unificada en la sede institucional.</span>
              </div>
            </div>
            <div class="stamp-badge">
              <span>🛂 SELLO OFICIAL DÍA 4: SOLIDARIDAD & VALORES CSD</span>
            </div>
          </div>

          <!-- Día 5 -->
          <div class="day-panel" id="panel-d5" style="display:none;">
            <div class="panel-header">
              <div class="panel-pill">Día 5 (Mañana) · Viernes 02 de Noviembre</div>
              <h3>🔬 Gran Feria de la Ciencia, Arte & Muestra Gastronómica</h3>
            </div>
            <p class="panel-desc">
              Stands de los países en el patio del colegio. Los estudiantes exponen experimentos científicos, descubrimientos tecnológicos, platos típicos y muestras artísticas representativas para el disfrute de la comunidad.
            </p>
            <div class="panel-details-grid">
              <div class="detail-box">
                <strong>🎒 Primaria & 🎓 Bachillerato:</strong>
                <div style="font-size:1.1rem; font-weight:800; color:#6B21A8; margin-top:4px;">7:00 AM – 11:30 AM</div>
                <span>Stands gastronómicos, feria experimental y premiación académica.</span>
              </div>
            </div>
            <div class="stamp-badge">
              <span>🛂 SELLO OFICIAL DÍA 5: CIENCIA, ARTE & GASTRONOMÍA</span>
            </div>
          </div>

          <!-- Día 6 -->
          <div class="day-panel" id="panel-d6" style="display:none;">
            <div class="panel-header">
              <div class="panel-pill">Día 5 (Noche) · Viernes 02 de Noviembre</div>
              <h3>🏮 Gran Noche de Faroles: Desfile Iluminado Familiar</h3>
            </div>
            <p class="panel-desc">
              El cierre dorado de nuestra Semana Cultural. Padres de familia, estudiantes y profesores iluminan el Barrio La Cumbre en un majestuoso desfile de faroles artesanales construidos en familia, celebrando la paz, la luz y la esperanza.
            </p>
            <div class="panel-details-grid">
              <div class="detail-box highlight-gold">
                <strong>👨‍👩‍👧‍👦 Toda la Comunidad CSD & Familias:</strong>
                <div style="font-size:1.25rem; font-weight:800; color:#78350F; margin-top:4px;">6:00 PM – 8:30 PM</div>
                <span>Punto de encuentro: Colegio CSD. ¡Trae tu farol artesanal para iluminar juntos nuestro barrio!</span>
              </div>
            </div>
            <div class="stamp-badge">
              <span>🛂 SELLO DE HONOR: GRAN CIERRE NOCHE DE FAROLES 2026</span>
            </div>
          </div>

        </div>
      </div>

      <!-- RESUMEN VISUAL DE HORARIOS PARA PADRES -->
      <div class="schedule-summary-box">
        <div class="schedule-header">
          <span style="font-size:1.8rem;">⏰</span>
          <div>
            <h3>Horarios de Asistencia por Jornadas</h3>
            <p>Punto de encuentro y retorno para todos los días: <strong>Colegio CSD (Sede La Cumbre)</strong></p>
          </div>
        </div>

        <div class="schedule-grid">
          <div class="schedule-card">
            <span class="sched-pill yellow">Lun 28 & Mar 29</span>
            <div class="sched-item"><strong>🎒 Primaria:</strong> 7:00 AM – 11:30 AM</div>
            <div class="sched-item"><strong>🎓 Bachillerato:</strong> 1:00 PM – 6:00 PM</div>
          </div>

          <div class="schedule-card">
            <span class="sched-pill red">Mié 30 Oct · Mundialito</span>
            <div class="sched-item"><strong>🎒 Primaria & 🎓 Bachillerato:</strong></div>
            <div class="sched-time-big">7:00 AM – 5:00 PM</div>
            <small>Jornada Deportiva Continua</small>
          </div>

          <div class="schedule-card">
            <span class="sched-pill green">Jue 31 Oct · Valores</span>
            <div class="sched-item"><strong>🎒 Primaria & 🎓 Bachillerato:</strong></div>
            <div class="sched-time-big">7:00 AM – 11:00 AM</div>
            <small>Jornada Fraterna y Acción Social</small>
          </div>

          <div class="schedule-card">
            <span class="sched-pill purple">Vie 02 Nov (Mañana)</span>
            <div class="sched-item"><strong>🎒 Primaria & 🎓 Bachillerato:</strong></div>
            <div class="sched-time-big">7:00 AM – 11:30 AM</div>
            <small>Feria de Ciencia & Gastronomía</small>
          </div>

          <div class="schedule-card full-span gold">
            <span class="sched-pill gold-pill">🏮 Vie 02 Nov (Noche de Faroles)</span>
            <div class="sched-item"><strong>👨‍👩‍👧‍👦 Familias, Estudiantes y Egresados:</strong></div>
            <div class="sched-time-big" style="color:#78350F;">6:00 PM – 8:30 PM</div>
            <small>Gran Desfile de Faroles por las Calles de La Cumbre</small>
          </div>
        </div>
      </div>

      <!-- BOTONES DE CONTACTO DIRECTO Y DIFUSIÓN -->
      <div class="action-buttons-grid">
        <a href="https://wa.me/573152904403?text=Hola%20Colegio%20CSD,%20quisiera%20m%C3%A1s%20informaci%C3%B3n%20sobre%20la%20Semana%20Cultural%202026" 
           target="_blank" rel="noopener" class="action-btn btn-wa">
          <div class="action-icon">💬</div>
          <div>
            <span class="action-sub">Atención Secretaría</span>
            <strong class="action-main">WhatsApp 315 290 4403</strong>
          </div>
        </a>

        <a href="https://www.google.com/maps/dir//CSD,+Cra.+6+Este+%23+27a-03,+Floridablanca,+Santander" 
           target="_blank" rel="noopener" class="action-btn btn-map">
          <div class="action-icon">📍</div>
          <div>
            <span class="action-sub">Sede La Cumbre</span>
            <strong class="action-main">Abrir en Google Maps</strong>
          </div>
        </a>

        <button type="button" onclick="shareCulturalNews()" class="action-btn btn-share">
          <div class="action-icon">📲</div>
          <div>
            <span class="action-sub">Difusión Escolar</span>
            <strong class="action-main">Compartir Noticia</strong>
          </div>
        </button>
      </div>

    </div>

    <!-- PIE DEL COMUNICADO -->
    <div class="cultural-footer">
      <p>© 2026 Colegio CSD · Semana Cultural "Mundial: Un recorrido por países" · Estudio, Amor y Paz</p>
    </div>

  </div>
</div>

<!-- ========================================================
     ESTILOS ESPECÍFICOS DEL PLEGABLE INTERACTIVO CSD
     ======================================================== -->
<style>
.cultural-container {
  max-width: 900px;
  margin: 0 auto;
  font-family: var(--font-body, 'Inter', sans-serif);
}

/* Banner del Reproductor */
.audio-player-banner {
  background: linear-gradient(135deg, #002244, #003865);
  border: 2.5px solid #FFC91B;
  border-radius: 16px;
  padding: 14px 20px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
  box-shadow: 0 8px 24px rgba(0, 56, 101, 0.25);
  color: white;
}
.player-left {
  display: flex;
  align-items: center;
  gap: 14px;
}
.player-label {
  display: block;
  font-size: 0.72rem;
  letter-spacing: 1px;
  color: #FFC91B;
  font-weight: 800;
}
.player-info strong {
  font-size: 1.05rem;
  font-family: var(--font-title, 'Plus Jakarta Sans', sans-serif);
  color: white;
}
.player-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}
.btn-play-pause {
  background: #FFC91B;
  color: #002244;
  border: none;
  border-radius: 999px;
  padding: 8px 18px;
  font-size: 0.88rem;
  font-weight: 800;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 12px rgba(255, 201, 27, 0.4);
  transition: transform 0.15s, background 0.15s;
}
.btn-play-pause:hover {
  background: #FFE066;
  transform: scale(1.03);
}
.btn-switch-song {
  background: rgba(255, 255, 255, 0.12);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  padding: 8px 14px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-switch-song:hover {
  background: rgba(255, 255, 255, 0.22);
}

/* Ecualizador animado */
.sound-wave {
  display: flex;
  align-items: flex-end;
  gap: 3px;
  height: 24px;
  width: 22px;
}
.sound-wave span {
  width: 3px;
  height: 6px;
  background: #FFC91B;
  border-radius: 3px;
  transition: height 0.2s ease;
}
.sound-wave.playing span:nth-child(1) { animation: wave 0.8s infinite ease-in-out alternate; }
.sound-wave.playing span:nth-child(2) { animation: wave 0.6s infinite ease-in-out alternate 0.15s; }
.sound-wave.playing span:nth-child(3) { animation: wave 0.9s infinite ease-in-out alternate 0.3s; }
.sound-wave.playing span:nth-child(4) { animation: wave 0.7s infinite ease-in-out alternate 0.1s; }
.sound-wave.playing span:nth-child(5) { animation: wave 0.85s infinite ease-in-out alternate 0.25s; }
@keyframes wave {
  0% { height: 4px; }
  100% { height: 22px; }
}

/* Tarjeta Principal */
.cultural-card {
  background: #FFFFFF;
  border-radius: 24px;
  border: 3px solid #002244;
  overflow: hidden;
  box-shadow: 0 16px 40px rgba(0, 34, 68, 0.12);
}
.cultural-header {
  background: linear-gradient(135deg, #002244 0%, #003865 100%);
  color: white;
  padding: 32px 28px 24px;
  border-bottom: 4px solid #FFC91B;
  position: relative;
}
.header-badges {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
}
.badge-flag {
  background: #FFC91B;
  color: #002244;
  font-weight: 800;
  font-size: 0.76rem;
  padding: 4px 12px;
  border-radius: 999px;
  text-transform: uppercase;
}
.badge-accent {
  background: #E11D48;
  color: white;
  font-weight: 800;
  font-size: 0.76rem;
  padding: 4px 12px;
  border-radius: 999px;
  text-transform: uppercase;
}
.badge-dates {
  margin-left: auto;
  font-size: 0.82rem;
  color: #E2E8F0;
  font-weight: 600;
}
.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}
.header-logo {
  width: 80px;
  height: 80px;
  object-fit: contain;
  background: white;
  padding: 6px;
  border-radius: 18px;
  border: 2.5px solid #FFC91B;
  box-shadow: 0 6px 16px rgba(0,0,0,0.25);
  flex-shrink: 0;
}
.header-titles h1 {
  font-family: var(--font-title, 'Plus Jakarta Sans', sans-serif);
  font-size: clamp(1.4rem, 3.2vw, 2.1rem);
  font-weight: 800;
  color: #FFFFFF;
  margin: 0 0 6px;
  line-height: 1.25;
}
.header-subtitle {
  color: #FFC91B;
  font-size: clamp(0.9rem, 2vw, 1.05rem);
  margin: 0;
  font-weight: 600;
}
.header-motto {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  font-size: 0.78rem;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #CBD5E1;
  text-align: center;
}

/* Cuerpo */
.cultural-body {
  padding: 28px 24px;
}
.intro-box {
  background: #F8FAFC;
  border-left: 4px solid #003865;
  border-radius: 0 14px 14px 0;
  padding: 18px 22px;
  margin-bottom: 28px;
  font-size: 0.96rem;
  line-height: 1.65;
  color: #334155;
}
.intro-box p { margin: 0 0 8px; }
.intro-box p:last-child { margin-bottom: 0; }

/* Escenario Interactivo del Folleto */
.interactive-stage {
  background: #002244;
  border: 3px solid #0F172A;
  border-radius: 20px;
  padding: 22px;
  color: white;
  margin-bottom: 28px;
  box-shadow: 0 8px 24px rgba(0, 34, 68, 0.2);
}
.stage-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}
.stage-tag {
  background: #FFC91B;
  color: #002244;
  font-weight: 800;
  font-size: 0.76rem;
  padding: 4px 12px;
  border-radius: 6px;
  text-transform: uppercase;
}
.stage-hint {
  font-size: 0.82rem;
  color: #94A3B8;
}

/* Pestañas de Días */
.day-tabs-slider {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(115px, 1fr));
  gap: 8px;
  margin-bottom: 20px;
}
.day-tab {
  background: rgba(255, 255, 255, 0.08);
  border: 1.5px solid rgba(255, 255, 255, 0.16);
  border-radius: 12px;
  padding: 10px 8px;
  color: white;
  cursor: pointer;
  text-align: center;
  transition: all 0.15s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.day-tab:hover {
  background: rgba(255, 255, 255, 0.18);
  border-color: #FFC91B;
}
.day-tab.active {
  background: #FFC91B;
  color: #002244;
  border-color: #FFC91B;
  font-weight: 800;
  box-shadow: 0 4px 14px rgba(255, 201, 27, 0.4);
  transform: translateY(-2px);
}
.tab-emoji { font-size: 1.3rem; margin-bottom: 2px; }
.tab-day { font-size: 0.74rem; font-weight: 700; opacity: 0.9; }
.tab-title { font-size: 0.72rem; margin-top: 2px; }

/* Panel de cada día */
.day-panel {
  background: #FFFFFF;
  color: #0F172A;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #E2E8F0;
  animation: fadeIn 0.25s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.panel-header {
  margin-bottom: 14px;
}
.panel-pill {
  display: inline-block;
  background: #EEF2F6;
  color: #003865;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 6px;
  margin-bottom: 6px;
}
.panel-header h3 {
  font-family: var(--font-title, 'Plus Jakarta Sans', sans-serif);
  font-size: 1.25rem;
  color: #002244;
  margin: 0;
  font-weight: 800;
}
.panel-desc {
  font-size: 0.94rem;
  color: #475569;
  line-height: 1.6;
  margin: 0 0 16px;
}
.panel-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}
.detail-box {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 0.88rem;
  color: #1E293B;
  line-height: 1.5;
}
.detail-box.highlight-box {
  background: #FEF2F2;
  border-color: #FCA5A5;
  grid-column: 1 / -1;
}
.detail-box.highlight-gold {
  background: #FFFBEB;
  border-color: #FDE68A;
  grid-column: 1 / -1;
}
.stamp-badge {
  background: #F1F5F9;
  border: 1.5px dashed #64748B;
  border-radius: 8px;
  padding: 8px 14px;
  text-align: center;
  font-size: 0.76rem;
  font-weight: 800;
  color: #475569;
  letter-spacing: 0.8px;
}

/* Cuadro Resumen Horarios */
.schedule-summary-box {
  background: #FFFBEB;
  border: 2px solid #F59E0B;
  border-radius: 18px;
  padding: 22px;
  margin-bottom: 28px;
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.12);
}
.schedule-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
}
.schedule-header h3 {
  font-family: var(--font-title, 'Plus Jakarta Sans', sans-serif);
  font-size: 1.15rem;
  font-weight: 800;
  color: #78350F;
  margin: 0;
  text-transform: uppercase;
}
.schedule-header p {
  font-size: 0.84rem;
  color: #92400E;
  margin: 2px 0 0;
}
.schedule-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}
.schedule-card {
  background: #FFFFFF;
  border: 1.5px solid #FDE68A;
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.03);
}
.schedule-card.full-span {
  grid-column: 1 / -1;
  background: #FEF3C7;
  border-color: #F59E0B;
}
.sched-pill {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 999px;
  margin-bottom: 8px;
  text-transform: uppercase;
}
.sched-pill.yellow { background: #FEF3C7; color: #92400E; }
.sched-pill.red { background: #FEE2E2; color: #991B1B; }
.sched-pill.green { background: #DCFCE7; color: #166534; }
.sched-pill.purple { background: #F3E8FF; color: #6B21A8; }
.sched-pill.gold-pill { background: #D97706; color: #FFFFFF; }
.sched-item {
  font-size: 0.84rem;
  color: #1E293B;
  margin-bottom: 4px;
}
.sched-time-big {
  font-size: 1.1rem;
  font-weight: 800;
  color: #0F172A;
  margin: 4px 0;
}
.schedule-card small {
  display: block;
  font-size: 0.74rem;
  color: #64748B;
  font-weight: 600;
}

/* Botones de Acción */
.action-buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}
.action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border-radius: 14px;
  text-decoration: none;
  border: 2px solid #002244;
  color: #002244;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 3px 3px 0px #002244;
}
.action-btn:hover {
  transform: translate(-2px, -2px);
  box-shadow: 5px 5px 0px #002244;
}
.btn-wa { background: #F0FDF4; }
.btn-map { background: #F0F9FF; }
.btn-share { background: #FEFCE8; border-color: #002244; }
.action-icon {
  font-size: 1.6rem;
  line-height: 1;
}
.action-sub {
  display: block;
  font-size: 0.72rem;
  text-transform: uppercase;
  font-weight: 800;
  color: #64748B;
}
.action-main {
  font-size: 0.88rem;
  font-weight: 800;
  color: #002244;
}

/* Pie */
.cultural-footer {
  background: #F8FAFC;
  border-top: 2px solid #E2E8F0;
  padding: 16px 20px;
  text-align: center;
  font-size: 0.78rem;
  color: #64748B;
}

@media (max-width: 640px) {
  .cultural-header { padding: 22px 18px; }
  .header-content { flex-direction: column; text-align: center; gap: 12px; }
  .header-badges { justify-content: center; }
  .badge-dates { margin-left: 0; width: 100%; text-align: center; }
  .day-tabs-slider { grid-template-columns: repeat(3, 1fr); }
  .audio-player-banner { flex-direction: column; align-items: stretch; text-align: center; }
  .player-left { justify-content: center; }
  .player-controls { justify-content: center; }
}
</style>

<!-- ========================================================
     SCRIPT INTERACTIVO (DÍAS + REPRODUCTOR DE MÚSICA)
     ======================================================== -->
<script>
(function() {
  // Lista de canciones
  var songs = [
    { title: "El Orgullo del CSD", src: "/assets/audio/El_Orgullo_del_CSD.mp3" },
    { title: "Semillero Mi Vida Entera", src: "/assets/audio/Semillero_mi_vida_entera.mp3" }
  ];
  var currentSongIndex = 0;
  var audio = document.getElementById("cultural-audio");
  var wave = document.getElementById("sound-wave");
  var playIcon = document.getElementById("play-icon");
  var playText = document.getElementById("play-text");
  var songTitle = document.getElementById("song-title");

  window.toggleAudio = function() {
    if (!audio) return;
    if (audio.paused) {
      audio.play().then(function() {
        wave.classList.add("playing");
        playIcon.textContent = "⏸️";
        playText.textContent = "Pausar Canción";
      }).catch(function(err) {
        console.log("Audio play blocked:", err);
      });
    } else {
      audio.pause();
      wave.classList.remove("playing");
      playIcon.textContent = "▶️";
      playText.textContent = "Escuchar Canción";
    }
  };

  window.switchSong = function() {
    if (!audio) return;
    currentSongIndex = (currentSongIndex + 1) % songs.length;
    var nextSong = songs[currentSongIndex];
    audio.src = nextSong.src;
    songTitle.textContent = nextSong.title;
    audio.play().then(function() {
      wave.classList.add("playing");
      playIcon.textContent = "⏸️";
      playText.textContent = "Pausar Canción";
    }).catch(function() {});
  };

  window.selectDay = function(dayNumber) {
    for (var i = 1; i <= 6; i++) {
      var tab = document.getElementById("tab-d" + i);
      var panel = document.getElementById("panel-d" + i);
      if (tab) {
        tab.classList.toggle("active", i === dayNumber);
        tab.setAttribute("aria-selected", i === dayNumber ? "true" : "false");
      }
      if (panel) {
        panel.style.display = (i === dayNumber) ? "block" : "none";
        panel.classList.toggle("active", i === dayNumber);
      }
    }
  };

  window.shareCulturalNews = function() {
    var shareData = {
      title: "Semana Cultural 2026 Colegio CSD - Mundial de la Alegría",
      text: "¡Consulta el pasaporte, la programación y los horarios oficiales de la Semana Cultural 2026 en el Colegio CSD!",
      url: window.location.href
    };
    if (navigator.share) {
      navigator.share(shareData).catch(function() {});
    } else {
      var waUrl = "https://api.whatsapp.com/send?text=" + encodeURIComponent(shareData.title + "\n" + shareData.text + "\n" + shareData.url);
      window.open(waUrl, "_blank");
    }
  };
})();
</script>
