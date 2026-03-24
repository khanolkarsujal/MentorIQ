async function analyzeProfile() {
    const input = document.querySelector('.github-input');
    const button = document.querySelector('.analyze-btn');
    const resultDiv = document.getElementById('result-display');
    let inputVal = input.value.trim();

    // 1. URL Cleanup: Extract username if they paste a full link
    if (inputVal.includes("github.com/")) {
        // Splits by 'github.com/', takes the last part, and removes any trailing slashes
        inputVal = inputVal.split("github.com/").pop().split("/")[0].split("?")[0];
    }

    const username = inputVal;
    if (!username) return alert("Please enter a GitHub username.");

    // 2. UI Loading State
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Analyzing Code...';
    resultDiv.style.opacity = "0.5"; // Dim current results while loading

    try {
        const response = await fetch(`/api/analyze?username=${encodeURIComponent(username)}`);
        const data = await response.json();

        if (response.ok) {
            // 3. Update the UI with the AI Audit results
            resultDiv.style.opacity = "1";
            resultDiv.innerHTML = `
                <div class="result-card fade-in">
                    <div class="result-header">
                        <img src="${data.avatar_url}" class="avatar" alt="GitHub Avatar">
                        <div class="header-text">
                            <h2>${data.username}</h2>
                            <span class="badge">${data.skill_level}</span>
                        </div>
                    </div>
                    
                    <div class="result-body">
                        <p class="stack-text"><strong>Stack:</strong> ${data.top_languages.join(', ')}</p>
                        
                        <div class="insight-box">
                            <p><strong>AI Audit:</strong> ${data.insights}</p>
                        </div>
                        
                        <div class="match-box">
                            <p><strong>Recommended Mentor:</strong> ${data.mentor_match}</p>
                        </div>
                    </div>
                </div>
            `;
            // Scroll to the results automatically
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            alert(data.detail || "Analysis failed.");
        }
    } catch (error) {
        console.error("Fetch error:", error);
        alert("Server error. Make sure your Python backend is running!");
    } finally {
        button.disabled = false;
        button.innerHTML = 'Analyze Profile';
    }
}