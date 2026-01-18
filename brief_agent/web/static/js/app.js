document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const generateForm = document.getElementById('generateForm');
    const briefsGrid = document.getElementById('briefsGrid');
    const modal = document.getElementById('briefModal');
    const modalBody = document.getElementById('modalBody');
    const modalTitle = document.getElementById('modalTitle');
    const closeModal = document.getElementById('closeModal');
    const refreshBtn = document.getElementById('refreshBtn');
    const generateBtn = document.getElementById('generateBtn');
    const spinner = generateBtn.querySelector('.spinner');
    const statusMsg = document.getElementById('statusMsg');
    const copyBtn = document.getElementById('copyBtn');

    // Default Date
    document.getElementById('date').valueAsDate = new Date();

    // Load Briefs on start
    fetchBriefs();

    // Event Listeners
    refreshBtn.addEventListener('click', fetchBriefs);
    closeModal.addEventListener('click', () => modal.classList.add('hidden'));
    
    // Close modal on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    });

    copyBtn.addEventListener('click', () => {
        const text = modalBody.innerText;
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = 'Copied!';
            setTimeout(() => copyBtn.textContent = 'Copy text', 2000);
        });
    });

    // Handle Generation
    generateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(generateForm);
        const data = {
            ticker: formData.get('ticker'),
            date: formData.get('date'),
            mode: formData.get('mode')
        };

        // UI State: Loading
        generateBtn.disabled = true;
        spinner.classList.remove('hidden');
        statusMsg.textContent = "Generating brief... this may take a moment.";
        statusMsg.style.color = "var(--text-secondary)";

        try {
            const res = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                statusMsg.textContent = "Generation started! refreshing shortly...";
                statusMsg.style.color = "var(--success)";
                
                // Poll for updates a few times
                let checks = 0;
                const interval = setInterval(async () => {
                    await fetchBriefs();
                    checks++;
                    if (checks > 10) clearInterval(interval);
                }, 2000);
            } else {
                throw new Error("API Error");
            }
        } catch (err) {
            console.error(err);
            statusMsg.textContent = "Error starting generation.";
            statusMsg.style.color = "var(--danger)";
        } finally {
            setTimeout(() => {
                generateBtn.disabled = false;
                spinner.classList.add('hidden');
            }, 2000);
        }
    });

    // Function to fetch and display briefs
    async function fetchBriefs() {
        try {
            const res = await fetch('/api/briefs');
            const briefs = await res.json();
            
            briefsGrid.innerHTML = '';
            
            if (briefs.length === 0) {
                briefsGrid.innerHTML = '<div class="loading-state">No briefs found. Generate one!</div>';
                return;
            }

            briefs.forEach(brief => {
                const card = createBriefCard(brief);
                briefsGrid.appendChild(card);
            });
        } catch (err) {
            console.error("Failed to fetch briefs", err);
            briefsGrid.innerHTML = '<div class="loading-state">Error loading briefs.</div>';
        }
    }

    function createBriefCard(brief) {
        const div = document.createElement('div');
        div.className = 'brief-card';
        div.innerHTML = `
            <h3>${brief.ticker}</h3>
            <span class="date">${brief.date}</span>
            <div class="preview">Click to view content...</div>
        `;
        div.addEventListener('click', () => openModal(brief.filename));
        return div;
    }

    async function openModal(filename) {
        modal.classList.remove('hidden');
        modalBody.innerHTML = 'Loading content...';
        modalTitle.textContent = filename;

        try {
            // Prefer MD view if available, we'll try to find the matching MD file
            // But the API lists JSON. Let's just guess the MD name or fetch JSON content
            // The API logic returns content based on extension.
            // Let's try to fetch the .md version if we clicked a json one, or just fetch what we have.
            
            const target = filename.replace('.json', '.md');
            let res = await fetch(`/api/briefs/${target}`);
            
            if (!res.ok) {
                // Fallback to original filename
                res = await fetch(`/api/briefs/${filename}`);
            }

            const data = await res.json();
            
            if (data.content) {
                modalBody.textContent = data.content; // It's MD string
            } else {
                modalBody.textContent = JSON.stringify(data, null, 2); // It's JSON object
            }

        } catch (err) {
            modalBody.textContent = "Error loading content.";
        }
    }
});
