// A small, dependency-free front-end to submit the rendered form via fetch().
// It reads the form fields, builds a JSON payload and posts to the submitUrl exposed
// by the template (window.FORM_CONFIG.submitUrl). It expects a JSON response.

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function normalizeFormData(form) {
  // Convert FormData to plain object. Checkbox handling is simplified:
  const fd = new FormData(form);
  const obj = {};
  for (const [k, v] of fd.entries()) {
    // Many browsers send 'on' for checked checkboxes; preserve string for other inputs
    // If multiple fields with same name exist (checkbox groups) this will only keep last.
    // You can extend to support arrays if needed.
    obj[k] = v;
  }
  // convert checkbox 'on' to true if attribute input type=checkbox exists
  form.querySelectorAll('input[type="checkbox"]').forEach(input => {
    if (!(input.name in obj)) {
      obj[input.name] = false; // unchecked checkbox won't appear in FormData
    } else {
      // checkbox value might be 'on' or custom; normalize to boolean
      const val = obj[input.name];
      obj[input.name] = (val === 'on' || val === 'true');
    }
  });
  return obj;
}

async function submitHandler(e) {
  e.preventDefault();
  const form = e.target;
  const messages = document.getElementById('messages');
  messages.style.color = 'black';
  messages.innerText = 'Submitting...';

  const data = normalizeFormData(form);

  try {
    const resp = await fetch(window.FORM_CONFIG.submitUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(data)
    });

    if (resp.ok) {
      const j = await resp.json();
      if (j.ok) {
        messages.style.color = 'green';
        messages.innerText = 'Thanks — submission saved.';
        form.reset();
      } else {
        messages.style.color = 'crimson';
        messages.innerText = 'Server rejected submission.';
      }
    } else {
      const j = await resp.json().catch(() => null);
      messages.style.color = 'crimson';
      if (j && j.errors) {
        messages.innerText = 'Errors: ' + JSON.stringify(j.errors);
      } else {
        messages.innerText = 'Submission failed: ' + resp.statusText;
      }
    }
  } catch (err) {
    messages.style.color = 'crimson';
    messages.innerText = 'Network error: ' + err.message;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('dynamic-form');
  if (form) form.addEventListener('submit', submitHandler);
});
