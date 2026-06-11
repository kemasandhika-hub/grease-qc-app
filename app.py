
import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Grease Colour QC System")

# ===== INPUT (UPLOAD + CAMERA) =====
st.subheader("Input Sample")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
camera_file = st.camera_input("Or take a picture")

# pilih input yang digunakan
image_file = None
if camera_file is not None:
    image_file = camera_file
elif uploaded_file is not None:
    image_file = uploaded_file

# ===== REFERENCE =====
ref = np.array([62.63, 132.01, 140.79])
threshold = 6  # gunakan nilai hasil kamu

# ===== PROCESS =====
if image_file is not None:
    image = Image.open(image_file)
    st.image(image, caption="Sample", use_container_width=True)

    # convert ke numpy
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    h, w, _ = img.shape

    # crop tengah (fokus grease)
    crop = img[h//2-50:h//2+50, w//2-50:w//2+50]

    # convert ke LAB
    lab = cv2.cvtColor(crop, cv2.COLOR_BGR2LAB)
    avg = np.mean(lab.reshape(-1,3), axis=0)

    # ✅ hanya A & B (tidak sensitif lighting)
    delta = np.linalg.norm(avg[1:] - ref[1:])

    # ===== OUTPUT =====
    st.subheader("Result")

    st.write("LAB Value:", avg)
    st.write("Delta (A,B only):", delta)

    if delta < threshold:
        st.success("✅ ON SPEC")
    else:
        st.error("❌ OFF SPEC")