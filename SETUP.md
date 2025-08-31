# Agri-Sage AI Setup Guide

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Gemini AI API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Configure Environment Variables
Create a `.env` file in the project root with:
```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
```

### 4. Run the Application
```bash
python app.py
```

## 🔧 Features

### ✨ What's New with Gemini AI:
- **Natural Conversations**: Chat like you do with Gemini AI directly
- **Context-Aware Responses**: AI understands your plant analysis
- **Multimodal Support**: Can analyze images in real-time
- **Nepal-Specific Advice**: Tailored for Nepali agricultural context
- **No Limitations**: Full conversational AI capabilities

### 🧹 Code Cleanup:
- Removed static disease database (500+ lines)
- Simplified chat logic
- Modular architecture with separate services
- Better error handling
- Environment-based configuration

## 🎯 Usage

1. **Upload Image**: Drag & drop or click to upload a plant leaf image
2. **Start Chatting**: Ask any question about your plant
3. **Get AI Analysis**: Gemini AI will analyze the image and provide expert advice
4. **Natural Conversation**: Chat freely about treatment, prevention, crops, etc.

## 🔍 Example Conversations

**User**: "What's wrong with my plant?"
**AI**: "Looking at your plant image, I can see signs of Early Blight. This is a common fungal disease that affects tomatoes and potatoes. The symptoms include dark brown spots with concentric rings on the leaves..."

**User**: "How do I treat this naturally?"
**AI**: "For natural treatment of Early Blight, you can try several organic methods. First, remove and destroy any infected leaves to prevent spread..."

**User**: "What crops grow well in my area?"
**AI**: "Based on your location in Kathmandu, I'd recommend several crops that thrive in this climate..."

## 🛠️ Troubleshooting

### Common Issues:
1. **API Key Error**: Make sure your Gemini API key is correct
2. **Model Loading**: Ensure all model files are present
3. **Image Upload**: Check file size (max 16MB)

### Support:
- Check the console for error messages
- Verify all dependencies are installed
- Ensure proper file permissions
