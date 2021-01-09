function toggle() {
    var checkboxes = document.getElementsByName("regions");
    console.log("here");
    for (var i = 0, n = checkboxes.length; i < n; i++) {
        checkboxes[i].checked = true;
    }
}

function clearEM() {
    var textbox = document.getElementById("em");
    var collection = textbox.getElementsByTagName("option");

    for (var i = 0; i < collection.length; i++) {
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner")[0];
    text.innerHTML = "<span style='color:#999'>Nothing selected</span>";
}

function clearOM() {
    var textbox = document.getElementById("om");
    var collection = textbox.getElementsByTagName("option");

    for (var i = 0; i < collection.length; i++) {
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner")[1];
    text.innerHTML = "<span style='color:#999'>Nothing selected</span>";
}

function clearCountry() {
    var textbox = document.getElementById("countries");
    var collection = textbox.getElementsByTagName("option");

    for (var i = 0; i < collection.length; i++) {
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner")[2];
    text.innerHTML = "<span style='color:#999'>Nothing selected</span>";
}

function clearSchool() {
    var textbox = document.getElementById("schools");
    var collection = textbox.getElementsByTagName("option");

    for (var i = 0; i < collection.length; i++) {
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner")[3];
    text.innerHTML = "<span style='color:#999'>Nothing selected</span>";
}

function onCountryClick(e) {
    console.log(e.id + "-pus");
    var pusContainer = document.getElementById(e.id + "-pus");
    pusContainer.classList.toggle("open");
}

function closeAlert(e){
    e.classList.add("closed");
}


//added
function randID() {
    return Math.floor(Math.random() * 1000000);
}

function togglePlan(uniObj, uniName, el) {
    el.classList.toggle("selected");
    var data = localStorage.getItem("plans")
    if (el.id) {
        if ( //remove
            data &&
            JSON.parse(data).find(function(plan) {
                    return parseInt(plan.plan_id) === parseInt(el.id);
                })
            ) {
            var prev = JSON.parse(localStorage.getItem("plans"));
            localStorage.setItem(
                "plans",
                JSON.stringify(prev.filter(function(plan) {
                    return plan.plan_id !== el.id;
                }))
            );
        } else { //add
            if (localStorage.getItem("plans")) {
                var prev = JSON.parse(localStorage.getItem("plans"));
                var newUni = { mappings: uniObj, uni: uniName, plan_id: el.id };
                console.log("here");
                prev.push(newUni)
                localStorage.setItem(
                    "plans",
                    JSON.stringify(prev)
                );
            } else {
                localStorage.setItem("plans", JSON.stringify([newUni]));
            }
        }
    } else {//add
        el.id = randID();
        var newUni = { mappings: uniObj, uni: uniName, plan_id: el.id };
        console.log(newUni);
        if (localStorage.getItem("plans")) {
            var prev = JSON.parse(localStorage.getItem("plans"));
            prev.push(newUni);
            localStorage.setItem("plans", JSON.stringify(prev));
        } else {
            localStorage.setItem("plans", JSON.stringify([newUni]));
        }
    }
}

function removeFavourite(el){
    console.log(el.id);
    var prev = JSON.parse(localStorage.getItem("plans"));
    localStorage.setItem(
        "plans",
        JSON.stringify(prev.filter(function(plan) {
            return plan.plan_id !== el.id;
        }))
    );
    var par = document.getElementById(el.id);
    par.parentNode.removeChild(par);
}

function clearDP(){
    var textbox = document.getElementById("department");
    var collection = textbox.getElementsByTagName("option");

    for (var i = 0; i < collection.length; i++) {
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner")[0];
    text.innerHTML = "<span style='color:#999'>Nothing selected</span>";
}
