async function fetchJsonFiles() {
    const response = await fetch('/__ScrapedData__/');
    const text = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(text, 'text/html');
    const files = Array.from(doc.querySelectorAll('a'))
        .map(a => a.href.split('/').pop())
        .filter(name => name.endsWith('.json'))
        .sort((a, b) => {
            const [prefixA, numA] = a.match(/([^\d]+)(\d+)/).slice(1);
            const [prefixB, numB] = b.match(/([^\d]+)(\d+)/).slice(1);
            if (prefixA === prefixB) {
                return parseInt(numA, 10) - parseInt(numB, 10);
            }
            return prefixA.localeCompare(prefixB);
        });

    const select = document.getElementById('file-select');
    files.forEach(file => {
        const option = document.createElement('option');
        option.value = file;
        option.textContent = file.replace(/_/g, ' ').replace('.json', '');
        select.appendChild(option);
    });
}

async function loadJsonData() {
    const container = document.getElementById('data-container');
    container.innerHTML = '';

    const select = document.getElementById('file-select');
    const filename = select.value;
    if (!filename) return;

    const response = await fetch(`/__ScrapedData__/${filename}`);
    const data = await response.json();

    data.forEach(item => {
        const div = document.createElement('div');
        div.className = 'item';

        const img = document.createElement('img');
        img.src = item.image;
        img.alt = item.title;
        img.className = 'thumbnail';
        img.onclick = () => playVideo(item.Video_URL);

        const title = document.createElement('p');
        title.textContent = item.title;

        div.appendChild(img);
        div.appendChild(title);
        container.appendChild(div);
    });
}

function playVideo(videoUrl) {
    const videoPlayer = document.getElementById('video-player');
    const videoContainer = document.getElementById('video-container');
    const downloadButton = document.getElementById('download-button');
    videoPlayer.src = videoUrl;
    videoContainer.style.display = 'block';
    videoPlayer.style.display = 'block'; // Ensure the video player is visible
    downloadButton.href = videoUrl;
    downloadButton.style.display = 'block'; // Show the download button
    videoPlayer.play();

    videoContainer.onclick = (e) => {
        if (e.target === videoContainer) {
            videoPlayer.pause();
            videoPlayer.style.display = 'none';
            videoContainer.style.display = 'none';
            downloadButton.style.display = 'none'; // Hide the download button
        }
    };
}

fetchJsonFiles();