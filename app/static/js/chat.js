
    const form = document.getElementById("question-form");
    const questionInput = document.getElementById("question");
    const chatBox = document.getElementById("chat-box");
    const askButton = form.querySelector("button[type='submit']");

    // STT Controls
    const recordBtn = document.getElementById("record-btn");
    const stopBtn = document.getElementById("stop-btn");
    const cancelBtn = document.getElementById("cancel-btn");

    let mediaRecorder;
    let recordedChunks = [];

    // Scroll to bottom
    function scrollToBottom() {
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const question = questionInput.value.trim();
      if (!question) return;

      askButton.disabled = true;

      // Display user message
      const userDiv = document.createElement("div");
      userDiv.className = "chat-message user";
      userDiv.innerHTML = `<div class="chat-bubble">${question}</div>`;
      chatBox.appendChild(userDiv);

      // Placeholder for AI response
      const aiDiv = document.createElement("div");
      aiDiv.className = "chat-message ai";
      const bubble = document.createElement("div");
      bubble.className = "chat-bubble";
      bubble.innerHTML = "🤖 ";
      aiDiv.appendChild(bubble);
      chatBox.appendChild(aiDiv);
      scrollToBottom();

      try {
        const response = await fetch("{{ url_for('chat.stream_chat', chat_id=chat.id) }}", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: question })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          bubble.innerHTML += chunk;
          scrollToBottom();
        }
      } catch (err) {
        bubble.innerHTML += `<br><span class="text-danger">❌ Error: ${err}</span>`;
      }

      questionInput.value = "";
      questionInput.focus();
      askButton.disabled = false;
    });

    // Start recording
    recordBtn.addEventListener("click", async () => {
      recordedChunks = [];
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) recordedChunks.push(e.data);
        };

        mediaRecorder.onstop = async () => {
          const blob = new Blob(recordedChunks, { type: 'audio/webm' });
          const formData = new FormData();
          formData.append("audio", blob);

          // POST to /transcribe endpoint (you must implement this backend)
          const response = await fetch("/transcribe", {
            method: "POST",
            body: formData
          });

          const result = await response.json();
          questionInput.value = result.text || "⚠️ No speech detected.";
        };

        mediaRecorder.start();
        recordBtn.textContent = "🎤 Recording...";
        recordBtn.classList.add("recording");
        stopBtn.style.display = "inline-block";
        cancelBtn.style.display = "inline-block";
        recordBtn.disabled = true;
      } catch (err) {
        alert("🎤 Microphone access denied.");
        console.error(err);
      }
    });

    // Stop and transcribe
    stopBtn.addEventListener("click", () => {
      mediaRecorder.stop();
      recordBtn.textContent = "🎤 Start";
      recordBtn.classList.remove("recording");
      recordBtn.disabled = false;
      stopBtn.style.display = "none";
      cancelBtn.style.display = "none";
    });

    // Cancel recording
    cancelBtn.addEventListener("click", () => {
      mediaRecorder.stop();
      recordedChunks = [];
      questionInput.value = "";
      recordBtn.textContent = "🎤 Start";
      recordBtn.classList.remove("recording");
      recordBtn.disabled = false;
      stopBtn.style.display = "none";
      cancelBtn.style.display = "none";
    });

    let currentUtterance = null;
    let currentId = null;

    document.querySelectorAll('.tts-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const text = btn.getAttribute('data-text');
        const id = btn.getAttribute('data-id');

        // Stop any current utterance
        if (currentUtterance) {
          speechSynthesis.cancel();
          document.querySelectorAll('.stop-tts-btn').forEach(b => b.style.display = 'none');
        }

        // Create and speak new utterance
        const utterance = new SpeechSynthesisUtterance(text);
        currentUtterance = utterance;
        currentId = id;

        // Show correct stop button
        const stopBtn = document.querySelector(`.stop-tts-btn[data-id="${id}"]`);
        stopBtn.style.display = 'inline-block';

        // Hide stop button when speech ends
        utterance.onend = () => {
          stopBtn.style.display = 'none';
          currentUtterance = null;
          currentId = null;
        };

        speechSynthesis.speak(utterance);
      });
    });

    document.querySelectorAll('.stop-tts-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        if (currentUtterance && currentId === btn.getAttribute('data-id')) {
          speechSynthesis.cancel();
          btn.style.display = 'none';
          currentUtterance = null;
          currentId = null;
        }
      });
    });
