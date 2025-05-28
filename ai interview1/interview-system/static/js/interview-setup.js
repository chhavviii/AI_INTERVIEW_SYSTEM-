document.addEventListener('DOMContentLoaded', () => {
    const cameraPreview = document.getElementById('cameraPreview');
    const screenPreview = document.getElementById('screenPreview');
    const cameraBtn = document.getElementById('cameraBtn');
    const micBtn = document.getElementById('micBtn');
    const screenBtn = document.getElementById('screenBtn');
    const startInterviewBtn = document.getElementById('startInterviewBtn');
    const cameraStatus = document.getElementById('cameraStatus');
    const micStatus = document.getElementById('micStatus');
    const screenStatus = document.getElementById('screenStatus');
    const audioLevel = document.getElementById('audioLevel');

    let cameraStream = null;
    let micStream = null;
    let screenStream = null;

    // Camera handling
    cameraBtn.addEventListener('click', async () => {
        try {
            cameraStream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                } 
            });
            cameraPreview.srcObject = cameraStream;
            cameraStatus.textContent = 'Granted';
            cameraStatus.className = 'status-badge granted';
            cameraBtn.disabled = true;
            checkAllPermissions();
        } catch (err) {
            cameraStatus.textContent = 'Denied';
            cameraStatus.className = 'status-badge denied';
            alert('Camera access is required for the interview. Please allow camera access and try again.');
            console.error('Camera error:', err);
        }
    });

    // Microphone handling
    micBtn.addEventListener('click', async () => {
        try {
            micStream = await navigator.mediaDevices.getUserMedia({ 
                audio: true 
            });
            
            // Set up audio visualization
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createMediaStreamSource(micStream);
            const analyser = audioContext.createAnalyser();
            source.connect(analyser);
            
            analyser.fftSize = 256;
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);

            function updateAudioLevel() {
                analyser.getByteFrequencyData(dataArray);
                const average = dataArray.reduce((a, b) => a + b) / bufferLength;
                const level = Math.min(100, average * 2);
                audioLevel.style.width = `${level}%`;
                requestAnimationFrame(updateAudioLevel);
            }

            updateAudioLevel();
            micStatus.textContent = 'Granted';
            micStatus.className = 'status-badge granted';
            micBtn.disabled = true;
            checkAllPermissions();
        } catch (err) {
            micStatus.textContent = 'Denied';
            micStatus.className = 'status-badge denied';
            alert('Microphone access is required for the interview. Please allow microphone access and try again.');
            console.error('Microphone error:', err);
        }
    });

    // Screen sharing handling
    screenBtn.addEventListener('click', async () => {
        try {
            screenStream = await navigator.mediaDevices.getDisplayMedia({
                video: {
                    displaySurface: 'monitor',
                    logicalSurface: true,
                    cursor: 'always'
                }
            });

            const track = screenStream.getVideoTracks()[0];
            const settings = track.getSettings();

            if (settings.displaySurface !== 'monitor') {
                screenStream.getTracks().forEach(track => track.stop());
                alert('Please share your entire screen, not just a window or tab. Click "Share Screen" again and select "Screen" or "Entire Screen".');
                return;
            }

            screenPreview.srcObject = screenStream;
            screenStatus.textContent = 'Granted';
            screenStatus.className = 'status-badge granted';
            screenBtn.disabled = true;
            checkAllPermissions();

            screenStream.getVideoTracks()[0].addEventListener('ended', () => {
                screenPreview.srcObject = null;
                screenStatus.textContent = 'Denied';
                screenStatus.className = 'status-badge denied';
                screenBtn.disabled = false;
                checkAllPermissions();
            });
        } catch (err) {
            screenStatus.textContent = 'Denied';
            screenStatus.className = 'status-badge denied';
            console.error('Screen sharing error:', err);
            alert('Screen sharing is required for the interview. Please allow screen sharing and try again.');
        }
    });

    function checkAllPermissions() {
        const allGranted = 
            cameraStatus.textContent === 'Granted' &&
            micStatus.textContent === 'Granted' &&
            screenStatus.textContent === 'Granted';

        startInterviewBtn.disabled = !allGranted;
    }

    startInterviewBtn.addEventListener('click', () => {
        // Add your code to proceed to the interview page
        alert('All permissions granted! Starting interview...');
    });
});