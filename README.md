# Mars Explorer 🚀

An interactive web application built with Streamlit that provides comprehensive information about Mars, featuring real-time NASA data, AI-powered chat, and educational quizzes.

## Features

### 🏠 Home Dashboard
- Dynamic welcome interface with latest Mars updates
- NASA's Astronomy Picture of the Day (APOD) integration
- Recent mission highlights and discoveries

### 🤖 AI Chatbot
- Interactive conversations about Mars and space exploration
- Powered by Groq's LLM API
- Contextual responses with scientific accuracy

### 📊 Mars Information Center
- Comprehensive Mars facts and statistics
- Interactive slideshow of Mars features:
  - Olympus Mons
  - Valles Marineris
  - Polar Ice Caps
  - Impact Craters
- Research updates and mission timelines

### 🛸 NASA Data Integration
- Real-time Mars weather data visualization
- Mars Rover photo gallery with filtering options
- Mission status updates and statistics

### 🎮 Space Quiz
- Progressive difficulty levels
- AI-generated questions about Mars and space
- Immediate feedback and explanations
- Progress tracking system

## Installation
```
# Clone the repository:
git clone https://github.com/Humam-hub/Mars.git 
cd mars-explorer

# Install required packages:
pip install -r requirements.txt

# Set up environment variables:
Create a `.env` file with:

GROQ_API_KEY=your_groq_api_key
NASA_API_KEY=your_nasa_api_key

# Run the application:
streamlit run app.py
```
## Project Structure
```
mars-explorer/
├── app.py # Main application file
├── requirements.txt # Project dependencies
├── sections/
│ ├── 1_AIChatbot.py # AI chat implementation
│ ├── 2_MarsInformation.py # Mars facts and features
│ ├── 3_NASAData.py # NASA API integration
│ └── game.py # Quiz implementation
└── utils.py # Utility functions
```
## Dependencies

- Streamlit
- Groq
- Plotly
- Pandas
- Requests
- python-dotenv

## API Integration

The project integrates with two main APIs:
1. NASA API - For APOD and Mars data
2. Groq API - For AI chat functionality

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NASA Open APIs
- Groq AI
- Streamlit Community
- Mars Science Laboratory Mission

## Contact

LinkedIN - [Muhammad Humam Tahir](https://www.linkedin.com/in/muhammad-humam-tahir-470267178/) 

Project Link: [https://github.com/Humam-hub/Mars/tree/main](https://github.com/Humam-hub/Mars/tree/main)
