import streamlit as st
from streamlit_calendar import calendar
import datetime

# --- CONFIG DASHBOARD ---
st.set_page_config(page_title="Lini Masa HIMASTA", layout="wide", page_icon="📅")

# --- CSS RESPONSIF MOBILE-FRIENDLY (Android & Desktop) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Card Detail - Glassmorphism Responsif */
    .proker-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 12px;
    }
    
    /* Tag Badge */
    .badge-dept {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    /* Kustomisasi Kalender agar Fleksibel di HP */
    .fc {
        background: rgba(15, 23, 42, 0.4) !important;
        padding: 8px !important;
        border-radius: 12px;
        font-size: 13px !important; /* Font agak kecil di HP agar muat */
    }
    
    /* CSS Khusus Layar HP / Android (Media Queries) */
    @media (max-width: 768px) {
        .fc-header-toolbar {
            display: flex;
            flex-direction: column;
            gap: 8px;
            align-items: center;
        }
        .fc-toolbar-title {
            font-size: 16px !important;
        }
        .proker-card h2 {
            font-size: 18px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PROKER ---
if "proker_data" not in st.session_state:
    st.session_state.proker_data = [
        # LDKM 25
        {"title": "LDKM 25: Rapat Perdana", "start": "2026-07-01", "end": "2026-07-02", "color": "#3b82f6", "dept": "PSDM", "desc": "Penyampaian arahan dan penyamaan konsep dasar Kepanitiaan."},
        {"title": "LDKM 25: Rapat Akbar", "start": "2026-07-05", "end": "2026-07-06", "color": "#60a5fa", "dept": "PSDM", "desc": "Evaluasi dan peninjauan progres berkala dari setiap divisi panitia."},
        {"title": "LDKM 25: Pematangan Rencana", "start": "2026-07-10", "end": "2026-07-24", "color": "#f59e0b", "dept": "PSDM", "desc": "Pematangan persiapan teknis, simulasi lapangan, dan penyelesaian administrasi LDKM 25."},
        {"title": "LDKM 25: Pembentukan Panitia", "start": "2026-07-25", "end": "2026-07-26", "color": "#10b981", "dept": "PSDM", "desc": "Finalisasi struktural komparasi dan penetapan panitia inti."},
        {"title": "LDKM 25: Hari H", "start": "2026-07-27", "end": "2026-07-29", "color": "#ef4444", "dept": "PSDM", "desc": "Pelaksanaan puncak Latihan Dasar Kepemimpinan Mahasiswa untuk angkatan 25."},
        
        # LDKM 26
        {"title": "LDKM 26: Pembentukan Panitia", "start": "2026-10-05", "end": "2026-10-13", "color": "#10b981", "dept": "PSDM", "desc": "Pembentukan kepanitiaan setelah aktif kuliah kembali."},
        {"title": "LDKM 26: Rapat Perdana", "start": "2026-10-13", "end": "2026-10-15", "color": "#3b82f6", "dept": "PSDM", "desc": "Koordinasi awal dan pemaparan grand design kepanitiaan."},
        {"title": "LDKM 26: Rapat Akbar", "start": "2026-10-23", "end": "2026-11-01", "color": "#60a5fa", "dept": "PSDM", "desc": "Sinkronisasi antar-divisi untuk memastikan kesiapan program berjalan terstruktur."},
        {"title": "LDKM 26: Pematangan Rencana", "start": "2026-11-01", "end": "2026-11-06", "color": "#f59e0b", "dept": "PSDM", "desc": "Rapat koordinasi final dan pematangan konsep Malam Keakraban 3 angkatan."},
        {"title": "LDKM 26 & Makrab: Hari H", "start": "2026-11-06", "end": "2026-11-09", "color": "#ef4444", "dept": "PSDM", "desc": "Pelaksanaan LDKM 26 sekaligus Malam Keakraban gabungan 3 angkatan."},
        
        # Lainnya
        {"title": "HIMA Champ", "start": "2026-11-05", "end": "2026-11-08", "color": "#a855f7", "dept": "PSDM", "desc": "Kompetisi internal sains data berfokus pada turnamen olahraga fisik (sport) antar-angkatan."},
        {"title": "Ruang Baca Rutin (Okt)", "start": "2026-10-15", "color": "#ec4899", "dept": "PSDM", "desc": "Sesi sharing internal mengenai bedah jurnal, artikel ilmiah, atau buku data science."},
        {"title": "Ruang Baca Rutin (Nov)", "start": "2026-11-12", "color": "#ec4899", "dept": "PSDM", "desc": "Sesi sharing internal mengenai bedah jurnal, artikel ilmiah, atau buku data science."}
    ]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛠️ CONTROL PANEL")
    filter_dept = st.multiselect(
        "Saring Departemen:",
        ["Akademik", "PSDM", "PR", "RION", "KOMINFO"],
        default=["Akademik", "PSDM", "PR", "RION", "KOMINFO"]
    )

# --- MAIN HEADER ---
st.markdown("## ⚡ HIMASTA Integrated Roadmap")
st.markdown(f"🚀 *Hari ini:* `{datetime.date.today().strftime('%A, %d %B %Y')}`")
st.markdown("---")

filtered_events = [e for e in st.session_state.proker_data if e['dept'] in filter_dept]

# --- LOGIKA RESPONSIF LAYAR (PENTING UNTUK ANDROID) ---
# Menggunakan deteksi lebar layar bawaan Streamlit secara tidak langsung
# Jika dibuka di HP, layout otomatis menumpuk ke bawah (bukan kiri-kanan)
col_cal, col_detail = st.columns([2, 1] if st.sidebar.checkbox("Mode Desktop/Tablet", value=True) else [1, 1])

# Namun agar lebih aman di Android murni, kita pisah pakai container standar jika ingin otomatis:
# Di sini kita gunakan trik layout kolom tunggal otomatis di mobile bawaan Streamlit
col_cal, col_detail = st.columns([1.8, 1.2])

with col_cal:
    st.markdown("#### 📅 Kalender Kegiatan")
    calendar_options = {
        "initialView": "dayGridMonth",
        "timeZone": "Asia/Jakarta",
        "headerToolbar": {
            "left": "prev,next",
            "center": "title",
            "right": "today,listMonth", # Diganti listMonth agar di HP gampang di-scroll ke bawah
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
    st.markdown("#### 🔍 Panel Informasi")
    
    if state.get("eventClick"):
        clicked = state["eventClick"]["event"]
        extended = clicked.get('extendedProps', {})
        dept_name = extended.get('dept', '-') if extended else '-'
        desc_text = extended.get('desc', 'Tidak ada deskripsi.') if extended else 'Tidak ada deskripsi.'
        
        st.markdown(f"""
            <div class="proker-card">
                <span class="badge-dept">🏢 Dept: {dept_name}</span>
                <h2 style='margin:0 0 8px 0; color:#3b82f6; font-size:18px; font-weight:700;'>{clicked['title']}</h2>
                <p style='margin: 2px 0; font-size:12px; color:#94a3b8;'>📅 <b>Mulai:</b> {clicked['start'][:10]}</p>
                {"<p style='margin: 2px 0; font-size:12px; color:#94a3b8;'>🏁 <b>Selesai:</b> " + clicked['end'][:10] + "</p>" if clicked.get('end') else ""}
                <hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 12px 0;'>
                <p style='margin:0; font-size:13px; color:#e2e8f0; line-height:1.5;'><b>📋 Detail:</b><br>{desc_text}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); border-radius: 8px; padding: 20px; text-align: center; color: #64748b; font-size:13px;'>
                Klik salah satu agenda di kalender untuk melihat detail di sini.
            </div>
        """, unsafe_allow_html=True)