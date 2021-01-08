function toggle(source) {
    checkboxes = document.getElementsByName('regions');
    for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
    }
}

function clearEM(){
    var textbox = document.getElementById('em');
    var collection = textbox.getElementsByTagName('option');

    for(var i = 0; i<collection.length; i++){
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner");
    text[0].innerHTML = "<span style='color:#999'>Nothing selected</span>";
}

function clearOM(){
    var textbox = document.getElementById('om');
    var collection = textbox.getElementsByTagName('option');

    for(var i = 0; i<collection.length; i++){
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner");
    text[1].innerHTML = "<span style='color:#999'>Nothing selected</span>";
}

function clearCountry(){
    var textbox = document.getElementById('countries');
    var collection = textbox.getElementsByTagName('option');

    for(var i = 0; i<collection.length; i++){
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner");
    text[2].innerHTML = "<span style='color:#999'>Nothing selected</span>";
}

function clearSchool(){
    var textbox = document.getElementById('schools');
    var collection = textbox.getElementsByTagName('option');

    for(var i = 0; i<collection.length; i++){
        collection[i].selected = false;
    }

    var text = document.getElementsByClassName("filter-option-inner-inner");
    text[3].innerHTML = "<span style='color:#999'>Nothing selected</span>";
}