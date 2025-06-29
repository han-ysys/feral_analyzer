import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

# Load data
df = pd.read_json('data_json/top_feral_apex_summary.json')

# Boxplot for categorical fields
sns.boxplot(x='region', y='apex_index', data=df)
plt.savefig('data_json/apex_index_by_region.png')
plt.show()
plt.clf()

sns.boxplot(x='fight_name', y='apex_index', data=df)
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.tight_layout()
plt.savefig('data_json/apex_index_by_dungeon.png')
plt.show()
plt.clf()

# Treat 'region' and 'fight_name' as categorical variables
model = smf.ols('apex_index ~ C(region) + C(fight_name)', data=df).fit()

with open('data_json/apex_index_model_summary.txt', 'w') as f:
    f.write(model.summary().as_text())