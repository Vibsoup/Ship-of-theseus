const replacementSlider = document.querySelector('#replacement');
const replacementOutput = document.querySelector('#replacement-output');
const stagePercent = document.querySelector('#stage-percent');
const shipStage = document.querySelector('#ship-stage');
const identitySlider = document.querySelector('#identity');
const identityOutput = document.querySelector('#identity-output');
const submitButton = document.querySelector('#submit-response');
const statusMessage = document.querySelector('#status');
const responseCount = document.querySelector('#response-count');

function updateReplacement() {
  const percent = Number(replacementSlider.value);
  replacementOutput.value = `${percent}%`;
  stagePercent.textContent = `${percent}% REPLACED`;
  shipStage.dataset.replacement = String(percent);
}

function updateIdentity() {
  identityOutput.value = `${identitySlider.value} / 100`;
}

function selectedValue(name) {
  return document.querySelector(`input[name="${name}"]:checked`).value;
}

async function loadSummary() {
  try {
    const response = await fetch('/api/summary');
    if (!response.ok) return;
    const summary = await response.json();
    responseCount.textContent = summary.response_count;
  } catch {
    responseCount.textContent = '—';
  }
}

async function submitResponse() {
  submitButton.disabled = true;
  statusMessage.classList.remove('error');
  statusMessage.textContent = 'Saving your judgment…';

  const payload = {
    object_type: 'ship',
    replacement_percent: Number(replacementSlider.value),
    continuity: selectedValue('continuity'),
    appearance_preserved: selectedValue('appearance_preserved'),
    history_preserved: selectedValue('history_preserved'),
    function_preserved: selectedValue('function_preserved'),
    identity_rating: Number(identitySlider.value),
    explanation: document.querySelector('#explanation').value,
  };

  try {
    const response = await fetch('/api/responses', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Could not save your response.');
    statusMessage.textContent = result.message;
    document.querySelector('#explanation').value = '';
    await loadSummary();
  } catch (error) {
    statusMessage.classList.add('error');
    statusMessage.textContent = `${error.message} Please try again.`;
  } finally {
    submitButton.disabled = false;
  }
}

replacementSlider.addEventListener('input', updateReplacement);
identitySlider.addEventListener('input', updateIdentity);
submitButton.addEventListener('click', submitResponse);
updateReplacement();
updateIdentity();
loadSummary();
