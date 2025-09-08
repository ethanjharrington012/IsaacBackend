// Basic form handling for GitHub Pages (no backend).
// To enable real submissions, create a free Formspree form and paste the endpoint below.
const FORM_ENDPOINT = ""; // e.g., "https://formspree.io/f/yourFormId"

const form = document.getElementById('signup-form');
const msg = document.getElementById('form-message');
const year = document.getElementById('year');
year.textContent = new Date().getFullYear();

form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(form).entries());

  if (!formData.email || !String(formData.email).includes('@')) {
    msg.textContent = 'Please enter a valid email address.';
    msg.className = 'mt-3 text-sm text-red-300';
    return;
  }

  // If no endpoint, simulate success and guide setup.
  if (!FORM_ENDPOINT) {
    msg.innerHTML = 'Thanks! This demo stored your email locally. To collect real signups, add your Formspree endpoint in <code>assets/app.js</code>.';
    msg.className = 'mt-3 text-sm text-emerald-300';
    try {
      const stored = JSON.parse(localStorage.getItem('simplomation_signups') || '[]');
      stored.push({ ...formData, ts: Date.now() });
      localStorage.setItem('simplomation_signups', JSON.stringify(stored));
    } catch {}
    form.reset();
    return;
  }

  try {
    const res = await fetch(FORM_ENDPOINT, {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    });
    if (res.ok) {
      msg.textContent = 'Thanks! Please check your inbox for a confirmation.';
      msg.className = 'mt-3 text-sm text-emerald-300';
      form.reset();
    } else {
      msg.textContent = 'Something went wrong. Please try again later.';
      msg.className = 'mt-3 text-sm text-red-300';
    }
  } catch (err) {
    msg.textContent = 'Network error. Please try again.';
    msg.className = 'mt-3 text-sm text-red-300';
  }
});
