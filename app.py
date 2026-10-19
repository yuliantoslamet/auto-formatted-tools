import json
import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Webinar Data Processor", page_icon="📊", layout="wide"
)

st.title("📊 Webinar Data Processor Tool")
st.write(
    "Unggah data peserta lengkap dan daftar email aktif untuk melakukan filter"
    " serta pencocokan kolom secara dinamis."
)

st.divider()

# --- 1. UPLOAD FILE ---
col_up1, col_up2 = st.columns(2)

with col_up1:
  st.subheader("1. File Data Peserta Lengkap (File 1)")
  file1 = st.file_uploader(
      "Unggah CSV atau Excel (Data Lengkap)",
      type=["csv", "xlsx"],
      key="file1",
  )

with col_up2:
  st.subheader("2. File Daftar Email Aktif (File 2)")
  file2 = st.file_uploader(
      "Unggah CSV atau Excel (Daftar Email Filter)",
      type=["csv", "xlsx"],
      key="file2",
  )

# Fungsi Pembaca File
def load_data(uploaded_file):
  if uploaded_file.name.endswith(".csv"):
    # Membaca semua kolom sebagai string terlebih dahulu agar angka '0' depan (No Telp) tidak hilang
    return pd.read_csv(uploaded_file, dtype=str)
  else:
    return pd.read_excel(uploaded_file, dtype=str)


if file1 and file2:
  try:
    df1 = load_data(file1)
    df2 = load_data(file2)

    st.success("✅ Kedua file berhasil diunggah!")
    st.divider()

    # --- 2. MAPPING KOLOM DINAMIS ---
    st.subheader("⚙️ Konfigurasi Mapping Kolom")

    cols1 = list(df1.columns)
    cols2 = list(df2.columns)

    c1, c2, c3 = st.columns(3)

    with c1:
      email_col_file1 = st.selectbox(
          "Pilih Header Email di File 1:",
          cols1,
          index=0 if "EMAIL" in cols1 else 0,
      )
      name_col_file1 = st.selectbox(
          "Pilih Header Nama di File 1:",
          cols1,
          index=(
              cols1.index("NAMA LENGKAP")
              if "NAMA LENGKAP" in cols1
              else min(1, len(cols1) - 1)
          ),
      )

    with c2:
      email_col_file2 = st.selectbox(
          "Pilih Header Email di File 2 (Penyaring):",
          cols2,
          index=0 if "Email" in cols2 else 0,
      )

    with c3:
      output_filename = st.text_input(
          "Nama File Hasil (Tanpa Ekstensi):", value="hasil_final"
      )

# --- 3. OPSI ATTRIBUTES (JSON) ---
    st.divider()
    st.subheader("🏷️ Opsi Atribut JSON Kustom")

    use_attributes = st.checkbox(
        "Gunakan Kolom 'attributes' (JSON)", value=True
    )
    attr_mapping = {}

    if use_attributes:
      selected_attr_cols = st.multiselect(
          "Pilih header kolom dari File 1 yang ingin dimasukkan ke dalam JSON"
          " 'attributes':",
          options=cols1,
          default=[col for col in cols1 if col not in [email_col_file1]],
      )

      if selected_attr_cols:
        st.write("##### 🛠️ Pengaturan Key JSON Kustom (Opsional)")
        st.caption(
            "Ubah nama key JSON sesuai kebutuhan (secara default akan"
            " menggunakan nama header asli):"
        )

        # Menampilkan input bidang untuk setiap kolom yang dipilih
        cols_per_row = 2
        for i in range(0, len(selected_attr_cols), cols_per_row):
          row_cols = st.columns(cols_per_row)
          for j, col_name in enumerate(
              selected_attr_cols[i : i + cols_per_row]
          ):
            with row_cols[j]:
              # Menentukan nilai default otomatis yang lebih rapi/bebas karakter khusus jika ada
              default_key = col_name.lower().strip()
              if "nama" in default_key:
                default_key = "name"
              elif "telp" in default_key or "wa" in default_key:
                default_key = "no wa"
              elif "sertifikat" in default_key:
                default_key = "sertifikat"

              custom_key = st.text_input(
                  f"Key JSON untuk `{col_name}`:",
                  value=default_key,
                  key=f"attr_key_{col_name}",
              )
              attr_mapping[col_name] = (
                  custom_key.strip() if custom_key.strip() else col_name
              )

    # --- 4. PROSES DATA & HASIL ---
    st.divider()
    if st.button("🚀 Proses Data Sekarang", type="primary"):
      # Cleaning email
      df1[email_col_file1] = (
          df1[email_col_file1].astype(str).str.strip().str.lower()
      )
      df2[email_col_file2] = (
          df2[email_col_file2].astype(str).str.strip().str.lower()
      )

      # Filter berdasarkan keberadaan email di File 2
      df_filtered = df1[
          df1[email_col_file1].isin(df2[email_col_file2])
      ].copy()
      df_filtered = df_filtered.fillna("")

      # Buat kolom attributes jika diaktifkan
      if use_attributes and attr_mapping:

        def make_attributes_json(row):
          # Membuat dictionary dengan key kustom buatan user
          attr_dict = {
              custom_key: row[original_col]
              for original_col, custom_key in attr_mapping.items()
          }
          return json.dumps(attr_dict, ensure_ascii=False)

        df_filtered["attributes"] = df_filtered.apply(
            make_attributes_json, axis=1
        )

      # Rename kolom utama
      rename_dict = {email_col_file1: "email", name_col_file1: "name"}
      df_filtered = df_filtered.rename(columns=rename_dict)

      # Susun kolom akhir
      final_cols = ["email", "name"]
      if use_attributes and "attributes" in df_filtered.columns:
        final_cols.append("attributes")

      df_result = df_filtered[final_cols]

      # Ringkasan Statistik & Preview
      st.subheader("📈 Hasil Pemrosesan")
      st.info(
          f"Total data di File 1: **{len(df1)}** | Total email aktif di File 2:"
          f" **{len(df2)}** | Data berhasil dicocokkan:"
          f" **{len(df_result)}**"
      )

      st.dataframe(df_result.head(10), use_container_width=True)

      # Export CSV
      csv_buffer = io.StringIO()
      df_result.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
      csv_data = csv_buffer.getvalue()

      final_file_name = f"{output_filename.strip() if output_filename else 'hasil_final'}.csv"
      st.download_button(
          label=f"📥 Unduh {final_file_name}",
          data=csv_data,
          file_name=final_file_name,
          mime="text/csv",
      )
