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

        if (!res.ok && res.status !== 200) {
            resultDiv.style.opacity = '1';
            resultDiv.innerHTML = `<div class="result-card fade-in" style="border-color: #f87171;"><p style="color:#f87171;">⚠️ Server error (${res.status}). Please try again.</p></div>`;
            return;
        }

        // Backend returns status field even on 200 for logical errors
        if (data.status === 'error') {
            resultDiv.style.opacity = '1';
            resultDiv.innerHTML = `<div class="result-card fade-in" style="border-color: #fbbf24;"><p style="color:#fbbf24; font-weight:600;">⚠️ ${data.detail || 'Analysis failed. Please try again.'}</p></div>`;
            return;
        }

        resultDiv.style.opacity = '1';
        const score = data.maturity_score || 0;
        const pct   = (score / 10) * 100;  // score is 0-10, bar is 0-100%
        const col   = score >= 7 ? '#4ade80' : score >= 4 ? '#fbbf24' : '#f87171';

            const strengthsHTML = (data.strengths || []).map(s =>
                `<li><span class="check-icon">✓</span>${s}</li>`).join('');
            const gapsHTML = (data.skill_gaps || []).map(g =>
                `<li><span class="gap-icon">▲</span>${g}</li>`).join('');
            const toolsHTML = (data.technologies_used || []).map(l =>
                `<span class="lang-pill">${l}</span>`).join('');
            const reposHTML = (data.top_3_repos || []).map(r =>
                `<div class="stat-chip" style="margin-right: 8px;">📁 ${r}</div>`).join('');

            resultDiv.innerHTML = `
                <div class="result-card fade-in">
                    <div class="result-header">
                        <img src="${data.avatar_url}" class="avatar" alt="${data.username}"
                             onerror="this.src='https://github.com/identicons/${data.username}.png'">
                        <div class="header-text">
                            <h2>${data.username}</h2>
                            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px;">
                                <span class="badge">Profile: ${data.github_profile_level || 'Unknown'}</span>
                                <span class="badge" style="background: rgba(74, 222, 128, 0.15); color: #4ade80;">Code: ${data.coding_skills_level || 'Unknown'}</span>
                                <span class="badge" style="background: rgba(168, 85, 247, 0.15); color: #c084fc;">Projects: ${data.project_quality_level || 'Unknown'}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin: 16px 0; display: flex; flex-wrap: wrap; gap: 8px;">
                        ${reposHTML}
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

                    <div class="tech-section" style="margin-bottom: 24px;">
                        <p class="section-label">Tools & Technologies Used</p>
                        <div class="lang-pills">${toolsHTML}</div>
                    </div>
                    
                    <div class="tech-section" style="margin-bottom: 24px;">
                        <p class="section-label">Open Source Contributions</p>
                        <p style="color: var(--dim); margin-top: 8px;">${data.open_source_contributions || 'No significant open source contributions detected.'}</p>
                    </div>

                    <div class="insight-box">
                        <p class="section-label">AI Audit</p>
                        <p>${data.insights}</p>
                    </div>

                    <div class="insight-box" style="border-left-color: #fbbf24; margin-top: 16px;">
                        <p class="section-label" style="color: #fbbf24;">How Active is ${data.username}?</p>
                        <p>${data.activity_overview || "Analyzing recent contribution frequency, code pushes, and issue activity to determine engagement level..."}</p>
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

                    ${data.matched_mentor ? `
                    <div class="match-box fade-in" style="margin-top: 24px; border-color: rgba(64,138,113,0.3); background: rgba(64,138,113,0.05);">
                        <p class="section-label" style="color: var(--primary);">🎯 Your Perfect Mentor Match</p>
                        <div style="display:flex; align-items:center; gap:20px; margin-top:16px;">
                            <img src="${data.matched_mentor.avatar_url}" style="width:70px; height:70px; border-radius:50%; border: 2px solid var(--primary);">
                            <div>
                                <h4 style="margin:0 0 4px 0; font-size:1.2rem; color:var(--bright);">${data.matched_mentor.name}</h4>
                                <p style="margin:0 0 10px 0; color:var(--text); font-size:0.95rem;">${data.matched_mentor.title} @ <strong style="color:var(--bright);">${data.matched_mentor.company}</strong></p>
                                <div style="display:flex; gap:6px; flex-wrap:wrap;">
                                    ${data.matched_mentor.tech_stack.map(t => `<span class="lang-pill" style="font-size:0.75rem; padding:2px 8px;">${t}</span>`).join('')}
                                </div>
                            </div>
                        </div>
                    </div>` : `
                    <div class="match-box">
                        <p class="section-label">Recommended Mentor</p>
                        <p class="mentor-title">🎯 ${data.mentor_match}</p>
                    </div>`}
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
            resultDiv.style.opacity = '1';
            resultDiv.innerHTML = `<div class="result-card fade-in" style="border-color: #f87171;"><p style="color:#f87171; font-weight:600;">⚠️ ${data.detail || 'Analysis failed. Please check the username and try again.'}</p></div>`;
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

// ==========================================
// GOOGLE SIGN-IN IMPLEMENTATION
// ==========================================
// 1. You MUST replace this with a real Client ID from Google Cloud Console
const GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com";
let tokenClient;

window.addEventListener('load', () => {
    // Initialize Google Identity Services
    if (typeof google !== "undefined" && google.accounts) {
        tokenClient = google.accounts.oauth2.initTokenClient({
            client_id: GOOGLE_CLIENT_ID,
            scope: "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
            callback: (tokenResponse) => {
                if (tokenResponse && tokenResponse.access_token) {
                    // Fetch real user info from Google
                    fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
                        headers: { Authorization: `Bearer ${tokenResponse.access_token}` }
                    })
                    .then(res => res.json())
                    .then(user => {
                        updateSignInUI(user.given_name, user.picture);
                    })
                    .catch(err => console.error("Error fetching user info:", err));
                }
            }
        });
    }
});

function handleGoogleSignIn() {
    if (!tokenClient) {
        alert("Google Sign-In failed to load. Check your internet connection or ad-blocker.");
        return;
    }

    if (GOOGLE_CLIENT_ID === "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com") {
        alert("Action Required: Real Google OAuth is hooked up, but you need to paste your Client ID into frontend/script.js!\n\n(Clicking 'OK' will show the visual mock for the hackathon demo.)");
        updateSignInUI("Guest", "https://ui-avatars.com/api/?name=Guest+User&background=408A71&color=fff");
        return;
    }

    // Opens the actual Google popup flow
    tokenClient.requestAccessToken();
}

function updateSignInUI(firstName, pictureUrl) {
    const btn = document.getElementById('nav-cta-btn');
    btn.innerHTML = `<img src="${pictureUrl}" style="width:20px; height:20px; border-radius:50%; vertical-align:-5px; margin-right:6px; object-fit:cover;">${firstName}`;
    btn.style.background = "transparent";
    btn.style.color = "var(--bright)";
    btn.style.borderColor = "var(--primary)";
    btn.onclick = null; // Prevent re-clicking
}