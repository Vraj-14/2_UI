// document.getElementById("upload-form").addEventListener("submit", async function (e) {
//   e.preventDefault();
//   const formData = new FormData(this);
//   const res = await fetch("/upload", { method: "POST", body: formData });
//   const text = await res.text();
//   alert(text);
// });

// document.getElementById("question-form").addEventListener("submit", async function (e) {
//   e.preventDefault();
//   const question = document.getElementById("question-input").value;
//   const res = await fetch("/query", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ question }),
//   });
//   const data = await res.json();
//   document.getElementById("response-box").innerHTML = `
//     <strong>Answer (${data.source}):</strong><br>${data.answer}
//     ${data.title ? `<br><em>From: ${data.title}</em>` : ""}
//   `;
// });


// ----------------------------------- GROK UI -----------------------------------

const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const uploadForm = document.getElementById('upload-form');
const fileList = document.getElementById('file-list');
const progressBar = document.getElementById('progress-bar');
const progressFill = document.getElementById('progress-fill');
const questionForm = document.getElementById('question-form');
const responseBox = document.getElementById('response-box');
const loadingIndicator = document.getElementById('loading-indicator');

// Drag and Drop Handlers
dropArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', (e) => {
  e.preventDefault();
  dropArea.classList.remove('dragover');
  const files = e.dataTransfer.files;
  fileInput.files = files;
  handleFiles(files);
});

dropArea.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  handleFiles(fileInput.files);
});

function handleFiles(files) {
  fileList.innerHTML = '';
  for (const file of files) {
    const fileCard = document.createElement('div');
    fileCard.className = 'file-card';
    fileCard.innerHTML = `
      <p>${file.name} (${(file.size / 1024).toFixed(2)} KB)</p>
      <span>Uploaded</span>
    `;
    fileList.appendChild(fileCard);
  }
}

// Upload Form Submission
uploadForm.addEventListener('submit', async function (e) {
  e.preventDefault();
  const formData = new FormData(this);
  progressBar.style.display = 'block';
  progressFill.style.width = '0%';

  try {
    const xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percent = (e.loaded / e.total) * 100;
        progressFill.style.width = `${percent}%`;
      }
    });

    xhr.open('POST', '/upload');
    xhr.send(formData);

    xhr.onload = () => {
      progressBar.style.display = 'none';
      alert(xhr.responseText);
    };

    xhr.onerror = () => {
      progressBar.style.display = 'none';
      alert('Upload failed. Please try again.');
    };
  } catch (error) {
    progressBar.style.display = 'none';
    alert('An error occurred during upload.');
  }
});

// Query Form Submission
questionForm.addEventListener('submit', async function (e) {
  e.preventDefault();
  const question = document.getElementById('question-input').value;
  if (!question) return;

  loadingIndicator.classList.add('active');

  try {
    const res = await fetch('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();

    const responseCard = document.createElement('div');
    responseCard.className = 'response-card';
    responseCard.innerHTML = `
      <strong>Answer (${data.source}):</strong><br>${data.answer}
      ${data.title ? `<br><span class="source-snippet">From: ${data.title}</span>` : ''}
    `;
    responseBox.appendChild(responseCard);
    responseBox.scrollTop = responseBox.scrollHeight;
  } catch (error) {
    const errorCard = document.createElement('div');
    errorCard.className = 'response-card';
    errorCard.innerHTML = '<strong>Error:</strong><br>Failed to fetch response. Please try again.';
    responseBox.appendChild(errorCard);
  } finally {
    loadingIndicator.classList.remove('active');
    document.getElementById('question-input').value = '';
  }
});