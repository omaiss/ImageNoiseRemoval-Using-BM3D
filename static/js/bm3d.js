const progressDivMain = document.getElementById('mainprog');
const progressDiv = document.getElementById('progressDiv');
function hideprogressDiv() {
    progressDivMain.classList.add("hide");
    progressDiv.classList.add("hide");
}

hideprogressDiv();
function downloadAndDisplayImage(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const imgElement = document.getElementById('view-image');
    const filename = document.getElementById('filename')
    if (file) {
        const imageUrl = URL.createObjectURL(file);
        imgElement.src = imageUrl;
        filename.textContent = "Selected File: " + file.name;
    } else {
        imgElement.src = '';
    }
}


function denoiseImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    progressDivMain.classList.remove("hide");
    progressDiv.classList.remove("hide");

    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const fileSizeInBytes = file.size;

    const largestImageSize = 1500 * 1000;
    const smallestImageSize = 200 * 200;
    const largestDuration = 123.8;
    const smallestDuration = 5.1;

    const duration = smallestDuration + ((fileSizeInBytes - smallestImageSize) / (largestImageSize - smallestImageSize)) * (largestDuration - smallestDuration);

    const intervalTimeInSeconds = 100;
    let currentTimeInSeconds = 0;

    function updateProgress() {
        if (currentTimeInSeconds < duration) {
            currentTimeInSeconds += intervalTimeInSeconds / 1000;
            const progressPercentage = Math.min((currentTimeInSeconds / duration) * 100, 100);
            progressDiv.style.width = progressPercentage + "%";
            progressDiv.innerHTML = Math.round(progressPercentage) + "%";
            setTimeout(updateProgress, intervalTimeInSeconds);
        } else {
            progressDiv.style.width = "100%";
            progressDiv.innerHTML = "100%";
        }
    }

    updateProgress();

    fetch('/denoise', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                return response.text(); // Assuming the server returns the filename
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(filename => {
            const resultImg = document.getElementById('result');
            const imageUrl = `/${filename}`;
            resultImg.src = imageUrl;
            resultImg.alt = 'Denoised Image';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });
}

