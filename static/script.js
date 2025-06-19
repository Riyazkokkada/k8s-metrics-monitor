function changeRefresh() {
    const value = document.getElementById("refresh-select").value;
    const url = new URL(window.location.href);
    url.searchParams.set("refresh", value);
    window.location.href = url.toString();
}

function autoRefresh(seconds) {
    if (seconds > 0) {
        setTimeout(() => {
            window.location.reload();
        }, seconds * 1000);
    }
}

