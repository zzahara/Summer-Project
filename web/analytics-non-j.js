var archive_analytics = { 
    startTime: new Date(), 
    loadtime: 0.0, 
    img_src: "http://analytics.archive.org/0.gif",
     
    onload:  addLoadEvent(function() {
        alert("Taking up some load time : )");
    
        var endTime = new Date();
        values = []
        values['loadTime'] = ((endTime.getTime() - startTime.getTime())/100)/10;

        // Get field values    
        values['timeDiff'] = (new Date().getTimezoneOffset()/60)*(-1); 
        values['locale'] = get_locale();
        values['referrer'] = document.referrer

        string = this.format_bug(values);

        loadtime_img = new Image(100,25);
        loadtime_img.src = img_src + "?" + string;
    }),
    
    format_bug: function(values) {
        ret = []
        for (var data in values)
          ret.push(encodeURIComponent(data) + "=" + encodeURIComponent(values[data]));

        return ret.join("&")
    },

    get_locale: function() {
        if (navigator) {
            if (navigator.language)
                return navigator.language;
                
            else if (naviagtor.browserLanguage)
                return navigator.browserLanguage;

            else if (navigator.systemLanguage) 
                return navigator.systemLanguage;

            else if (navigator.userLanguage)
                return navigator.userLanguage;
    }}
    }

function addLoadEvent(func) {
    var oldOnload = window.onload;

    if (typeof window.onload != 'function') {
        window.onload = func;
    } else {
        window.onload = function() {
            func()
            oldOnload();
        }   
    }
};

archive_analytics.onload

