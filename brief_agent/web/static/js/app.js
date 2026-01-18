document.addEventListener('DOMContentLoaded', () => {
    // Elementit
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
    const tickerInput = document.getElementById('ticker');
    const autocompleteList = document.getElementById('autocompleteList');

    // Oletuspäivämäärä
    document.getElementById('date').valueAsDate = new Date();

    // Lataa tiivistelmät käynnistyksen yhteydessä
    fetchBriefs();

    // Tapahtumakuuntelijat
    refreshBtn.addEventListener('click', fetchBriefs);
    closeModal.addEventListener('click', () => modal.classList.add('hidden'));

    // Sulje modaali klikkaamalla ulkopuolelle
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    });

    copyBtn.addEventListener('click', () => {
        const text = modalBody.innerText;
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = 'Kopioitu!';
            setTimeout(() => copyBtn.textContent = 'Kopioi teksti', 2000);
        });
    });

    // Ticker autocomplete
    let debounceTimer;
    tickerInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();

        if (query.length < 1) {
            autocompleteList.classList.add('hidden');
            return;
        }

        debounceTimer = setTimeout(async () => {
            try {
                const res = await fetch(`/api/tickers?q=${encodeURIComponent(query)}`);
                const tickers = await res.json();
                showAutocomplete(tickers);
            } catch (err) {
                console.error('Autocomplete error:', err);
            }
        }, 200);
    });

    // Sulje autocomplete kun klikataan muualle
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.autocomplete-wrapper')) {
            autocompleteList.classList.add('hidden');
        }
    });

    function showAutocomplete(tickers) {
        if (tickers.length === 0) {
            autocompleteList.classList.add('hidden');
            return;
        }

        autocompleteList.innerHTML = tickers.map(t => `
            <div class="autocomplete-item" data-ticker="${t.ticker}">
                <span class="ticker-symbol">${t.ticker}</span>
                <span class="ticker-name">${t.name}</span>
                <span class="ticker-market">${t.market}</span>
            </div>
        `).join('');

        autocompleteList.classList.remove('hidden');

        // Klikkaus-käsittelijät
        autocompleteList.querySelectorAll('.autocomplete-item').forEach(item => {
            item.addEventListener('click', () => {
                tickerInput.value = item.dataset.ticker;
                autocompleteList.classList.add('hidden');
            });
        });
    }

    // Tiivistelmän luonti
    generateForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(generateForm);
        const data = {
            ticker: formData.get('ticker'),
            date: formData.get('date'),
            mode: formData.get('mode')
        };

        // UI-tila: Lataus
        generateBtn.disabled = true;
        spinner.classList.remove('hidden');
        statusMsg.textContent = "Luodaan tiivistelmää... tämä voi kestää hetken.";
        statusMsg.style.color = "var(--text-secondary)";

        try {
            const res = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                statusMsg.textContent = "Luonti aloitettu! Päivitetään pian...";
                statusMsg.style.color = "var(--success)";

                // Tarkista päivitykset muutaman kerran
                let checks = 0;
                const interval = setInterval(async () => {
                    await fetchBriefs();
                    checks++;
                    if (checks > 10) clearInterval(interval);
                }, 2000);
            } else {
                throw new Error("API-virhe");
            }
        } catch (err) {
            console.error(err);
            statusMsg.textContent = "Virhe luonnissa.";
            statusMsg.style.color = "var(--danger)";
        } finally {
            setTimeout(() => {
                generateBtn.disabled = false;
                spinner.classList.add('hidden');
            }, 2000);
        }
    });

    // Hae ja näytä tiivistelmät
    async function fetchBriefs() {
        try {
            const res = await fetch('/api/briefs');
            const briefs = await res.json();

            briefsGrid.innerHTML = '';

            if (briefs.length === 0) {
                briefsGrid.innerHTML = '<div class="loading-state">Ei tiivistelmiä. Luo ensimmäinen!</div>';
                return;
            }

            briefs.forEach(brief => {
                const card = createBriefCard(brief);
                briefsGrid.appendChild(card);
            });
        } catch (err) {
            console.error("Tiivistelmien haku epäonnistui", err);
            briefsGrid.innerHTML = '<div class="loading-state">Virhe tiivistelmien latauksessa.</div>';
        }
    }

    function createBriefCard(brief) {
        const div = document.createElement('div');
        div.className = 'brief-card';
        div.innerHTML = `
            <h3>${brief.ticker}</h3>
            <span class="date">${brief.date}</span>
            <div class="preview">Klikkaa nähdäksesi sisällön...</div>
        `;
        div.addEventListener('click', () => openModal(brief.filename));
        return div;
    }

    async function openModal(filename) {
        modal.classList.remove('hidden');
        modalBody.innerHTML = 'Ladataan sisältöä...';
        modalTitle.textContent = filename;

        try {
            // Yritä hakea MD-versio ensin
            const target = filename.replace('.json', '.md');
            let res = await fetch(`/api/briefs/${target}`);

            if (!res.ok) {
                // Varasuunnitelma: hae alkuperäinen tiedosto
                res = await fetch(`/api/briefs/${filename}`);
            }

            const data = await res.json();

            if (data.content) {
                modalBody.textContent = data.content; // MD-merkkijono
            } else {
                modalBody.textContent = JSON.stringify(data, null, 2); // JSON-objekti
            }

        } catch (err) {
            modalBody.textContent = "Virhe sisällön latauksessa.";
        }
    }
});
