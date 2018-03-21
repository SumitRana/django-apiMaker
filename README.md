## django-apiMaker

django-apiMaker is a django based app , simply to automate the process of making apis for a defined django
model by executing a single command .

The App generates Interface File within the app directory of the model , generating code for handling 
GET, POST ,PUT ,DELETE request handling for a model .

Advantages :
 * App makes project more structured according to MVC architecture.
 * App seperates the Http Interface code with the logical code .
 * App encourages to focus more on design good Database Architecture .
 * Within django app Model , Interface , other-programming-logic is separated .

#### Quick start
-----------
1. Define models within the app , add app to installed apps in settings . 
   Run Migrations and migrate to the database.

2. In project Directory :
    Run : python manage.py generateApi <appName> <modelName>

    On successful Execution of command : A Interface file will be created .

3. Add url string for the Model in the app url.py file:
	
	```python
    from . import <GeneratedFileName>
    ...

    MIDDLEWARE_CLASSES = [
        ...
        url(r'^',<GeneratedFileName>.<ModelHttpInterface>.as_view())
    ]
    ```
