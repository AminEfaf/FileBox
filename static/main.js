/* ── FileBox – main.js ─────────────────────────────────────────────────────── */

const form              = document.getElementById("uploadForm");
const input             = document.getElementById("fileInput");
const uploadBtn         = document.getElementById("uploadBtn");
const progressContainer = document.getElementById("progressContainer");
const progressBar       = document.getElementById("progressBar");
const filePreview       = document.getElementById("filePreview");
const currentFile       = document.getElementById("currentFile");
const fileProgress      = document.getElementById("fileProgress");
const uploadSpeed       = document.getElementById("uploadSpeed");
const uploadETA         = document.getElementById("uploadETA");
const fileList          = document.getElementById("fileList");

let isUploading = false;


// ── QR Code modal ──────────────────────────────────────────────────────────────

function showQRModal() {
    document.getElementById("qrModal").style.display = "block";
}

function closeQRModal() {
    document.getElementById("qrModal").style.display = "none";
}


// ── Action modal (stream vs download) ─────────────────────────────────────────

function showActionModal(encodedFilename, displayName) {
    const streamBtn   = document.getElementById("confirmStreamBtn");
    const downloadBtn = document.getElementById("confirmDownloadBtn");

    downloadBtn.href = `/download/${encodedFilename}`;

    streamBtn.onclick = function () {
        closeActionModal();
        streamVideo(encodedFilename, displayName);
    };

    document.getElementById("actionModal").style.display = "block";
}

function closeActionModal() {
    document.getElementById("actionModal").style.display = "none";
}


// ── Video streaming modal ──────────────────────────────────────────────────────

function streamVideo(encodedFilename, displayName) {
    const modal = document.getElementById("videoModal");
    const video = document.getElementById("modalVideo");
    const title = document.getElementById("modalTitle");

    title.textContent = displayName;
    video.src = `/stream/${encodedFilename}`;
    modal.style.display = "block";

    video.play().catch(e => console.log("Auto-play prevented:", e));
}

function closeVideoModal() {
    const video = document.getElementById("modalVideo");
    video.pause();
    video.src = "";
    document.getElementById("videoModal").style.display = "none";
}


// ── Global modal close handlers ────────────────────────────────────────────────

window.addEventListener("click", function (event) {
    const videoModal  = document.getElementById("videoModal");
    const actionModal = document.getElementById("actionModal");
    const qrModal     = document.getElementById("qrModal");

    if (event.target === videoModal)  closeVideoModal();
    if (event.target === actionModal) closeActionModal();
    if (event.target === qrModal)     closeQRModal();
});

document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeVideoModal();
        closeActionModal();
        closeQRModal();
    }
});


// ── Utilities ──────────────────────────────────────────────────────────────────

function isVideoFile(filename) {
    const videoExts = [
        "mp4", "avi", "mov", "wmv", "flv", "webm", "mkv",
        "m4v", "3gp", "ogv", "ts", "m2ts", "mts", "vob",
        "asf", "rm", "rmvb", "divx", "xvid"
    ];
    return videoExts.includes(filename.split(".").pop().toLowerCase());
}

function getFileIcon(filename) {
    const ext = filename.split(".").pop().toLowerCase();
    const icons = {
        pdf: "📄", txt: "📄", doc: "📄", docx: "📄",
        xls: "📊", xlsx: "📊", ppt: "📊", pptx: "📊",
        jpg: "🖼️", jpeg: "🖼️", png: "🖼️", gif: "🖼️", webp: "🖼️", bmp: "🖼️",
        mp4: "🎞️", mkv: "🎞️", avi: "🎞️", mov: "🎞️", wmv: "🎞️",
        flv: "🎞️", webm: "🎞️", m4v: "🎞️", "3gp": "🎞️", ogv: "🎞️",
        mp3: "🎵", wav: "🎵", flac: "🎵", aac: "🎵",
        zip: "🗜️", rar: "🗜️", "7z": "🗜️", tar: "🗜️", gz: "🗜️",
    };
    return icons[ext] || "📁";
}

