import streamlit as st
from streamlit_calendar import calendar
import datetime
import base64
import os
from PIL import Image, ImageDraw
import io

# --- CONFIG DASHBOARD ---
st.set_page_config(page_title="Himasta Schedule Center", layout="wide", page_icon="📅")

# --- FUNGSI MENGUBAH GAMBAR BIASA KE BASE64 ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    return None

# --- FUNGSI OTOMATIS MEMOTONG LOGO UTAMA MENJADI BULAT SEMPURNA ---
def get_circular_logo_base64(image_path):
    if os.path.exists(image_path):
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        
        min_dim = min(width, height)
        left = int((width - min_dim) / 2)
        top = int((height - min_dim) / 2)
        right = left + min_dim
        bottom = top + min_dim
        img = img.crop((left, top, right, bottom))
        
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((1, 1, img.size[0] - 1, img.size[1] - 1), fill=255)
        
        img.putalpha(mask)
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    return None

# Load Semua Logo (Utama dan 5 Divisi Kustom)
logo_base64 = get_circular_logo_base64("saran_perubahan_logo-removebg-preview.png")
rion_base64 = get_base64_image("Cuplikan layar 2026-07-15 202602.png")
psdm_base64 = get_base64_image("Cuplikan layar 2026-07-15 203856.png")
akademik_base64 = get_base64_image("Cuplikan layar 2026-07-15 204138.png")
kominfo_base64 = get_base64_image("Cuplikan layar 2026-07-15 204409.png")
pr_base64 = get_base64_image("Cuplikan layar 2026-07-15 204601.png")

