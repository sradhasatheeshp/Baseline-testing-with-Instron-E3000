 #5.1 code snippets
 #5.1.1 German standards to English standards
 import pandas as pd
 column_translation = {
 "Gesamtzeit (s)": "Total time (s)",
 "Verstrichene Zykluszeit (s)": "Elapsed cycle time (s)",
 "Gesamtzyklen": "Total cycles",
 "Verstrichene Zyklen": "Elapsed cycles",
 "Schritt": "Step",
 "Gesamtzyklenzahl(Linear Wellenform)":
 "Total cycle count (Linear waveform)",
 "Position des Aktuators (mm)": "Actuator position (mm)",
 "Kraft (N)": "Force (N)",
 "Spannung (MPa)": "Stress (MPa)",
 "Digitale Position (mm)": "Digital position (mm)",
 "Temperatur (C)": "Temperature (C)"
 }
 file_path = ’Test1.steps.tracking.csv’ # change if different
 df = pd.read_csv(file_path, delimiter=’;’, decimal=’,’)
 df.rename(columns=column_translation, inplace=True)
 output_path = "Test1.steps.tracking_converted.csv"
 df.to_csv(output_path, index=False, sep=’;’, decimal=’.’)
 print("Converted and saved:", output_path)
 21
pd.set_option(’display.max_rows’, None)
 pd.set_option(’display.max_columns’, None)
 #5.1.2 Data Interpretation
 import pandas as pd
 import os
 import re
 def extract_summary_from_file(file_path):
 filename = os.path.basename(file_path)
 specimen_number = int(re.search(r’\d+’, filename).group())
 if file_path.endswith(".csv"):
 df = pd.read_csv(file_path, delimiter=’;’)
 df = df.applymap(lambda x: str(x).replace(’,’, ’.’)
 if isinstance(x, str) else x)
 df = df.apply(pd.to_numeric, errors=’ignore’)
 df.columns = [col.strip() for col in df.columns]
 df.rename(columns={
 "Gesamtzeit (s)": "Total time (s)",
 "Gesamtzyklen": "Total cycles",
 "Position des Aktuators (mm)": "Actuator position (mm)",
 "Kraft (N)": "Force (N)"
 }, inplace=True)
 else:
 df = pd.read_excel(file_path)
 df.columns = [col.strip() for col in df.columns]
 total_records = len(df)
 start_time = df["Total time (s)"].min()
 end_time = df["Total time (s)"].max()
 duration = end_time- start_time
 max_elapsed_cycles = df["Total cycles"].max()
 min_force = df["Force (N)"].min()
 max_force = df["Force (N)"].max()
 relative_force = df["Force (N)"]- df["Force (N)"].iloc[0]
 max_relative_force = relative_force.abs().max()
 displacement = df["Actuator position (mm)"]
 relative_displacement = displacement- displacement.iloc[0]
 max_relative_displacement = relative_displacement.abs().max()
return {
 "Specimen": specimen_number,
 "Total Records": total_records,
 "Max Elapsed Cycles": max_elapsed_cycles,
 "Start Time (s)": start_time,
 "End Time (s)": end_time,
 "Duration (s)": duration,
 "Min Force (N)": min_force,
 "Max Force (N)": max_force,
 "Max Relative Force (N)": max_relative_force,
 "Max Relative Displacement (mm)": max_relative_displacement
 }
 def process_files(file_paths):
 summary_list = []
 for file_path in file_paths:
 try:
 summary = extract_summary_from_file(file_path)
 summary_list.append(summary)
 except Exception as e:
 print(f"Error processing {file_path}: {e}")
 summary_df = pd.DataFrame(summary_list)
 summary_df.sort_values("Specimen", inplace=True)
 summary_df.to_excel("summary0.92_2_output.xlsx", index=False)
 print(" Summary saved to ’summary0.092_2_output.xlsx’")
 return summary_df
 file_list = ["/content/30.xlsx"]
 summary = process_files(file_list)
 display(summary)
 #5.1.3 Maximum force per specimen
 plt.figure(figsize=(10, 6))
 plt.bar(df_05_2[’Specimen’], df_05_2[’Max Force (N)’])
 plt.xlabel(’Specimen’)
 plt.ylabel(’Max Force (N)’)
 plt.title(’Maximum Force per Specimen (0.5 mm / 2 Hz)’)
 plt.xticks(df_05_2["Specimen"].unique())
 plt.tight_layout()
 plt.show()
 23
