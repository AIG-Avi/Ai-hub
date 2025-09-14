// Chatbox UI logic and backend connection
const chatboxBtn = document.getElementById('chatbox-float-btn');
const chatboxWidget = document.getElementById('chatbox-widget');
const chatboxClose = document.getElementById('chatbox-close');
const chatboxForm = document.getElementById('chatbox-form');
const chatboxInput = document.getElementById('chatbox-input');
const chatboxHistory = document.getElementById('chatbox-history');

chatboxBtn.onclick = () => {
  chatboxWidget.classList.toggle('hidden');
  chatboxWidget.classList.toggle('flex-col');
};
chatboxClose.onclick = () => {
  chatboxWidget.classList.add('hidden');
  chatboxWidget.classList.remove('flex-col');
};

function addMessage(text, sender) {
  const msgDiv = document.createElement('div');
  msgDiv.className = 'chatbox-message ' + sender;
  const bubble = document.createElement('div');
  bubble.className = 'chatbox-bubble';
  bubble.textContent = text;
  msgDiv.appendChild(bubble);
  chatboxHistory.appendChild(msgDiv);
  chatboxHistory.scrollTop = chatboxHistory.scrollHeight;
}

function showTypingEffect() {
  const typingDiv = document.createElement('div');
  typingDiv.className = 'chatbox-message bot';
  const bubble = document.createElement('div');
  bubble.className = 'chatbox-bubble';
  bubble.textContent = 'AI is thinking...';
  typingDiv.appendChild(bubble);
  typingDiv.id = 'chatbox-typing';
  chatboxHistory.appendChild(typingDiv);
  chatboxHistory.scrollTop = chatboxHistory.scrollHeight;
}

function removeTypingEffect() {
  const typingDiv = document.getElementById('chatbox-typing');
  if (typingDiv) chatboxHistory.removeChild(typingDiv);
}

chatboxForm.onsubmit = async (e) => {
  e.preventDefault();
  const question = chatboxInput.value.trim();
  if (!question) return;
  addMessage(question, 'user');
  chatboxInput.value = '';
  showTypingEffect();
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    const data = await res.json();
    removeTypingEffect();
    addMessage(data.answer, 'bot');
  } catch (err) {
    removeTypingEffect();
    addMessage('Sorry, there was an error fetching the answer.', 'bot');
  }
};
// Enter key support
chatboxInput.addEventListener('keydown', function(e) {
  if (e.key === 'Enter') {
    chatboxForm.dispatchEvent(new Event('submit'));
  }
});
