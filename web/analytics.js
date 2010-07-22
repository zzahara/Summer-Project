var startTime = new Date();

var archive_analytics = {
    loadtime: 0, 
    img_src: "http://analytics.archive.org/0.gif",
    values: {},
    
    onload_func: function() {
        var endTime = new Date();
        
        // Get field values    
        loadtime = ((endTime.getTime() - startTime.getTime())/100)/10;
        loadtime = parseInt(loadtime * 1000);
        
        archive_analytics.values['loadtime'] = loadtime
        archive_analytics.values['timediff'] = (new Date().getTimezoneOffset()/60)*(-1); 
        archive_analytics.values['locale'] = archive_analytics.get_locale();
        archive_analytics.values['referrer'] = document.referrer;
        
        string = archive_analytics.format_bug(archive_analytics.values);

        loadtime_img = new Image(100,25);
        loadtime_img.src = archive_analytics.img_src + "?" + string;
    },

    format_bug: function(values) {
        ret = []
        for (var data in values) 
            ret.push(encodeURIComponent(data) + "=" + encodeURIComponent(values[data]));
        return ret.join("&");
    },

    get_locale: function() {
        if (navigator) {
            if (navigator.language)
                return navigator.language;
                
            else if (navigator.browserLanguage)
                return navigator.browserLanguage;

            else if (navigator.systemLanguage) 
                return navigator.systemLanguage;

            else if (navigator.userLanguage)
                return navigator.userLanguage;
        }
    }
}

$(window).load(archive_analytics.onload_func)


