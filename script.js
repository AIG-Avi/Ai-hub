
// --- AI Hub Frontend Script ---
// Centralized chatbox widget logic, navigation, and UI enhancements

document.addEventListener('DOMContentLoaded', () => {
		// --- Navigation Smooth Scroll ---
		document.querySelectorAll('a[href^="#"]').forEach(link => {
			link.addEventListener('click', e => {
				const href = link.getAttribute('href');
				if (href.length > 1 && document.getElementById(href.slice(1))) {
					e.preventDefault();
					const target = document.getElementById(href.slice(1));
					window.scrollTo({
						top: target.offsetTop - 20,
						behavior: 'smooth'
					});
				}
			});
		});

		// --- Scroll-triggered fade-in for sections/cards ---
		function revealOnScroll() {
			document.querySelectorAll('.scroll-fadein').forEach(el => {
				const rect = el.getBoundingClientRect();
				if (rect.top < window.innerHeight - 60) {
					el.classList.add('visible');
				}
			});
		}
		window.addEventListener('scroll', revealOnScroll);
		window.addEventListener('load', revealOnScroll);

	// --- Chatbox Widget Logic ---
	// Selectors match index.html
	const chatboxWidget = document.getElementById('chatbox-widget');
	const chatboxFloatBtn = document.getElementById('chatbox-float-btn');
	const chatboxClose = document.getElementById('chatbox-close');
	const chatboxForm = document.getElementById('chatbox-form');
	const chatboxInput = document.getElementById('chatbox-input');
	const chatboxHistory = document.getElementById('chatbox-history');

	// --- Floating Button: Toggle Chatbox ---
		chatboxFloatBtn.addEventListener('click', () => {
			chatboxWidget.classList.toggle('hidden');
			if (!chatboxWidget.classList.contains('hidden')) {
				chatboxWidget.classList.add('chatbox-slidein');
				chatboxInput.focus();
			}
		});

	// --- Close Button: Hide Chatbox ---
	chatboxClose.addEventListener('click', () => {
		chatboxWidget.classList.add('hidden');
	});

	// --- Message Appending Logic ---
	function addMessage(text, sender) {
		// sender: 'user' or 'bot'
		const msgDiv = document.createElement('div');
		msgDiv.className = `chatbox-message ${sender}`;
		const bubble = document.createElement('div');
		bubble.className = 'chatbox-bubble';
		bubble.textContent = text;
		msgDiv.appendChild(bubble);
		chatboxHistory.appendChild(msgDiv);
		chatboxHistory.scrollTop = chatboxHistory.scrollHeight;
	}

	// --- Typing Indicator ---
	function showTypingEffect() {
		const typingDiv = document.createElement('div');
		typingDiv.className = 'chatbox-message bot';
		typingDiv.id = 'chatbox-typing';
		const bubble = document.createElement('div');
		bubble.className = 'chatbox-bubble';
		bubble.textContent = 'Thinking...';
		typingDiv.appendChild(bubble);
		chatboxHistory.appendChild(typingDiv);
		chatboxHistory.scrollTop = chatboxHistory.scrollHeight;
	}
	function removeTypingEffect() {
		const typingDiv = document.getElementById('chatbox-typing');
		if (typingDiv) chatboxHistory.removeChild(typingDiv);
	}

	// --- Chatbox Form Submission ---
		chatboxForm.addEventListener('submit', function(e) {
			e.preventDefault();
			const question = chatboxInput.value.trim();
			if (!question || /[<>]/.test(question)) return;
			addMessage(question, 'user');
			chatboxInput.value = '';
			showTypingEffect();
			setTimeout(() => {
				removeTypingEffect();
				addMessage('This is a demo response. Connect to backend for real answers.', 'bot');
			}, 1200);
		});

	// --- Enter Key Submits Message ---
	chatboxInput.addEventListener('keydown', e => {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			chatboxForm.dispatchEvent(new Event('submit'));
		}
	});

	// --- Responsive: Hide on mobile nav open (optional) ---
	// Add logic here if you have a mobile nav menu

	// --- Accessibility: Focus trap (optional) ---
	// Add logic here for keyboard navigation if needed

	// --- UI Consistency: Ensure chatbox is hidden on load ---
	chatboxWidget.classList.add('hidden');

	// --- Section/Card Layout Validation ---
	// All cards/grids use Tailwind classes in index.html, so no extra JS needed

	// --- Code Comments ---
	// All event listeners and DOM manipulation are explained above
});
