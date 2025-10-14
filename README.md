# Pet Adoption & Welfare Hub

A comprehensive Django-based web application for pet adoption, lost & found pets, and animal welfare management with advanced user profiles and admin functionality.

## 🚀 New Features

### Enhanced User Registration & Profiles
- **Extended Registration**: Age, phone number, gender, and location fields
- **Profile Management**: Complete user profiles with detailed information
- **Contact Integration**: Pet owners can provide contact details for inquiries

### Advanced Pet Management
- **Detailed Pet Information**: Age, gender, description, contact information
- **Multiple Pet Categories**: For Adoption, Lost Pets, Found Pets, Adopted/Reunited
- **Auto-Status Updates**: Found pets automatically move to adoption after 15 days
- **Image Upload**: Pet photo management with fallback placeholders

### Smart Found Pet System
- **15-Day Rule**: Found pets automatically transfer to adoption if unclaimed
- **Countdown Display**: Visual indicators showing days remaining
- **Automatic Management**: Background process handles status transitions
- **Owner Notification**: Clear timeline for pet recovery

### Multi-Level Admin System
- **Limited Admin Accounts**: Maximum 3 admin accounts allowed
- **Admin Registration**: Special registration with security code
- **Admin Dashboard**: Comprehensive overview with statistics
- **Pet Management**: Full CRUD operations for all pets
- **User Management**: View and manage all user accounts
- **Status Controls**: Real-time pet status updates

### Improved User Experience
- **Modern UI**: Bootstrap 5 with custom styling
- **Dark/Light Theme**: Toggle between themes
- **Responsive Design**: Mobile-friendly interface
- **Interactive Elements**: Real-time updates and confirmations
- **Better Navigation**: Intuitive menu structure with admin access

## 📁 Project Structure
```
├── db.sqlite3                          # SQLite database
├── manage.py                           # Django management script
├── home/                               # Django project settings
│   ├── settings.py                     # Application configuration
│   ├── urls.py                        # Main URL routing
│   └── ...
├── webapp/                            # Main application
│   ├── models.py                      # Database models (Pet, UserProfile, AdminProfile)
│   ├── views.py                       # Application views and logic
│   ├── forms.py                       # Form definitions
│   ├── admin.py                       # Admin interface configuration
│   ├── urls.py                        # App-specific URLs
│   ├── management/                    # Custom management commands
│   │   └── commands/
│   │       └── move_found_pets.py     # Auto-move found pets command
│   ├── templates/webapp/              # HTML templates
│   │   ├── base.html                  # Base template with navigation
│   │   ├── register.html              # Enhanced user registration
│   │   ├── admin_register.html        # Admin registration
│   │   ├── dashboard.html             # User dashboard
│   │   ├── admin_dashboard.html       # Admin dashboard
│   │   ├── pet_details.html           # Detailed pet view
│   │   ├── pet_list.html              # Pet listings with countdown
│   │   ├── add_pet.html               # Pet creation form
│   │   └── ...
│   └── static/webapp/                 # Static files (CSS, JS)
└── media/pet_images/                  # Uploaded pet images
```

## 🛠 Installation & Setup

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abhijit1018/Pet-Adoption-app.git
   cd Pet-Adoption-app
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django pillow
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🔧 Configuration

### Database Configuration
The application uses SQLite by default. To use MySQL:
1. Uncomment the MySQL configuration in `home/settings.py`
2. Install MySQL connector: `pip install mysqlclient`
3. Update database credentials

### Admin Account Setup
1. Visit `/admin-register/` to create admin accounts
2. Use admin code: `PET_ADMIN_2025`
3. Maximum 3 admin accounts allowed

### Management Commands
Run the found pet auto-transfer command:
```bash
python manage.py move_found_pets
```

## 🎯 Key Features

### For Users
- **Register** with detailed profile information
- **Add pets** for adoption, report lost/found pets
- **Search & browse** available pets by category
- **Request adoption** with messaging system
- **Track requests** and manage incoming applications
- **View countdown** for found pets

### For Pet Owners
- **Post detailed pet information** with photos and descriptions
- **Manage adoption requests** with approve/reject functionality
- **Update pet status** throughout the process
- **Provide contact information** for direct communication

### For Administrators
- **Comprehensive dashboard** with statistics and alerts
- **Manage all pets** across the platform
- **View user accounts** and activity
- **Monitor found pets** approaching adoption deadline
- **Access Django admin** for advanced management

## 🔄 Auto-Management Features

### Found Pet Auto-Transfer
- Found pets automatically move to "For Adoption" status after 15 days
- Visual countdown shows remaining days
- Batch processing via management command
- Can be automated with cron jobs or task schedulers

### Status Management
- Real-time status updates from admin panel
- Automatic date tracking for found pets
- Status validation and consistency checks

## 🎨 User Interface

### Modern Design
- Bootstrap 5 framework
- Custom CSS styling
- Font Awesome icons
- Responsive grid layouts

### Theme Support
- Dark/Light mode toggle
- Persistent theme preferences
- Smooth transitions

### Interactive Elements
- Real-time form validation
- AJAX status updates
- Modal dialogs
- Progress indicators

## 🚀 Deployment

### Production Considerations
1. **Security**: Update SECRET_KEY and disable DEBUG
2. **Database**: Use PostgreSQL or MySQL for production
3. **Static Files**: Configure static file serving
4. **Media Files**: Set up media file handling
5. **Environment Variables**: Use environment-specific settings

### Suggested Production Stack
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: PostgreSQL
- **Cache**: Redis
- **Storage**: AWS S3 for media files

## 🔧 Customization

### Adding New Pet Fields
1. Update the Pet model in `models.py`
2. Create and apply migrations
3. Update forms and templates accordingly

### Extending User Profiles
1. Modify UserProfile model
2. Update registration forms
3. Adjust templates and views

### Custom Status Workflows
1. Update STATUS_CHOICES in models
2. Modify business logic in views
3. Update templates and admin interface

## 🐛 Troubleshooting

### Common Issues
- **Migration errors**: Delete db.sqlite3 and re-run migrations
- **Static files not loading**: Run `python manage.py collectstatic`
- **Image upload issues**: Check MEDIA_ROOT and MEDIA_URL settings
- **Admin registration failing**: Verify admin code and account limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License
MIT License - See LICENSE file for details

## 👨‍💻 Author
**Abhijit1018**
- GitHub: [@Abhijit1018](https://github.com/Abhijit1018)

## 🙏 Acknowledgments
- Django framework and community
- Bootstrap for UI components
- Font Awesome for icons
- Contributors and testers

---
*Built with ❤️ for animal welfare and pet adoption*
