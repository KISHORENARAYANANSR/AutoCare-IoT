import random


def generate_ev_data():
    # Use weighted probabilities to simulate mostly normal values
    motor_temp = random.choices(
        population=[random.randint(30, 90), random.randint(91, 100)],
        weights=[0.95, 0.05],  # 95% chance normal, 5% chance high
        k=1
    )[0]

    soc = random.choices(
        population=[random.randint(10, 100), random.randint(0, 9)],
        weights=[0.95, 0.05],  # 95% chance normal, 5% chance low
        k=1
    )[0]

    battery_health = random.choices(
        population=[random.randint(75, 100), random.randint(70, 74)],
        weights=[0.95, 0.05],  # 95% chance normal, 5% chance low
        k=1
    )[0]

    dtc = random.choices(
        population=["", "BMS_ERROR", "OVERTEMP", "LOW_SOC", "INVERTER_FAULT"],
        weights=[0.85, 0.05, 0.03, 0.05, 0.02],  # Mostly no DTC
        k=1
    )[0]

    return {
        "speed": random.randint(0, 140),
        "battery_voltage": round(random.uniform(300, 420), 2),
        "soc": soc,
        "motor_temp": motor_temp,
        "battery_health": battery_health,
        "regen_braking": random.choice([True, False]),
        "dtc": dtc,
    }
