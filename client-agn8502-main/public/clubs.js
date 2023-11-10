function plus_capacity() {
    var capacity;
    var warning;
    var limit;
    var message;
    var color;
    if(document.getElementById("ca_radio").checked) {
        capacity = 'ca_capacity';
        message = 'ca_message';
        warning = 70;
        limit = 100;
        color = 'ClubArcane';
    } else if(document.getElementById("cu_radio").checked) {
        capacity = 'cu_capacity';
        message = 'cu_message';
        warning = 30;
        limit = 50;
        color = 'ClubUnderground';
    } else if(document.getElementById("cs_radio").checked) {
        capacity = 'cs_capacity';
        message = 'cs_message';
        warning = 12;
        limit = 20;
        color = 'ClubSoda';
    } else if(document.getElementById("s52_radio").checked) {
        capacity = 's52_capacity';
        message = 's52_message';
        warning = 32;
        limit = 52;
        color = 'Studio52';
    } else {
        return;
    }

    capacity_num = document.getElementById(capacity).innerHTML;
    capacity_num++;
    document.getElementById(capacity).innerHTML = capacity_num;

    if(capacity_num >= warning && capacity_num < limit) {
        document.getElementById(color).style.backgroundColor = 'yellow';
        document.getElementById(message).innerHTML = "Warn the bouncers...";
    } else if(capacity_num >= limit) {
        document.getElementById(color).style.backgroundColor = 'red';
        document.getElementById(message).innerHTML = "No one allowed in!";
    } else {
        document.getElementById(color).style.backgroundColor = 'lightgreen';
        document.getElementById(message).innerHTML = "Welcome!"
    }
}

function minus_capacity() {
    var capacity;
    var warning;
    var limit;
    var message;
    var color;
    if(document.getElementById("ca_radio").checked) {
        capacity = 'ca_capacity';
        message = 'ca_message';
        warning = 70;
        limit = 100;
        color = 'ClubArcane';
    } else if(document.getElementById("cu_radio").checked) {
        capacity = 'cu_capacity';
        message = 'cu_message';
        warning = 30;
        limit = 50;
        color = 'ClubUnderground';
    } else if(document.getElementById("cs_radio").checked) {
        capacity = 'cs_capacity';
        message = 'cs_message';
        warning = 12;
        limit = 20;
        color = 'ClubSoda';
    } else if(document.getElementById("s52_radio").checked) {
        capacity = 's52_capacity';
        message = 's52_message';
        warning = 32;
        limit = 52;
        color = 'Studio52';
    } else {
        return;
    }

    capacity_num = document.getElementById(capacity).innerHTML;
    if(capacity_num <= 0) {
    return;
    }
    capacity_num--;
    document.getElementById(capacity).innerHTML = capacity_num;

    if(capacity_num >= warning && capacity_num < limit) {
        document.getElementById(color).style.backgroundColor = 'yellow';
        document.getElementById(message).innerHTML = "Warn the bouncers...";
    } else if(capacity_num >= limit) {
        document.getElementById(color).style.backgroundColor = 'red';
        document.getElementById(message).innerHTML = "No one allowed in!";
    } else {
        document.getElementById(color).style.backgroundColor = 'lightgreen';
        document.getElementById(message).innerHTML = "Welcome!"
    }
}