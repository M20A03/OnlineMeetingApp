// basic client-side helpers for the simple prototype

document.addEventListener('DOMContentLoaded', function () {
  // Example: simple form validation can be added here
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      // we rely on required attributes; extra checks here if needed
    });
  }

  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', function (e) {
      // basic password length check
      const pw = registerForm.querySelector('input[name="password"]').value;
      if (pw.length < 4) {
        e.preventDefault();
        alert('Password should be at least 4 characters (for demo).');
      }
    });
  }

  const createForm = document.getElementById('createForm');
  if (createForm) {
    createForm.addEventListener('submit', function (e) {
      // basic date/time presence checks are already required
    });
  }

  // --- Interactive Meeting Controls & Chat Logic ---
  const toggleMicBtn = document.getElementById('toggleMicBtn');
  const selfAvatar = document.getElementById('selfAvatar');
  const selfMicIcon = document.getElementById('selfMicIcon');
  let isMuted = false;

  if (toggleMicBtn) {
    toggleMicBtn.addEventListener('click', function () {
      isMuted = !isMuted;
      if (isMuted) {
        toggleMicBtn.classList.add('active-muted');
        toggleMicBtn.querySelector('.icon').textContent = '🔇';
        toggleMicBtn.querySelector('.label').textContent = 'Unmute';
        if (selfAvatar) selfAvatar.style.animation = 'none';
        if (selfMicIcon) selfMicIcon.textContent = '🔇';
      } else {
        toggleMicBtn.classList.remove('active-muted');
        toggleMicBtn.querySelector('.icon').textContent = '🎙️';
        toggleMicBtn.querySelector('.label').textContent = 'Mute';
        if (selfAvatar) selfAvatar.style.animation = 'pulse-ring 2s infinite ease-in-out';
        if (selfMicIcon) selfMicIcon.textContent = '🎤';
      }
    });
  }

  const toggleCamBtn = document.getElementById('toggleCamBtn');
  let isCamOff = false;
  if (toggleCamBtn) {
    toggleCamBtn.addEventListener('click', function () {
      isCamOff = !isCamOff;
      if (isCamOff) {
        toggleCamBtn.classList.add('active-muted');
        toggleCamBtn.querySelector('.icon').textContent = '🚫';
        toggleCamBtn.querySelector('.label').textContent = 'Start Video';
        if (selfAvatar) selfAvatar.style.opacity = '0.3';
      } else {
        toggleCamBtn.classList.remove('active-muted');
        toggleCamBtn.querySelector('.icon').textContent = '📹';
        toggleCamBtn.querySelector('.label').textContent = 'Stop Video';
        if (selfAvatar) selfAvatar.style.opacity = '1';
      }
    });
  }

  const toggleScreenBtn = document.getElementById('toggleScreenBtn');
  let isScreenSharing = false;
  if (toggleScreenBtn) {
    toggleScreenBtn.addEventListener('click', function () {
      isScreenSharing = !isScreenSharing;
      if (isScreenSharing) {
        toggleScreenBtn.classList.add('active-muted');
        toggleScreenBtn.querySelector('.label').textContent = 'Stop Share';
      } else {
        toggleScreenBtn.classList.remove('active-muted');
        toggleScreenBtn.querySelector('.label').textContent = 'Share';
      }
    });
  }

  const toggleChatBtn = document.getElementById('toggleChatBtn');
  const chatSidebar = document.getElementById('chatSidebar');
  if (toggleChatBtn && chatSidebar) {
    toggleChatBtn.addEventListener('click', function () {
      chatSidebar.style.display = chatSidebar.style.display === 'none' ? 'flex' : 'none';
    });
  }

  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const chatMessages = document.getElementById('chatMessages');
  const chatCount = document.getElementById('chatCount');
  let messageCount = 2;

  if (chatForm && chatInput && chatMessages) {
    chatForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (!text) return;

      messageCount++;
      const bubble = document.createElement('div');
      bubble.className = 'msg-bubble';
      bubble.innerHTML = `<span class="msg-author">You</span><p class="msg-text">${escapeHtml(text)}</p>`;
      chatMessages.appendChild(bubble);
      chatMessages.scrollTop = chatMessages.scrollHeight;
      chatInput.value = '';
      if (chatCount) chatCount.textContent = `${messageCount} messages`;

      // Simulated auto-acknowledgement after 1.2s
      setTimeout(function () {
        messageCount++;
        const reply = document.createElement('div');
        reply.className = 'msg-bubble';
        reply.innerHTML = `<span class="msg-author" style="color: #10B981;">AI Assistant</span><p class="msg-text">Noted: "${escapeHtml(text)}"</p>`;
        chatMessages.appendChild(reply);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        if (chatCount) chatCount.textContent = `${messageCount} messages`;
      }, 1200);
    });
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
});

