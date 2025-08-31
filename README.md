# 🌿 Agri-Sage AI - Plant Disease Diagnosis & Crop Recommendation System

A comprehensive AI-powered agricultural assistant for Nepal that combines plant disease diagnosis with intelligent crop recommendations and conversational AI support.

## 🎯 Project Overview

Agri-Sage AI is an intelligent agricultural system that helps Nepali farmers identify plant diseases, get crop recommendations, and receive expert advice through natural conversation. The system operates on the **Sense-Think-Act** cycle architecture.

### 🌟 Key Features

- **🔬 Plant Disease Diagnosis**: CNN-based image analysis for accurate disease detection
- **🌱 Crop Recommendations**: Decision Tree model for district-specific crop suggestions
- **💬 Conversational AI**: Natural language interface for follow-up questions and expert advice
- **📱 Modern Web Interface**: Beautiful, responsive design with drag-and-drop functionality
- **🇳🇵 Nepal-Specific**: Tailored for Nepali climate, soil conditions, and farming practices

## 🏗️ System Architecture

The system follows the **Sense-Think-Act** cycle:

### **SENSE** (Front-end Input Capture)
- HTML web interface captures district and plant leaf image
- Drag-and-drop image upload with real-time feedback
- User-friendly form inputs

### **THINK** (Back-end Processing)
- **Flask Server**: Handles all backend processing and API endpoints
- **Crop Recommender**: Decision Tree model for crop recommendations
- **Disease Diagnoser**: CNN model for plant disease detection

### **ACT** (Response Generation)
- Consolidated analysis report with confidence scores
- Interactive chat interface for follow-up questions
- Context-aware AI responses

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- TensorFlow 2.13.0
- Flask 2.3.3

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agri-sage-ai.git
   cd agri-sage-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   FLASK_SECRET_KEY=your-secret-key-here
   FLASK_DEBUG=True
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to `http://127.0.0.1:5000`

## 📁 Project Structure

```
agri-sage-ai/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── gemini_service.py      # AI conversation service
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── SETUP.md              # Detailed setup guide
├── templates/
│   └── index.html        # Main web interface
├── static/               # Static assets (CSS, JS, images)
├── models/               # Trained ML models
│   ├── plant_disease_model.h5
│   ├── crop_recommender_model.joblib
│   ├── crop_model_columns.joblib
│   └── crop_label_encoder.joblib
├── data/                 # Training datasets
└── training/             # Model training scripts
    ├── train_disease_model.py
    └── train_crop_model.py
```

## 🤖 AI Models

### Disease Diagnosis Model
- **Type**: Convolutional Neural Network (CNN)
- **Input**: Plant leaf images (224x224 pixels)
- **Output**: Disease classification with confidence scores
- **Supported Diseases**: Early blight, Late blight, Leaf mold, Septoria leaf spot, Spider mites, Target spot, Yellow leaf curl virus, Mosaic virus, Healthy plants

### Crop Recommendation Model
- **Type**: Decision Tree
- **Input**: District name
- **Output**: Recommended crop for the district
- **Coverage**: Major districts of Nepal

## 💬 Conversational AI

The system includes an intelligent chat interface that:
- Provides natural, conversational responses
- Offers context-aware advice based on analysis results
- Suggests treatment and prevention strategies
- Considers local Nepali agricultural context
- Supports follow-up questions and detailed explanations

## 🎨 User Interface

### Modern Design Features
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Easy image upload functionality
- **Real-time Feedback**: Loading states and progress indicators
- **Beautiful Animations**: Smooth transitions and interactions
- **Color-coded Results**: Easy-to-understand analysis display

### Workflow
1. **Upload Image**: Drag & drop or click to upload plant leaf image
2. **Get Analysis**: Instant disease diagnosis and crop recommendations
3. **Learn More**: Interactive prompt to explore additional information
4. **Chat with AI**: Natural conversation for detailed advice and follow-up questions

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini AI API key for enhanced conversations
- `FLASK_SECRET_KEY`: Flask application secret key
- `FLASK_DEBUG`: Debug mode (True/False)

### Model Configuration
- Disease model: `plant_disease_model.h5`
- Crop model: `crop_recommender_model.joblib`
- Model columns: `crop_model_columns.joblib`
- Label encoder: `crop_label_encoder.joblib`

## 📊 Performance

### Model Accuracy
- **Disease Diagnosis**: High accuracy with confidence scoring
- **Crop Recommendations**: District-specific recommendations
- **Response Time**: Fast analysis with real-time feedback

### Supported Formats
- **Images**: JPG, PNG, GIF (up to 16MB)
- **Districts**: All major districts of Nepal
- **Languages**: English interface with Nepali context

## 🛠️ Development

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Training New Models
- Use `train_disease_model.py` for disease classification
- Use `train_crop_model.py` for crop recommendations
- Ensure proper data preprocessing and validation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TensorFlow**: For deep learning capabilities
- **Flask**: For web framework
- **Google Gemini AI**: For conversational AI features
- **Nepali Agricultural Community**: For domain expertise and testing

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the [SETUP.md](SETUP.md) for detailed setup instructions
- Review the troubleshooting section in the documentation

## 🔮 Future Enhancements

- [ ] Multi-language support (Nepali interface)
- [ ] Mobile app development
- [ ] Integration with weather APIs
- [ ] Soil analysis integration
- [ ] Community features for farmers
- [ ] Advanced disease prediction models

---

**Made with ❤️ for Nepali Farmers**
