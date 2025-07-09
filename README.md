# Survey Form Builder

A powerful and flexible survey form builder that allows users to create and manage surveys with ease.
![image](FormBuilder\media\Survey App - Google Chrome 2025-07-09 09-38-33.mp4)

## Table of content
- [Installation](#installation)
- [Features](#features)
    - [Manage Surveys](#manage-a-survey)
    - [Option Config](#option-survey)
    - [Question Types](#questioin-type)

- [For Contributor](#for-contributor)


## Installation
- Install django using:
    ```
    pip install Django
    django-admin startproject SurveyBuilder
    cd SurveyBuilder
    python manage.py startapp survey
    ```

  - Add `survey` to your `INSTALLED_APPS` setting like this
      ```
      INSTALLED_APPS = [
          ...
            'survey',
            'tailwind',# dependency
            'theme', # dependency
            'django_browser_reload",# dependency
      ]
      ```


    ```
- Run `python manage.py migrate` to create the surveys models.
- Include url `surveys` in your root url
    ```
    ....

    urlpatterns = [
        path('admin/', admin.site.urls),
        .....
        path('surveys/', include('survey.urls'))
    ]
    ```
  
- Access `http://127.0.0.1:8000/surveys/create/` to enter admin page to create a survey.
- Access `http://127.0.0.1:8000/user/dashboard` get list of survey 
- Access `http://127.0.0.1:8000/surveys/{id}` get form of survey


## Features
#### Manage a Survey
You must as superuser to manage survey. You can `create, edit, delete, search and show all available survey`. To manage survey you can access `http://localhost:8000/surveys/create/`.
      ![image](C:\Users\LOKESH\Desktop\Form_Builder\FormBuilder\media\Screenshot 2025-07-09 094126.png)

#### Option Survey
You can use the options below
- `editable`: this option allows the user to edit the answer
- `deletable`: this option allows the user to delete the answer
- `duplicate entry`: this option allows users to submit more than once
- `private reponse`: this option makes the answer list only visible to admin
- `can anonymous user`: This option allows users without authentication to submit

#### Questioin Type
Available field types include:
![image](C:\Users\LOKESH\Desktop\Form_Builder\FormBuilder\media\Screenshot 2025-07-09 094239.png)
- Text 
- Number
- Options
- Checkbox

## For Contributor
### Required Tools
- Python 3.13.3
- django  5.2.3
- clone project
- symlink app to `FormBuilder`

- create `env` development
- active `env`
- enter directory `SurveyBuilder`
- now, you can access all command `manage.py`