import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

variable = 'frenzy_per_berserk'  # Change this to the variable you want to analyze

# Load data
df = pd.read_json(f'data_json/top_feral_frenzy_summary.json')

# Violin plot for categorical fields
sns.violinplot(x='region', y=variable, data=df)
plt.savefig(f'data_json/{variable}_by_region.png')
plt.show()
plt.clf()

sns.violinplot(x='fight_name', y=variable, data=df)
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.tight_layout()
plt.savefig(f'data_json/{variable}_by_dungeon.png')
plt.show()
plt.clf()

# Treat 'region' and 'fight_name' as categorical variables
model = smf.ols(f'{variable} ~ C(region) + C(fight_name)', data=df).fit()

with open(f'data_json/{variable}_model_summary.txt', 'w') as f:
    f.write(model.summary().as_text())