import streamlit as st
from streamlit_calendar import calendar
import datetime

# --- CONFIG DASHBOARD ---
st.set_page_config(page_title="Lini Masa HIMASTA", layout="wide", page_icon="📅")

# --- CUSTOM ULTRA MODERN CSS (Glassmorphism & Cyberpunk Accent) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Mengubah Font Global */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Mempercantik Card Detail Proker (Efek Glassmorphism) */
    .proker-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    .proker-card:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(59, 130, 246, 0.5);
        box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.15);
    }
    
    /* Tag Badge untuk Departemen */
    .badge-dept {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
    }
    
    /* Customisasi Tampilan Kalender */
    .fc {
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 15px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    .fc-header-toolbar {
        margin-bottom: 20px !important;
    }
    .fc-button-primary {
        background-color: #3b82f6 !important;
        border-color: #3b82f6 !important;
    }
    .fc-button-primary:hover {
        background-color: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
    }
    .fc-button-active {
        background-color: #1e40af !important;
        border-color: #1e40af !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PROKER ---
if "proker_data" not in st.session_state:
    st.session_state.proker_data = [
        # PSDM - LDKM 25
        {"title": "LDKM 25: Rapat Perdana", "start": "2026-07-01", "end": "2026-07-02", "color": "#3b82f6", "dept": "PSDM", "desc": "Penyampaian arahan dan penyamaan konsep dasar Kepanitiaan."},
        {"title": "LDKM 25: Rapat Akbar", "start": "2026-07-05", "end": "2026-07-06", "color": "#60a5fa", "dept": "PSDM", "desc": "Evaluasi dan peninjauan progres berkala dari setiap divisi panitia."},
        {"title": "LDKM 25: Pematangan Rencana", "start": "2026-07-10", "end": "2026-07-24", "color": "#f59e0b", "dept": "PSDM", "desc": "Pematangan persiapan teknis, simulasi lapangan, dan penyelesaian administrasi LDKM 25."},
        {"title": "LDKM 25: Pembentukan Panitia", "start": "2026-07-25", "end": "2026-07-26", "color": "#10b981", "dept": "PSDM", "desc": "Finalisasi struktural komparasi dan penetapan panitia inti."},
        {"title": "LDKM 25: Hari H", "start": "2026-07-27", "end": "2026-07-29", "color": "#ef4444", "dept": "PSDM", "desc": "Pelaksanaan puncak Latihan Dasar Kepemimpinan Mahasiswa untuk angkatan 25."},
        
        # PSDM - LDKM 26
        {"title": "LDKM 26: Pembentukan Panitia", "start": "2026-10-05", "end": "2026-10-13", "color": "#10b981", "dept": "PSDM", "desc": "Pembentukan kepanitiaan setelah aktif kuliah kembali."},
        {"title": "LDKM 26: Rapat Perdana", "start": "2026-10-13", "end": "2026-10-15", "color": "#3b82f6", "dept": "PSDM", "desc": "Koordinasi awal dan pemaparan grand design kepanitiaan."},
        {"title": "LDKM 26: Rapat Akbar", "start": "2026-10-23", "end": "2026-11-01", "color": "#60a5fa", "dept": "PSDM", "desc": "Sinkronisasi antar-divisi untuk memastikan kesiapan program berjalan terstruktur."},
        {"title": "LDKM 26: Pematangan Rencana", "start": "2026-11-01", "end": "2026-11-06", "color": "#f59e0b", "dept": "PSDM", "desc": "Rapat koordinasi final dan pematangan konsep Malam Keakraban 3 angkatan."},
        {"title": "LDKM 26 & Makrab: Hari H", "start": "2026-11-06", "end": "2026-11-09", "color": "#ef4444", "dept": "PSDM", "desc": "Pelaksanaan LDKM 26 sekaligus Malam Keakraban gabungan 3 angkatan."},
        
        # PSDM - Lainnya
        {"title": "HIMA Champ", "start": "2026-11-05", "end": "2026-11-08", "color": "#a855f7", "dept": "PSDM", "desc": "Kompetisi internal sains data berfokus pada turnamen olahraga fisik (sport) antar-angkatan."},
        
        # PSDM - Ruang Baca Rutin (Bulanan)
        {"title": "Ruang Baca Rutin (Okt)", "start": "2026-10-15", "color": "#ec4899", "dept": "PSDM", "desc": "Sesi sharing internal mengenai bedah jurnal, artikel ilmiah, atau buku data science."},
        {"title": "Ruang Baca Rutin (Nov)", "start": "2026-11-12", "color": "#ec4899", "dept": "PSDM", "desc": "Sesi sharing internal mengenai bedah jurnal, artikel ilmiah, atau buku data science."},
        {"title": "Ruang Baca Rutin (Des)", "start": "2026-12-10", "color": "#ec4899", "dept": "PSDM", "desc": "Sesi sharing internal mengenai bedah jurnal, artikel ilmiah, atau buku data science."},
        {"title": "Ruang Baca Rutin (Jan)", "start": "2027-01-14", "color": "#ec4899", "dept": "PSDM", "desc": "Sesi sharing internal mengenai bedah jurnal, artikel ilmiah, atau buku data science."},
        {"title": "Ruang Baca Rutin (Feb)", "start": "2027-02-11", "color": "#ec4899", "dept": "PSDM", "desc": "Sesi sharing internal mengenai bedah jurnal, artikel ilmiah, atau buku data science."},
        {"title": "Ruang Baca Rutin (Mar)", "start": "2027-03-11", "color": "#ec4899", "dept": "PSDM", "desc": "Sesi sharing internal mengenai bedah jurnal, artikel ilmiah, atau buku data science."},
    ]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛠️ CONTROL PANEL")
    filter_dept = st.multiselect(
        "Saring Berdasarkan Departemen:",
        ["Akademik", "PSDM", "PR", "RION", "KOMINFO"],
        default=["Akademik", "PSDM", "PR", "RION", "KOMINFO"]
    )
    st.divider()
    st.markdown("### 💡 TIPS NAVIGASI")
    st.caption("Klik salah satu agenda berwarna pada kalender untuk membuka panel detail komprehensif di sisi kanan.")

# --- MAIN HEADER AREA ---
st.markdown("## ⚡ HIMASTA Data Dashboard & Integrated Roadmap")
st.markdown(f"🚀 *Sistem Pusat Informasi Terpadu Terkendali* | Hari ini: `{datetime.date.today().strftime('%A, %d %B %Y')}`")
st.markdown("---")

# Filter data berdasarkan departemen
filtered_events = [e for e in st.session_state.proker_data if e['dept'] in filter_dept]

# Grid Utama (Pembagian Kolom Kalender & Detail)
col_cal, col_detail = st.columns([22, 11])

with col_cal:
    st.markdown("#### 📅 Lini Masa Kegiatan Terjadwal")
    
    calendar_options = {
        "initialView": "dayGridMonth",
        "timeZone": "Asia/Jakarta",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,listMonth",
        },
        "editable": False,
        "selectable": True,
    }
    
    state = calendar(
        events=filtered_events,
        options=calendar_options,
        key="himasta_calendar",
    )

with col_detail:
    st.markdown("#### 🔍 Panel Detail & Informasi Proker")
    
    # Logika Interaksi Klik Agenda
    if state.get("eventClick"):
        clicked = state["eventClick"]["event"]
        # Mengambil properti tambahan jika ada
        extended = clicked.get('extendedProps', {})
        dept_name = extended.get('dept', '-') if extended else '-'
        desc_text = extended.get('desc', 'Tidak ada deskripsi.') if extended else 'Tidak ada deskripsi.'
        
        st.markdown(f"""
            <div class="proker-card">
                <span class="badge-dept">🏢 Dept: {dept_name}</span>
                <h2 style='margin:0 0 10px 0; color:#3b82f6; font-size:22px; font-weight:700;'>{clicked['title']}</h2>
                <p style='margin: 4px 0; font-size:14px; color:#94a3b8;'>📅 <b>Tanggal Mulai:</b> {clicked['start'][:10]}</p>
                {"<p style='margin: 4px 0; font-size:14px; color:#94a3b8;'>🏁 <b>Tanggal Selesai:</b> " + clicked['end'][:10] + "</p>" if clicked.get('end') else ""}
                <hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 16px 0;'>
                <p style='margin:0; font-size:15px; color:#e2e8f0; line-height:1.6;'><b>📋 Deskripsi Teknis:</b><br>{desc_text}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; padding: 30px; text-align: center; color: #64748b;'>
                <p style='font-size: 24px; margin-bottom: 8px;'>👆</p>
                <b>Belum Ada Agenda Dipilih</b><br>Silakan ketuk salah satu agenda di kalender untuk menampilkan detail instruksi operasional di sini.
            </div>
        """, unsafe_allow_html=True)
        
        # Penampilan List Proker Mendatang yang Lebih Cantik
        st.markdown("<br><h5>📌 Agenda Terdekat Pengurus:</h5>", unsafe_allow_html=True)
        if filtered_events:
            for p in filtered_events[:3]:
                st.markdown(f"""
                    <div style='background: rgba(59, 130, 246, 0.05); border-left: 4px solid #3b82f6; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;'>
                        <strong style='color:#e2e8f0; font-size:14px;'>{p['title']}</strong><br>
                        <span style='color:#64748b; font-size:12px;'>📅 Mulai: {p['start']}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Tidak ada agenda terdekat pada filter departemen yang dipilih.")