# --- CSS BACKGROUND: MAIN BODY (POLA PATTERN NAVY BLUE) ---
if logo_base64:
    background_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: #0b2240 !important;
        background-image: linear-gradient(rgba(11, 34, 64, 0.80), rgba(11, 34, 64, 0.80)), url("data:image/png;base64,{logo_base64}");
        background-size: 200px 200px;
        background-repeat: repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# --- CSS KUSTOM UNTUK ELEMEN UI & CLICKABLE CARDS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .proker-card, .filter-card {
        background: rgba(17, 43, 80, 0.70);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 16px;
    }

    .stExpander {
        background: rgba(17, 43, 80, 0.50) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* ==================================================
       DESAIN KARTU DIVISI INTERAKTIF (BISA DIKLIK)
       ================================================== */
    
    /* Reset Kolom Bawaan Expander agar Mengikuti Desain Kartu Kita */
    [data-testid="stExpander"] [data-testid="column"] {
        background: transparent !important;
        border: none !important;
        padding: 0px !important;
        box-shadow: none !important;
        position: relative !important; /* Wajib untuk overlay tombol */
    }

    /* Base Styling Kartu Divisi */
    .divisi-card {
        width: 100%;
        padding: 24px 16px;
        border-radius: 12px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        cursor: pointer;
    }

    /* KONDISI 1: JIKA NONAKTIF (Meredup & Border Gelap) */
    .divisi-card.inactive {
        background: rgba(13, 37, 69, 0.35);
        border: 2px solid rgba(255, 255, 255, 0.08);
        filter: grayscale(85%) opacity(0.5);
    }
    
    /* Hover Effect Saat Divisi Nonaktif Disentuh */
    .divisi-card.inactive:hover {
        filter: grayscale(30%) opacity(0.85);
        border: 2px solid rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
    }

    /* KONDISI 2: JIKA AKTIF (Glowing & Berwarna Cerah) */
    .divisi-card.active-Akademik {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 2px solid #10b981 !important;
        box-shadow: 0 0 18px rgba(16, 185, 129, 0.4);
    }
    .divisi-card.active-PSDM {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 2px solid #ef4444 !important;
        box-shadow: 0 0 18px rgba(239, 68, 68, 0.4);
    }
    .divisi-card.active-PR {
        background: rgba(245, 158, 11, 0.15) !important;
        border: 2px solid #f59e0b !important;
        box-shadow: 0 0 18px rgba(245, 158, 11, 0.4);
    }
    .divisi-card.active-RION {
        background: rgba(168, 85, 247, 0.15) !important;
        border: 2px solid #a855f7 !important;
        box-shadow: 0 0 18px rgba(168, 85, 247, 0.4);
    }
    .divisi-card.active-KOMINFO {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 2px solid #3b82f6 !important;
        box-shadow: 0 0 18px rgba(59, 130, 246, 0.4);
    }

    /* Hover Effect Saat Divisi Aktif Disentuh */
    .divisi-card[class*="active-"]:hover {
        transform: translateY(-2px);
    }

    /* ==================================================
       TRIK TRANSPARANSI TOMBOL OVERLAY STREAMLIT
       ================================================== */
    /* Menyulap tombol asli Streamlit agar benar-benar transparan & menutupi seluruh kartu */
    [data-testid="stExpander"] [data-testid="column"] div[data-testid="stButton"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important; /* Tombol tidak terlihat tetapi tetap bisa diklik */
        z-index: 10 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stExpander"] [data-testid="column"] div[data-testid="stButton"] button {
        width: 100% !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        cursor: pointer !important;
    }
    /* ================================================== */

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
    
    .fc {
        background: rgba(13, 37, 69, 0.65) !important;
        backdrop-filter: blur(8px);
        padding: 8px !important;
        border-radius: 12px;
        font-size: 13px !important;
    }
    
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
        {"title": "LDKM 25: Rapat Perdana", "start": "2026-07-01", "end": "2026-07-02", "color": "#3b82f6", "dept": "PSDM", "desc": "Penyampaian arahan dan penyamaan konsep dasar Kepanitiaan."},
        {"title": "LDKM 25: Rapat Akbar", "start": "2026-07-05", "end": "2026-07-06", "color": "#60a5fa", "dept": "PSDM", "desc": "Evaluasi dan peninjauan progres berkala dari setiap divisi panitia."},
        {"title": "RION: Mapping Riset Data", "start": "2026-08-12", "color": "#a855f7", "dept": "RION", "desc": "Pemetaan topik riset sains data strategis untuk perlombaan eksternal."},
        {"title": "PR: Kunjungan Industri PT Japfa", "start": "2026-08-20", "color": "#f59e0b", "dept": "PR", "desc": "Pelaksanaan kunjungan industri strategis Himpunan Mahasiswa Sains Data ke PT Japfa Comfeed Indonesia Tbk untuk membuka peluang riset dan kerja sama eksternal."},
        {"title": "LDKM 26 & Makrab: Hari H", "start": "2026-11-06", "end": "2026-11-09", "color": "#ef4444", "dept": "PSDM", "desc": "Pelaksanaan LDKM 26 sekaligus Malam Keakraban gabungan 3 angkatan."},
        {"title": "HIMA Champ", "start": "2026-11-05", "end": "2026-11-08", "color": "#a855f7", "dept": "PSDM", "desc": "Kompetisi internal sains data berfokus pada turnamen olahraga fisik antar-angkatan."},
        {"title": "KOMINFO: Rilis Grand Design Web", "start": "2026-07-20", "color": "#60a5fa", "dept": "KOMINFO", "desc": "Publikasi konsep arsitektur visual dan pusat data jadwal Himasta terbaru."}
    ]

# --- MAIN HEADER ---
if logo_base64:
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 24px; margin-top: -10px;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 150px; height: 150px; object-fit: contain; margin-bottom: 16px;">
            <h1 style="margin: 0; font-size: 46px; font-weight: 800; color: #ffffff; letter-spacing: -1px; line-height: 1.2;">
                Himasta Schedule Center
            </h1>
            <p style="margin-top: 8px; font-size: 14px; color: #94a3b8;">
                🚀 <i>Hari ini: {datetime.date.today().strftime('%A, %d %B %Y')}</i>
            </p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center;'>Himasta Schedule Center</h1>", unsafe_allow_html=True)

st.markdown("---")

