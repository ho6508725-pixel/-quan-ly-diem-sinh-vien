import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="📚",
    layout="wide"
)

# 1. Tạo dữ liệu 10 sinh viên
data = {
    "Ho_ten": [
        "An", "Binh", "Chi", "Dung", "Ha",
        "Lan", "Minh", "Nam", "Phuc", "Trang"
    ],
    "Chuyen_can": [8, 9, 7, 10, 8, 6, 9, 7, 8, 10],
    "Giua_ky":    [7, 8, 6, 9, 8, 5, 9, 7, 8, 9],
    "Cuoi_ky":    [8, 8, 7, 9, 7, 6, 8, 8, 9, 10]
}

df = pd.DataFrame(data)

# 2. Tính điểm tổng kết
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# 3. Xếp loại sinh viên
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 4. Tiêu đề và bảng điểm
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.subheader("Bảng điểm của lớp")

st.dataframe(
    df.rename(columns={
        "Ho_ten": "Họ tên",
        "Chuyen_can": "Chuyên cần",
        "Giua_ky": "Giữa kỳ",
        "Cuoi_ky": "Cuối kỳ",
        "Tong_ket": "Tổng kết",
        "Xep_loai": "Xếp loại"
    }),
    use_container_width=True,
    hide_index=True
)

# 5. Thống kê
st.subheader("Thống kê kết quả học tập")

diem_tb = df["Tong_ket"].mean()
cao_nhat = df.loc[df["Tong_ket"].idxmax()]
thap_nhat = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5).sum()

c1, c2 = st.columns(2)

with c1:
    st.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
    st.write(
        f"**Điểm cao nhất:** {cao_nhat['Ho_ten']} "
        f"({cao_nhat['Tong_ket']})"
    )

with c2:
    st.metric("Số sinh viên đạt từ 5 điểm", f"{so_sv_dat}/10")
    st.write(
        f"**Điểm thấp nhất:** {thap_nhat['Ho_ten']} "
        f"({thap_nhat['Tong_ket']})"
    )

# 6. Chọn sinh viên và xem điểm chi tiết
st.subheader("Tra cứu điểm từng sinh viên")

ten_sv = st.selectbox(
    "Chọn sinh viên:",
    df["Ho_ten"].tolist()
)

sv = df[df["Ho_ten"] == ten_sv].iloc[0]

st.write(f"**Họ tên:** {sv['Ho_ten']}")
st.write(f"**Điểm chuyên cần:** {sv['Chuyen_can']}")
st.write(f"**Điểm giữa kỳ:** {sv['Giua_ky']}")
st.write(f"**Điểm cuối kỳ:** {sv['Cuoi_ky']}")
st.write(f"**Điểm tổng kết:** {sv['Tong_ket']}")
st.write(f"**Xếp loại:** {sv['Xep_loai']}")

# 7. Biểu đồ điểm tổng kết
st.subheader("Biểu đồ điểm tổng kết của 10 sinh viên")

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(df["Ho_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Tên sinh viên")
ax.set_xlim(0, 10)
ax.invert_yaxis()
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# 8. Thông tin người thực hiện
st.divider()
st.caption("Người thực hiện: Hồ Nhất Huy - 054208001202")
