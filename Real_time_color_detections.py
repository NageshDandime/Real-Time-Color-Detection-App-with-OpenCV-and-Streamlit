import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="🎨 Color Detection", layout="wide")
st.title("🎨 Real-Time Color Detection with HSV Range Sliders ---By Nagesh ")

# ............................................................Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("❌ Could not open webcam.")
else:
    st.success("✅ Webcam initialized successfully.")

#..............................................................HSV sliders
st.sidebar.header("🎛️ HSV Range Controls")

col1, col2 = st.sidebar.columns(2)

with col1:
    h_min = st.slider("Hue Min", 0, 179, 0)
    s_min = st.slider("Sat Min", 0, 255, 0)
    v_min = st.slider("Val Min", 0, 255, 0)
with col2:
    h_max = st.slider("Hue Max", 0, 179, 179)
    s_max = st.slider("Sat Max", 0, 255, 255)
    v_max = st.slider("Val Max", 0, 255, 255)

capture = st.button("📸 Capture Frame")

frame_placeholder = st.empty()
mask_placeholder = st.empty()
result_placeholder = st.empty()

if capture:
    ret, frame = cap.read()
    if ret:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #............................................................. Create HSV range
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        #.............................................................Mask and result
        mask = cv2.inRange(hsv_frame, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        #............................................................. Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        #............................................................... Display
        frame_placeholder.image(frame_rgb, channels="RGB", caption="Original Frame")
        mask_placeholder.image(mask, channels="GRAY", caption="Mask")
        result_placeholder.image(result_rgb, channels="RGB", caption="Detected Color")
    else:
        st.error("Failed to capture frame.")

cap.release()
