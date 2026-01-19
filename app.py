"""
Flask application for Voice-Based Health Monitoring System.
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import librosa
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
import json

from model.feature_extraction import extract_all_features
from model.health_predictor import HealthPredictor
from database.db_handler import DatabaseHandler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'm4a', 'flac', 'ogg'}

# Initialize components
predictor = HealthPredictor()
db_handler = DatabaseHandler()

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_audio():
    """Handle audio file upload and analysis."""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract features
            features = extract_all_features(audio_path=filepath)
            
            if features is None:
                return jsonify({'error': 'Failed to extract features from audio'}), 500
            
            # Predict health indicators
            health_results = predictor.predict(features)
            
            # Combine results
            analysis_results = {
                'features': features,
                'health_indicators': health_results,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save to database
            report_id = db_handler.save_report(health_results, audio_filename=filename)
            analysis_results['report_id'] = report_id
            
            return jsonify(analysis_results), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_audio():
    """Analyze audio data sent directly (for recorded audio)."""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio data provided'}), 400
        
        file = request.files['audio']
        
        # Save temporary file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'recorded_{timestamp}.wav'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract features
        features = extract_all_features(audio_path=filepath)
        
        if features is None:
            return jsonify({'error': 'Failed to extract features from audio'}), 500
        
        # Predict health indicators
        health_results = predictor.predict(features)
        
        # Combine results
        analysis_results = {
            'features': features,
            'health_indicators': health_results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to database
        report_id = db_handler.save_report(health_results, audio_filename=filename)
        analysis_results['report_id'] = report_id
        
        return jsonify(analysis_results), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get all health reports."""
    try:
        limit = request.args.get('limit', 50, type=int)
        reports = db_handler.get_all_reports(limit=limit)
        return jsonify({'reports': reports}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """Get a specific report by ID."""
    try:
        report = db_handler.get_report_by_id(report_id)
        if report:
            return jsonify(report), 200
        else:
            return jsonify({'error': 'Report not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """Delete a report by ID."""
    try:
        deleted = db_handler.delete_report(report_id)
        if deleted:
            return jsonify({'message': 'Report deleted successfully'}), 200
        else:
            return jsonify({'error': 'Report not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-report/<int:report_id>', methods=['GET'])
def download_report(report_id):
    """Download health report as PDF (optional feature)."""
    try:
        report = db_handler.get_report_by_id(report_id)
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Generate PDF (simplified - returns JSON for now)
        # In production, use reportlab or similar library
        return jsonify({
            'message': 'PDF generation not implemented',
            'report': report
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
