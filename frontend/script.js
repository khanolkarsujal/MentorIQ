async function analyzeProfile() {
    const input = document.querySelector('.github-input');
    const button = document.querySelector('.analyze-btn');
    const resultDiv = document.getElementById('result-display');
    let inputVal = input.value.trim();

    // URL Cleanup: extract username if pasting a full GitHub link
    if (inputVal.includes("github.com/")) {
        inputVal = inputVal.split("github.com/").pop().split("/")[0].split("?")[0];
    }

    const username = inputVal;
    if (!username) return alert("Please enter a GitHub username.");

    // UI Loading State
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Auditing Code...';
    resultDiv.innerHTML = '';
    resultDiv.style.opacity = "0.5";

    try {
        const response = await fetch(`/api/analyze?username=${encodeURIComponent(username)}`);
        const data = await response.json();

        if (response.ok) {
            resultDiv.style.opacity = "1";

            // Build strengths list
            const strengthsHTML = (data.strengths || []).map(s =>
                `<li><span class="check-icon">✓</span>${s}</li>`
            ).join('');

            // Build skill gaps list
            const gapsHTML = (data.skill_gaps || []).map(g =>
                `<li><span class="gap-icon">▲</span>${g}</li>`
            ).join('');

            // Languages pills
            const langsHTML = (data.top_languages || []).map(l =>
                `<span class="lang-pill">${l}</span>`
            ).join('');

            // Maturity Score bar
            const score = data.maturity_score || 0;
            const scorePercent = (score / 10) * 100;
            const scoreColor = score >= 8 ? '#4ade80' : score >= 5 ? '#fbbf24' : '#f87171';

            resultDiv.innerHTML = `
                <div class="result-card fade-in">

                    <!-- Header -->
                    <div class="result-header">
                        <img src="${data.avatar_url}" class="avatar" alt="GitHub Avatar" onerror="this.src='https://github.com/identicons/${data.username}.png'">
                        <div class="header-text">
                            <h2>${data.username}</h2>
                            <span class="badge">${data.skill_level || 'Unknown'}</span>
                        </div>
                        <div class="stats-cluster">
                            ${data.total_repos ? `<div class="stat-chip">📁 ${data.total_repos} repos</div>` : ''}
                            ${data.stars ? `<div class="stat-chip">⭐ ${data.stars} stars</div>` : ''}
                        </div>
                    </div>

                    <!-- Maturity Score -->
                    <div class="maturity-section">
                        <div class="maturity-label">
                            <span>Code Maturity Score</span>
                            <strong style="color:${scoreColor}">${score}/10</strong>
                        </div>
                        <div class="maturity-bar-bg">
                            <div class="maturity-bar-fill" style="width:${scorePercent}%; background:${scoreColor};"></div>
                        </div>
                    </div>

                    <!-- Stack -->
                    <div class="tech-section">
                        <p class="section-label">Tech Stack</p>
                        <div class="lang-pills">${langsHTML}</div>
                    </div>

                    <!-- AI Audit Insights -->
                    <div class="insight-box">
                        <p class="section-label">AI Audit</p>
                        <p>${data.insights}</p>
                    </div>

                    <!-- Strengths & Gaps Side by Side -->
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

                    <!-- Mentor Match -->
                    <div class="match-box">
                        <p class="section-label">Recommended Mentor</p>
                        <p class="mentor-title">🎯 ${data.mentor_match}</p>
                    </div>

                </div>
            `;
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            alert(data.detail || "Analysis failed.");
        }
    } catch (error) {
        console.error("Fetch error:", error);
        alert("Server error. Make sure your Python backend is running!");
    } finally {
        button.disabled = false;
        button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round" class="sparkles">
                <path d="M12 3l1.912 5.813a2 2 0 001.275 1.275L21 12l-5.813 1.912a2 2 0 00-1.275 1.275L12 21l-1.912-5.813a2 2 0 00-1.275-1.275L3 12l5.813-1.912a2 2 0 001.275-1.275L12 3z"></path>
            </svg>
            Analyze Profile`;
    }
}