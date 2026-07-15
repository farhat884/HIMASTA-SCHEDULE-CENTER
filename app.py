import streamlit as st
from streamlit_calendar import calendar
import datetime
import base64
import os
from PIL import Image, ImageDraw
import io
import textwrap
from PIL import Image

# --- CONFIG DASHBOARD ---
logo_path = "saran_perubahan_logo-removebg-preview.png"

# 2. Cek apakah file logonya ada, jika ada buka pakai PIL, jika tidak pakai emoji cadangan
if os.path.exists(logo_path):
    icon_himpunan = Image.open(logo_path)
else:
    icon_himpunan = "📅"  # Cadangan jika file logo tidak ditemukan

# 3. Pasang di set_page_config
st.set_page_config(
    page_title="Himasta Schedule Center", 
    layout="wide", 
    page_icon=icon_himpunan
)

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

# --- LOAD SEMUA LOGO DEPARTEMEN & HIMPUNAN ---
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
        background-image: linear-gradient(rgba(11, 34, 64, 0.85), rgba(11, 34, 64, 0.85)), url("data:image/png;base64,{logo_base64}");
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

# --- CSS UTK ELEMEN LUAR (CARDS & BUTTONS) ---
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

    [data-testid="stExpander"] [data-testid="column"] {
        background: transparent !important;
        border: none !important;
        padding: 0px !important;
        box-shadow: none !important;
        position: relative !important;
    }

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

    .divisi-card.inactive {
        background: rgba(13, 37, 69, 0.35);
        border: 2px solid rgba(255, 255, 255, 0.08);
        filter: grayscale(85%) opacity(0.5);
    }
    
    .divisi-card.inactive:hover {
        filter: grayscale(30%) opacity(0.85);
        border: 2px solid rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
    }

    .divisi-card.active-Akademik { background: rgba(16, 185, 129, 0.15) !important; border: 2px solid #10b981 !important; box-shadow: 0 0 18px rgba(16, 185, 129, 0.4); }
    .divisi-card.active-PSDM { background: rgba(239, 68, 68, 0.15) !important; border: 2px solid #ef4444 !important; box-shadow: 0 0 18px rgba(239, 68, 68, 0.4); }
    .divisi-card.active-PR { background: rgba(245, 158, 11, 0.15) !important; border: 2px solid #f59e0b !important; box-shadow: 0 0 18px rgba(245, 158, 11, 0.4); }
    .divisi-card.active-RION { background: rgba(168, 85, 247, 0.15) !important; border: 2px solid #a855f7 !important; box-shadow: 0 0 18px rgba(168, 85, 247, 0.4); }
    .divisi-card.active-KOMINFO { background: rgba(59, 130, 246, 0.15) !important; border: 2px solid #3b82f6 !important; box-shadow: 0 0 18px rgba(59, 130, 246, 0.4); }

    [data-testid="stExpander"] [data-testid="column"] div[data-testid="stButton"] {
        position: absolute !important;
        top: 0 !important; left: 0 !important; width: 100% !important; height: 100% !important;
        opacity: 0 !important; z-index: 10 !important; margin: 0 !important; padding: 0 !important;
    }
    [data-testid="stExpander"] [data-testid="column"] div[data-testid="stButton"] button {
        width: 100% !important; height: 100% !important; margin: 0 !important; padding: 0 !important; cursor: pointer !important;
    }

    .badge-dept {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; display: inline-block; margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INISIALISASI DATA PROGRAM KERJA ---
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
                <i>Hari ini: {datetime.date.today().strftime('%A, %d %B %Y')}</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- FILTER DEPARTEMEN ---
with st.expander("Pilih Divisi", expanded=False):
    if "filter_depts" not in st.session_state:
        st.session_state.filter_depts = {"Akademik": True, "PSDM": True, "PR": True, "RION": True, "KOMINFO": True}

    cols = st.columns(5)
    depts = ["Akademik", "PSDM", "PR", "RION", "KOMINFO"]

    for col, dept in zip(cols, depts):
        with col:
            is_active = st.session_state.filter_depts[dept]
            card_class = f"active-{dept}" if is_active else "inactive"
            img_base64 = globals().get(f"{dept.lower()}_base64", "")
            
            img_html = f'<img src="data:image/png;base64,{img_base64}" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 8px; display: block; margin-left: auto; margin-right: auto;">' if img_base64 else '🏢'
            
            st.markdown(textwrap.dedent(f"""
                <div class="divisi-card {card_class}">
                    {img_html}
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff;">{dept}</div>
                </div>
            """), unsafe_allow_html=True)
            
            if st.button("Pilih", key=f"btn_toggle_{dept}", use_container_width=True):
                st.session_state.filter_depts[dept] = not st.session_state.filter_depts[dept]
                st.rerun()

filtered_dept = [dept for dept, active in st.session_state.filter_depts.items() if active]
filtered_events = [e for e in st.session_state.proker_data if e['dept'] in filtered_dept]

# ==========================================================
# PROSES MENYUNTIKKAN BADGE [H-ANGKA] DI DEPAN JUDUL (BIAR RAPI SEPERTI KOLOM)
# ==========================================================
display_events = []
today = datetime.date.today()

for event in filtered_events:
    event_copy = event.copy()
    try:
        event_date = datetime.datetime.strptime(event['start'][:10], "%Y-%m-%d").date()
        delta = (event_date - today).days
        
        # Format penulisan H- / Hari H / H+ (Selesai)
        if delta > 0:
            countdown = f"H-{delta}"
        elif delta == 0:
            countdown = "Hari H"
        else:
            countdown = f"H+{abs(delta)}"
            
        # Kita letakkan di depan agar berbaris sejajar lurus ke bawah di List View!
        event_copy['title'] = f"[{countdown}]  {event['title']}"
    except Exception:
        pass
    display_events.append(event_copy)

st.markdown("---")

# --- LAYOUT UTAMA ---
col_cal, col_detail = st.columns([1.8, 1.2])

with col_cal:
    st.markdown("#### Kalender Kegiatan")
    
    calendar_options = {
        "initialView": "dayGridMonth",
        "timeZone": "Asia/Jakarta",
        "headerToolbar": {
            "left": "prev,next",
            "center": "title",
            "right": "today,dayGridMonth,listMonth",
        },
        "editable": False,
        "selectable": True,
    }
    
    # ==========================================================
    # TRIK INJEKSI IFRAME: Menyuntikkan CSS langsung ke dalam Kalender
    # ==========================================================
    iframe_custom_css = """
        /* Singkirkan warna hitam pekat background bawaan iframe streamlit */
        .fc, .fc-view-harness, .fc-scrollgrid {
            background: rgba(17, 43, 80, 0.40) !important;
            background-color: rgba(17, 43, 80, 0.40) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 14px !important;
            color: #ffffff !important;
        }
        
        /* Hancurkan kotak hitam di grid sel tanggal */
        .fc-theme-standard td, 
        .fc-theme-standard th, 
        .fc-daygrid-day,
        .fc-daygrid-bg-harness,
        .fc-scroller {
            background: transparent !important;
            background-color: transparent !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        /* Warna teks tanggal & hari */
        .fc .fc-col-header-cell-cushion { color: #94a3b8 !important; font-weight: 600 !important; text-decoration: none !important; }
        .fc .fc-daygrid-day-number { color: #cbd5e1 !important; text-decoration: none !important; font-weight: 600; }
        
        /* Highlight hari ini */
        .fc .fc-day-today { background: rgba(59, 130, 246, 0.2) !important; }

        /* Styling Tombol Navigasi */
        .fc .fc-button-primary {
            background-color: #3b82f6 !important;
            border-color: transparent !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }
        .fc .fc-button-primary:hover { background-color: #2563eb !important; }
        .fc .fc-button-primary:not(:disabled).fc-button-active { background-color: #1d4ed8 !important; }

        /* Sembunyikan kolom "all-day" di List View */
        .fc-list-event-time {
            display: none !important;
        }
    """
    
    state = calendar(
        events=display_events,
        options=calendar_options,
        custom_css=iframe_custom_css,
        key="himasta_calendar",
    )

with col_detail:
    st.markdown("#### 🔍 Panel Informasi")
    if state.get("eventClick"):
        clicked = state["eventClick"]["event"]
        extended = clicked.get('extendedProps', {})
        dept_name = extended.get('dept', '-') if extended else '-'
        
        # 1. AMBIL DATA DARI EVENT SECARA AMAN
        raw_title = clicked.get('title', 'Tanpa Nama Kegiatan')
        
        # BERSIHKAN JUDUL: Potong embel-embel "[H-...]  " di depan agar judul utama di panel tetap rapi dan bersih
        if "]  " in raw_title:
            title = raw_title.split("]  ", 1)[-1]
        else:
            title = raw_title
        
        start_date = clicked.get('start', '-')[:10]
        end_date = clicked.get('end')[:10] if clicked.get('end') else None
        desc_text = extended.get('desc', 'Tidak ada deskripsi kegiatan.') if extended else 'Tidak ada deskripsi kegiatan.'
        
        # 2. ATUR WARNA & LOGO DEPARTEMEN
        dept_colors = {"Akademik": "#10b981", "PSDM": "#ef4444", "PR": "#f59e0b", "RION": "#a855f7", "KOMINFO": "#60a5fa"}
        current_color = dept_colors.get(dept_name, "#3b82f6")
        img_base64 = globals().get(f"{dept_name.lower()}_base64", "")
        
        logo_html = f"""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{img_base64}" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 6px;">
                <div style="font-size: 14px; font-weight: 700; color: {current_color}; letter-spacing: 0.5px;">DIVISI {dept_name.upper()}</div>
            </div>
        """ if img_base64 else ""
            
        end_date_html = f"""
            <p style="margin: 4px 0; font-size: 13px; color: #94a3b8;">
                🏁 <b>Selesai / Tenggat:</b> <span style="color: #cbd5e1;">{end_date}</span>
            </p>
        """ if end_date else ""

        # 3. GABUNGKAN HTML UTUH
        html_content = f"""
            <div class="proker-card">
                <span class="badge-dept"> Dept: {dept_name}</span>
                {logo_html}
                
                <h2 style="margin: 12px 0 8px 0; color: #3b82f6; font-size: 20px; font-weight: 700; line-height: 1.3;">
                    {title}
                </h2>
                
                <div style="margin-bottom: 12px;">
                    <p style="margin: 4px 0; font-size: 13px; color: #94a3b8;">
                        📅 <b>Mulai:</b> <span style="color: #cbd5e1;">{start_date}</span>
                    </p>
                    {end_date_html}
                </div>
                
                <hr style="border: 0; border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 12px 0;">
                
                <div style="margin-top: 8px;">
                    <p style="margin: 0 0 4px 0; font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                        📋 Deskripsi Kegiatan
                    </p>
                    <p style="margin: 0; font-size: 13px; color: #e2e8f0; line-height: 1.6;">
                        {desc_text}
                    </p>
                </div>
            </div>
        """
        
        cleaned_html = "\n".join([line.strip() for line in html_content.split("\n")])
        st.markdown(cleaned_html, unsafe_allow_html=True)
        
    else:
        no_event_html = """
            <div style='background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); border-radius: 8px; padding: 20px; text-align: center; color: #64748b; font-size:13px;'>
                Klik salah satu agenda di kalender untuk melihat detail di sini.
            </div>
        """
        cleaned_no_event = "\n".join([line.strip() for line in no_event_html.split("\n")])
        st.markdown(cleaned_no_event, unsafe_allow_html=True)