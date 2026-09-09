/**
 Pathology Disease Prediction & Treatment Recommendation System
 Frontend Client Controller 
 */

// Realistic clinical test samples for quick 1-click evaluation
const CLINICAL_SAMPLES = {
    anemia: {
        sex: '1',          // Male
        hbsag: '0',        // Negative
        hemoglobin: '10.5',// Low Hb indicates Anemia (< 13 g/dL for male)
        rbs: '5.5',
        creatinine: '0.95',
        esr: '45.0',
        wbc: '6200'
    },
    diabetes: {
        sex: '0',          // Female
        hbsag: '0',        // Negative
        hemoglobin: '13.0',
        rbs: '22.4',       // Elevated RBS indicates Diabetes (> 11.1 mmol/L)
        creatinine: '0.85',
        esr: '14.0',
        wbc: '7100'
    },
    hepatitis: {
        sex: '1',          // Male
        hbsag: '1',        // Reactive HBsAg indicates Hepatitis B infection
        hemoglobin: '15.2',
        rbs: '5.2',
        creatinine: '0.90',
        esr: '16.0',
        wbc: '6800'
    },
    normal: {
        sex: '0',          // Female
        hbsag: '0',        // Negative
        hemoglobin: '13.5',// All laboratory metrics within healthy reference ranges
        rbs: '5.1',
        creatinine: '0.80',
        esr: '10.0',
        wbc: '6500'
    }
};

/**
 * Fills the pathology form fields with one of the predefined clinical samples
 * @param {string} sampleKey - Key of the sample ('anemia', 'diabetes', 'hepatitis', 'normal')
 */
function fillSample(sampleKey) {
    const sample = CLINICAL_SAMPLES[sampleKey];
    if (!sample) return;

    document.getElementById('sex').value = sample.sex;
    document.getElementById('hbsag').value = sample.hbsag;
    document.getElementById('hemoglobin').value = sample.hemoglobin;
    document.getElementById('rbs').value = sample.rbs;
    document.getElementById('creatinine').value = sample.creatinine;
    document.getElementById('esr').value = sample.esr;
    document.getElementById('wbc').value = sample.wbc;
}

/**
 * Resets all form fields to blank defaults
 */
function clearForm() {
    const form = document.getElementById('predict-form');
    if (form) {
        form.reset();
    }
}

/**
 * Initializes form submission listener on DOM load
 */
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('predict-form');
    if (!form) return;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const loadingIndicator = document.getElementById('loading');
        const submitButton = document.querySelector('.btn-predict');

        // Show loading spinner and disable submit button to prevent duplicate submissions
        if (loadingIndicator) loadingIndicator.style.display = 'block';
        if (submitButton) submitButton.disabled = true;

        const formData = new FormData(form);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            // Hide loading indicator
            if (loadingIndicator) loadingIndicator.style.display = 'none';

            if (data.success) {
                renderResults(data);
            } else {
                alert('Prediction Error: ' + (data.error || 'An unexpected error occurred.'));
                if (submitButton) submitButton.disabled = false;
            }
        } catch (error) {
            if (loadingIndicator) loadingIndicator.style.display = 'none';
            alert('Connection Error: Unable to reach the server. Please ensure the Flask app is running.');
            if (submitButton) submitButton.disabled = false;
        }
    });
});

/**
 * Renders diagnostic results and recommendations into the results container
 * @param {Object} data - Prediction payload returned from /predict endpoint
 */
function renderResults(data) {
    // Hide form card and display results area
    const formCard = document.getElementById('form-card');
    const resultArea = document.getElementById('result-area');
    if (formCard) formCard.style.display = 'none';
    if (resultArea) resultArea.style.display = 'block';

    const isNormal = data.is_normal || (data.diseases && data.diseases.includes('Normal'));
    const headerElement = document.getElementById('result-header');

    if (isNormal) {
        headerElement.className = 'result-header normal';
        headerElement.innerHTML = `
            <h2>All Laboratory Parameters Normal</h2>
            <p>No pathological diseases detected. Patient's lab values fall within healthy reference limits.</p>
        `;
    } else {
        headerElement.className = 'result-header has-disease';
        headerElement.innerHTML = `
            <h2>${data.count} Pathological Condition(s) Detected</h2>
            <p>Potential health risks flagged by the model. Please review the clinical recommendations below.</p>
        `;
    }

    const cardsContainer = document.getElementById('disease-cards');
    cardsContainer.innerHTML = '';

    // If completely normal, display the healthy summary card
    if (isNormal) {
        const normalInfo = data.treatments[0] || {};
        const adviceTags = (normalInfo.advice || [])
            .map(item => `<span class="tag adv">${item}</span>`)
            .join('');

        cardsContainer.innerHTML = `
            <div class="normal-card">
                <div class="big-icon">${normalInfo.icon || '✅'}</div>
                <h3>Healthy Physiological Profile</h3>
                <p>${normalInfo.description || 'All clinical parameters are within baseline medical ranges.'}</p>
                <div style="margin-top: 1.25rem;">
                    <div class="tag-list" style="justify-content: center;">
                        ${adviceTags}
                    </div>
                </div>
            </div>
        `;

        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
    }

    // Render individual cards for each detected condition
    data.diseases.forEach((diseaseName, index) => {
        const info = data.treatments[index];
        if (!info) return;

        const medicineTags = (info.medicines || [])
            .map(med => `<span class="tag med">${med}</span>`)
            .join('');

        const adviceTags = (info.advice || [])
            .map(adv => `<span class="tag adv">${adv}</span>`)
            .join('');

        const card = document.createElement('div');
        card.className = 'disease-card';
        card.style.borderColor = info.color;

        card.innerHTML = `
            <div class="disease-card-header" style="background: ${info.color};">
                <span class="icon">${info.icon}</span>
                <div>
                    <div class="name">${diseaseName}</div>
                    <div class="desc">${info.description}</div>
                </div>
            </div>
            <div class="disease-card-body">
                <div class="info-section">
                    <h4>💊 Recommended Medications & Interventions</h4>
                    <div class="tag-list">
                        ${medicineTags}
                    </div>
                </div>
                <div class="info-section">
                    <h4>📋 Clinical & Lifestyle Advice</h4>
                    <div class="tag-list">
                        ${adviceTags}
                    </div>
                </div>
            </div>
        `;

        cardsContainer.appendChild(card);
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Returns the interface to the patient input form for a new prediction
 */
function resetForm() {
    const formCard = document.getElementById('form-card');
    const resultArea = document.getElementById('result-area');

    if (formCard) formCard.style.display = 'block';
    if (resultArea) resultArea.style.display = 'none';

    const submitButton = document.querySelector('.btn-predict');
    if (submitButton) {
        submitButton.disabled = false;
    }

    const form = document.getElementById('predict-form');
    if (form) {
        form.reset();
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
}
