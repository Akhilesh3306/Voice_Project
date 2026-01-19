# Voice-Based Health Monitoring System

A web application that analyzes voice samples to infer health indicators such as stress level, fatigue, respiratory issues, and emotional state using voice signal features.

## Features

- **Voice Recording**: Record audio directly from your microphone
- **File Upload**: Upload audio files (WAV, MP3, M4A, FLAC, OGG)
- **Feature Extraction**: 
  - MFCC (Mel-Frequency Cepstral Coefficients)
  - Pitch (Fundamental Frequency)
  - Energy (RMS Energy)
  - Speech Rate (Syllables per second)
- **Health Analysis**: Predicts:
  - Stress Level (Low/Medium/High)
  - Fatigue (Low/Medium/High)
  - Respiratory Issues (None/Mild/Possible)
  - Emotional State (Neutral/Positive/Negative/Anxious)
- **Dashboard**: View your health history and track changes over time
- **Database Storage**: SQLite database for storing analysis reports

## Project Structure

```
voiceproject/
├── app.py                 # Flask main application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── model/                # ML model and feature extraction
│   ├── __init__.py
│   ├── feature_extraction.py
│   ├── health_predictor.py
│   ├── train_model.py    # Model training script (optional)
│   └── visualization.py  # Feature visualization (optional)
├── database/             # Database handling
│   ├── __init__.py
│   └── db_handler.py
├── templates/            # HTML templates
│   └── index.html
├── static/               # CSS and JavaScript
│   ├── style.css
│   └── script.js
└── uploads/              # Uploaded audio files (created automatically)
```

## Installation

1. **Clone or download the project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Recording Audio
1. Click "Start Recording" button
2. Speak into your microphone
3. Click "Stop Recording" when done
4. The system will automatically analyze your voice

### Uploading Audio File
1. Click "Choose File" and select an audio file
2. Click "Upload & Analyze"
3. Wait for the analysis to complete

### Viewing Results
- Analysis results are displayed immediately after processing
- Each health indicator shows:
  - Predicted value
  - Confidence score
  - Visual confidence bar
- View your health history in the dashboard below

## API Endpoints

- `GET /` - Main page
- `POST /api/upload` - Upload audio file for analysis
- `POST /api/analyze` - Analyze recorded audio
- `GET /api/reports` - Get all health reports
- `GET /api/reports/<id>` - Get specific report
- `DELETE /api/reports/<id>` - Delete a report

## Technical Details

### Feature Extraction
- **MFCC**: 13 coefficients extracted using Librosa
- **Pitch**: Fundamental frequency detection using autocorrelation
- **Energy**: RMS energy calculation
- **Speech Rate**: Estimated using onset detection and zero-crossing rate

### Health Prediction
Currently uses a **rule-based approach** with feature thresholds:
- High pitch + high variation → Stress
- Low pitch + low energy → Fatigue
- Abnormal pitch range + low energy → Respiratory issues
- Pitch + energy patterns → Emotional state

### Machine Learning
The project includes a training script (`model/train_model.py`) for future ML model integration. To use ML models:
1. Collect labeled training data
2. Run the training script
3. Update `HealthPredictor` to load trained models

## Database

SQLite database (`database/health_reports.db`) stores:
- Timestamp
- Audio filename
- Health indicators with confidence scores
- Extracted features (JSON)
- Optional notes

## Optional Features

### Visualization
The `model/visualization.py` module provides functions to visualize:
- MFCC features
- Audio waveform
- Spectrogram
- Feature comparison charts

### PDF Reports
PDF report generation can be added using libraries like `reportlab` or `weasyprint`.

## Browser Compatibility

- Modern browsers with Web Audio API support
- Chrome, Firefox, Edge, Safari (latest versions)
- Requires microphone access for recording

## Limitations

- **Rule-based predictions**: Current predictions are based on thresholds, not trained ML models
- **No medical diagnosis**: This is for educational/research purposes only
- **Audio quality**: Results depend on audio quality and recording conditions
- **Language**: Optimized for English speech patterns

## Future Improvements

- [ ] Train ML models with actual labeled data
- [ ] Add PDF report generation
- [ ] Implement feature visualization in UI
- [ ] Add user authentication
- [ ] Support for multiple languages
- [ ] Real-time audio streaming analysis
- [ ] Export data to CSV/JSON
- [ ] Advanced visualization dashboards

## Dependencies

- Flask: Web framework
- Librosa: Audio analysis
- NumPy: Numerical computations
- SciPy: Scientific computing
- Scikit-learn: Machine learning
- Matplotlib: Visualization

## License

This project is for educational purposes only. Not intended for medical diagnosis.

## Disclaimer

**This system is for educational and research purposes only. It should NOT be used for medical diagnosis or treatment decisions. Always consult with qualified healthcare professionals for health-related concerns.**
