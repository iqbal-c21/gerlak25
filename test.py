import altair as alt
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Demo Dashboard", layout="wide")

st.title(":first_quarter_moon: Black Zetsu : 2025 Insights")
st.subheader("📊 Performance summarry", divider=True)


# tampilan side bar

menu = st.sidebar.radio("The Big Screen:",[
    "Non Pump Mates",
    "Pump Mates",
    "Total"
],
captions = [
    "semua produk lokal",
    "semua produk import",
    "semua produk import dan lokal",
]
)

# tampilan tengah ketika medu di klik
df = pd.read_csv("data.csv")
summary = df.groupby("supplier").agg(
    total_sales=("Penjualan", "sum"),
    total_qty=("Jumlah", "sum"),
    n_products=("Nama Produk", "nunique")
).reset_index()

#df1 = pd.read_csv("data1.csv")
#df1 = df1.reset_index(drop=True)  # pastikan kolom 'Bulan' muncul
df1 = (
    df.groupby(by=["Bulan", "supplier"], as_index=False)
       .agg(
           total_sales=("Penjualan", "sum"),
           total_qty=("Jumlah", "sum"),
               )
)
if menu == "Total":
    st.subheader("Distribusi Penjualan Pump Mates dan non-Pump Mates")
    col1,col2,col3 = st.columns(3)
    with col1:
        summary["label"] = summary.apply(lambda x: f"{x['supplier']} - Rp {x['total_sales']:,.0f}".replace(",", "."), axis=1)
        fig = px.pie(summary, values='total_sales', names='label', title='Distribusi Penjualan import dan local')
        st.plotly_chart(fig, use_container_width=True)
        st.caption("total penjualan dari supplier lokal dan import sepanjang 2025")

    with col2:
        summary["label"] = summary.apply(lambda x: f"{x['supplier']} - {x['total_qty']:,.0f}".replace(",", "."), axis=1)
        fig = px.pie(summary, values='total_qty', names='label', title='Distribusi qty import dan local')
        st.plotly_chart(fig, use_container_width=True)
        st.caption("total quantity terjual dari semua produk sepanjang tahun 2025")

    with col3:
        summary["label"] = summary.apply(lambda x: f"{x['supplier']} -  {x['n_products']:,.0f}".replace(",", "."), axis=1)
        fig = px.pie(summary, values='n_products', names='label', title='Distribusi n_products import dan local')
        st.plotly_chart(fig, use_container_width=True)
        st.caption("total variasi produk yang terjual sepanjang 2025")

    with st.container():

        fig = px.line(
            df1,
            x='Bulan',
            y='total_sales',
            color='supplier',
            markers=True , # Titik per data point
            title="Penjualan produk 2 supplier"
        )

        st.plotly_chart(fig)
        st.caption("Perbandingan penjualan 2025 semua produk yang berasal dari lokal dan impor")

    with st.container():

        fig = px.line(
            df1,
            x='Bulan',
            y='total_qty',
            color='supplier',
            markers=True , # Titik per data point
            title="Qty terjual berdasarkan lokal dan import"
        )

        st.plotly_chart(fig)
        st.caption("Perbandingan jumlah qty produk yang bberasal dari sumber lokal dan import")

    with st.expander("See dataframe"):
        st.write('source')
        st.dataframe(df1)

