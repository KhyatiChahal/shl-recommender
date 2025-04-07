from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Create a database of assessments with keywords
assessments_db = [
    {
        'name': 'Coding Proficiency Java',
        'url': 'https://www.shl.com/solutions/products/coding-assessment/',
        'remote_testing': 'Yes',
        'adaptive_support': 'No',
        'keywords': ['java', 'coding', 'programming', 'software development', 'developer', 'engineering', 'computer science']
    },
    {
        'name': 'Software Development Assessment',
        'url': 'https://www.shl.com/solutions/products/developer-assessment/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['software', 'development', 'programming', 'web', 'application', 'developer', 'full stack', 'front end', 'back end']
    },
    {
        'name': 'IT Technical Knowledge Test',
        'url': 'https://www.shl.com/solutions/products/it-technical-knowledge/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['it', 'technical', 'support', 'helpdesk', 'systems', 'administration', 'network', 'infrastructure']
    },
    {
        'name': 'Technical Reasoning',
        'url': 'https://www.shl.com/solutions/products/technical-test/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['technical', 'reasoning', 'engineering', 'problem solving', 'analytical', 'logical']
    },
    {
        'name': 'Problem Solving Assessment',
        'url': 'https://www.shl.com/solutions/products/problem-solving/',
        'remote_testing': 'Yes',
        'adaptive_support': 'No',
        'keywords': ['problem solving', 'critical thinking', 'analytical', 'decision making', 'strategy']
    },
    {
        'name': 'Inductive Reasoning',
        'url': 'https://www.shl.com/solutions/products/inductive-reasoning/',
        'remote_testing': 'No',
        'adaptive_support': 'Yes',
        'keywords': ['reasoning', 'inductive', 'pattern recognition', 'logical', 'analytical thinking']
    },
    {
        'name': 'Occupational Personality Questionnaire',
        'url': 'https://www.shl.com/solutions/products/personality-assessment/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['personality', 'behavioral', 'leadership', 'team work', 'communication', 'management']
    },
    {
        'name': 'Agile Methodology Assessment',
        'url': 'https://www.shl.com/solutions/products/agile-assessment/',
        'remote_testing': 'Yes',
        'adaptive_support': 'No',
        'keywords': ['agile', 'scrum', 'kanban', 'sprint', 'product owner', 'scrum master', 'project management']
    },
    {
        'name': 'Business Judgment',
        'url': 'https://www.shl.com/solutions/products/business-judgment-test/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['business', 'judgment', 'decision making', 'management', 'leadership', 'strategy', 'executive']
    },
    {
        'name': 'Situational Judgment',
        'url': 'https://www.shl.com/solutions/products/situational-judgment/',
        'remote_testing': 'Yes',
        'adaptive_support': 'No',
        'keywords': ['situational', 'judgment', 'workplace', 'scenarios', 'decision making', 'behavior', 'conflict resolution']
    },
    {
        'name': 'Data Analysis Assessment',
        'url': 'https://www.shl.com/solutions/products/data-analysis/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['data', 'analysis', 'statistics', 'excel', 'reporting', 'analytics', 'visualization', 'sql', 'python', 'r']
    },
    {
        'name': 'Project Management Assessment',
        'url': 'https://www.shl.com/solutions/products/project-management/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['project', 'management', 'planning', 'coordination', 'pmp', 'prince2', 'scrum', 'agile', 'waterfall']
    },
    {
        'name': 'Mechanical Comprehension Test',
        'url': 'https://www.shl.com/solutions/products/mechanical-test/',
        'remote_testing': 'Yes',
        'adaptive_support': 'No',
        'keywords': ['mechanical', 'engineering', 'physics', 'machinery', 'maintenance', 'technician', 'manufacturing']
    },
    {
        'name': 'Leadership Assessment',
        'url': 'https://www.shl.com/solutions/products/leadership-assessment/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['leadership', 'management', 'executive', 'directing', 'team', 'strategic', 'vision', 'coaching']
    },
    {
        'name': 'Customer Service Assessment',
        'url': 'https://www.shl.com/solutions/products/customer-service/',
        'remote_testing': 'Yes',
        'adaptive_support': 'Yes',
        'keywords': ['customer', 'service', 'support', 'client', 'call center', 'helpdesk', 'communication', 'representative']
    }
]

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

def calculate_similarity(text, keywords):
    """Calculate similarity score between text and keywords"""
    # Convert text to lowercase and tokenize
    text = text.lower()
    
    # Count how many keywords appear in the text
    matches = 0
    keyword_count = len(keywords)
    matched_keywords = []
    
    for keyword in keywords:
        if keyword.lower() in text:
            matches += 1
            matched_keywords.append(keyword)
    
    if matches == 0:
        return 0, []
    
    # Calculate similarity percentage
    # Formula gives higher weight to matching more keywords
    similarity = min(95, (matches / keyword_count) * 100)
    
    return similarity, matched_keywords

def process_query(query_text):
    """Process the query text and return matching assessments"""
    if not query_text:
        return []
    
    matched_assessments = []
    
    for assessment in assessments_db:
        similarity, matched_keywords = calculate_similarity(query_text, assessment['keywords'])
        
        if similarity > 0:
            assessment_copy = assessment.copy()
            assessment_copy['similarity'] = f"{similarity:.2f}%"
            assessment_copy['matched_keywords'] = matched_keywords
            matched_assessments.append(assessment_copy)
    
    # Sort by similarity (highest first)
    matched_assessments.sort(key=lambda x: float(x['similarity'].rstrip('%')), reverse=True)
    
    # Remove the matched_keywords field from the result
    for assessment in matched_assessments:
        if 'matched_keywords' in assessment:
            del assessment['matched_keywords']
        if 'keywords' in assessment:
            del assessment['keywords']
    
    return matched_assessments

@app.route('/recommend', methods=['POST'])
def recommend():
    """Process input and return recommendations"""
    try:
        query_type = request.form.get('query_type', '')
        
        if query_type == 'text':
            query_text = request.form.get('query_text', '')
            matched_assessments = process_query(query_text)
            
        elif query_type == 'url':
            query_url = request.form.get('query_url', '')
            # In a real application, you would fetch and parse the URL content
            # For this example, we'll just use the URL itself as text
            matched_assessments = process_query(query_url)
            
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid query type'
            })
        
        # If no matches, return top assessments as default
        if not matched_assessments:
            default_assessments = assessments_db[:5]
            for assessment in default_assessments:
                assessment_copy = assessment.copy()
                assessment_copy['similarity'] = "50.00%"  # Default similarity
                if 'keywords' in assessment_copy:
                    del assessment_copy['keywords']
                matched_assessments.append(assessment_copy)
        
        return jsonify({
            'success': True,
            'assessments': matched_assessments
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Process uploaded job description file"""
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            })
        
        # Read file content
        file_content = file.read().decode('utf-8')
        
        # Process the file content
        matched_assessments = process_query(file_content)
        
        # If no matches, return top assessments as default
        if not matched_assessments:
            default_assessments = assessments_db[:5]
            for assessment in default_assessments:
                assessment_copy = assessment.copy()
                assessment_copy['similarity'] = "50.00%"  # Default similarity
                if 'keywords' in assessment_copy:
                    del assessment_copy['keywords']
                matched_assessments.append(assessment_copy)
        
        return jsonify({
            'success': True,
            'assessments': matched_assessments
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

if __name__ == '__main__':
    print("Starting Flask app with dynamic assessment recommendation...")
    app.run(debug=True, port=5000)