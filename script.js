const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api'
    : '/api';

let currentLang = 'hi';

// Language Toggle
document.getElementById('langToggle').addEventListener('click', () => {
    currentLang = currentLang === 'hi' ? 'en' : 'hi';
    updateLanguage();
});

function updateLanguage() {
    const elements = document.querySelectorAll('[data-en][data-hi]');
    elements.forEach(el => {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = el.getAttribute(`data-${currentLang}-placeholder`);
        } else if (el.tagName === 'OPTION') {
            el.textContent = el.getAttribute(`data-${currentLang}`);
        } else {
            el.textContent = el.getAttribute(`data-${currentLang}`);
        }
    });
    
    document.getElementById('langToggle').innerHTML = 
        `<i class="fas fa-language"></i> ${currentLang === 'hi' ? 'English' : 'हिंदी'}`;
}

// Form Submit
document.getElementById('financeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        monthly_income: parseFloat(document.getElementById('monthlyIncome').value),
        monthly_expenses: parseFloat(document.getElementById('monthlyExpenses').value),
        savings: parseFloat(document.getElementById('savings').value),
        debt: parseFloat(document.getElementById('debt').value),
        family_size: parseInt(document.getElementById('familySize').value),
        age: parseInt(document.getElementById('age').value),
        occupation: document.getElementById('occupation').value,
        has_bank_account: document.getElementById('hasBankAccount').value === 'true'
    };
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) throw new Error('Analysis failed');
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        // Fallback calculation
        const fallbackResult = calculateFallback(formData);
        displayResults(fallbackResult);
    } finally {
        showLoading(false);
    }
});

function calculateFallback(data) {
    const surplus = data.monthly_income - data.monthly_expenses;
    const savingsRate = (surplus / data.monthly_income * 100) || 0;
    const debtToIncome = (data.debt / (data.monthly_income * 12) * 100) || 0;
    
    let score = 50;
    if (savingsRate >= 20) score += 25;
    else if (savingsRate >= 10) score += 15;
    if (debtToIncome === 0) score += 25;
    else if (debtToIncome < 20) score += 20;
    
    return {
        health_score: Math.min(score, 100),
        monthly_surplus: surplus,
        savings_rate: savingsRate,
        debt_to_income: debtToIncome,
        recommendations: generateFallbackRecs(data, surplus, savingsRate),
        schemes: generateFallbackSchemes(data),
        budget: generateFallbackBudget(data.monthly_income),
        goals: generateFallbackGoals(data.monthly_income, surplus)
    };
}

function generateFallbackRecs(data, surplus, savingsRate) {
    const recs = [];
    
    if (!data.has_bank_account) {
        recs.push({
            priority: 'high',
            title: 'खाता खोलें | Open Bank Account',
            description: 'Jan Dhan Yojana के तहत मुफ्त बैंक खाता खोलें',
            action: 'Visit nearest bank with Aadhaar'
        });
    }
    
    if (surplus < 0) {
        recs.push({
            priority: 'high',
            title: 'खर्च कम करें | Reduce Expenses',
            description: `आप ₹${Math.abs(surplus).toFixed(0)} अधिक खर्च कर रहे हैं`,
            action: 'Track and cut unnecessary expenses'
        });
    }
    
    if (data.savings < data.monthly_income * 3) {
        recs.push({
            priority: 'high',
            title: 'आपातकालीन फंड | Emergency Fund',
            description: '3-6 महीने के खर्च के बराबर बचत रखें',
            action: `Save ₹${(data.monthly_income * 3 - data.savings).toFixed(0)}`
        });
    }
    
    if (savingsRate < 10 && surplus > 0) {
        recs.push({
            priority: 'medium',
            title: 'बचत बढ़ाएं | Increase Savings',
            description: 'आय का 10-20% बचत करें',
            action: `Try to save ₹${(data.monthly_income * 0.1).toFixed(0)}/month`
        });
    }
    
    return recs;
}

function generateFallbackSchemes(data) {
    const schemes = [];
    
    if (!data.has_bank_account) {
        schemes.push({
            name: 'Pradhan Mantri Jan Dhan Yojana',
            description: 'Zero balance bank account',
            benefits: ['₹10,000 overdraft', '₹2 lakh insurance', 'Zero balance']
        });
    }
    
    if (data.age >= 18 && data.age <= 50 && data.has_bank_account) {
        schemes.push({
            name: 'PM Jeevan Jyoti Bima Yojana',
            description: 'Life insurance - ₹330/year',
            benefits: ['₹2 lakh life cover', 'Low premium']
        });
    }
    
    if (data.occupation === 'farmer') {
        schemes.push({
            name: 'Kisan Credit Card',
            description: 'Credit for farmers',
            benefits: ['Low interest loans', 'Flexible repayment']
        });
    }
    
    if (data.age >= 18 && data.age <= 40) {
        schemes.push({
            name: 'Atal Pension Yojana',
            description: 'Pension scheme',
            benefits: ['₹1,000-5,000 monthly pension', 'Government support']
        });
    }
    
    return schemes;
}

