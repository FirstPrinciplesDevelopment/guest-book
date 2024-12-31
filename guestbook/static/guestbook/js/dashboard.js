window.onload = function () {

    let reload_interval = 30;

    const progressElement = document.getElementById("countdown");

    function decrement() {
        --reload_interval;
        progressElement.setAttribute("value", reload_interval);
        if (reload_interval <= 1) {
            location.reload();
        }
    }


    console.log("This is the dashboard page.");

    setInterval(decrement, 1000);

};