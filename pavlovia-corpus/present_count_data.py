import pickle
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

plugin_dict = pickle.load(open('./plugin_counts.pickle', 'rb'))
plugin_dict_no_zeros = plugin_dict

plugin_list = plugin_dict.keys()
plugin_list_no_zeroes = [p[0] for p in plugin_dict.items() if p[1] > 0]

p_counts = plugin_dict.values()
p_counts = [p for p in p_counts if p != 0]
top_plugins = sorted(plugin_dict.items(), key=lambda x: x[1], reverse=True)[:10]

sns.set_theme(style="darkgrid")

y_pos = np.arange(len(plugin_list_no_zeroes))

plt.barh(y_pos, p_counts, align='center', alpha=0.5)
plt.yticks(y_pos, plugin_list_no_zeroes)
plt.subplots_adjust(left=0.2)
plt.xlabel('Trial Number')
plt.title('jsPsych Plugin Usage by Total Trials')

plt.show()

print("top plugins: " + top_plugins.__str__())

project_plugin_dict = pickle.load(open('./project_plugin_counts.pickle', 'rb'))
project_plugin_dict = {i[0]: len(i[1].keys()) for i in project_plugin_dict.items()}

print(project_plugin_dict)
print(len(project_plugin_dict))

sns.set_theme(style="darkgrid")

plt.hist(project_plugin_dict.values(), bins=10)
plt.xlabel('# Plugins')
plt.ylabel("Frequency")
plt.title('Distribution of Number of Plugins Used')
plt.show()
