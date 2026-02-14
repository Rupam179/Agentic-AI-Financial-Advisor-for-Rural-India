from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Government schemes data for rural India
SCHEMES = {
    'pmjdy': {
        'name': 'Pradhan Mantri Jan Dhan Yojana',
        'description': 'Zero balance bank account with insurance',
        'eligibility': 'All Indian citizens',
        'benefits': ['₹10,000 overdraft', '₹2 lakh accident insurance', 'Zero balance']
    },
    'pmjjby': {
        'name': 'Pradhan Mantri Jeevan Jyoti Bima Yojana',
        'description': 'Life insurance scheme',
        'eligibility': '18-50 years with bank account',
        'benefits': ['₹2 lakh life cover', '₹330/year premium']
    },
    'pmsby': {
        'name': 'Pradhan Mantri Suraksha Bima Yojana',
        'description': 'Accident insurance scheme',
        'eligibility': '18-70 years with bank account',
        'benefits': ['₹2 lakh accident cover', '₹12/year premium']
    },
    'atal_pension': {
        'name': 'Atal Pension Yojana',
        'description': 'Pension scheme for unorganized sector',
        'eligibility': '18-40 years',
        'benefits': ['₹1,000-5,000 monthly pension', 'Government co-contribution']
    },
    'kisan_credit': {
        'name': 'Kisan Credit Card',
        'description': 'Credit facility for farmers',
        'eligibility': 'Farmers with land',
        'benefits': ['Low interest loans', 'Flexible repayment', 'Insurance coverage']
    },
    'mudra': {
        'name': 'MUDRA Loan',
        'description': 'Micro-enterprise loans',
        'eligibility': 'Small businesses',
        'benefits': ['Up to ₹10 lakh loan', 'No collateral', 'Low interest']
    }
}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/analyze', methods=['POST'])
def analyze_finances():
    try:
        data = request.json
        
        monthly_income = float(data.get('monthly_income', 0))
        monthly_expenses = float(data.get('monthly_expenses', 0))
        savings = float(data.get('savings', 0))
        debt = float(data.get('debt', 0))
        family_size = int(data.get('family_size', 1))
        occupation = data.get('occupation', 'other')
        has_bank_account = data.get('has_bank_account', False)
        age = int(data.get('age', 25))
        
        # Calculate financial metrics
        monthly_surplus = monthly_income - monthly_expenses
        savings_rate = (monthly_surplus / monthly_income * 100) if monthly_income > 0 else 0
        debt_to_income = (debt / (monthly_income * 12) * 100) if monthly_income > 0 else 0
        
        # Financial health score (0-100)
        health_score = calculate_health_score(savings_rate, debt_to_income, savings, monthly_income)
        
        # Generate recommendations
        recommendations = generate_recommendations(
            monthly_income, monthly_surplus, savings, debt, 
            occupation, has_bank_account, age, savings_rate
        )
        
        # Suggest government schemes
        schemes = suggest_schemes(occupation, has_bank_account, age, monthly_income)
        
        # Budget plan
        budget = create_budget_plan(monthly_income, family_size)
        
        # Savings goals
        goals = create_savings_goals(monthly_income, monthly_surplus, age)
        
        return jsonify({
            'health_score': round(health_score, 1),
            'monthly_surplus': round(monthly_surplus, 2),
            'savings_rate': round(savings_rate, 1),
            'debt_to_income': round(debt_to_income, 1),
            'recommendations': recommendations,
            'schemes': schemes,
            'budget': budget,
            'goals': goals,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def calculate_health_score(savings_rate, debt_to_income, savings, monthly_income):
    score = 50  # Base score
    
    # Savings rate contribution (0-25 points)
    if savings_rate >= 20:
        score += 25
    elif savings_rate >= 10:
        score += 15
    elif savings_rate >= 5:
        score += 10
    
    # Debt contribution (0-25 points)
    if debt_to_income == 0:
        score += 25
    elif debt_to_income < 20:
        score += 20
    elif debt_to_income < 40:
        score += 10
    
    # Emergency fund (0-25 points)
    emergency_months = savings / monthly_income if monthly_income > 0 else 0
    if emergency_months >= 6:
        score += 25
    elif emergency_months >= 3:
        score += 15
    elif emergency_months >= 1:
        score += 10
    
    return min(score, 100)

def generate_recommendations(monthly_income, monthly_surplus, savings, debt, occupation, has_bank_account, age, savings_rate):
    recs = []
    
    if not has_bank_account:
        recs.append({
            'priority': 'high',
            'title': 'खाता खोलें (Open Bank Account)',
            'description': 'Jan Dhan Yojana के तहत मुफ्त बैंक खाता खोलें',
            'action': 'Visit nearest bank with Aadhaar card'
        })
    
    if monthly_surplus < 0:
        recs.append({
            'priority': 'high',
            'title': 'खर्च कम करें (Reduce Expenses)',
            'description': f'आप महीने में ₹{abs(monthly_surplus):.0f} अधिक खर्च कर रहे हैं',
            'action': 'Track daily expenses and cut unnecessary costs'
        })
    
    if savings < monthly_income * 3:
        recs.append({
            'priority': 'high',
            'title': 'आपातकालीन फंड बनाएं (Build Emergency Fund)',
            'description': '3-6 महीने के खर्च के बराबर बचत रखें',
            'action': f'Save ₹{(monthly_income * 3 - savings):.0f} for emergency fund'
        })
    
    if debt > 0:
        recs.append({
            'priority': 'medium',
            'title': 'कर्ज चुकाएं (Pay Off Debt)',
            'description': f'कुल कर्ज: ₹{debt:.0f}',
            'action': 'Prioritize high-interest debt first'
        })
    
    if savings_rate < 10 and monthly_surplus > 0:
        recs.append({
            'priority': 'medium',
            'title': 'बचत बढ़ाएं (Increase Savings)',
            'description': 'आय का कम से कम 10-20% बचत करें',
            'action': f'Try to save ₹{monthly_income * 0.1:.0f} per month'
        })
    
    if occupation == 'farmer' and monthly_income > 0:
        recs.append({
            'priority': 'medium',
            'title': 'किसान क्रेडिट कार्ड (Kisan Credit Card)',
            'description': 'कम ब्याज पर कृषि ऋण प्राप्त करें',
            'action': 'Apply at nearest bank or CSC'
        })
    
    if age >= 18 and age <= 40 and has_bank_account:
        recs.append({
            'priority': 'low',
            'title': 'पेंशन योजना (Pension Scheme)',
            'description': 'Atal Pension Yojana में निवेश करें',
            'action': 'Start with ₹210/month contribution'
        })
    
    return recs

def suggest_schemes(occupation, has_bank_account, age, monthly_income):
    schemes = []
    
    if not has_bank_account:
        schemes.append(SCHEMES['pmjdy'])
    
    if has_bank_account and age >= 18 and age <= 50:
        schemes.append(SCHEMES['pmjjby'])
    
    if has_bank_account and age >= 18 and age <= 70:
        schemes.append(SCHEMES['pmsby'])
    
    if age >= 18 and age <= 40:
        schemes.append(SCHEMES['atal_pension'])
    
    if occupation == 'farmer':
        schemes.append(SCHEMES['kisan_credit'])
    
    if occupation in ['business', 'self_employed'] and monthly_income < 100000:
        schemes.append(SCHEMES['mudra'])
    
    return schemes[:4]  # Return top 4 schemes

def create_budget_plan(monthly_income, family_size):
    # 50-30-20 rule adapted for rural India
    needs = monthly_income * 0.60  # 60% for needs
    wants = monthly_income * 0.20  # 20% for wants
    savings = monthly_income * 0.20  # 20% for savings
    
    return {
        'needs': {
            'amount': round(needs, 2),
            'percentage': 60,
            'categories': ['भोजन (Food)', 'आवास (Housing)', 'शिक्षा (Education)', 'स्वास्थ्य (Health)']
        },
        'wants': {
            'amount': round(wants, 2),
            'percentage': 20,
            'categories': ['मनोरंजन (Entertainment)', 'यात्रा (Travel)', 'अन्य (Others)']
        },
        'savings': {
            'amount': round(savings, 2),
            'percentage': 20,
            'categories': ['बचत खाता (Savings)', 'निवेश (Investment)', 'बीमा (Insurance)']
        }
    }

def create_savings_goals(monthly_income, monthly_surplus, age):
    goals = []
    
    if monthly_surplus > 0:
        # Emergency fund
        goals.append({
            'name': 'आपातकालीन फंड (Emergency Fund)',
            'target': monthly_income * 6,
            'monthly_save': min(monthly_surplus * 0.4, monthly_income * 0.1),
            'months': int((monthly_income * 6) / (monthly_surplus * 0.4)) if monthly_surplus > 0 else 0,
            'priority': 'high'
        })
        
        # Child education
        goals.append({
            'name': 'बच्चों की शिक्षा (Child Education)',
            'target': 200000,
            'monthly_save': min(monthly_surplus * 0.3, monthly_income * 0.05),
            'months': int(200000 / (monthly_surplus * 0.3)) if monthly_surplus > 0 else 0,
            'priority': 'medium'
        })
        
        # Retirement
        if age < 50:
            goals.append({
                'name': 'रिटायरमेंट (Retirement)',
                'target': 500000,
                'monthly_save': min(monthly_surplus * 0.3, monthly_income * 0.05),
                'months': int(500000 / (monthly_surplus * 0.3)) if monthly_surplus > 0 else 0,
                'priority': 'low'
            })
    
    return goals[:3]

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').lower()
        
        response = generate_chat_response(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def generate_chat_response(message):
    # Simple rule-based chatbot
    if 'loan' in message or 'ऋण' in message:
        return 'आप MUDRA Loan (₹10 लाख तक) या Kisan Credit Card के लिए आवेदन कर सकते हैं। क्या आप किसान हैं या व्यवसायी?'
    
    elif 'insurance' in message or 'बीमा' in message:
        return 'PM Jeevan Jyoti (₹330/वर्ष) और PM Suraksha Bima (₹12/वर्ष) सबसे सस्ती बीमा योजनाएं हैं। दोनों के लिए बैंक खाता जरूरी है।'
    
    elif 'pension' in message or 'पेंशन' in message:
        return 'Atal Pension Yojana में ₹210/माह से शुरू करें। 60 साल की उम्र में ₹1,000-5,000 मासिक पेंशन मिलेगी।'
    
    elif 'save' in message or 'बचत' in message:
        return 'अपनी आय का 20% बचत करने की कोशिश करें। पहले आपातकालीन फंड (6 महीने का खर्च) बनाएं।'
    
    elif 'bank' in message or 'खाता' in message:
        return 'Jan Dhan Yojana के तहत मुफ्त बैंक खाता खोलें। आधार कार्ड लेकर नजदीकी बैंक जाएं।'
    
    else:
        return 'मैं आपकी वित्तीय सलाह में मदद कर सकता हूं। आप loan, insurance, pension, savings या bank account के बारे में पूछ सकते हैं।'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
