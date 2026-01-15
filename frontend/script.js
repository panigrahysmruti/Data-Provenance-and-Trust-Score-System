const uploadBtn = document.getElementById("uploadBtn");
const verifyBtn = document.getElementById("verifyBtn");
const fileInput = document.getElementById("fileInput");
const fileBox = document.getElementById("fileBox");
const fileLabel = document.getElementById("fileLabel");
const statusBox = document.getElementById("statusBox");

let currentFilename = null;

/* 📂 Open file picker */
fileBox.addEventListener("click", () => {
  fileInput.click();
});

/* 📄 File selected */
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  statusBox.classList.add("hidden");

  if (!file) return;

  fileLabel.textContent = file.name;

  // New file selected → unlock upload, lock verify
  if (file.name !== currentFilename) {
    currentFilename = file.name;
    uploadBtn.disabled = false;
    verifyBtn.disabled = true;
  }
});

/* ⬆️ Upload */
uploadBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://127.0.0.1:8000/data/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (data.status === "UPLOAD_LOCKED") {
      showStatus("🔒 Dataset already uploaded. You can verify it.", "locked");
      uploadBtn.disabled = true;
      verifyBtn.disabled = false;
      return;
    }

    showStatus("✅ Dataset uploaded successfully", "authentic");
    uploadBtn.disabled = true;
    verifyBtn.disabled = false;

  } catch (err) {
    showStatus("❌ Upload failed", "error");
    console.error(err);
  }
});

/* 🔍 Verify */
verifyBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://127.0.0.1:8000/data/verify", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (data.status === "AUTHENTIC") {
      showStatus("🟢 Dataset is authentic", "authentic");
    } else if (data.status === "TAMPERED") {
      showStatus("🔴 Dataset has been tampered", "tampered");
    } else {
      showStatus("ℹ️ Upload the dataset first", "info");
    }

  } catch (err) {
    showStatus("❌ Verification failed", "error");
    console.error(err);
  }
});

/* 📢 Status helper */
function showStatus(text, type) {
  statusBox.className = `status ${type}`;
  statusBox.textContent = text;
  statusBox.classList.remove("hidden");
}
