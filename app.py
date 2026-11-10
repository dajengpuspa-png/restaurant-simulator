import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fine Dining Launching Simulator", layout="wide")

st.title("🍽️ Fine Dining Set Menu & Launching Simulator")
st.markdown(
    "Simulator perencanaan stok bahan, penentuan harga jual (*Food Cost* 25%–30%), "
    "serta perhitungan untung/rugi untuk peluncuran restoran *Fine Dining*."
)

st.divider()

# ==========================================
# LANGKAH 1: INPUT STOK & MODAL BAHAN SET MENU
# ==========================================
st.subheader("1️⃣ Input Stok & Harga Bahan per Kategori (1 Set Menu)")
st.caption(
    "Ketik langsung di dalam tabel di bawah ini untuk mengubah nama bahan/menu, total harga belanja, "
    "dan jumlah porsi yang bisa dibuat. Kamu juga bisa menambah baris baru dengan klik tanda (+) di bawah tabel."
)

default_ingredients = pd.DataFrame([
    {"Kategori": "1. Appetizer", "Nama Bahan / Menu": "Bahan Appetizer Lengkap", "Total Harga Beli (NT$)": 3500, "Bisa Buat Berapa Porsi": 100},
    {"Kategori": "2. Salad", "Nama Bahan / Menu": "Sayuran & Dressing Salad", "Total Harga Beli (NT$)": 2500, "Bisa Buat Berapa Porsi": 100},
    {"Kategori": "3. Soup", "Nama Bahan / Menu": "Bahan Dasar & Kaldu Soup", "Total Harga Beli (NT$)": 3000, "Bisa Buat Berapa Porsi": 100},
    {"Kategori": "4. Main Course", "Nama Bahan / Menu": "Protein Utama & Garnish", "Total Harga Beli (NT$)": 8500, "Bisa Buat Berapa Porsi": 100},
    {"Kategori": "5. Dessert", "Nama Bahan / Menu": "Bahan Pastry & Plating Dessert", "Total Harga Beli (NT$)": 3000, "Bisa Buat Berapa Porsi": 100},
    {"Kategori": "6. Beverage (Pilih 1)", "Nama Bahan / Menu": " Bahan Signature Drink", "Total Harga Beli (NT$)": 2000, "Bisa Buat Berapa Porsi": 100},
])

edited_df = st.data_editor(
    default_ingredients,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Kategori": st.column_config.SelectboxColumn(
            "Kategori Set Menu",
            options=[
                "1. Appetizer",
                "2. Salad",
                "3. Soup",
                "4. Main Course",
                "5. Dessert",
                "6. Beverage (Pilih 1)"
            ],
            required=True
        ),
        "Nama Bahan / Menu": st.column_config.TextColumn("Nama Bahan / Menu", required=True),
        "Total Harga Beli (NT$)": st.column_config.NumberColumn("Total Harga Beli (NT$)", min_value=0, step=100, required=True),
        "Bisa Buat Berapa Porsi": st.column_config.NumberColumn("Bisa Buat Berapa Porsi", min_value=1, step=1, required=True),
    }
)

# Hitung modal per 1 porsi untuk tiap baris
edited_df["Modal per 1 Porsi (NT$)"] = (
    edited_df["Total Harga Beli (NT$)"] / edited_df["Bisa Buat Berapa Porsi"]
).round(1)

# Ringkasan modal per kategori & kapasitas maksimal set menu
total_belanja_semua_bahan = float(edited_df["Total Harga Beli (NT$)"].sum())
food_cost_per_set = float(edited_df["Modal per 1 Porsi (NT$)"].sum())
max_set_tersedia = int(edited_df["Bisa Buat Berapa Porsi"].min()) if not edited_df.empty else 0

with st.expander("📋 Lihat Rincian Modal Bahan (HPP) per Porsi", expanded=False):
    st.dataframe(edited_df, use_container_width=True)

st.divider()

# ==========================================
# LANGKAH 2: SARAN HARGA & INPUT TARGET PENJUALAN
# ==========================================
st.subheader("2️⃣ Rekomendasi Harga & Input Target Pelanggan")

# Perhitungan saran harga Food Cost 25% - 30%
rekomendasi_harga_30 = round(food_cost_per_set / 0.30) if food_cost_per_set > 0 else 0
rekomendasi_harga_25 = round(food_cost_per_set / 0.25) if food_cost_per_set > 0 else 0

