from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    # Save the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Load and clean data
    try:
        df = pd.read_csv(filepath)
        df.dropna(inplace=True)
        if 'date' not in df.columns or 'visit' not in df.columns:
            raise ValueError("CSV must contain 'date' and 'visit' columns.")
    except Exception as e:
        return str(e)

    # Visualize data
    return visualize_data(df)

@app.route('/visualize', methods=['POST'])
def visualize_data(df):
    dates = pd.to_datetime(df['date'])
    visits = df['visit']

    plt.figure(figsize=(10, 5))
    plt.bar(dates, visits)
    plt.title('Web Traffic Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Visits')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the figure
    img_path = os.path.join('static', 'traffic_plot.png')
    plt.savefig(img_path)
    plt.close()

    return render_template('visualize.html', img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)
