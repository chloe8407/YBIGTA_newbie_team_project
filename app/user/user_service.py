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
        """
        이메일과 비밀번호 통한 사용자 인증

        arg:
            user: email로 구분한 사용자 객체

        return:
            ValueError: 이메일 찾지 못한 경우에 User not Found 에러
            ValueError: 비밀번호가 틀릴 경우에 Invalid ID/PW 에러
        """
        
    def register_user(self, new_user: User) -> User:
        ## TODO
        exist_user = self.repo.get_user_by_email(new_user.email)
        
        if exist_user != None:
            raise ValueError("User already Exists.")

        return self.repo.save_user(new_user)
        """
        이메일을 통한 새로운 유저 등록

        arg:
            exist_user: email로 구분한 기존 사용자 객체

        return:
            ValueError: 이메일이 존재하는 경우에 User already Exist 에러
            self.repo.save_user(new_user): 새로운 사용자 정보 저장 후 사용자 객체 반환
        """

    def delete_user(self, email: str) -> User:
        ## TODO
        user = self.repo.get_user_by_email(email)

        if user == None:
            raise ValueError("User not Found.")

        return self.repo.delete_user(user)
        """
        기존 유저 삭제

        arg:
            user: email로 구분한 사용자 객체

        return:
            ValueError: 이메일 찾을 수 없는 경우에 User not Found 에러
            self.repo.delete_user(user): 사용자 정보 삭제 후 삭제된 사용자 객체 반환
        """
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
        """
        이메일을 통한 유저 비밀번호 업데이트

        arg:
            user: email로 구분한 사용자 객체
            updated_user: 비밀번호 변경한 사용자 객체
        return:
            ValueError: 이메일 찾을 수 없는 경우에 User not Found 에러
            updated_user: 비밀번호 변경 후의 사용자 객체 반환
        """