#5.1.4 Maximum Relative Displacement per Specimen
 plt.figure(figsize=(10, 6))
 plt.plot(
 df_05_2["Specimen"],
 df_05_2["Max Relative Displacement (mm)"],
 marker=’o’,
 linestyle=’-’
 )
 plt.xlabel("Specimen")
 plt.ylabel("Max Relative Displacement (mm)")
 plt.xticks(df_05_2["Specimen"].unique())
 plt.grid(True)
 plt.tight_layout()
 plt.show()
 #5.1.5 Absolute Maximum Force per Specimen
 df_05_2["Abs Max Force (N)"] = df_05_2["Max Force (N)"].abs()
 plt.figure(figsize=(10, 6))
 plt.bar(df_05_2[’Specimen’], df_05_2[’Abs Max Force (N)’])
 plt.xlabel(’Specimen’)
 plt.ylabel(’Absolute Max Force (N)’)
 plt.title(’Absolute Maximum Force per Specimen (0.5 mm / 2 Hz)’)
 plt.xticks(df_05_2["Specimen"].unique())
 plt.tight_layout()
 plt.show()
 #5.1.6 Boxplot for maximum and minimum force
 import pandas as pd
 import matplotlib.pyplot as plt
 df = pd.read_excel("/content/.092_3.xlsx")
 force_values = pd.concat([df["Min Force (N)"],
 df["Max Force (N)"]], ignore_index=True)
 min_force = force_values.min()
 max_force = force_values.max()
 plt.figure(figsize=(8, 6))
 box = plt.boxplot(force_values, vert=True, patch_artist=True)
