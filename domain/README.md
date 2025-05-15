# Domain Folder

  The `/domain` folder contains the core business logic and entities of the JeruyiqAPI project, following clean architecture principles. It is independent of external frameworks and focuses on the application's domain rules.

  ## Structure
  - **`models/`**: Defines domain entities.
    - `chat.py`: Represents a chat session with message handling.
    - `user.py`: Represents a user with validation logic.
  - **`services/`**:
    - **`ai_service/`**:
      - `gemini_ai_model.py`: Implements interaction with the Gemini AI model.
    - **`chat_service/`**:
      - `chat_service.py`: Manages chat sessions and AI interactions.
    - **`user_service/`**:
      - `user_service.py`: Handles user creation and password verification.

  ## Usage
  - The `models/` module defines the core entities used across the application.
  - The `services/` module encapsulates business logic, interacting with entities and external services via ports defined in `/core`.

  ## Development Guidelines
  - Keep the `/domain` layer independent of external frameworks (e.g., Flask, SQLAlchemy).
  - Use `/core/entities/` for shared definitions like `Role` and `Permission`.
  - Ensure all business logic in `services/` is covered by unit tests in `tests/unit/domain/`.
  - Validate entity data in the `models/` layer to enforce domain rules.