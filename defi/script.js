// State Management
let state = {
    pairs: [],
    withdrawals: []
};

// DOM Elements
const elements = {
    totalInvested: document.getElementById('totalInvested'),
    totalWithdrawn: document.getElementById('totalWithdrawn'),
    netProfit: document.getElementById('netProfit'),
    pairsTableBody: document.getElementById('pairsTableBody'),
    withdrawalsTableBody: document.getElementById('withdrawalsTableBody'),

    // Buttons
    addPairBtn: document.getElementById('addPairBtn'),
    addWithdrawalBtn: document.getElementById('addWithdrawalBtn'),
    importBtn: document.getElementById('importBtn'),
    exportBtn: document.getElementById('exportBtn'),
    importFile: document.getElementById('importFile'),

    // Modals
    pairModal: document.getElementById('pairModal'),
    withdrawalModal: document.getElementById('withdrawalModal'),
    pairForm: document.getElementById('pairForm'),
    withdrawalForm: document.getElementById('withdrawalForm'),
    closeBtns: document.querySelectorAll('.close')
};

// --- Initialization ---

function init() {
    loadData();
    renderAll();
    setupEventListeners();
}

function loadData() {
    const saved = localStorage.getItem('defi_manager_data');
    if (saved) {
        state = JSON.parse(saved);
        // Ensure arrays exist if migrating from older version or empty
        if (!state.pairs) state.pairs = [];
        if (!state.withdrawals) state.withdrawals = [];
    }
}

function saveData() {
    localStorage.setItem('defi_manager_data', JSON.stringify(state));
    renderAll();
}

// --- Rendering ---

function renderAll() {
    renderPairs();
    renderWithdrawals();
    renderDashboard();
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function renderDashboard() {
    const totalInvested = state.pairs.reduce((sum, p) => sum + p.amount, 0);
    const totalWithdrawn = state.withdrawals.reduce((sum, w) => sum + w.amount, 0);
    const profit = totalWithdrawn - totalInvested;

    elements.totalInvested.textContent = formatCurrency(totalInvested);
    elements.totalWithdrawn.textContent = formatCurrency(totalWithdrawn);

    elements.netProfit.textContent = formatCurrency(profit);
    elements.netProfit.className = `amount ${profit >= 0 ? 'positive' : 'negative'}`;
}

function renderPairs() {
    elements.pairsTableBody.innerHTML = state.pairs.map(pair => `
        <tr>
            <td>${pair.name}</td>
            <td>${formatCurrency(pair.amount)}</td>
            <td>${new Date(pair.date).toLocaleDateString('pt-BR')}</td>
            <td>
                <button class="btn btn-danger" onclick="deletePair(${pair.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function renderWithdrawals() {
    // Sort by date descending
    const sortedWithdrawals = [...state.withdrawals].sort((a, b) => new Date(b.date) - new Date(a.date));

    elements.withdrawalsTableBody.innerHTML = sortedWithdrawals.map(w => `
        <tr>
            <td>${new Date(w.date).toLocaleDateString('pt-BR')}</td>
            <td>${formatCurrency(w.amount)}</td>
            <td>${w.notes || '-'}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteWithdrawal(${w.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// --- Actions ---

window.deletePair = function (id) {
    if (confirm('Tem certeza que deseja excluir este par?')) {
        state.pairs = state.pairs.filter(p => p.id !== id);
        saveData();
    }
};

window.deleteWithdrawal = function (id) {
    if (confirm('Tem certeza que deseja excluir este saque?')) {
        state.withdrawals = state.withdrawals.filter(w => w.id !== id);
        saveData();
    }
};

// --- Excel Import/Export ---

function exportToExcel() {
    const wb = XLSX.utils.book_new();

    // Prepare Pairs Data
    const pairsData = state.pairs.map(p => ({
        'ID': p.id,
        'Par': p.name,
        'Investido': p.amount,
        'Data': p.date
    }));
    const wsPairs = XLSX.utils.json_to_sheet(pairsData);
    XLSX.utils.book_append_sheet(wb, wsPairs, "Pares DeFi");

    // Prepare Withdrawals Data
    const withdrawalsData = state.withdrawals.map(w => ({
        'ID': w.id,
        'Data': w.date,
        'Valor': w.amount,
        'Notas': w.notes
    }));
    const wsWithdrawals = XLSX.utils.json_to_sheet(withdrawalsData);
    XLSX.utils.book_append_sheet(wb, wsWithdrawals, "Saques");

    XLSX.writeFile(wb, "defi_controle.xlsx");
}

function importFromExcel(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });

        // Parse Pairs
        if (workbook.Sheets["Pares DeFi"]) {
            const pairsRaw = XLSX.utils.sheet_to_json(workbook.Sheets["Pares DeFi"]);
            state.pairs = pairsRaw.map(p => ({
                id: p.ID || Date.now() + Math.random(),
                name: p.Par,
                amount: parseFloat(p.Investido),
                date: p.Data
            }));
        }

        // Parse Withdrawals
        if (workbook.Sheets["Saques"]) {
            const withdrawalsRaw = XLSX.utils.sheet_to_json(workbook.Sheets["Saques"]);
            state.withdrawals = withdrawalsRaw.map(w => ({
                id: w.ID || Date.now() + Math.random(),
                date: w.Data,
                amount: parseFloat(w.Valor),
                notes: w.Notas
            }));
        }

        saveData();
        alert('Importação concluída com sucesso!');
        elements.importFile.value = ''; // Reset input
    };
    reader.readAsArrayBuffer(file);
}

// --- Event Listeners ---

function setupEventListeners() {
    // Modals
    elements.addPairBtn.onclick = () => elements.pairModal.style.display = 'block';
    elements.addWithdrawalBtn.onclick = () => elements.withdrawalModal.style.display = 'block';

    elements.closeBtns.forEach(btn => {
        btn.onclick = () => {
            elements.pairModal.style.display = 'none';
            elements.withdrawalModal.style.display = 'none';
        }
    });

    window.onclick = (event) => {
        if (event.target == elements.pairModal) elements.pairModal.style.display = 'none';
        if (event.target == elements.withdrawalModal) elements.withdrawalModal.style.display = 'none';
    };

    // Forms
    elements.pairForm.onsubmit = (e) => {
        e.preventDefault();
        const newPair = {
            id: Date.now(),
            name: document.getElementById('pairName').value,
            amount: parseFloat(document.getElementById('pairAmount').value),
            date: document.getElementById('pairDate').value
        };
        state.pairs.push(newPair);
        saveData();
        elements.pairForm.reset();
        elements.pairModal.style.display = 'none';
    };

    elements.withdrawalForm.onsubmit = (e) => {
        e.preventDefault();
        const newWithdrawal = {
            id: Date.now(),
            amount: parseFloat(document.getElementById('withdrawalAmount').value),
            date: document.getElementById('withdrawalDate').value,
            notes: document.getElementById('withdrawalNotes').value
        };
        state.withdrawals.push(newWithdrawal);
        saveData();
        elements.withdrawalForm.reset();
        elements.withdrawalModal.style.display = 'none';
    };

    // Import/Export
    elements.exportBtn.onclick = exportToExcel;
    elements.importBtn.onclick = () => elements.importFile.click();
    elements.importFile.onchange = importFromExcel;
}

// Start
init();
