import streamlit as st
from streamlit_calendar import calendar
import datetime

st.set_page_config(page_title="Lini Masa HIMASTA", layout="wide")

st.markdown("""
    <style>
    /* Mengubah font dan background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Mempercantik Card Detail */
    .proker-card {
        background-color: #1e293b;
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 10px;
    }
    
    /* Mengatur header kalender */
    .fc-header-toolbar {
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if "proker_data" not in st.session_state:
    st.session_state.proker_data = [
        # PSDM
        {"title": "LDKM 25: Pembentukan Panitia", "start": "2026-07-25", "end": "2026-07-25", "color": "#f87171", "dept": "PSDM", "desc": "Pembentukan Panitia untuk LDKM 25."},
        {"title": "LDKM 25: Rapat Perdana", "start": "2026-07-01", "end": "2026-07-1", "color": "#f87171", "dept": "PSDM", "desc": "Memberi tahu konsep Kepanitian"},
        {"title": "LDKM 25: Rapat Akbar", "start": "2026-07-05", "end": "2026-07-26", "color": "#f87171", "dept": "PSDM", "desc": "Progres yang sudah jelas atau setidaknya terdapat progress."},
        {"title": "LDKM 25: Pematangan Rencana", "start": "2026-07-05", "end": "2026-07-26", "color": "#f87171", "dept": "PSDM", "desc": "Pematangan persiapan teknis LDKM 25."},
        {"title": "LDKM 25: Hari H", "start": "2026-07-27", "end": "2026-07-28", "color": "#ef4444", "dept": "PSDM", "desc": "Pelaksanaan Latihan Dasar Kepemimpinan Mahasiswa untuk angkatan 25."},
        
        {"title": "LDKM 26: Pembentukan Panitia", "start": "2026-10-05", "end": "2026-10-12", "color": "#fbbf24", "dept": "PSDM", "desc": "Pembentukan kepanitiaan setelah aktif kuliah kembali."},
        {"title": "LDKM 26: Rapat Perdana", "start": "2026-10-13", "end": "2026-11-05", "color": "#f87171", "dept": "PSDM", "desc": "Memberi tahu Konsep Kepanitian"},
        {"title": "LDKM 26: Rapat Akbar", "start": "2026-10-23", "end": "2026-11-30", "color": "#f87171", "dept": "PSDM", "desc": "Progress yang sudah jelas atau setidaknya terdapat progress."},
        {"title": "LDKM 26: Pematangan Rencana", "start": "2026-11-01", "end": "2026-11-05", "color": "#f87171", "dept": "PSDM", "desc": "Rapat koordinasi berkala dan pematangan konsep Makrab 3 angkatan."},
        {"title": "LDKM 26 & Makrab: Hari H", "start": "2026-11-06", "end": "2026-11-08", "color": "#ef4444", "dept": "PSDM", "desc": "Pelaksanaan LDKM 26 sekaligus Malam Keakraban gabungan 3 angkatan."},{"title": "HIMA Champ", "start": "2026-11-05", "end": "2026-11-07", "color": "#ef4444", "dept": "PSDM", "desc": "Kompetisi internal sains data & sport."},
        {"title": "Ruang Baca Rutin (Okt)", "start": "2026-10-15", "color": "#ef4444", "dept": "PSDM", "desc": "Sesi sharing jurnal/artikel bulan Oktober."},
        {"title": "Ruang Baca Rutin (Nov)", "start": "2026-11-12", "color": "#ef4444", "dept": "PSDM", "desc": "Sesi sharing jurnal/artikel bulan November."},
        {"title": "Ruang Baca Rutin (Des)", "start": "2026-12-10", "color": "#ef4444", "dept": "PSDM", "desc": "Sesi sharing jurnal/artikel bulan Desember."},
        {"title": "Ruang Baca Rutin (Jan)", "start": "2027-01-14", "color": "#ef4444", "dept": "PSDM", "desc": "Sesi sharing jurnal/artikel bulan Januari."},
        {"title": "Ruang Baca Rutin (Feb)", "start": "2027-02-11", "color": "#ef4444", "dept": "PSDM", "desc": "Sesi sharing jurnal/artikel bulan Februari."},
        {"title": "Ruang Baca Rutin (Mar)", "start": "2027-03-11", "color": "#ef4444", "dept": "PSDM", "desc": "Sesi sharing jurnal/artikel bulan Maret."},
    ]

with st.sidebar:
    st.title("Control Panel")
    filter_dept = st.multiselect(
        "Pilih Departemen:",
        ["Akademik", "PSDM", "PR", "RION", "KOMINFO"],
        default=["Akademik", "PSDM", "PR", "RION", "KOMINFO"]
    )
    
    st.divider()
    st.info("💡 Klik pada kalender untuk melihat detail proker di kolom kanan.")

st.title("📅 HIMASTA Annual Roadmap 2026/2027")
st.write(f"Selamat Datang, Pengurus! Hari ini: **{datetime.date.today().strftime('%d %B %Y')}**")

# Filter data berdasarkan departemen yang dipilih di sidebar
filtered_events = [e for e in st.session_state.proker_data if e['dept'] in filter_dept]

col_cal, col_detail = st.columns([2, 1])

with col_cal:
    # --- KONFIGURASI KALENDER ---
    calendar_options = {
        "initialView": "dayGridMonth",
        "timeZone": "Asia/Jakarta",  # Zona waktu WIB
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,listMonth",
        },
        "editable": True,
        "selectable": True,
    }
    
    # Render Kalender
    state = calendar(
        events=filtered_events,
        options=calendar_options,
        key="calendar",
    )

with col_detail:
    st.subheader("🔍 Detail Proker")
    
    # Logika jika ada event yang diklik
    if state.get("eventClick"):
        clicked = state["eventClick"]["event"]
        st.markdown(f"""
            <div class="proker-card">
                <h3 style='margin:0; color:#3b82f6;'>{clicked['title']}</h3>
                <p><b>📅 Tanggal:</b> {clicked['start']}</p>
                <p><b>🏢 Dept:</b> {clicked.get('extendedProps', {}).get('dept', '-')}</p>
                <hr>
                <p><b>Keterangan:</b><br>{clicked.get('extendedProps', {}).get('desc', 'Tidak ada deskripsi')}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.write("Silahkan klik salah satu event di kalender untuk melihat detailnya.")
        
        # Tampilkan list proker terdekat
        st.write("---")
        st.write("**📌 Proker Mendatang:**")
        for p in filtered_events[:3]: # Ambil 3 teratas
            st.caption(f"• {p['title']} ({p['start']})")