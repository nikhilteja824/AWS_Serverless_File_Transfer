// Replace this with your actual API Gateway base URL
const API_BASE_URL = CONFIG.API_BASE_URL;

// Function to upload a file
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("Please select a file to upload!");
        return;
    }

    const file = fileInput.files[0];
    const fileName = file.name;

    try {
        // Fetch the pre-signed URL for upload
        const response = await fetch(`${API_BASE_URL}?fileName=${fileName}`, {
            method: "POST",
            headers: { "Content-Type": "text/plain" }
        });

        if (!response.ok) {
            throw new Error("Failed to get upload URL.");
        }

        const uploadUrl = await response.text();

        // Upload the file to S3 using the pre-signed URL
        await fetch(uploadUrl, {
            method: "PUT",
            body: file
        });

        document.getElementById("result").innerText = `File "${fileName}" uploaded successfully!`;
    } catch (error) {
        document.getElementById("result").innerText = `Error: ${error.message}`;
    }
}

// Function to download a file
async function downloadFile() {
    const fileNameInput = document.getElementById("fileNameInput");
    const fileName = fileNameInput.value.trim();

    if (!fileName) {
        alert("Please enter a file name to download!");
        return;
    }

    try {
        // Fetch the pre-signed URL for download
        const response = await fetch(`${API_BASE_URL}?fileName=${fileName}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error("Failed to get download URL.");
        }

        const downloadUrl = await response.text();

        // Redirect the browser to the pre-signed URL to download the file
        window.location.href = downloadUrl;
    } catch (error) {
        document.getElementById("result").innerText = `Error: ${error.message}`;
    }
}
