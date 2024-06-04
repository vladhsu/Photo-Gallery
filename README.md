**Photo Management Web App**

`For login: user:admin, password:password`

1. **How to use**
    You will need to have Python3 and Docker installed on your machine.
    After installing the required software, run the following commands:
    Clone the repository:
        -`git clone`
    Navigte to the directory where the dockerfile is situated:
        -`cd test`
    Run the following commands:
        - `docker build -t photo-gallery .`
        - `docker run -p 5000:5000 -it photo-gallery`

2. **Project Structure**
    The project contains two main directories: `static` and `templates`. The `static` directory contains the profile picture for the about page and images along with their thumbnails organized by categories. The `templates` directory contains the templates for the front-end. The base template includes the navigation bar and styles for various components of the application. The index template extends the base template and contains the actual gallery. The login template contains the login form. The upload template contains the upload form and the About Me template contains the profile page. At the same level as the `static` and `templates` directories, there is a Dockerfile, this readme, the `requirements.txt` file, and the Python file where we have the backend.

3. **Appearance**
    Upon launch, the user lands on the home page, where the current gallery is presented. If there are no pictures in the gallery, a message is displayed. The navbar is always present and has two states. When the administrator is not logged in, the upload form does not appear, but when they log in, the form appears.

4. **Functionality**
    The functionality is provided by the backend. In the `server.py` file, you can see how each route is managed. The `'/'` route is the route to the start page of the application. Here, the image gallery is displayed through thumbnails. The `'/image/<path:filename>'` route is the route for displaying a specific image. The user can access an image by clicking on its thumbnail in the gallery. The `'/login'` route is the route for authentication. If the user is already authenticated, they will be redirected to the main page. Otherwise, the login form will be displayed. The `'/logout'` route is the route for logging out. The user will be logged out and redirected to the main page. The `'/upload'` route manages the uploading of images to the application. This accepts both HTTP GET and POST methods. If the method is POST, it means that the user has submitted the upload form data. In this case, the function will process the uploaded image. First, it checks if the user is authenticated. If they are not authenticated, it redirects them to the login page. Then, it extracts the image and name from the form data. If the name is not provided, it uses the filename of the image. It also extracts the category from the form data. If it is not provided, it uses 'default' as the category. It creates a secure filename for the image using the `secure_filename` function. If the name does not have an extension, it adds the original extension of the image. It creates a directory for the specified category, if it does not already exist. It saves the image in the category directory. It opens the image using the PIL (Pillow) library and creates a thumbnail of it. It saves the thumbnail in the same directory as the original image, but with the suffix '_thumb' added to the name. It sends a flash message to inform the user that the upload was successful. Finally, it redirects the user back to the main page. If the method is GET, it means that the user wants to see the upload form. In this case, the function will display the upload form. It returns the 'upload.html' template, which contains the upload form. The `'/delete_image/<path:filename>'` route is the route for deleting an image. If the user is not authenticated, they will be redirected to the login page. Otherwise, the specified image will be deleted. The `'/about'` route is the route for the "About Me" page. Here, information about the author of the application is displayed. Finally, the application is started with `app.run(host='0.0.0.0', debug=True)`. This makes the server accessible at the address http://localhost:5000 on the local machine.