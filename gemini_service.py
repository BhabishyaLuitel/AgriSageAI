import base64
import requests
import time
from PIL import Image
import io
from config import GEMINI_API_KEY, GEMINI_MODEL

class GeminiService:
    def __init__(self):
        """Initialize Gemini AI service."""
        self.api_key = GEMINI_API_KEY
        self.model = GEMINI_MODEL
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        self.api_available = bool(self.api_key)
        
        if not self.api_available:
            print("⚠️  Running in test mode without Gemini API")
        else:
            print("✅ Gemini API service initialized successfully")
        
    def create_context_prompt(self, analysis_data):
        """Create a context prompt for the AI based on analysis data."""
        disease = analysis_data.get('disease_result', 'Unknown')
        confidence = analysis_data.get('confidence', 'Unknown')
        district = analysis_data.get('district_query', 'Unknown')
        crop = analysis_data.get('crop_result', 'Unknown')
        
        context = f"""
You are Agri-Sage AI, a specialized agricultural assistant for Nepal. You have analyzed a plant leaf image and detected the following:

**Plant Analysis Results:**
- Disease Detected: {disease}
- Confidence Level: {confidence}
- Location: {district}, Nepal
- Recommended Crop for this area: {crop}

**Your Role:**
- Provide expert agricultural advice for Nepali farmers
- Explain plant diseases in simple, understandable terms
- Suggest practical treatment and prevention methods
- Recommend crops suitable for Nepali climate and soil
- Consider local farming practices and available resources
- Be conversational, helpful, and encouraging

**Guidelines:**
- Respond in a natural, conversational tone
- Provide practical, actionable advice
- Consider the local context of Nepal
- Be encouraging and supportive
- If you're not sure about something, recommend consulting local experts
- Use simple language that farmers can understand

The user will ask you questions about their plant diagnosis. Provide helpful, contextual responses based on the analysis above.
"""
        return context
    
    def _call_gemini_api(self, prompt):
        """Make API call to Gemini."""
        if not self.api_available:
            return None
            
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        max_retries = 3
        delay = 1
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url, 
                    json=payload, 
                    headers={'Content-Type': 'application/json'}, 
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
                
            except requests.exceptions.RequestException as e:
                print(f"API request failed (attempt {attempt + 1}): {e}")
                if hasattr(e, 'response') and e.response and e.response.status_code == 403:
                    print("❌ Gemini API key is invalid or has insufficient permissions.")
                    return None
                if hasattr(e, 'response') and e.response and e.response.status_code == 400:
                    print("❌ Invalid request format or model name.")
                    return None
                time.sleep(delay)
                delay *= 2
                
        print("❌ API connection failed after multiple retries.")
        return None

    def chat_with_image(self, user_message, analysis_data, image_b64=None):
        """Chat with AI using the analysis data and optionally an image."""
        try:
            # Create context prompt
            context = self.create_context_prompt(analysis_data)
            full_prompt = f"{context}\n\nUser Question: {user_message}"
            
            # Try API call first
            if self.api_available:
                api_response = self._call_gemini_api(full_prompt)
                if api_response:
                    return api_response
            
            # Fallback to pre-built responses
            response = self._generate_natural_response(user_message, analysis_data)
            return response
            
        except Exception as e:
            print(f"Error in AI chat: {e}")
            return f"I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
    
    def simple_chat(self, user_message):
        """Simple chat without analysis context."""
        try:
            # Try API call first
            if self.api_available:
                prompt = f"You are Agri-Sage AI, a friendly agricultural assistant for Nepal. User says: '{user_message}'. Respond helpfully and concisely."
                api_response = self._call_gemini_api(prompt)
                if api_response:
                    return api_response
            
            # Fallback to pre-built responses
            response = self._generate_simple_response(user_message)
            return response
            
        except Exception as e:
            print(f"Error in simple chat: {e}")
            return f"I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
    
    def _generate_natural_response(self, user_message, analysis_data):
        """Generate natural, conversational responses like ChatGPT/Gemini."""
        message_lower = user_message.lower()
        disease = analysis_data.get('disease_result', 'Unknown')
        confidence = analysis_data.get('confidence', 'Unknown')
        district = analysis_data.get('district_query', 'Unknown')
        crop = analysis_data.get('crop_result', 'Unknown')
        
        # Natural response patterns based on user questions
        if any(word in message_lower for word in ['treat', 'cure', 'fix', 'solution', 'medicine', 'help', 'save']):
            return f"""Looking at your plant with {disease}, I can help you with treatment options! 

For treating {disease}, here are some effective approaches you can try:

**Immediate Actions:**
• Remove and destroy any infected leaves or plant parts to prevent spread
• Improve air circulation around your plants by proper spacing
• Avoid overhead watering - water at the base of plants instead

**Natural Treatment Options:**
• Neem oil spray (mix 2 tablespoons neem oil with 1 gallon water)
• Baking soda solution (1 tablespoon baking soda + 1 gallon water + few drops dish soap)
• Garlic spray (crush 3-4 garlic cloves, steep in hot water, strain and spray)

**Chemical Options (if needed):**
• Copper-based fungicides are effective for fungal diseases
• Always follow label instructions and safety precautions

**Prevention Tips:**
• Keep your garden clean and remove plant debris
• Rotate crops each season
• Use disease-resistant varieties when possible

Since you're in {district}, these methods should work well with your local climate. Start with the gentler approaches first - sometimes just improving air circulation can make a big difference!

Would you like me to explain any of these treatments in more detail, or do you have questions about preventing this disease in the future?"""

        elif any(word in message_lower for word in ['symptom', 'sign', 'look', 'appear', 'show']):
            return f"""Great question! Let me explain what to look for with {disease}.

**Common Symptoms of {disease}:**

**Visual Signs:**
• Dark brown or black spots on leaves, often with concentric rings
• Yellowing of leaves around the affected areas
• Wilting or drooping of plant parts
• White or grayish powdery growth on leaf undersides (in some cases)

**Progression Pattern:**
• Symptoms usually start on lower, older leaves first
• Spots gradually increase in size and number
• Leaves may eventually turn completely yellow and fall off
• The disease can spread to stems and fruits if left untreated

**What to Monitor:**
• Check your plants regularly, especially after rain or high humidity
• Look for any unusual discoloration or spots
• Pay attention to leaf texture changes
• Monitor plant growth and vigor

**Early Detection Tips:**
• Inspect plants weekly during growing season
• Look at both upper and lower leaf surfaces
• Check for any spots that seem to be spreading
• Monitor weather conditions that favor disease development

Since you're in {district}, be especially watchful during the monsoon season when humidity is high. Early detection is key to successful treatment!

Would you like me to explain how to distinguish this from other similar diseases, or do you have questions about monitoring your other plants?"""

        elif any(word in message_lower for word in ['prevent', 'avoid', 'stop', 'future', 'protect']):
            return f"""Excellent! Prevention is always better than cure. Here's how you can protect your plants from {disease} and similar problems:

**Cultural Prevention Methods:**

**Garden Management:**
• Clean up plant debris and fallen leaves regularly
• Maintain proper spacing between plants for good air circulation
• Avoid working with plants when they're wet
• Rotate crops each season to break disease cycles

**Watering Practices:**
• Water at the base of plants, not overhead
• Water early in the morning so leaves dry quickly
• Avoid overwatering - let soil dry between waterings
• Use drip irrigation when possible

**Plant Health:**
• Choose disease-resistant varieties when available
• Ensure plants get adequate sunlight and nutrients
• Don't overcrowd plants
• Remove any diseased plants immediately

**Soil and Environment:**
• Maintain good soil drainage
• Add organic matter to improve soil health
• Monitor humidity levels in greenhouses
• Use mulch to prevent soil splash onto leaves

**Seasonal Tips for {district}:**
• Be extra vigilant during monsoon season
• Prune plants to improve air circulation
• Consider using row covers during wet periods
• Plan your garden layout to maximize sunlight exposure

**Natural Prevention Sprays:**
• Regular neem oil applications (every 7-10 days)
• Baking soda spray as a preventive measure
• Compost tea for overall plant health

Remember, healthy plants are more resistant to diseases! Focus on creating the best growing conditions, and your plants will be much better at fighting off diseases naturally.

Would you like me to explain any of these prevention methods in more detail?"""

        elif any(word in message_lower for word in ['tell me more', 'explain', 'what is', 'about this disease']):
            return f"""I'd be happy to explain more about {disease}! This is actually a common plant disease that many farmers in Nepal deal with.

**What is {disease}?**

{disease} is typically a fungal disease that affects various plants. It's caused by fungal pathogens that thrive in warm, humid conditions - which we often have in Nepal, especially during the monsoon season.

**How it Develops:**
• The fungus overwinters in plant debris and soil
• Spores are spread by wind, water, or garden tools
• Infection occurs when spores land on wet plant surfaces
• The disease spreads rapidly in warm, humid conditions

**Why it's Common in Nepal:**
• Our monsoon climate provides ideal conditions for fungal growth
• High humidity and frequent rain create perfect breeding grounds
• Many traditional farming practices can inadvertently spread the disease

**Impact on Plants:**
• Reduces photosynthesis by damaging leaves
• Can cause significant yield loss if left untreated
• Weakens plants and makes them more susceptible to other problems
• Can spread quickly to other plants in the garden

**Good News:**
• It's very treatable when caught early
• Many effective control methods are available
• Prevention strategies can significantly reduce outbreaks
• Your plants can recover fully with proper care

**Local Context for {district}:**
• This area's climate makes prevention especially important
• Local farmers have developed effective traditional methods
• The disease is well-understood by agricultural experts in your region

The key is early detection and consistent prevention. With the right approach, you can keep your plants healthy and productive!

Would you like me to explain specific treatment methods, or do you have questions about how this disease affects different types of plants?"""

        else:
            return f"""I can see you're asking about {disease} that was detected in your plant with {confidence} confidence. 

Based on your analysis from {district}, I can help you with several aspects:

**What I can help you with:**
• Treatment methods and solutions
• Understanding symptoms and signs
• Prevention strategies for future outbreaks
• General information about this disease
• Tips specific to your local climate

**Some common questions farmers ask:**
• "How do I treat this disease?"
• "What are the symptoms to watch for?"
• "How can I prevent this in the future?"
• "Tell me more about this disease"

Feel free to ask me anything specific about your plant's condition, treatment options, or prevention strategies. I'm here to help you get your plants healthy again!

What would you like to know more about?"""

    def _generate_simple_response(self, user_message):
        """Generate simple responses for general questions."""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return """Hello! 👋 I'm Agri-Sage AI, your agricultural assistant for Nepal. 

I can help you with:
• Plant disease identification and treatment
• Crop recommendations for your area
• Agricultural advice and best practices
• Prevention strategies for common plant problems

To get started, just upload a photo of your plant leaf and I'll analyze it for you. What would you like to know about today?"""

        elif any(word in message_lower for word in ['help', 'what can you do']):
            return """I'm here to help you with all things agriculture! 🌱

**What I can do for you:**
• Analyze plant leaf images for disease detection
• Provide treatment recommendations for plant diseases
• Suggest prevention strategies to protect your plants
• Recommend crops suitable for your area in Nepal
• Answer questions about farming practices and plant care

**How to use me:**
1. Upload a photo of your plant leaf
2. I'll analyze it and show you the results
3. Ask me any questions about treatment, prevention, or general plant care
4. I'll provide personalized advice for your situation

I'm designed specifically for Nepali farmers and consider local climate, soil conditions, and farming practices in my recommendations.

Ready to get started? Just upload a plant image!"""

        else:
            return """I'm Agri-Sage AI, your agricultural assistant for Nepal! 🌿

I can help you identify plant diseases, suggest treatments, and provide farming advice tailored to your local conditions.

To get the most out of our conversation, please upload a photo of your plant leaf first. This will help me provide more specific and helpful advice for your situation.

What would you like to know about plant health or farming today?"""
