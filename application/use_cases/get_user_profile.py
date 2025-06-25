from infrastructure.db.repositories.user_repository import UserRepository

# This use case depends on the UserRepository abstraction
def get_user_profile(user_id: str, user_repository: UserRepository):
    db_user = user_repository.get_by_id(user_id)
    if db_user:
        # Convert DB model to domain model if necessary
        # domain_user = User(id=db_user.user_id, name=db_user.name, ...)
        # return domain_user
        return db_user # Or return the DB model directly if it's simple
    return None # Or raise a domain exception like UserNotFoundException