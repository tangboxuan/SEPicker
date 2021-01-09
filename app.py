import os
from flask import Flask, redirect, render_template, request, send_from_directory
from static import Algo
from static import Algo_module_codes

app = Flask(__name__)

## To generate dictionary for nus mod code: nus mod title
nus_code_title_dict = {}
nus_modules_filename = "static/nus_modules.txt"
nus_modules_file = open(nus_modules_filename, "r")
for line in nus_modules_file:
    mod_title = line.split(">")[1].split("<")[0].split(" ")[1:]
    nus_code_title_dict[line.split(">")[1].split("<")[0].split(" ")[0]] = " ".join(mod_title)

## Generate list of all countries
countries_options_filename = "static/countries_options.txt"
countries_options_file = open(countries_options_filename, "r")
list_of_countries = []
for line in countries_options_file:
    list_of_countries.append(line.split(">")[1].split("<")[0])

## Generate list of all schools
schools_options_filename = "static/schools_options.txt"
schools_options_file = open(schools_options_filename, "r")
list_of_schools = []
for line in schools_options_file:
    list_of_schools.append(line.split(">")[1].split("<")[0])

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
    order_of_regions = ['Americas', 'Asia', 'Europe', 'Oceania', 'Africa']
    selected_regions = []
    essentialModules = []
    optionalModules = []
    selected_countries = []
    selected_schools = []
    if request.method == "GET":
        return render_template("picker.html", is_get=True, selected_regions=selected_regions,
                               order_of_regions=order_of_regions, nus_code_title_dict=nus_code_title_dict,
                               essentialModules=essentialModules,optionalModules=optionalModules,
                               selected_countries=selected_countries,list_of_countries=list_of_countries,
                               selected_schools=selected_schools,list_of_schools=list_of_schools)
    else: #POST
        essentialModules = request.form.getlist("em")
        optionalModules = request.form.getlist("om")

        if not essentialModules+optionalModules:
            return render_template("picker.html", error="No modules selected!")
        for i in range(len(essentialModules)):
            essentialModules[i] = essentialModules[i].split()[0]
        for i in range(len(optionalModules)):
            optionalModules[i] = optionalModules[i].split()[0]

        selected_regions = request.form.getlist("regions")
        selected_countries = request.form.getlist("countries")
        selected_schools = request.form.getlist("schools")

        # Select all regions by default
        error = ''
        if not selected_regions+selected_countries+selected_schools:
            error = 'NOTE: All regions selected by default'
            selected_regions = ['Americas', 'Asia', 'Europe', 'Oceania', 'Africa']

        output_dict = {}
        input_dict = {'Ess_nus_codes': essentialModules, 'Op_nus_codes': optionalModules}

        if len(selected_regions) > 0:
            input_dict['Location_type'] = 'regions'
            input_dict['Location'] = selected_regions
            output_dict1 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict1)

        if len(selected_countries) > 0:
            input_dict['Location_type'] = 'countries'
            input_dict['Location'] = selected_countries
            output_dict2 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict2)

        if len(selected_schools) > 0:
            input_dict['Location_type'] = 'universities'
            input_dict['Location'] = selected_schools
            output_dict3 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict3)

        # To ensure the regions appear in same order in the results
        # list_of_regions = []
        # output_regions = list(output_dict.keys())
        # for i in range(len(order_of_regions)):
        #     if order_of_regions[i] in output_regions:
        #         list_of_regions.append(order_of_regions[i])

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
                                order_of_regions=order_of_regions, selected_regions=selected_regions,
                                min=min, max=max, error = error,nus_code_title_dict=nus_code_title_dict,
                                essentialModules=essentialModules,optionalModules=optionalModules,
                                selected_countries=selected_countries,list_of_countries=list_of_countries,
                                selected_schools=selected_schools,list_of_schools=list_of_schools)


@app.route("/sub_search", methods=["GET", "POST"])
def sub_search():
    order_of_regions = ['Americas', 'Asia', 'Europe', 'Oceania', 'Africa']
    selected_regions = []
    essentialModules = []
    optionalModules = []
    selected_countries = []
    selected_schools = []
    if request.method == "GET":
        return render_template("picker_sub_search.html", is_get=True, selected_regions=selected_regions,
                               order_of_regions=order_of_regions, nus_code_title_dict=nus_code_title_dict,
                               essentialModules=essentialModules,optionalModules=optionalModules,
                               selected_countries=selected_countries,list_of_countries=list_of_countries,
                               selected_schools=selected_schools,list_of_schools=list_of_schools)
    else: #POST
        essentialModules = request.form.getlist("em")
        optionalModules = request.form.getlist("om")

        if not essentialModules+optionalModules:
            return render_template("picker.html", error="No modules selected!")
        for i in range(len(essentialModules)):
            essentialModules[i] = essentialModules[i].split()[0]
        for i in range(len(optionalModules)):
            optionalModules[i] = optionalModules[i].split()[0]

        selected_regions = request.form.getlist("regions")
        selected_countries = request.form.getlist("countries")
        selected_schools = request.form.getlist("schools")

        # Select all regions by default
        error = ''
        if not selected_regions+selected_countries+selected_schools:
            error = 'NOTE: All regions selected by default'
            selected_regions = ['Americas', 'Asia', 'Europe', 'Oceania', 'Africa']

        output_dict = {}
        input_dict = {'Ess_nus_codes': essentialModules, 'Op_nus_codes': optionalModules}

        if len(selected_regions) > 0:
            input_dict['Location_type'] = 'regions'
            input_dict['Location'] = selected_regions
            output_dict1 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict1)

        if len(selected_countries) > 0:
            input_dict['Location_type'] = 'countries'
            input_dict['Location'] = selected_countries
            output_dict2 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict2)

        if len(selected_schools) > 0:
            input_dict['Location_type'] = 'universities'
            input_dict['Location'] = selected_schools
            output_dict3 = Algo.main(input_dict)
            output_dict = dict_merger(output_dict,output_dict3)

        # To ensure the regions appear in same order in the results
        # list_of_regions = []
        # output_regions = list(output_dict.keys())
        # for i in range(len(order_of_regions)):
        #     if order_of_regions[i] in output_regions:
        #         list_of_regions.append(order_of_regions[i])

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
        return render_template("picker_sub_search.html", output_dict = country_first_dict, str_of_nusmods=str_nusmods,
                                order_of_regions=order_of_regions, selected_regions=selected_regions,
                                min=min, max=max, error = error,nus_code_title_dict=nus_code_title_dict,
                                essentialModules=essentialModules,optionalModules=optionalModules,
                                selected_countries=selected_countries,list_of_countries=list_of_countries,
                                selected_schools=selected_schools,list_of_schools=list_of_schools)


@app.route('/department', methods=["GET", "POST"])
def department():
    if request.method == "GET":
        return render_template("department.html")
    else:
        departments = request.form.getlist("department")
        d = {}
        for i in range(len(departments)):
            d[departments[i]] = 'placeholder'
        input_dict = {'Location_type': 'regions','Location':['Asia'],'Departments': d}
        display = Algo_module_codes.main(input_dict)
        return render_template("department.html", display=display,tmp=input_dict)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/plans')
def plans():
    return render_template("plans.html")



if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
    app.run(debug=True)
