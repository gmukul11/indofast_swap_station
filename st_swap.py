import streamlit as st

# ---------------- Constants ----------------
ASSUMPTIONS = {
    "2W": {
        "energy_per_swap_kWh": 1.5,
        "swaps_per_day_per_vehicle": 1.2,
    },
    "3W": {
        "energy_per_swap_kWh": 3.0,
        "swaps_per_day_per_vehicle": 1.0,
    },
    "station_operational_hours": 16,
    "charging_speed_kW": 6.0,  # kW per port
    "ports_per_station": 10
}

# ---------------- Helper Functions ----------------
def calculate_stations(vehicle_counts, utilization_pct, running_pct):
    total_energy_needed = 0
    for vehicle_type, count in vehicle_counts.items():
        if vehicle_type not in ASSUMPTIONS:
            continue
        daily_swaps = count * (running_pct / 100) * ASSUMPTIONS[vehicle_type]["swaps_per_day_per_vehicle"]
        energy_needed = daily_swaps * ASSUMPTIONS[vehicle_type]["energy_per_swap_kWh"]
        total_energy_needed += energy_needed

    effective_power_per_station = (
        ASSUMPTIONS["ports_per_station"]
        * ASSUMPTIONS["charging_speed_kW"]
        * (utilization_pct / 100)
        * (ASSUMPTIONS["station_operational_hours"] / 24)
    )

    # kWh per day per station
    station_energy_capacity_per_day = effective_power_per_station * 24

    required_stations = total_energy_needed / station_energy_capacity_per_day
    return round(required_stations, 2)


# ---------------- UI ----------------
st.title("Swap Station Requirement Calculator")

st.markdown("### 📥 Input Vehicle Counts")
vehicle_2w = st.number_input("Number of 2W Vehicles", min_value=0, value=1000)
vehicle_3w = st.number_input("Number of 3W Vehicles", min_value=0, value=500)

st.markdown("### ⚙️ Station Parameters")
utilization = st.slider("Station Utilization (%)", 10, 100, 80)
running_pct = st.slider("Percentage of Vehicles Running Daily (%)", 10, 100, 70)

# Button Actions
if st.button("Calculate"):
    vehicle_data = {"2W": vehicle_2w, "3W": vehicle_3w}
    required_stations = calculate_stations(vehicle_data, utilization, running_pct)
    st.success(f"✅ Estimated Swap Stations Required: **{required_stations}**")

if st.button("View Assumptions"):
    st.markdown("### 🔍 Assumptions Used")
    st.json(ASSUMPTIONS)
