import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt
session = fastf1.get_session(2023, "Monaco", 'R')
session.load()
laps = session.laps
drivers = session.drivers
print(drivers)
drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
print(drivers)
stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
stints = stints.groupby(["Driver", "Stint", "Compound"])
stints = stints.count().reset_index()
stints = stints.rename(columns={"LapNumber": "StintLength"})
print(stints)
fig, ax = plt.subplots(figsize=(5, 10))
compound_colors = {compound: color for compound, color in fastf1.plotting.COMPOUND_COLORS.items()}
for driver in drivers:
    driver_stints = stints.loc[stints["Driver"] == driver]

    previous_stint_end = 0
    for idx, row in driver_stints.iterrows():
        compound = row["Compound"]
        color = compound_colors.get(compound, "gray") 
        if compound != "unknown":
            # Create the horizontal bar with the compound color
            plt.barh(
                y=driver,
                width=row["StintLength"],
                left=previous_stint_end,
                color=color,
                edgecolor="black",
                label=compound
            )

        previous_stint_end += row["StintLength"]

plt.title("2023 Monaco Grand Prix Tire Strategies")
plt.xlabel("Lap Number")
plt.grid(False)
# invert the y-axis so drivers that finish higher are closer to the top
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Create a legend outside of the loop
legend_labels = [plt.Rectangle((0, 0), 1, 1, color=compound_colors[compound]) for compound in fastf1.plotting.COMPOUND_COLORS if compound != "unknown"]
plt.legend(legend_labels, [compound for compound in fastf1.plotting.COMPOUND_COLORS if compound != "unknown"], title='Tire Compound', loc='lower right')

plt.tight_layout()
plt.show()
