<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('../data/friday.csv', encoding='latin1')
df.columns = df.columns.str.strip()

# Plot label distribution
df['Label'].value_counts().plot(kind='bar')
plt.title("Attack vs Normal Traffic")
plt.xlabel("Class")
plt.ylabel("Count")
=======
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('../data/friday.csv', encoding='latin1')
df.columns = df.columns.str.strip()

# Plot label distribution
df['Label'].value_counts().plot(kind='bar')
plt.title("Attack vs Normal Traffic")
plt.xlabel("Class")
plt.ylabel("Count")
>>>>>>> 62378f46b605f4d73ef0fa7d1153e9aff172100e
plt.show()