# --- FITUR MENU LIPAT (EXPANDER FILTER - CLICKABLE CARDS) ---
with st.expander("📂 Klik di Sini untuk Menyaring Departemen / Divisi", expanded=False):
    if "filter_depts" not in st.session_state:
        st.session_state.filter_depts = {
            "Akademik": True, "PSDM": True, "PR": True, "RION": True, "KOMINFO": True
        }

    cols = st.columns(5)
    depts = ["Akademik", "PSDM", "PR", "RION", "KOMINFO"]

    for col, dept in zip(cols, depts):
        with col:
            # Mengambil status keaktifan divisi saat ini
            is_active = st.session_state.filter_depts[dept]
            
            # Menentukan CSS class berdasarkan status (aktif/nonaktif)
            card_class = f"active-{dept}" if is_active else "inactive"
            
            # Memilih gambar yang sesuai
            img_base64 = ""
            if dept == "Akademik": img_base64 = akademik_base64
            elif dept == "PSDM": img_base64 = psdm_base64
            elif dept == "PR": img_base64 = pr_base64
            elif dept == "RION": img_base64 = rion_base64
            elif dept == "KOMINFO": img_base64 = kominfo_base64
            
            # Konversi gambar ke tag HTML
            if img_base64:
                img_html = f'<img src="data:image/png;base64,{img_base64}" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 8px; display: block; margin-left: auto; margin-right: auto;">'
            else:
                img_html = '<h2 style="margin: 0 0 8px 0; font-size: 55px; text-align: center;">🏢</h2>'
            
            # Rendering struktur kartu visual divisi
            st.markdown(f"""
                <div class="divisi-card {card_class}">
                    {img_html}
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff; text-align: center;">{dept}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Menumpuk tombol transparan rahasia tepat di atas kartu visual.
            # Saat diklik, status divisi akan otomatis terbalik dan merender ulang tampilan (rerun).
            if st.button("Pilih", key=f"btn_toggle_{dept}", use_container_width=True):
                st.session_state.filter_depts[dept] = not st.session_state.filter_depts[dept]
                st.rerun()

filtered_dept = [dept for dept, active in st.session_state.filter_depts.items() if active]
filtered_events = [e for e in st.session_state.proker_data if e['dept'] in filtered_dept]

st.markdown("---")

# --- LAYOUT KOLOM (KALENDER & DETAIL) ---
col_cal, col_detail = st.columns([1.8, 1.2])

with col_cal:
    st.markdown("#### 📅 Kalender Kegiatan")
    calendar_options = {
        "initialView": "dayGridMonth",
        "timeZone": "Asia/Jakarta",
        "headerToolbar": {
            "left": "prev,next",
            "center": "title",
            "right": "today,listMonth",
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
        
        # Logika memunculkan masing-masing logo divisi di panel detail
        logo_html = ""
        if dept_name == "Akademik" and akademik_base64:
            logo_html = f"""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{akademik_base64}" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 6px;">
                <div style="font-size: 14px; font-weight: 700; color: #10b981; letter-spacing: 0.5px;">DEPARTEMEN AKADEMIK</div>
            </div>
            """
        elif dept_name == "PSDM" and psdm_base64:
            logo_html = f"""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{psdm_base64}" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 6px;">
                <div style="font-size: 14px; font-weight: 700; color: #ef4444; letter-spacing: 0.5px;">DIVISI PSDM</div>
            </div>
            """
        elif dept_name == "PR" and pr_base64:
            logo_html = f"""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{pr_base64}" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 6px;">
                <div style="font-size: 14px; font-weight: 700; color: #f59e0b; letter-spacing: 0.5px;">DEPARTEMEN PUBLIC RELATIONS</div>
            </div>
            """
        elif dept_name == "RION" and rion_base64:
            logo_html = f"""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{rion_base64}" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 6px;">
                <div style="font-size: 14px; font-weight: 700; color: #a855f7; letter-spacing: 0.5px;">DIVISI RION</div>
            </div>
            """
        elif dept_name == "KOMINFO" and kominfo_base64:
            logo_html = f"""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{kominfo_base64}" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 6px;">
                <div style="font-size: 14px; font-weight: 700; color: #60a5fa; letter-spacing: 0.5px;">DEPARTEMEN KOMINFO</div>
            </div>
            """
            
        st.markdown(f"""
            <div class="proker-card">
                <span class="badge-dept">🏢 Dept: {dept_name}</span>
                {logo_html}
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