st.info(
    f"💡 **Saran Harga Jual Ideal (Target Food Cost 25% – 30%):**\n"
    f"- Modal bahan 1 Set Menu lengkap saat ini adalah **NT$ {food_cost_per_set:,.1f}**.\n"
    f"- Agar **Food Cost berada di angka 30%**, patok harga minimal **NT$ {rekomendasi_harga_30:,} / set**.\n"
    f"- Agar **Food Cost berada di angka 25%** (margin lebih aman), patok harga **NT$ {rekomendasi_harga_25:,} / set**."
)

col_in1, col_in2 = st.columns(2)
with col_in1:
    harga_jual_set = st.number_input(
        "Harga Jual 1 Set Menu yang Dipatok (NT$)",
        min_value=50,
        max_value=20000,
        value=800,
        step=50
    )
with col_in2:
    jumlah_pelanggan = st.number_input(
        "Jumlah Pelanggan / Tamu yang Datang (Orang)",
        min_value=1,
        max_value=2000,
        value=100,
        step=5
    )

st.divider()

# ==========================================
# LANGKAH 3: HASIL KEUNTUNGAN & KERUGIAN (MODE PRAKTEK SEKOLAH)
# ==========================================
st.subheader("3️⃣ Hasil Simulasi Untung / Rugi (Mode Tugas Praktek)")
st.caption("Perhitungan khusus tugas praktek sekolah (tanpa beban gaji karyawan, sewa tempat, dan listrik).")

# Cek apakah stok cukup untuk jumlah pelanggan
porsi_terjual = min(jumlah_pelanggan, max_set_tersedia)
kekurangan_porsi = max(0, jumlah_pelanggan - max_set_tersedia)
sisa_porsi = max(0, max_set_tersedia - jumlah_pelanggan)

# Hitung metrik per 1 set
untung_kotor_per_set = harga_jual_set - food_cost_per_set
persen_food_cost_aktual = (food_cost_per_set / harga_jual_set) * 100 if harga_jual_set > 0 else 0

# Hitung metrik total praktek
total_pendapatan = porsi_terjual * harga_jual_set
total_modal_terpakai = porsi_terjual * food_cost_per_set
untung_berdasarkan_porsi = total_pendapatan - total_modal_terpakai
untung_rugi_kas_praktek = total_pendapatan - total_belanja_semua_bahan

m1, m2, m3, m4 = st.columns(4)
m1.metric("Modal Bahan 1 Set (HPP)", f"NT$ {food_cost_per_set:,.0f}", f"Food Cost: {persen_food_cost_aktual:.1f}%")
m2.metric("Keuntungan per 1 Set", f"NT$ {untung_kotor_per_set:,.0f}", "Harga Jual - Modal 1 Set")
m3.metric("Total Pendapatan (Revenue)", f"NT$ {total_pendapatan:,}", f"Dari {porsi_terjual} Tamu Terlayani")
m4.metric(
    "Untung / Rugi Bersih Praktek",
    f"NT$ {untung_rugi_kas_praktek:,.0f}",
    f"Total Belanja Bahan: NT$ {total_belanja_semua_bahan:,.0f}"
)

# Peringatan stok dan status untung/rugi praktek
if kekurangan_porsi > 0:
    st.error(
        f"⚠️ **Stok Bahan Kurang!** Stok bahanmu maksimal hanya cukup untuk **{max_set_tersedia} set**, "
        f"sedangkan ada **{jumlah_pelanggan} tamu** (kurang **{kekurangan_porsi} set**). Naikkan jumlah porsi belanja di tabel atas."
    )
elif sisa_porsi > 0:
    st.warning(
        f"📦 **Ada Sisa Stok Bahan:** Dari kapasitas **{max_set_tersedia} set**, terjual **{porsi_terjual} set** "
        f"(tersisa bahan untuk **{sisa_porsi} set**)."
    )

if untung_rugi_kas_praktek >= 0:
    st.success(
        f"✅ **STATUS PRAKTEK UNTUNG:** Setelah seluruh biaya belanja bahan (**NT$ {total_belanja_semua_bahan:,.0f}**) "
        f"dibayar lunas dari hasil penjualan, tim kamu mendapatkan keuntungan bersih **NT$ {untung_rugi_kas_praktek:,.0f}**."
    )
else:
    st.error(
        f"❌ **STATUS PRAKTEK RUGI:** Pendapatan (**NT$ {total_pendapatan:,}**) belum menutup total uang belanja bahan "
        f"(**NT$ {total_belanja_semua_bahan:,.0f}**). Masih minus/rugi sebesar **NT$ {abs(untung_rugi_kas_praktek):,.0f}**."
    )

st.divider()

