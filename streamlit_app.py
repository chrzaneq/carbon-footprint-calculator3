import streamlit as st

def calculate_carbon_footprint(diameter, length, color, mix, cap_type, cap_color, head_color, print_method, num_colors, print_method_2, num_colors_2):
    # Dane referencyjne
    base_length = 150  # Bazowa długość tuby w mm (dla której podano masy)
    mass_data = {50: 0.011, 40: 0.0075, 35: 0.0065, 30: 0.0045, 25: 0.0035, 19: 0.002}
    head_mass_data = {50: 0.0025, 40: 0.002, 35: 0.0013, 30: 0.001, 25: 0.0006, 19: 0.0005}
    mix_data = {
        "STANDARD": (50, 0, 50, 0), "SOFT": (0, 70, 30, 0), "HARD": (0, 30, 70, 0),
        "PCR 30%": (70, 0, 0, 30), "PCR 50%": (50, 0, 0, 50), "PCR 70%": (30, 0, 0, 70),
        "Sugarcane": (50, 0, 50, 0)
    }
    cap_data = {
        "50 Flip Top": 0.06256, "50 Standard screw-on": 0.04692, "40 Flip Top": 0.04692, "40 Standard screw-on": 0.03128,
        "35 Flip Top": 0.0391, "35 Standard screw-on": 0.02346, "30 Flip Top": 0.02346, "30 Standard screw-on": 0.01955,
        "25 Standard screw-on": 0.01173, "19 Standard screw-on": 0.01173, "19 Kaniula": 0.01955
    }
    color_impact = {"BIAŁA": 0, "TRANSPARENT": 0, "BARWIONA": 0.005}
    head_color_impact = {"BIAŁA": 0, "TRANSPARENT": 0, "BARWIONA": 0.0025}
    cap_color_impact = {"BIAŁA": 0, "TRANSPARENT": 0, "BARWIONA": 0.001}
    print_emission = {"Sitodruk": 0.010, "Fleksografia": 0.007, "Offset": 0.012, "brak": 0.0}

    co2_ldpe = 1.9
    co2_ll_dpe = 2.0
    co2_hdpe = 1.9
    co2_pcr = 1.0
    co2_ldpe_sugarcane = -2.12

    base_mass = mass_data.get(diameter, 0)
    adjusted_mass = base_mass * (length / base_length)
    head_mass = head_mass_data.get(diameter, 0)
    mix_values = mix_data.get(mix, (0, 0, 0, 0))
    cap_emission = cap_data.get(cap_type, 0) + cap_color_impact.get(cap_color, 0)
    print_emission_total = print_emission.get(print_method, 0) * num_colors
    print_emission_total_2 = print_emission.get(print_method_2, 0) * num_colors_2

    if mix == "Sugarcane":
        sled_weglowy_korpusu = ((mix_values[0] * co2_hdpe + mix_values[1] * co2_ll_dpe +
                                  mix_values[2] * co2_hdpe + mix_values[3] * co2_pcr +
                                  mix_values[1] * co2_ldpe_sugarcane) / 100) * adjusted_mass
    else:
        sled_weglowy_korpusu = ((mix_values[0] * co2_ldpe + mix_values[1] * co2_ll_dpe +
                                  mix_values[2] * co2_hdpe + mix_values[3] * co2_pcr) / 100) * adjusted_mass

    sled_weglowy_glowki = (head_mass * co2_hdpe)
    head_color_co2 = head_color_impact.get(head_color, 0)

    total_emission = (sled_weglowy_korpusu + sled_weglowy_glowki + cap_emission + print_emission_total +
                      print_emission_total_2 + color_impact.get(color, 0) + head_color_co2)

    return total_emission

st.title("Kalkulator Śladu Węglowego Tubki")

diameter = st.selectbox("Średnica tuby (mm)", [50, 40, 35, 30, 25, 19])
length = st.number_input("Długość tuby (mm)", min_value=50, max_value=250, value=150, step=1)
color = st.selectbox("Kolor tuby", ["BIAŁA", "TRANSPARENT", "BARWIONA"])
head_color = st.selectbox("Kolor główki", ["TRANSPARENT", "BIAŁA", "BARWIONA"])
mix = st.selectbox("Mieszanka", ["STANDARD", "SOFT", "HARD", "PCR 30%", "PCR 50%", "PCR 70%", "Sugarcane"])
cap_type = st.selectbox("Rodzaj nakrętki", ["50 Flip Top", "50 Standard screw-on", "40 Flip Top", "40 Standard screw-on",
                                           "35 Flip Top", "35 Standard screw-on", "30 Flip Top", "30 Standard screw-on",
                                           "25 Standard screw-on", "19 Standard screw-on", "19 Kaniula"])
cap_color = st.selectbox("Kolor nakrętki", ["BIAŁA", "TRANSPARENT", "BARWIONA"])
print_method = st.selectbox("Metoda nadruku", ["Sitodruk", "Fleksografia", "Offset"])
num_colors = st.number_input("Ilość kolorów", min_value=1, max_value=10, value=4, step=1)
print_method_2 = st.selectbox("Metoda nadruku 2", ["brak", "Sitodruk", "Fleksografia"])
num_colors_2 = st.number_input("Ilość kolorów (metoda 2)", min_value=0, max_value=8, value=0, step=1)

if st.button("Oblicz Ślad Węglowy"):
    total_footprint = calculate_carbon_footprint(
        diameter, length, color, mix, cap_type, cap_color,
        head_color, print_method, num_colors,
        print_method_2, num_colors_2
    )
    st.success(f"Całkowity ślad węglowy tubki: {total_footprint:.5f} kg CO₂e")

    