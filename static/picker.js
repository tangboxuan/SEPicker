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