# ==========================================
# LANGKAH 4 (OPSIONAL): SIMULASI RESTORAN KOMERSIAL NYATA (100%)
# ==========================================
with st.expander("🏢 Opsional: Simulasi Biaya Operasional Restoran Nyata (Struktur Biaya 100%)", expanded=True):
    st.markdown(
        "Bagian ini **tidak wajib dibayar saat tugas praktek sekolah**, namun ditampilkan secara terpisah sebagai "
        "simulasi jika restoran beroperasi secara komersial dengan rincian struktur biaya standar industri:"
    )

    # Perhitungan Komponen Biaya Komersial dari Total Pendapatan
    biaya_labor_30 = total_pendapatan * 0.30
    biaya_rent_12 = total_pendapatan * 0.12
    biaya_other_13 = total_pendapatan * 0.13
    target_profit_10 = total_pendapatan * 0.10

    total_biaya_operasional_non_bahan = biaya_labor_30 + biaya_rent_12 + biaya_other_13
    total_seluruh_pengeluaran_komersial = total_belanja_semua_bahan + total_biaya_operasional_non_bahan
    untung_rugi_komersial_nyata = total_pendapatan - total_seluruh_pengeluaran_komersial

    c_op1, c_op2, c_op3, c_op4 = st.columns(4)
    c_op1.metric("Labor Cost (30%)", f"NT$ {biaya_labor_30:,.0f}", "Gaji Chef & Server")
    c_op2.metric("Rent & Utilities (12%)", f"NT$ {biaya_rent_12:,.0f}", "Sewa, Listrik, Air, Gas")
    c_op3.metric("Other Expenses (13%)", f"NT$ {biaya_other_13:,.0f}", "Marketing, Kemasan, dll")
    c_op4.metric("Target Net Profit (10%)", f"NT$ {target_profit_10:,.0f}", "Target Laba Ideal")

    st.markdown("**Ringkasan Untung / Rugi Jika Membayar Biaya Komersial Lengkap:**")
    tabel_komersial = pd.DataFrame([
        {"Komponen Biaya / Pendapatan": "Total Pendapatan Penjualan (100%)", "Persentase Aktual": "100.0%", "Nominal (NT$)": round(total_pendapatan)},
        {"Komponen Biaya / Pendapatan": "Total Belanja Bahan Makanan (Food Cost)", "Persentase Aktual": f"{(total_belanja_semua_bahan / total_pendapatan * 100) if total_pendapatan > 0 else 0:.1f}%", "Nominal (NT$)": -round(total_belanja_semua_bahan)},
        {"Komponen Biaya / Pendapatan": "Biaya Gaji Karyawan (Labor Cost 30%)", "Persentase Aktual": "30.0%", "Nominal (NT$)": -round(biaya_labor_30)},
        {"Komponen Biaya / Pendapatan": "Biaya Sewa & Utilitas (Rent & Utilities 12%)", "Persentase Aktual": "12.0%", "Nominal (NT$)": -round(biaya_rent_12)},
        {"Komponen Biaya / Pendapatan": "Biaya Lain-lain (Other Expenses 13%)", "Persentase Aktual": "13.0%", "Nominal (NT$)": -round(biaya_other_13)},
        {"Komponen Biaya / Pendapatan": "LABA / RUGI BERSIH KOMERSIAL (NET PROFIT/LOSS)", "Persentase Aktual": f"{(untung_rugi_komersial_nyata / total_pendapatan * 100) if total_pendapatan > 0 else 0:.1f}%", "Nominal (NT$)": round(untung_rugi_komersial_nyata)},
    ])
    st.table(tabel_komersial)

    if untung_rugi_komersial_nyata >= target_profit_10:
        st.success(
            f"🌟 **Sangat Layak Bisnis:** Bahkan setelah dikurangi gaji (30%), sewa (12%), dan biaya lain (13%), "
            f"restoran masih mencatat keuntungan bersih **NT$ {untung_rugi_komersial_nyata:,.0f}** "
            f"(melampaui target Net Profit 10% sebesar NT$ {target_profit_10:,.0f})."
        )
    elif untung_rugi_komersial_nyata >= 0:
        st.info(
            f"⚖️ **Masih Untung Tipis:** Restoran mencatat laba bersih **NT$ {untung_rugi_komersial_nyata:,.0f}**, "
            f"namun belum mencapai target ideal 10% (**NT$ {target_profit_10:,.0f}**). Coba tekan Food Cost ke 25%–30%."
        )
    else:
        st.warning(
            f"📉 **Catatan Evaluasi Komersial:** Jika harus membayar biaya sewa dan gaji penuh, skenario ini masih mengalami "
            f"kerugian **NT$ {abs(untung_rugi_komersial_nyata):,.0f}** karena persentase biaya bahan atau sisa stok masih terlalu tinggi."
        )
