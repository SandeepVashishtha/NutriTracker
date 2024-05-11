document.getElementById("file").onchange = function(event) {
    document.getElementById("submit").click();
};

document.getElementById("submit").onclick = function(event) {
    event.preventDefault();
    var form_data = new FormData();
    var upload_option = document.querySelector('input[name="upload"]:checked').value;
    form_data.append("upload_option", upload_option);
    if (upload_option == "Upload Photo") {
        var file_input = document.getElementById("file");
        if (!file_input.files.length) {
            alert("Please select an image.");
            return;
        }
        form_data.append("file", file_input.files[0]);
    }
    fetch("/analyse", {
        method: "POST",
        body: form_data
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById("output").innerHTML = data;
        });
};
