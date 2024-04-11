# conversational-state-bot
Converesational Stateful chat bot

## Setup Instructions

### Prerequisites
- Python 3.x
- Django
- Postgres
- Docker
- docker-compose

### Installation Steps
1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd <project_directory>`
3. Configure .env environmental variables for Database creation on project root
    - DATABASE_NAME=''
    - DATABASE_USER=''
    - DATABASE_PASSWORD=''
4. Build Container: `docker-compose -f docker-compose.yml build`
5. Run compose-up: `docker-compose up`
6. Makemigrations: `docker-compose exec web python manage.py makemigrations`
7. Apply migrations: `docker-compose exec web python manage.py migrate`
8. Development Server should be running and create a superuser

## DRF API Usage Examples with cURL

### Sending a Message
```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello"}' http://0.0.0.0:8000/api/send-message/
```

### Retrieving Conversation History
```bash
curl http://0.0.0.0:8000/api/chat/
```

## Explanation of the State Machine Logic

The state machine logic governs the behavior of the chatbot, determining its responses based on the current state and user input. Here's a brief overview of the state machine logic:
- **Initialization**: When a conversation starts, the default state is set to greeting.
- **Processing User Input**: We make use of an open source LLM on hugging face to classify the user input into states and generate  a response from openai's chatGPT
- **State Transition**: Once we get a response/error, we store the user and system response in the Log model which has a post save signal to update the state
- **Session**: A session is created from the start of the first user input and persists. The system will have a record of past conversations but will not necessarily allude / make inferebce from them


## Assumptions or Design Decisions Made

### Assumptions
- Only text input is expected from the user.
- The interaction is conversational based and not flow based

### Design Decisions
- **System Response Layer**: Using chatGPT's Assistant as the response layer does most of the heavy lifting and enables predefine the conversation etiquette and can accomodate more states without much work.
- Furthermore there will be two sources of information for conversations.
- **Authentication and Authorization**: This is session based and relies on django's built in authentication system. They key factors being that the session management is robust and integrates well with the ORM.
- **Error Handling**: Errors were concetrated on the assistant functionality and the error handling is extensive. In the future fallback mechanisms would have to instituted such as passing the conversation to an agent the system cannot compute, retries on failed user inputs.
- **Testing Approach**: Took the approach of unit tests as the codebase is quite modular. a coverage of 91% was reported.



