var startTime = new Date();
var loadTime = 0.0;
img_src = "http://analytics.archive.org/0.gif"

$(document).ready(function() {
    alert("Taking up some load time : )");
    var endTime = new Date();
    loadTime = ((endTime.getTime() - startTime.getTime())/100)/10;

    // Get field values
    timeDiff = (new Date().getTimezoneOffset()/60)*(-1); 
    locale = get_locale();
    referrer = document.referrer
    
    loadtime_img = new Image(100,25);
    loadtime_img.src = img_src + "?loadtime=" + loadTime;
    
    format_bug(loadTime, locale, timeDiff);

    // Console Logging
    console.log("Loadtime = " + loadTime);
    console.log("Time Difference = " + timeDiff);
    console.log("Locale = " + locale);
    console.log("Referrer = " + referrer);
});

function format_bug(loadtime, locale, timediff) {
    var values = {'loadtime': loadtime, 'locale': locale, 'timediff': timeDiff};

    ret = []
    for (var data in values)
      ret.push(encodeURIComponent(data) + "=" + encodeURIComponent(values[data]));
   console.log(img_src + "?" + ret.join("&"));
    
    
    
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

// args should be an array
function format_request(loadtime, locale, timediff) {

    values = "loadtime=" + loadtime + "&locale=" + escape(locale) + "&timediff=" + escape(timediff);
    src = img_src + "?" + escape(values);
    console.log("src = " + src)
    //document.write(src);

    var data = { 'loadtime': 578, 'locale': 'en-US'};

   var ret = [];
   for (var d in data)
      ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
   console.log(ret.join("&"));

};

