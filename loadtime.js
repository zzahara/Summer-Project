var startTime = new Date();
var loadTime = 0.0;

    $(document).ready(function() {
        alert("Taking up some load time : )");
        var endTime = new Date();
        loadTime = ((endTime.getTime() - startTime.getTime())/100)/10;

        loadtime_img = new Image(100,25);
        loadtime_img.src = "../images/flower.jpg?loadtime=" + loadTime;
        console.log("Loadtime = " + loadTime);

    });
