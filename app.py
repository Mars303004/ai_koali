import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl  # Library untuk menulis file Excel
import os
import json
from io import BytesIO

# --- Initialize Session State ---
if 'kpi_data_2025' not in st.session_state:
    st.session_state.kpi_data_2025 = pd.DataFrame(columns=[
        'Perspective', 'Nomor KPI', 'KPI', 'PIC', 'BU',
        'Measurement Type', 'YTD Achievement Type', 'Bulan',
        'YTD Target', 'YTD Actual'
    ])

if 'kpi_edit_history' not in st.session_state:
    st.session_state.kpi_edit_history = []

# --- Functions ---

def save_kpi_to_excel(df, filename="kpi_data_2025.xlsx"):
    """Simpan data KPI ke file Excel"""
    try:
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='KPI Data')
        st.success("✅ Data berhasil disimpan secara permanen ke Excel!")
        st.session_state.kpi_edit_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'action': 'Auto-saved to Excel',
            'details': f'Saved {len(df)} rows to {filename}'
        })
    except Exception as e:
        st.error(f"❌ Gagal menyimpan ke Excel: {e}")

def load_kpi_from_excel(filename="kpi_data_2025.xlsx"):
    """Muat data KPI dari file Excel"""
    if os.path.exists(filename):
        try:
            return pd.read_excel(filename)
        except Exception as e:
            st.warning(f"⚠️ Tidak bisa membaca file Excel: {e}")
            return st.session_state.kpi_data_2025
    else:
        return st.session_state.kpi_data_2025

def display_scorecard(title, value, change):
    change_class = "positive" if change >= 0 else "negative"
    change_symbol = "▲" if change > 0 else "▼"
    change_color = "#22c55e" if change >= 0 else "#ef4444"
    formatted_value = f"{value:.1f}%" if isinstance(value, float) and value < 100 else str(value)

    st.markdown(f"""
    <div class="scorecard">
        <h4>{title}</h4>
        <div class="metric-value">{formatted_value}</div>
        <div class="metric-change {change_class}">
            <span style="color: {change_color};">{change_symbol} {abs(change):.1f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_enhanced_kpi_input_section():
    st.markdown("### 📝 Input dan Edit Data KPI")

    # Tombol Mode View/Edit
    col1, col2 = st.columns([4, 1])
    with col1:
        view_mode = st.selectbox("🔧 Mode", ["👁️ View Only", "✏️ Edit Mode"], key="enhanced_kpi_view_mode")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True, key="refresh_kpi"):
            st.rerun()

    # Load data dari file Excel jika sudah ada
    if 'kpi_data_2025' not in st.session_state or st.session_state.kpi_data_2025.empty:
        st.session_state.kpi_data_2025 = load_kpi_from_excel()

    # Hanya tampilkan editor di tab Edit Mode
    if view_mode == "✏️ Edit Mode":
        # Tombol Aksi
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Tambah Baris", use_container_width=True, key="add_row_excel"):
                new_row = {
                    'Perspective': 'Financial',
                    'Nomor KPI': '',
                    'KPI': '',
                    'PIC': '',
                    'BU': 'BU1',
                    'Measurement Type': 'Higher better',
                    'YTD Achievement Type': 'SUM',
                    'Bulan': 'Jan-25',
                    'YTD Target': 0.0,
                    'YTD Actual': 0.0
                }
                st.session_state.kpi_data_2025 = pd.concat(
                    [st.session_state.kpi_data_2025, pd.DataFrame([new_row])],
                    ignore_index=True
                )
                st.rerun()
        with col2:
            if st.button("🗑️ Hapus Baris Terakhir", use_container_width=True, key="delete_last_excel"):
                if len(st.session_state.kpi_data_2025) > 0:
                    deleted_kpi = st.session_state.kpi_data_2025.iloc[-1]['KPI']
                    st.session_state.kpi_data_2025 = st.session_state.kpi_data_2025.iloc[:-1]
                    st.session_state.kpi_edit_history.append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'action': 'Deleted last row',
                        'details': f'Deleted KPI: {deleted_kpi}'
                    })
                    st.rerun()
        with col3:
            if st.button("💾 Simpan ke Excel", use_container_width=True, key="save_excel"):
                if not st.session_state.kpi_data_2025.empty:
                    save_kpi_to_excel(st.session_state.kpi_data_2025)
                else:
                    st.warning("Tidak ada data untuk disimpan")

    # Tabel Interaktif
    edited_df = st.data_editor(
        st.session_state.kpi_data_2025,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Perspective": st.column_config.SelectboxColumn(options=["Financial", "Customer n Service", "Quality", "Employee"]),
            "BU": st.column_config.SelectboxColumn(options=["BU1", "BU2", "BU3"]),
            "Measurement Type": st.column_config.SelectboxColumn(options=["Higher better", "Lower better"]),
            "YTD Achievement Type": st.column_config.SelectboxColumn(options=["SUM", "AVERAGE", "WEIGHTED AVERAGE", "LAST"]),
            "Bulan": st.column_config.SelectboxColumn(options=["Jan-25", "Feb-25"]),
            "YTD Target": st.column_config.NumberColumn(format="%.2f"),
            "YTD Actual": st.column_config.NumberColumn(format="%.2f")
        },
        hide_index=True,
        key="data_editor_excel"
    )

    # Update session_state jika ada perubahan
    if not edited_df.equals(st.session_state.kpi_data_2025):
        st.session_state.kpi_data_2025 = edited_df
        st.info("✍️ Perubahan terdeteksi. Gunakan tombol 'Simpan ke Excel' untuk menyimpan permanen.")

    # Tampilkan jumlah baris
    st.markdown(f"**Jumlah KPI:** {len(st.session_state.kpi_data_2025)} baris")

    # History Section
    if st.session_state.kpi_edit_history:
        with st.expander("📜 Riwayat Perubahan"):
            for item in reversed(st.session_state.kpi_edit_history[-5:]):
                st.markdown(f"- **{item['timestamp']}**: {item['action']} - {item['details']}")

# --- Main App Logic ---
def main():
    st.title("💾 Auto-Save KPI ke Excel")

    display_enhanced_kpi_input_section()

    # Tombol Download Manual
    if not st.session_state.kpi_data_2025.empty:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state.kpi_data_2025.to_excel(writer, sheet_name='KPI Data', index=False)
        st.download_button(
            label="📥 Download Excel File",
            data=buffer.getvalue(),
            file_name=f"kpi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    else:
        st.info("Belum ada data. Silakan tambah baris di atas.")

# --- Run App ---
if __name__ == "__main__":
    main()