if menu == "Pump Mates":
    st.title("Let's dive in to Pump Mates")

    data_import = df[df["supplier"] == "import"]
    impor_sales = data_import.groupby(by="Bulan", as_index=False)["Penjualan"].sum()
    impor_qty = data_import.groupby(by="Bulan", as_index=False)["Jumlah"].sum()


    pm_ranks_sales = data_import.groupby("Nama Variasi")["Penjualan"].sum().nlargest(50)
    pm_ranks_qty = data_import.groupby('Nama Variasi')['Jumlah'].sum().nlargest(50)

    # Checkbox pertama
    monthly_sales = st.checkbox("Penjualan Pump Mates sepanjang 2025")
    if monthly_sales:
        st.line_chart(impor_sales[["Bulan", "Penjualan"]], x="Bulan", y="Penjualan")

    # Checkbox kedua
    monthly_qty = st.checkbox("Qty terjual Pump Mates sepanjang 2025")

    if monthly_qty:
        st.line_chart(impor_qty[["Bulan", "Jumlah"]], x="Bulan", y="Jumlah")

    # checkbox ketiga
    ranks_sales = st.checkbox("Peringkat produk Pump Mates berdasarkan sales")

    if ranks_sales:
        # altair
        df_chart = pm_ranks_sales.reset_index()
        df_chart.columns = ["Nama Variasi", "Penjualan"]  # rename eksplisit

        # Buat chart dengan data diset di Chart(df_chart) ✅
        chart = (
            alt.Chart(df_chart)  # <-- ini wajib ada!
            .mark_bar()
            .encode(
                x=alt.X("Penjualan:Q"),
                y=alt.Y("Nama Variasi:N", sort='-x'),  # type N (nominal)
                tooltip=["Nama Variasi", "Penjualan"]
            )
            .properties(width=800, height=1200)
            .configure_axis(labelLimit=500)
        )

        st.altair_chart(chart, use_container_width=True)


         # checkbox ke 4
    ranks_qty = st.checkbox("Peringkat produk Pump Mates berdasar qty terjual")
    if ranks_qty:
        # altair
        df_chart = pm_ranks_qty.reset_index()
        df_chart.columns = ["Nama Variasi", "Jumlah"]  # rename eksplisit

        # Buat chart dengan data diset di Chart(df_chart) ✅
        chart = (
            alt.Chart(df_chart)  # <-- ini wajib ada!
            .mark_bar()
            .encode(
                x=alt.X("Jumlah:Q"),
                y=alt.Y("Nama Variasi:N", sort='-x'),  # type N (nominal)
                tooltip=["Nama Variasi", "Jumlah"]
            )
            .properties(width=800, height=1200)
            .configure_axis(labelLimit=500)
        )

        st.altair_chart(chart, use_container_width=True)
        with st.expander("See Dataframe", width=400):
          st.dataframe(pm_ranks_qty)

    option = st.selectbox("Top 30 Pump Mates monthly:", ["colostrum collector",
                                                 "nipple ruller",
                                                 "backflow membran",
                                                 "selang biasa",
                                                 "insert std",
                                                 "tutup corong 85mm",
                                                 "valve",
                                                 "box&brush",
                                                 "adapter kantong asi",
                                                 "cushion ins",
                                                 "flange connector",
                                                 "oval flange",
                                                 "comfort cushion",
                                                 "cushion 28mm",
                                                 "petal pad",
                                                 "silicone pad",
                                                 "silicone bag",
                                                "aids"
                                                 ])

    def create_df(tipe): # fungsi membuat data frame untuk altair
      df_filtered = data_import[data_import["Nama Variasi"].str.contains(tipe, na=False)]
      df_grouped = df_filtered.groupby(by=["Bulan", "Nama Variasi"], as_index=False)["Jumlah"].sum()
      return df_grouped

    def create_chart(df):
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x='Bulan:N',
                y=alt.Y('Jumlah:Q'),  # sudah sort descending
                tooltip=['Nama Variasi', 'Jumlah'],
                color='Nama Variasi:N'
            )
            .properties(
                width=800,
                height=800
            )
            .configure_axis(
                labelLimit=500)  # supaya teks tidak terpotong
        )

        st.altair_chart(chart, use_container_width=True)


    # Tampilkan grafik sesuai pilihan
    if option == "colostrum collector":

        df_colostrum = create_df("Colostrum")
        create_chart(df_colostrum)

    elif option == "nipple ruller":
        df_RULER = create_df("RULER")
        create_chart(df_RULER)

    elif option == "backflow membran":
        df_bf = create_df("Membrane|BF")
        create_chart(df_bf)

    elif option == "selang biasa":
        df_selang = create_df("Selang Biasa")
        create_chart(df_selang)

    elif option == "insert std":
        ins = data_import[data_import["Nama Variasi"].str.contains("Insert", na=False)]
        data_ins = ins.groupby(by=["Bulan", "Nama Variasi"], as_index=False)["Jumlah"].sum()
        #data_ins = data_ins.reset_index()

        import re

        def normalize_variation(name):
            # Check if the input is a string before applying string methods
            if isinstance(name, str):
                # ambil angka sebelum "mm"
                match = re.search(r'(\d+)\s*mm', name.lower())
                if match:
                    size = match.group(1)  # ambil angkanya
                    return f"PM Insert std {size}mm"
            return name  # return the original value if not a string or no match

        data_ins["Nama Variasi Normalized"] = data_ins["Nama Variasi"].apply(normalize_variation)



        chart = (
        alt.Chart(data_ins)
        .mark_bar()
        .encode(
            x='Bulan:N',
            y=alt.Y('Jumlah:Q'),  # sudah sort descending
            tooltip=['Nama Variasi Normalized', 'Jumlah'],
            color='Nama Variasi Normalized:N'
        )
        .properties(
            width=800,
            height=800
        )
        .configure_axis(
            labelLimit=500)  # supaya teks tidak terpotong
    )

        st.altair_chart(chart, use_container_width=True)


    elif option == "valve":
       df_valve = create_df("VALVE|valve|Valve")
       create_chart(df_valve)

    elif option == "tutup corong 85mm":
        df_85 = create_df("TUTUP CORONG 85mm")
        create_chart(df_85)

    elif option == "box&brush":
        df_box = create_df("PM Box & Brush")
        create_chart(df_box)

    elif option == "adapter kantong asi":
        df_adapter = create_df("Konektor K. ASI")
        create_chart(df_adapter)

    elif option == "cushion ins":
        df_cushion = create_df("Cushion INS")
        create_chart(df_cushion)

    elif option == "flange connector":
        df_fcon = create_df("FLANGE CONNECTOR")
        create_chart(df_fcon)

    elif option == "oval flange":
        df_ovalf = create_df("OVAL FLANGE")
        create_chart(df_ovalf)

    elif option == "comfort cushion":
        df_comfort = create_df("Comfort")
        create_chart(df_comfort)

    elif option == "cushion 28mm":
        df_cushion28mm = create_df("CUSHION")
        create_chart(df_cushion28mm)

    elif option == "petal pad":
        df_petalPad = create_df("PETAL PAD")
        create_chart(df_petalPad)

    elif option == "silicone pad":
        df_siliPad = create_df("Pad Silicone")
        create_chart(df_siliPad)

    elif option == "silicone bag":
        df_siliBag = create_df("Silbag|SilBag")
        create_chart(df_siliBag)

    elif option == "aids":
        df_aids = create_df("SNS")
        create_chart(df_aids)

