📬 Messaging App API

A RESTful messaging API built with Django and Django REST Framework (DRF).
This project allows users to create conversations, send messages, and manage participants in a structured and scalable way.

🏗 Project Structure
messaging_app/
├── chats/                  # App containing messaging functionality
│   ├── migrations/
│   ├── models.py           # User, Conversation, Message models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API endpoints using ViewSets
│   ├── urls.py             # App-level URL routing
│   └── admin.py
├── messaging_app/          # Project settings
│   ├── settings.py
│   ├── urls.py             # Project-level URL routing
│   └── wsgi.py
├── manage.py
├── README.md
└── requirements.txt

⚡ Features

Custom User Model: Extends Django’s AbstractUser with UUID, role, phone_number, and created_at.

Conversations: Track participants using a many-to-many relationship.

Messages: Users can send messages within conversations.

RESTful API: Built with DRF ViewSets for scalable endpoints.

Nested Serialization: Conversations include participants and messages.

🛠 Setup Instructions

Clone the repository

git clone <your-repo-url>
cd messaging_app


Create a virtual environment

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


Apply migrations

python manage.py makemigrations
python manage.py migrate


Create a superuser (for admin access)

python manage.py createsuperuser


Run the server

python manage.py runserver

🚀 API Endpoints

Base URL: http://127.0.0.1:8000/api/

Endpoint	Method	Description
/conversations/	GET	List all conversations
/conversations/	POST	Create a new conversation
/messages/	GET	List all messages
/messages/	POST	Send a message in a conversation
Example JSON Payloads

Create Conversation

{
  "participants": ["user_uuid_1", "user_uuid_2"]
}


Send Message

{
  "conversation": "conversation_uuid",
  "sender": "user_uuid",
  "message_body": "Hello, this is a test message!"
}

👥 Models
User

user_id: UUID (Primary Key)

first_name, last_name, email

password_hash

phone_number

role: guest, host, admin

created_at: Timestamp

Conversation

conversation_id: UUID (Primary Key)

participants: Many-to-Many Users

created_at: Timestamp

Message

message_id: UUID (Primary Key)

conversation: ForeignKey to Conversation

sender: ForeignKey to User

message_body: Text

sent_at: Timestamp

🔧 Tools Used

Python 3.x

Django 4.x

Django REST Framework

SQLite (default DB, can be replaced with PostgreSQL)

📄 Notes

The API supports nested serialization to include messages and participants in conversations.

All models use UUIDs as primary keys for better security and scalability.

Tested locally with DRF browsable API and Postman.

✅ License

This project is for educational purposes as part of the ALX backend curriculum.