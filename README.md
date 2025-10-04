<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Task Management System - README</title>
  <style>
    body {
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      margin: 40px;
      background-color: #fafafa;
      color: #333;
      line-height: 1.6;
    }
    h1, h2, h3 {
      color: #2c3e50;
    }
    code {
      background: #f4f4f4;
      padding: 3px 6px;
      border-radius: 4px;
    }
    pre {
      background: #f4f4f4;
      padding: 10px;
      border-radius: 6px;
      overflow-x: auto;
    }
    ul {
      margin-left: 20px;
    }
    .highlight {
      background: #e3f2fd;
      padding: 15px;
      border-left: 4px solid #2196f3;
    }
  </style>
</head>
<body>

  <h1>🧭 Task Management System (Django)</h1>
  <p>A simple and efficient <strong>Task Management System</strong> built with Django. It allows admins to assign tasks to users, and users can mark tasks as completed, log hours worked, and optionally add a completion report.</p>

  <h2>🚀 Features</h2>
  <ul>
    <li>Custom <strong>User Model</strong> with roles: Super Admin, Admin, and User</li>
    <li>Role-based dashboards for Admins and Users</li>
    <li>Task creation, assignment, and reporting system</li>
    <li>JWT-based authentication (stored securely in cookies)</li>
    <li>Environment-based configuration using <code>.env</code></li>
  </ul>

  <h2>📁 Project Structure</h2>
  <pre>
task_management/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── user_dashboard.html
│   └── ...
│
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── task_management/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── .env
├── .env.example
├── manage.py
└── README.md
  </pre>

  <h2>⚙️ Installation</h2>
  <ol>
    <li><strong>Clone the repository:</strong></li>
    <pre><code>git clone https://github.com/yourusername/task_management.git</code></pre>

    <li><strong>Navigate into the project folder:</strong></li>
    <pre><code>cd task_management</code></pre>

    <li><strong>Create and activate a virtual environment:</strong></li>
    <pre><code>python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux</code></pre>

    <li><strong>Install dependencies:</strong></li>
    <pre><code>pip install -r requirements.txt</code></pre>

    <li><strong>Copy and configure your environment variables:</strong></li>
    <pre><code>cp .env.example .env</code></pre>

    <li><strong>Edit your <code>.env</code> file:</strong></li>
    <pre><code>SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost</code></pre>

    <li><strong>Run migrations:</strong></li>
    <pre><code>python manage.py makemigrations
python manage.py migrate</code></pre>

    <li><strong>Create a Super Admin manually (since custom user model is used):</strong></li>
    <pre><code>python manage.py shell</code></pre>
    <div class="highlight">
      <pre><code>from accounts.models import User
user = User(username="superadmin", email="superadmin@example.com", phone_number="9999999999", role="Super Admin")
user.set_password("admin123")
user.save()</code></pre>
    </div>

    <li><strong>Run the development server:</strong></li>
    <pre><code>python manage.py runserver</code></pre>
  </ol>

  <h2>🌐 Usage</h2>
  <ul>
    <li>Access the site at <code>http://127.0.0.1:8000/</code></li>
    <li>Super Admins can create Admins and Users, and assign Users to Admins.</li>
    <li>Admins can view and manage tasks for their assigned Users.</li>
    <li>Users can view their assigned tasks and mark them complete.</li>
  </ul>

  <h2>🧩 Technologies Used</h2>
  <ul>
    <li>Django 5.2+</li>
    <li>Python 3.11+</li>
    <li>SQLite (default) / PostgreSQL (optional)</li>
    <li>Bootstrap 5 (for UI)</li>
    <li>python-dotenv / decouple (for environment management)</li>
  </ul>

  <h2>📄 Example <code>.env.example</code> File</h2>
  <pre><code>SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=sqlite:///db.sqlite3

  </code></pre>

  <hr>
  <p align="center">Made using Django and Python</p>

</body>
</html>
