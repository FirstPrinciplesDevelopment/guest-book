window.onload = function () {
    // Global timestamp to keep track of the last time we updated the visitors.
    var LAST_UPDATE_TS = get_timestamp(30);

    // Initialize the QRCode object.
    var qrcode = new QRCode("qrcode", {
        text: "Page loading, scan again in a moment.",
        width: 512,
        height: 512,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H,
    });

    const progressElement = document.getElementById("countdown");
    const codeElement = document.getElementById("join-code");
    const visitorsSection = document.getElementById("visitors-section");

    async function refresh() {
        data = await getData();
        const { code, step, remaining, url } = data;
        // Update the countdown indicator.
        progressElement.setAttribute("value", remaining);
        progressElement.setAttribute("max", step);
        // Update the join code.
        codeElement.innerText = code;
        // Update the QRCode if the url has changed.
        var join_url = url + code;
        if (qrcode.text != join_url) {
            qrcode.clear();
            qrcode.makeCode(join_url);
        }
        // Update visitors section.
        var visitorsPartial = await getVisitorsPartial();
        if (visitorsPartial.length > 0) {
            visitorsSection.innerHTML = visitorsPartial;
            // Update the last updated timestamp.
            LAST_UPDATE_TS = get_timestamp(10);
        }
    }

    // Make the initial call so the data is quickly refreshed.
    refresh();

    // Refresh the data every second.
    setInterval(refresh, 1000);

    async function getData() {
        const url = "/refresh-code/";
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const json = await response.json();
            return json;
        } catch (error) {
            console.error(error.message);
        }
    }

    async function getVisitorsPartial() {
        const url = `/visitors-partial/${LAST_UPDATE_TS}`;
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const html = await response.text();
            return html;
        } catch (error) {
            console.error(error.message);
        }
    }

    function get_timestamp(offset) {
        // Subtract `offset` seconds to be cautious and account for slow requests.
        return Math.floor((new Date()).getTime() / 1000) - offset;
    }
};
