import pickle

SPACE_BULLET = "      * "
PREFIX = "jspsych-"
n = len(SPACE_BULLET)

plugin_list = open("../plugin_list.txt").read().splitlines()
plugin_counts = {key[len(PREFIX):]: 0 for key in plugin_list}
project_plugin_counts = {}
repo_lines = open("./inpractice.txt").read().splitlines()


def get_num(line):
    return int(line.split()[-1])


def get_repo(line):
    return line[2:].split(",")[0]


curr_proj = get_repo(repo_lines[0][1:])
project_plugin_counts[curr_proj] = {}
for r in repo_lines[1:]:
    if not (r[:n] == SPACE_BULLET):
        curr_proj = get_repo(r)
        project_plugin_counts[curr_proj] = {}
    else:
        plugin_name = r[n:].split(":")[0].lower()
        num = get_num(r)
        project_plugin_counts[curr_proj][plugin_name] = num

        if plugin_name not in plugin_counts.keys():
            plugin_counts[plugin_name] = 0
        plugin_counts[plugin_name] += num

with open('project_plugin_counts.pickle', 'wb') as handle:
    pickle.dump(project_plugin_counts, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('plugin_counts.pickle', 'wb') as handle:
    pickle.dump(plugin_counts, handle, protocol=pickle.HIGHEST_PROTOCOL)
