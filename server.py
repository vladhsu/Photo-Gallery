from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Directory where images will be uploaded
app.config['SECRET_KEY'] = 'your-secret-key'  # Secret key for the app

@app.route('/', methods=['GET'])
def home():
    images = {}
    # Traverse the upload directory and add images to their respective categories
    for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            if file.endswith('_thumb.jpg') or file.endswith('_thumb.png'):
                category = os.path.basename(root)
                if category not in images:
                    images[category] = []
                images[category].append(os.path.join(category, file))
    return render_template('index.html', categories=images)  # Display the main page with images

@app.route('/image/<path:filename>', methods=['GET'])
def display_image(filename):
    # Display a specific image
    full_image_path = filename.replace('_thumb', '')
    return send_from_directory(app.config['UPLOAD_FOLDER'], full_image_path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # User authentication
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            session['username'] = username
            flash('Successfully logged in')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')  # Display the login form

@app.route('/logout', methods=['GET'])
def logout():
    # User logout
    session.pop('username', None)
    flash('Successfully logged out')
    return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Image upload
    if request.method == 'POST':
        if 'username' not in session:
            flash('You need to log in first')
            return redirect(url_for('login'))

        image = request.files['image']
        name = request.form.get('name', image.filename)
        category = request.form.get('category', 'default')

        filename = secure_filename(name)
        if '.' not in filename:
            filename += os.path.splitext(image.filename)[1]
        category_path = os.path.join(app.config['UPLOAD_FOLDER'], category)
        
        os.makedirs(category_path, exist_ok=True)

        path = os.path.join(category_path, filename)
        image.save(path)
        # Create a thumbnail
        img = Image.open(path)
        img.thumbnail((200, 200))
        base, ext = os.path.splitext(path)
        thumbnail_path = base + '_thumb' + ext
        img.save(thumbnail_path, format=img.format)

        flash('Image uploaded successfully')
        return redirect(url_for('home'))
    else:
        return render_template('upload.html')  # Display the upload form

@app.route('/delete_image/<path:filename>', methods=['POST'])
def delete_image(filename):
    # Image deletion
    if 'username' not in session:
        flash('You need to log in first')
        return redirect(url_for('login'))

    full_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    thumbnail_path = full_image_path.replace('.jpg', '_thumb.jpg').replace('.png', '_thumb.png')

    try:
        if os.path.exists(full_image_path):
            os.remove(full_image_path)
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        flash('Image deleted successfully')
    except Exception as e:
        flash(f'Error deleting image: {str(e)}')

    return redirect(url_for('home'))

@app.route('/about', methods=['GET'])
def about():
    return render_template('about_me.html')  # Display the "About Me" page

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Start the application