function formatFileSize(bytes) {
    if (bytes === 0) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

function formatTime(seconds) {
    seconds = Math.round(seconds);
    if (seconds <= 0) return "--";
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
}


// ── File preview on selection ──────────────────────────────────────────────────

input.addEventListener("change", () => {
    filePreview.innerHTML = "";
    if (!input.files.length) return;

    const container = document.createElement("div");
    container.classList.add("preview-container");

    Array.from(input.files).forEach(file => {
        const card = document.createElement("div");
        card.classList.add("preview-card");

        const icon = document.createElement("div");
        icon.classList.add("file-icon");
        icon.textContent = getFileIcon(file.name);

        const info = document.createElement("div");
        info.classList.add("file-info");

        const fileName = document.createElement("div");
        fileName.classList.add("file-name");
        fileName.textContent = file.name;
        fileName.title = file.name;

        const fileSize = document.createElement("div");
        fileSize.classList.add("file-size");
        fileSize.textContent = formatFileSize(file.size);

        info.appendChild(fileName);
        info.appendChild(fileSize);
        card.appendChild(icon);
        card.appendChild(info);
        container.appendChild(card);
    });

    filePreview.appendChild(container);
});


// ── Add uploaded file to the live list ────────────────────────────────────────

function addFileToList(file) {
    const newItem = document.createElement("li");
    const ext = file.name.split(".").pop().toLowerCase();
    const imageExts = ["png", "jpg", "jpeg", "gif", "webp", "bmp"];

    if (imageExts.includes(ext)) {
        const img = document.createElement("img");
        img.src = `/thumbnail/${encodeURIComponent(file.name)}`;
        img.alt = "thumbnail";
        img.classList.add("thumb");
        newItem.appendChild(img);
    } else {
        const icon = document.createElement("span");
        icon.classList.add("file-icon");
        icon.setAttribute("data-ext", ext);
        icon.textContent = getFileIcon(file.name);
        newItem.appendChild(icon);
    }

    const link = document.createElement("a");
    if (isVideoFile(file.name)) {
        link.href = "#";
        link.onclick = function () {
            showActionModal(encodeURIComponent(file.name), file.name);
            return false;
        };
    } else {
        link.href = `/download/${encodeURIComponent(file.name)}`;
    }
    link.textContent = file.name;
    link.title = file.name;
    newItem.appendChild(link);

    const sizeSpan = document.createElement("span");
    sizeSpan.classList.add("file-size");
    sizeSpan.textContent = formatFileSize(file.size);
    newItem.appendChild(sizeSpan);

    const empty = fileList.querySelector(".empty");
    if (empty) empty.remove();

    fileList.insertBefore(newItem, fileList.firstChild);
}


// ── Upload handler ─────────────────────────────────────────────────────────────

form.addEventListener("submit", function (e) {
    e.preventDefault();
    const files = input.files;
    if (!files.length || isUploading) return;

    isUploading = true;
    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading…";
    progressContainer.classList.add("visible");

    let uploaded = 0;
    const total = files.length;

    function uploadNext() {
        const file = files[uploaded];
        const xhr = new XMLHttpRequest();
        const formData = new FormData();
        formData.append("file", file);

        const startTime = Date.now();

        currentFile.textContent = `Uploading: ${file.name}`;
        fileProgress.textContent = `File ${uploaded + 1} of ${total}`;

        xhr.open("POST", "/upload", true);

        xhr.upload.onprogress = function (e) {
            if (!e.lengthComputable) return;

            const timeElapsed = (Date.now() - startTime) / 1000;
            const filePercent = Math.round((e.loaded / e.total) * 100);

            progressBar.style.width = filePercent + "%";
            progressBar.textContent = filePercent + "%";

            if (timeElapsed > 0) {
                const speedBps  = e.loaded / timeElapsed;
                const speedMbps = (speedBps * 8) / (1024 * 1024);
                const eta       = speedBps > 0 ? (e.total - e.loaded) / speedBps : 0;

                uploadSpeed.textContent = `Speed: ${speedMbps.toFixed(1)} Mbps`;
                uploadETA.textContent   = `ETA: ${formatTime(eta)}`;
            }
        };

        xhr.onload = function () {
            addFileToList(file);
            uploaded++;
            if (uploaded < total) {
                setTimeout(uploadNext, 100);
            } else {
                finishUpload();
            }
        };

        xhr.onerror = function () {
            console.error("Upload error for:", file.name);
            uploaded++;
            if (uploaded < total) setTimeout(uploadNext, 100);
            else finishUpload();
        };

        xhr.send(formData);
    }

    function finishUpload() {
        progressContainer.classList.remove("visible");
        isUploading = false;
        uploadBtn.disabled = false;
        uploadBtn.textContent = "Upload";
        input.value = "";
        filePreview.innerHTML = "";
        progressBar.style.width = "0%";
        progressBar.textContent = "0%";
    }

    uploadNext();
});
