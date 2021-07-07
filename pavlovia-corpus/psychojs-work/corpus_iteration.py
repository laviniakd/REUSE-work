import base64
import pickle
import gitlab

module_names = open('psychojs-work/psychojs_modules.txt').read().splitlines()

access_token = ""
# oauth token authentication
gl = gitlab.Gitlab('https://gitlab.pavlovia.org', oauth_token=access_token)

project_ids = pickle.load(open("psychojs-work/project_ids.pickle", 'rb'))
filepath = "/html/index.html"
# common set-up: index.html which points to JS file defining experiment in body via script tag.

project_dataset = {}
num_trial_counts = {}


def process_index_html(f_input):
    file = str(base64.b64decode(f_input.content))
    file.replace("\\\\", "\\")

    randomID_count = 0
    random_count = 0

    if "randomID" in file:
        print("uses randomness for ID")
        randomID_count += 1
    elif "random" in file:
        print("uses randomness for other stuff")
        random_count += 1

    num_trials = file.count("type: ")

    return file, randomID_count, random_count, num_trials


random_c = 0
randomID_c = 0

# pavlovia stuff
print("num project ids: " + len(project_ids).__str__())
counter = 0
for proj_id in project_ids:
    print("project_id counter: " + counter.__str__())
    proj = gl.projects.get(proj_id)
    try:
        f = proj.files.get(file_path=filepath, ref="master")
        d, rID_c, r_c, n_trials = process_index_html(f)  # this is where it gets buggy for #25
        project_dataset[proj_id] = d
        random_c += r_c
        randomID_c += rID_c
        num_trial_counts[proj_id] = n_trials
    except gitlab.exceptions.GitlabHttpError as e:
        try:
            f = proj.files.get(file_path="/html" + filepath, ref="master")
            d, rID_c, r_c, n_trials = process_index_html(f)  # this is where it gets buggy for #25
            project_dataset[proj_id] = d
            random_c += r_c
            randomID_c += rID_c
            num_trial_counts[proj_id] = n_trials
        except gitlab.exceptions.GitlabHttpError as e:
            print(e)
    except Exception as e:
        print(e)

    counter += 1
    # rn for debugging
    # time.sleep(5)

print("number of randomID uses: " + randomID_c.__str__())
print("number of random uses: " + random_c.__str__())

print("project trial counts: " + num_trial_counts.__str__())

with open('project_index.pickle', 'wb') as handle:
    pickle.dump(project_dataset, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('project_trial_counts.pickle', 'wb') as handle:
    pickle.dump(num_trial_counts, handle, protocol=pickle.HIGHEST_PROTOCOL)
