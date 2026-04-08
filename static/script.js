const fileInput = document.getElementById("fileInput");
const filePreview = document.getElementById("filePreview");
const fileName = document.getElementById("fileName");

function openFile() {
    fileInput.click();
}

fileInput.addEventListener("change", function() {
    if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
        filePreview.style.display = "flex";
    }
});

function removeFile() {
    fileInput.value = "";
    filePreview.style.display = "none";
}

function submitFile() {
    if (fileInput.files.length === 0) {
        alert("Please upload a file first!");
        return;
    }

    alert("File submitted!");
}