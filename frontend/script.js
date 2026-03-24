function fillAndAnalyze(username) {
    document.getElementById('github-input').value = username;
    analyzeProfile();
}

async function analyzeProfile() {
    const input = document.getElementById('github-input');
    const button = document.getElementById('analyze-btn');
    const resultDiv = document.getElementById('result-display');

    let inputVal = input.value.trim();
    if (inputVal.includes("github.com/")) {
        inputVal = inputVal.split("github.com/").pop().split("/")[0].split("?")[0];
    }
    const username = inputVal;
    if (!username) { input.focus(); return; }

    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Auditing...';
    resultDiv.innerHTML = '';
    resultDiv.style.opacity = '0.5';

    try {
        const res = await fetch(`/api/analyze?username=${encodeURIComponent(username)}`);
        const data = await res.json();

        if (res.ok) {
            resultDiv.style.opacity = '1';
            const score = data.maturity_score || 0;
            const pct   = (score / 10) * 100;
            const col   = score >= 7 ? '#4ade80' : score >= 4 ? '#fbbf24' : '#f87171';

            const strengthsHTML = (data.strengths || []).map(s =>
                `<li><span class="check-icon">✓</span>${s}</li>`).join('');
            const gapsHTML = (data.skill_gaps || []).map(g =>
                `<li><span class="gap-icon">▲</span>${g}</li>`).join('');
            const langsHTML = (data.top_languages || []).map(l =>
                `<span class="lang-pill">${l}</span>`).join('');

            resultDiv.innerHTML = `
                <div class="result-card fade-in">
                    <div class="result-header">
                        <img src="${data.avatar_url}" class="avatar" alt="${data.username}"
                             onerror="this.src='https://github.com/identicons/${data.username}.png'">
                        <div class="header-text">
                            <h2>${data.username}</h2>
                            <span class="badge">${data.skill_level || 'Unknown'}</span>
                        </div>
                        <div class="stats-cluster">
                            ${data.total_repos ? `<div class="stat-chip">📁 ${data.total_repos} repos</div>` : ''}
                            ${data.stars ? `<div class="stat-chip">⭐ ${data.stars.toLocaleString()} stars</div>` : ''}
                        </div>
                    </div>

                    <div class="maturity-section">
                        <div class="maturity-label">
                            <span>Code Maturity Score</span>
                            <strong style="color:${col}">${score}<span style="font-size:1rem;font-weight:400;color:var(--dim)">/10</span></strong>
                        </div>
                        <div class="maturity-bar-bg">
                            <div class="maturity-bar-fill" style="width:0%;background:${col};"
                                 id="maturity-fill"></div>
                        </div>
                    </div>

                    <div class="tech-section">
                        <p class="section-label">Tech Stack</p>
                        <div class="lang-pills">${langsHTML}</div>
                    </div>

                    <div class="insight-box">
                        <p class="section-label">AI Audit</p>
                        <p>${data.insights}</p>
                    </div>

                    <div class="two-col">
                        <div class="strength-box">
                            <p class="section-label">Core Strengths</p>
                            <ul class="audit-list">${strengthsHTML}</ul>
                        </div>
                        <div class="gap-box">
                            <p class="section-label">Skill Gaps</p>
                            <ul class="audit-list">${gapsHTML}</ul>
                        </div>
                    </div>

                    <div class="match-box">
                        <p class="section-label">Recommended Mentor</p>
                        <p class="mentor-title">🎯 ${data.mentor_match}</p>
                    </div>
                </div>`;

            // Animate bar after render
            requestAnimationFrame(() => {
                setTimeout(() => {
                    const fill = document.getElementById('maturity-fill');
                    if (fill) fill.style.width = pct + '%';
                }, 100);
            });

            document.getElementById('result-display').scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            alert(data.detail || "Analysis failed. Please try again.");
        }
    } catch (err) {
        console.error("Fetch error:", err);
        alert("Could not reach the server. Ensure the backend is running.");
    } finally {
        button.disabled = false;
        button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="sparkles">
                <path d="M12 3l1.912 5.813a2 2 0 001.275 1.275L21 12l-5.813 1.912a2 2 0 00-1.275 1.275L12 21l-1.912-5.813a2 2 0 00-1.275-1.275L3 12l5.813-1.912a2 2 0 001.275-1.275L12 3z"></path>
            </svg>
            Analyze Profile`;
    }
}

// Enter key support
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('github-input');
    if (input) {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') analyzeProfile();
        });
    }
});