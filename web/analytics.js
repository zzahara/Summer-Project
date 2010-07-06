/* 
* Contact Info:
* Zahara Docena
* zahara.docena@gmail.com
* zahara@archive.org
*/

var startTime = new Date();
var loadTime = 0.0;
img_src = "analytics.archive.org/0.gif"

$(document).ready(function() {
    alert("Taking up some load time : )");

    var endTime = new Date();
    values = []
    values['loadTime'] = ((endTime.getTime() - startTime.getTime())/100)/10;

    // Get field values    
    values['timeDiff'] = (new Date().getTimezoneOffset()/60)*(-1); 
    values['locale'] = get_locale();
    values['referrer'] = document.referrer

    string = format_bug(values);
    console.log(string)

    loadtime_img = new Image(100,25);
    loadtime_img.src = img_src + "?" + string;
});


function format_bug(values) {
    ret = []
    for (var data in values)
      ret.push(encodeURIComponent(data) + "=" + encodeURIComponent(values[data]));

    return ret.join("&")
};

function get_locale() {
    if (navigator) {
        if (navigator.language)
            return navigator.language;
            
        else if (naviagtor.browserLanguage)
            return navigator.browserLanguage;

        else if (navigator.systemLanguage) 
            return navigator.systemLanguage;

        else if (navigator.userLanguage)
            return navigator.userLanguage;
    }

};


