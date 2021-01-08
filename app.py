import os
from flask import Flask, redirect, render_template, request, send_from_directory
from static import Algo

app = Flask(__name__)

def dict_merger(dict1,dict2):
    for region in dict2:
        if region not in dict1:
            dict1[region] = dict2[region]
            continue
        for country in dict2[region]:
            if country not in dict1[region]:
                dict1[region][country] = dict2[region][country]
                continue
            for uni in dict1[region][country]:
                dict1[region][country][uni] = dict2[region][country][uni]
    return dict1

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("picker.html")
    else: #POST
        text1 = request.form.get("em")
        text2 = request.form.get("om")
        essentialModules = text1.upper().split()
        optionalModules = text2.upper().split()
        for module in essentialModules + optionalModules:
            if len(module) > 8:
                return render_template("picker.html", error="Module Code Too Long: " + module + "!", text1=text1, text2=text2)
            if len(module) < 6:
                return render_template("picker.html", error="Module Code Too Short: " + module + "!", text1=text1, text2=text2)

        regions = request.form.getlist("regions")
        countries = request.form.getlist("countries")
        schools = request.form.getlist("schools")
        
        output_dict = {}
        if len(regions) > 0:
            input_dict1 = {}
            input_dict1['Location_type'] = 'regions'
            input_dict1['Location'] = regions
            input_dict1['Ess_nus_codes'] = essentialModules
            input_dict1['Op_nus_codes'] = optionalModules
            output_dict1 = Algo.main(input_dict1)
            output_dict = dict_merger(output_dict,output_dict1)
        
        if len(countries) > 0:
            input_dict2 = {}
            input_dict2['Location_type'] = 'countries'
            input_dict2['Location'] = countries
            input_dict2['Ess_nus_codes'] = essentialModules
            input_dict2['Op_nus_codes'] = optionalModules
            output_dict2 = Algo.main(input_dict2)
            output_dict = dict_merger(output_dict,output_dict2)
            
        if len(schools) > 0:
            input_dict3 = {}
            input_dict3['Location_type'] = 'universities'
            input_dict3['Location'] = schools
            input_dict3['Ess_nus_codes'] = essentialModules
            input_dict3['Op_nus_codes'] = optionalModules
            output_dict3 = Algo.main(input_dict3)
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
                max = list(set(list_for_n_mods))[1]
        # min, max = list(set(list_for_n_mods))[0], list(set(list_for_n_mods))[1]
        return render_template("picker.html", text1=text1, text2=text2, output_dict = output_dict,
                               list_of_regions=list_of_regions, min=min, max=max)

@app.route('/help')
def help():
    return render_template("help.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)