plt.ylabel("Force (N)")
 plt.grid(True, axis=’y’)
 plt.text(1.1, min_force, f"Max: {min_force:.2f} N",
 verticalalignment=’center’, color=’red’)
 plt.text(1.1, max_force, f"Min: {max_force:.2f} N",
 verticalalignment=’center’, color=’green’)
 plt.tight_layout()
 plt.show()
 #5.1.7 Final summarizied file
 import pandas as pd
 file_paths = {
 "0.5_4Hz": "/content/summary0.5_4_output.xlsx",
 "0.092_3Hz": "/content/summary0.092_3_output.xlsx",
 "0.5_2Hz": "/content/summary0.5_2_output.xlsx",
 "0.092_4Hz": "/content/summary0.92_4_output.xlsx",
 "0.092_2Hz": "/content/summary0.092_2_output.xlsx",
 "0.5_3Hz": "/content/summary0.5_3_output.xlsx"
 }
 summary_rows = []
 for label, path in file_paths.items():
 df = pd.read_excel(path)
 amplitude, freq = label.split("_")
 amplitude = float(amplitude)
 freq = int(freq.replace("Hz", ""))
 sample_count = len(df)
 avg_duration = df["Duration (s)"].mean()
 avg_max_force = df["Max Relative Force (N)"].mean()
 avg_max_disp = df["Max Relative Displacement (mm)"].mean()
 summary_rows.append({
 "Label": label,
"Amplitude (mm)": amplitude,
 "Frequency (Hz)": freq,
 "Sample Count": sample_count,
 "Avg Duration (s)": round(avg_duration,
 "Avg Duration (s)": round(avg_duration, 2),
 "Avg Max Relative Force (N)": round(avg_max_force, 2),
 "Avg Max Rel. Displacement (mm)": round(avg_max_disp, 3)
 })
 summary_df = pd.DataFrame(summary_rows)
 print(summary_df)
 summary_df = summary_df.drop(columns=[’Label’])
 summary_df.to_excel("final_summary.xlsx", index=False)
 print("Summary table saved to final_summary.xlsx")
 #5.1.8 Displacement per specimen final result
 Maximum Relative Displacement per Specimen (Line Graph)
 plt.figure(figsize=(10, 6))
 plt.plot(
 df_05_2["Specimen"],
 df_05_2["Max Relative Displacement (mm)"],
 marker=’o’,
 linestyle=’-’
 plt.xlabel("Specimen")
 plt.ylabel("Max Relative Displacement (mm)")
 plt.xticks(df_05_2["Specimen"].unique())
 plt.grid(True)
 plt.tight_layout()
 plt.show()
 #5.1.9 T distribution
 import pandas as pd
 import numpy as np
 import matplotlib.pyplot as plt
 import seaborn as sns
from scipy import stats
 file_path = "final_summary.xlsx"
 df = pd.read_excel(file_path)
 force_data = df["Avg Max Relative Force (N)"].dropna()
 mean_force = np.mean(force_data)
 sem_force = stats.sem(force_data)
 df_force = len(force_data)- 1
 t_dist_fit = stats.t(df=df_force,
 loc=mean_force, scale=sem_force)
 x = np.linspace(min(force_data)- 5,
 max(force_data) + 5, 500)
 y = t_dist_fit.pdf(x)
 plt.figure(figsize=(10, 6))
 sns.histplot(force_data, bins=6,
 stat=’density’, color=’skyblue’,
 edgecolor=’black’, label="Max Relative Force")
 plt.plot(x, y, color=’green’, linewidth=2,
 label="t-distribution fit")
 plt.axvline(mean_force, color=’blue’, linestyle=’--’,
 label=f"Mean: {mean_force:.2f} N")
 for idx, val in enumerate(force_data):
 plt.plot(val,-0.005, ’kx’)
 plt.title("T-Distribution of Average Max Relative Force")
 plt.xlabel("Average Max Relative Force (N)")
 plt.ylabel("Density")
 plt.legend()
 plt.grid(True)
 plt.tight_layout()
 plt.savefig("t_distribution_force_plot.png", dpi=300)
 plt.show()
 plt.show()
 # 5.1.10 Force vs Displacement by amplitude
 import pandas as pd
 import matplotlib.pyplot as plt
 import seaborn as sns
 df = pd.read_excel("final_summary.xlsx")
 plt.figure(figsize=(10, 6))
sns.scatterplot(
 data=df,
 x="Avg Max Rel. Displacement (mm)",
 y="Avg Max Relative Force (N)",
 hue="Amplitude (mm)",
 palette="viridis",
 s=100,
 edgecolor="black"
 )
 sns.regplot(
 data=df,
 x="Avg Max Rel. Displacement (mm)",
 y="Avg Max Relative Force (N)",
 import pandas as pd
 import numpy as np
 import matplotlib.pyplot as plt
 import seaborn as sns
 from scipy import stats
 # Load your summary Excel file
 file_path = "final_summary.xlsx"
 df = pd.read_excel(file_path)
 force_data = df["Avg Max Relative Force (N)"].dropna()
 mean_force = np.mean(force_data)
 sem_force = stats.sem(force_data)
 df_force = len(force_data)- 1
 t_dist_fit = stats.t(df=df_force, loc=mean_force, scale=sem_force)
 x = np.linspace(min(force_data)- 5, max(force_data) + 5, 500)
 y = t_dist_fit.pdf(x)
 plt.figure(figsize=(10, 6))
 T distribution of Average max relative force
sns.histplot(force_data, bins=6, stat=’density’,
 color=’skyblue’, edgecolor=’black’, label="Max Relative Force")
 plt.plot(x, y, color=’green’, linewidth=2,
 label="t-distribution fit")
 plt.axvline(mean_force, color=’blue’, linestyle=’--’,
 label=f"Mean: {mean_force:.2f} N") #
 for idx, val in enumerate(force_data):
 plt.plot(val,-0.005, ’kx’)
 plt.title("T-Distribution of Average Max Relative Force")
 plt.xlabel("Average Max Relative Force (N)")
 plt.ylabel("Density")
 plt.legend()
 plt.grid(True)
 plt.tight_layout()
 plt.savefig("t_distribution_force_plot.png", dpi=300)
 plt.show()
 import pandas as pd
 import numpy as np
 import matplotlib.pyplot as plt
 import seaborn as sns
 from scipy import stats
 file_path = "final_summary.xlsx"
 df = pd.read_excel(file_path)
 disp_data = df["Avg Max Rel. Displacement (mm)"].dropna()
 mean_disp = np.mean(disp_data)
 sem_disp = stats.sem(disp_data)
 df_disp = len(disp_data) { 1
 t_dist_fit = stats.t(df=df_disp, loc=mean_disp, scale=sem_disp)
 x = np.linspace(min(disp_data)- 0.5, max(disp_data) + 0.5, 500)
 y = t_dist_fit.pdf(x)
 plt.figure(figsize=(10, 6)
 sns.histplot(disp_data, bins=6, stat=’density’,
 color=’skyblue’, edgecolor=’black’, label="Max Relative Displacement")
 plt.plot(x, y, color=’green’, linewidth=2, label="t-distribution fit")
 plt.axvline(mean_disp, color=’blue’, linestyle=’--’,
 label=f"Mean: {mean_disp:.2f} mm")
 for idx, val in enumerate(disp_data):
 plt.plot(val,-0.005, ’kx’)
for idx, val in enumerate(disp_data):
 plt.plot(val,-0.005, ’kx’)
 plt.title("T-Distribution of Max Relative Displacement")
 plt.xlabel("Max Relative Displacement (mm)")
 plt.ylabel("Density")
 plt.legend()
 plt.grid(True)
 plt.tight_layout()
 plt.savefig("t_distribution_displacement_plot.png", dpi=300)
 plt.show()