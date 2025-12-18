import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Metro Ticket Booking", layout="centered")

st.title("🚆 Metro Ticket & Cab Booking")

st.divider()

# Station list in correct order
stations = ["Balanagar", "Kukatpally", "KPHB", "JNTU", "Nizampet", "Miyapur"]

with st.container():
    st.subheader("Passenger Information")
    name = st.text_input("Full Name")

st.divider()

with st.container():
    st.subheader("Journey Details")

    col1, col2 = st.columns(2)
    with col1:
        from_station = st.selectbox("From Station", stations)
    with col2:
        to_station = st.selectbox("To Station", stations)

    tickets = st.number_input("Number of Tickets", min_value=1, step=1)

st.divider()

with st.container():
    st.subheader("Cab Requirement")

    need_cab = st.radio("Do you need a cab after reaching?", ["Yes", "No"], horizontal=True)

    cab_type = None
    drop_location = None

    if need_cab == "Yes":
        col3, col4 = st.columns(2)
        with col3:
            cab_type = st.selectbox("Select Cab Type", ["supercar","Sedan", "SUV", "Auto", "Mini"])
        with col4:
            drop_location = st.text_input("Drop Location")

st.divider()

# BOOKING BUTTON
if st.button("✅ Confirm Booking", use_container_width=True):

    # Calculate price
    from_index = stations.index(from_station)
    to_index = stations.index(to_station)
    station_gap = abs(to_index - from_index)
    price = station_gap * 30
    total_amount = price * tickets

    st.subheader("📄 Booking Summary")
    st.write(f"**Name:** {name}")
    st.write(f"**From:** {from_station}")
    st.write(f"**To:** {to_station}")
    st.write(f"**Stations Travelled:** {station_gap}")
    st.write(f"**Ticket Price:** ₹{price}")
    st.write(f"**Tickets:** {tickets}")
    st.write(f"**Total Amount:** ₹{total_amount}")
    st.write(f"**Cab Required:** {need_cab}")

    if need_cab == "Yes":
        st.write(f"**Cab Type:** {cab_type}")
        st.write(f"**Drop Location:** {drop_location}")

    st.divider()

    # QR Code Data
    qr_data = (
        f"Name: {name}\n"
        f"From: {from_station}\n"
        f"To: {to_station}\n"
        f"Stations: {station_gap}\n"
        f"Price: ₹{price}\n"
        f"Tickets: {tickets}\n"
        f"Total: ₹{total_amount}\n"
        f"Cab: {need_cab}"
    )

    if need_cab == "Yes":
        qr_data += f"\nCab Type: {cab_type}\nDrop Location: {drop_location}"

    # Generate QR Code
    qr = qrcode.make(qr_data)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)

    st.subheader("📱 Your QR Code")
    st.image(Image.open(buf), width=250)

    st.success("Booking Confirmed Successfully!")