if menu == "Non Pump Mates":
    st.title("Let's dive in to Non Pump Mates")
    # tidak mengandung "Pump Mates" (case-insensitive), NaN dianggap TIDAK match
    df_nonpm = df[~df["Nama Produk"].str.contains("Pump Mates", case=False, na=False)]
    st.dataframe(df_nonpm)

    nonpm_sales =df_nonpm.groupby("Bulan").agg(
        total_sales=("Penjualan", "sum"),
        total_qty=("Jumlah", "sum"))

    nonpm_qty = df_nonpm.groupby("Bulan").agg(
        total_qty=("Jumlah", "sum"))

    nonpm_ranks_sales = df_nonpm.groupby("Nama Variasi")["Penjualan"].sum().nlargest(30)
    nonpm_ranks_qty = df_nonpm.groupby('Nama Variasi')['Jumlah'].sum().nlargest(30)

    # Checkbox pertama
    monthly_sales = st.checkbox("Penjualan non Pump Mates sepanjang 2025")

    if monthly_sales:
        st.line_chart(nonpm_sales)

    # Checkbox keduaa
    monthly_qty = st.checkbox("Qty non Pump Mates sepanjang 2025")
    if monthly_qty:
        st.line_chart(nonpm_qty)

    # checkbox ketiga
    ranks_sales = st.checkbox("Peringkat produk non Pump Mates berdasarkan sales")

    if ranks_sales:
        # altair
        df_chart = nonpm_ranks_sales.reset_index()
        df_chart.columns = ["Nama Variasi", "Penjualan"]  # rename eksplisit

        # Buat chart dengan data diset di Chart(df_chart) ✅
        chart = (
            alt.Chart(df_chart)  # <-- ini wajib ada!
            .mark_bar()
            .encode(
                x=alt.X("Penjualan:Q"),
                y=alt.Y("Nama Variasi:N", sort='-x'),  # type N (nominal)
                tooltip=["Nama Variasi", "Penjualan"]
            )
            .properties(width=800, height=1000)
            .configure_axis(labelLimit=500)
        )

        st.altair_chart(chart, use_container_width=True)
        with st.expander("See Dataframe", width=400):
          st.dataframe(nonpm_ranks_sales)

    # checkbox ke4
    ranks_qty = st.checkbox("Peringkat produk non Pump Mates berdasarkan Qty")

    if ranks_qty:
        # altair
        df_chart = nonpm_ranks_qty.reset_index()
        df_chart.columns = ["Nama Variasi", "Jumlah"]  # rename eksplisit

        # Buat chart dengan data diset di Chart(df_chart) ✅
        chart = (
            alt.Chart(df_chart)  # <-- ini wajib ada!
            .mark_bar()
            .encode(
                x=alt.X("Jumlah:Q"),
                y=alt.Y("Nama Variasi:N", sort='-x'),  # type N (nominal)
                tooltip=["Nama Variasi", "Jumlah"]
            )
            .properties(width=800, height=1000)
            .configure_axis(labelLimit=500)
        )

        st.altair_chart(chart, use_container_width=True)
        with st.expander("See Dataframe", width=400):
            st.dataframe(nonpm_ranks_qty)