function generateFallbackBudget(income) {
    return {
        needs: { amount: income * 0.6, percentage: 60 },
        wants: { amount: income * 0.2, percentage: 20 },
        savings: { amount: income * 0.2, percentage: 20 }
    };
}

function generateFallbackGoals(income, surplus) {
    if (surplus <= 0) return [];
    
    return [
        {
            name: 'आपातकालीन फंड | Emergency Fund',
            target: income * 6,
            monthly_save: surplus * 0.4,
            months: Math.ceil((income * 6) / (surplus * 0.4)),
            priority: 'high'
        },
        {
            name: 'बच्चों की शिक्षा | Child Education',
            target: 200000,
            monthly_save: surplus * 0.3,
            months: Math.ceil(200000 / (surplus * 0.3)),
            priority: 'medium'
        }
    ];
}

function displayResults(result) {
    document.getElementById('results').style.display = 'grid';
    
    // Health Score
    animateValue('healthScore', 0, result.health_score, 1000);
    document.getElementById('monthlySurplus').textContent = `₹${result.monthly_surplus.toFixed(0)}`;
    document.getElementById('savingsRate').textContent = `${result.savings_rate.toFixed(1)}%`;
    
    // Recommendations
    const recsList = document.getElementById('recommendationsList');
    recsList.innerHTML = result.recommendations.map(rec => `
        <div class="recommendation-item ${rec.priority}">
            <h4>${rec.title}</h4>
            <p>${rec.description}</p>
            <small><strong>Action:</strong> ${rec.action}</small>
        </div>
    `).join('');
    
    // Schemes
    const schemesList = document.getElementById('schemesList');
    schemesList.innerHTML = result.schemes.map(scheme => `
        <div class="scheme-item">
            <h4>${scheme.name}</h4>
            <p>${scheme.description}</p>
            <ul>
                ${scheme.benefits ? scheme.benefits.map(b => `<li>${b}</li>`).join('') : ''}
            </ul>
        </div>
    `).join('');
    
    // Budget
    const budgetPlan = document.getElementById('budgetPlan');
    budgetPlan.innerHTML = `
        <div class="budget-item">
            <div>
                <h4>जरूरतें | Needs (${result.budget.needs.percentage}%)</h4>
            </div>
            <div class="amount">₹${result.budget.needs.amount.toFixed(0)}</div>
        </div>
        <div class="budget-item">
            <div>
                <h4>इच्छाएं | Wants (${result.budget.wants.percentage}%)</h4>
            </div>
            <div class="amount">₹${result.budget.wants.amount.toFixed(0)}</div>
        </div>
        <div class="budget-item">
            <div>
                <h4>बचत | Savings (${result.budget.savings.percentage}%)</h4>
            </div>
            <div class="amount">₹${result.budget.savings.amount.toFixed(0)}</div>
        </div>
    `;
    
    // Goals
    const goalsList = document.getElementById('goalsList');
    goalsList.innerHTML = result.goals.map(goal => `
        <div class="goal-item">
            <h4>${goal.name}</h4>
            <div class="goal-details">
                <span>Target: <strong>₹${goal.target.toLocaleString('en-IN')}</strong></span>
                <span>Monthly: <strong>₹${goal.monthly_save.toFixed(0)}</strong></span>
                <span>Duration: <strong>${goal.months} months</strong></span>
                <span>Priority: <strong>${goal.priority}</strong></span>
            </div>
        </div>
    `).join('');
    
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function animateValue(id, start, end, duration) {
    const element = document.getElementById(id);
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 16);
}

// Chat
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;
    
    const chatMessages = document.getElementById('chatMessages');
    
    // User message
    chatMessages.innerHTML += `<div class="message user">${message}</div>`;
    input.value = '';
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        const result = await response.json();
        chatMessages.innerHTML += `<div class="message bot">${result.response}</div>`;
        
    } catch (error) {
        chatMessages.innerHTML += `<div class="message bot">मैं आपकी मदद करने के लिए यहां हूं। कृपया फिर से प्रयास करें।</div>`;
    }
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

document.getElementById('chatInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

function showLoading(show) {
    document.getElementById('loading').classList.toggle('active', show);
}
