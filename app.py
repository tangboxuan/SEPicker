import os
from flask import Flask, redirect, render_template, request, send_from_directory
from static import Algo

app = Flask(__name__)

## To generate dictionary for nus mod code: nus mod title
nus_code_title_dict = {}
filename = "static/nus_modules.txt"
file = open(filename, "r")
for line in file:
    mod_title = line.split(">")[1].split("<")[0].split(" ")[1:]
    nus_code_title_dict[line.split(">")[1].split("<")[0].split(" ")[0]] = " ".join(mod_title)

def dict_merger(dict1,dict2):
    for region in dict2:
        if region not in dict1:
            dict1[region] = dict2[region]
            continue
        for country in dict2[region]:
            if country not in dict1[region]:
                dict1[region][country] = dict2[region][country]
                continue
            # Doesn't matter if we overwrite since the data is the same if they exist in both
            for uni in dict2[region][country]:
                dict1[region][country][uni] = dict2[region][country][uni]

    return dict1

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("picker.html", is_get=True)
    else: #POST
        essentialModules = request.form.getlist("em")
        optionalModules = request.form.getlist("om")

        if not essentialModules+optionalModules:
            return render_template("picker.html", error="No modules selected!")
        for i in range(len(essentialModules)):
            essentialModules[i] = essentialModules[i].split()[0]
        for i in range(len(optionalModules)):
            optionalModules[i] = optionalModules[i].split()[0]

        regions = request.form.getlist("regions")
        countries = request.form.getlist("countries")
        schools = request.form.getlist("schools")

        # Select all regions by default
        error = ''
        if not regions+countries+schools:
            error = 'NOTE: All regions selected by default'
            regions = ['Americas', 'Asia', 'Europe', 'Oceania', 'Africa']

        output_dict = {}
        input_dict = {'Ess_nus_codes': essentialModules, 'Op_nus_codes': optionalModules}

        if len(regions) > 0:
            input_dict['Location_type'] = 'regions'
            input_dict['Location'] = regions
            output_dict1 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict1)

        if len(countries) > 0:
            input_dict['Location_type'] = 'countries'
            input_dict['Location'] = countries
            output_dict2 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict2)

        if len(schools) > 0:
            input_dict['Location_type'] = 'universities'
            input_dict['Location'] = schools
            output_dict3 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict3)

        # To ensure the regions appear in same order in the results
        order_of_regions = ['Americas', 'Asia', 'Europe', 'Oceania', 'Africa']
        list_of_regions = []
        output_regions = list(output_dict.keys())
        for i in range(len(order_of_regions)):
            if order_of_regions[i] in output_regions:
                list_of_regions.append(order_of_regions[i])

        # Get the min and max number of mods among all the PUs
        list_for_n_mods = []
        counter = 0
        for region in output_dict:
            for country in output_dict[region]:
                for uni in output_dict[region][country]:
                    list_for_n_mods.append(output_dict[region][country][uni]["n_mods"])
                    counter += 1
        min, max = 0,0
        if len(list(set(list_for_n_mods))) > 0:
            min =  list(set(list_for_n_mods))[0]
            max = min
            if len(list(set(list_for_n_mods))) > 1:
                max = list(set(list_for_n_mods))[-1]

        # New dictionary removing first layer (regions)
        country_first_dict = {}
        for region in output_dict:
            country_first_dict.update(output_dict[region])
        # min, max = list(set(list_for_n_mods))[0], list(set(list_for_n_mods))[1]
        str_nusmods = {}
        for country in country_first_dict:
            for uni in country_first_dict[country]:
                str_nusmods[uni] = ', '.join(list(country_first_dict[country][uni].keys())[:-1])
        return render_template("picker.html", output_dict = country_first_dict, str_of_nusmods=str_nusmods,
                           list_of_regions=list_of_regions, min=min, max=max, error = error,
                           nus_code_title_dict=nus_code_title_dict)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
#     app.run(debug=True)
