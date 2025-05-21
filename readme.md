# Django AllAuth Project Template

A robust Django starter project with django-allauth integration, ready for rapid development.

## Features

- User authentication (signup, login, password reset)
- Social authentication (optional)
- Environment-based settings (development/production)
- Bootstrap 5 integration
- Static files configuration
- Ready-to-use templates

## Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/django-all-auth.git your-project-name
cd your-project-name
```

### 2. Create a virtual environment

In VS code you might need to run this command before you can run any scripts

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Copy env.example and modify

```bash
cp env.py.example env.py
# Edit env.py with your settings
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 6.1 Creating Static Directories

The project expects certain static directories to exist. Create them using:

```bash
# Create static directories
mkdir -p static/css static/js static/images

# Create basic files
echo "/* Custom styles */" > static/css/style.css
echo "// Project scripts" > static/js/main.js
```

### 7. Create a site object

```bash
python manage.py shell
```

```bash
from django.contrib.sites.models import Site
Site.objects.update_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'Development'})
exit()
```

### 8. Run the server

```bash
python manage.py runserver
```

### 9. Comprehensive gitignore included

With a mind to keeping your SECRET_KEY's secure

### Repository Management

#### Update Repository URL

```bash
git remote -v

git remote remove origin

# Add your new repository as the origin
git remote add origin https://github.com/yourusername/my-new-project.git

# Push your code to the new repository
git push -u origin main
```

Now you have a django project with all auth installed ready to go make whatever you want out of it.

Go get it!