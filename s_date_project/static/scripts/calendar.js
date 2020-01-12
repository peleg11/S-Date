var dt = new Date();
function renderDate() {
  data : null, // Events for the selected period
sDay : 0, // Current selected day
sMth : 0, // Current selected month
sYear : 0, // Current selected year
    dt.setDate(1);
    var day = dt.getDay();
    var today = new Date();
    var endDate = new Date(
        dt.getFullYear(),
        dt.getMonth() + 1,
        0
    ).getDate();

    var prevDate = new Date(
        dt.getFullYear(),
        dt.getMonth(),
        0
    ).getDate();
    var months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    document.getElementById("month").innerHTML = months[dt.getMonth()];
    document.getElementById("date_str").innerHTML = dt.toDateString();
    var cells = "";
    for (x = day; x > 0; x--) {
        cells += "<div class='prev_date'>" + (prevDate - x + 1) + "</div>";
    }
    console.log(day);
    for (i = 1; i <= endDate; i++) {
        if (i == today.getDate() && dt.getMonth() == today.getMonth()) cells += "<div class='today'>" + i + "</div>";
        else
            cells += "<div>" + i + "</div>";
    }
    document.getElementsByClassName("days")[0].innerHTML = cells;

}

function moveDate(para) {
    if(para == "prev") {
        dt.setMonth(dt.getMonth() - 1);
    } else if(para == 'next') {
        dt.setMonth(dt.getMonth() + 1);
    }
    renderDate();
}

// REMOVE ANY ADD/EDIT EVENT DOCKET
// cal.close();
//},

show : function (el) {
// cal.show() : show edit event docket for selected day
// PARAM el : Reference back to cell clicked

 // FETCH EXISTING DATA
 dt.sDay = el.getElementsByClassName("days")[0].innerHTML;

 // DRAW FORM
 var tForm = "<h1>" + (dt.data[dt.sDay] ? "EDIT" : "ADD") + " EVENT</h1>";
 tForm += "<div id='evt-date'>" + dt.sDay + " " + dt.months[dt.sMth] + " " + dt.sYear + "</div>";
 tForm += "<textarea id='evt-details' required>" + (dt.data[dt.sDay] ? dt.data[dt.sDay] : "") + "</textarea>";
 tForm += "<input type='button' value='Close' onclick='dt.close()'/>";
 tForm += "<input type='button' value='Delete' onclick='dt.del()'/>";
 tForm += "<input type='submit' value='Save'/>";

 // ATTACH
 var eForm = document.createElement("form");
 eForm.addEventListener("submit", dt.save);
 eForm.innerHTML = tForm;
 var container = document.getElementById("event");
 container.innerHTML = "";
 container.appendChild(eForm);
},

close : function () {
// cal.close() : close event docket

 document.getElementById("cal-event").innerHTML = "";
},

save : function (evt) {
// cal.save() : save event

 evt.stopPropagation();
 evt.preventDefault();
 dt.data[dt.sDay] = document.getElementById("evt-details").value;
 localStorage.setItem("dt-" + dt.sMth + "-" + dt.sYear, JSON.stringify(dt.data));
 cal.list();
},

del : function () {
// cal.del() : Delete event for selected date

 if (confirm("Remove event?")) {
   delete dt.data[dt.sDay];
   localStorage.setItem("dt-" + dt.sMth + "-" + dt.sYear, JSON.stringify(dt.data));
   cal.list();
 }
}
};
