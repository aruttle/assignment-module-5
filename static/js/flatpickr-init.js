document.addEventListener('DOMContentLoaded', function () {
    const jsonScript = document.getElementById('booked-ranges-data');

    let bookedRanges = [];

    if (jsonScript) {
        try {
            bookedRanges = JSON.parse(jsonScript.textContent);
        } catch (e) {
            console.error("Error parsing booked ranges JSON:", e);
        }
    } else {
        console.warn("booked-ranges-data script not found.");
    }

    function getFlatpickrConfig() {
        return {
            dateFormat: "Y-m-d",
            disable: bookedRanges.map(range => ({
                from: range.from,
                to: range.to
            })),
        };
    }

    const checkIn = document.querySelector("#check_in");
    const checkOut = document.querySelector("#check_out");

    if (checkIn) flatpickr(checkIn, getFlatpickrConfig());
    if (checkOut) flatpickr(checkOut, getFlatpickrConfig());
});
