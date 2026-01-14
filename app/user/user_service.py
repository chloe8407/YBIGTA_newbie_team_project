from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate

class UserService:
    def __init__(self, userRepoitory: UserRepository) -> None:
        self.repo = userRepoitory

    def login(self, user_login: UserLogin) -> User:
        ## TODO
        user = self.repo.get_user_by_email(user_login.email)
        
        if user == None:
            raise ValueError("User not Found.")
        
        if user.password != user_login.password:
            raise ValueError("Invalid ID/PW")
        
        return user
        
    def register_user(self, new_user: User) -> User:
        ## TODO
        exist_user = self.repo.get_user_by_email(new_user.email)
        
        if exist_user != None:
            raise ValueError("User already Exists.")

        return self.repo.save_user(new_user)

    def delete_user(self, email: str) -> User:
        ## TODO
        user = self.repo.get_user_by_email(email)

        if user == None:
            raise ValueError("User not Found.")

        return self.repo.delete_user(user)

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        ## TODO
        user = self.repo.get_user_by_email(user_update.email)

        if user == None:
            raise ValueError("User not Found.")
        
        updated_user = User(
            email=user.email,
            password=user_update.new_password,
            username=user.username
        )

        self.repo.save_user(updated_user)
        return updated_user
        