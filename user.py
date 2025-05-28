import hashlib
import uuid
from typing import Optional, List
import pickle
import os
from Utils.singleton import Singleton


class User:
    """用户模型类"""

    def __init__(self, username: str,nickname: str, password: str, learned_book: int, learning_book: int, group_word: int,
                 def_learned: int, user_id: Optional[int] = None):
        self.user_id = str(uuid.uuid4())  # 默认生成唯一ID
        self.username = username
        self.nickname = nickname
        self.password_hash = self._hash_password(password)
        self.learned_book = learned_book
        self.learning_book = learning_book
        self.group_word = group_word
        self.def_learned = def_learned

    def _hash_password(self, password: str) -> str:
        """对密码进行哈希处理"""
        salt = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:16]
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${hashed_password.hex()}"

    def verify_password(self, password: str) -> bool:
        """验证密码是否正确"""
        if not self.password_hash:
            return False

        salt, stored_hash = self.password_hash.split('$')
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return stored_hash == new_hash.hex()

    def update_password(self, old_password: str, new_password: str) -> bool:
        """更新密码"""
        if not self.verify_password(old_password):
            return False
        self.password_hash = self._hash_password(new_password)
        return True

    def update_learned_book(self, learned_book: int) -> bool:
        """更新已学词书"""
        self.learned_book = learned_book
        return True

    def change_learning_book(self, learning_book: int) -> bool:
        """更新正在学习词书"""
        self.learning_book = learning_book
        return True

    def change_group_word(self, group_word: int) -> bool:
        """改变单词组数"""
        self.group_word = group_word
        return True

    def chang_def_learned(self, def_learned: int) -> bool:
        """改变单词熟练度定义"""
        self.def_learned = def_learned
        return True

    def __str__(self):
        return f"User(ID={self.user_id}, Username={self.username})"


@Singleton
class UserController:
    """用户控制器，管理所有用户操作"""

    def __init__(self):
        self.users: List[User] = []
        if os.path.exists(r"./static/user.pickle"):
            if os.path.getsize(r"./static/user.pickle") == 0:
                print("文件为空")
            else:
                with open(r"./static/user.pickle", "rb") as file:
                    self.users = pickle.load(file)
                    print("user ok")
        else:
            print("文件不存在")

    def add_user(self, username: str, nickname: str, password: str) -> User:
        """添加新用户"""
        # 检查用户名是否已存在
        if any(user.username == username for user in self.users):
            raise ValueError(f"用户名 '{username}' 已存在")

        new_user = User(username, nickname, password, 0, 0, 10, 3)
        self.users.append(new_user)
        with open(r"./static/user.pickle", "wb") as file:
            pickle.dump(self.users, file)

        return new_user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        for user in self.users:
            if user.username == username:
                return user
        return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """根据用户ID获取用户"""
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_id_by_username(self, username: str) -> Optional[int]:
        """根据用户名获取用户ID"""
        for user in self.users:
            if user.username == username:
                return user.user_id
        return None

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """修改用户密码"""
        user = self.get_user_by_username(username)
        if not user:
            return False
        with open(r"./static/user.pickle", "wb") as file:
            pickle.dump(self.users, file)

        return user.update_password(old_password, new_password)

    def login(self, username: str, password: str) -> Optional[User]:
        """用户登录验证"""
        user = self.get_user_by_username(username)
        if user and user.verify_password(password):
            return user
        return None

    def del_user(self, user_id: str) -> bool:
        """删除用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.users.remove(user)
        with open(r"./static/user.pickle", "wb") as file:
            pickle.dump(self.users, file)
        return True

    def update_learned_book(self, user_id: str, learned_book: int) -> bool:
        """更新已学词书"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        with open(r"./static/user.pickle", "wb") as file:
            pickle.dump(self.users, file)
        return user.update_learned_book(learned_book)

    def change_learning_book(self, user_id: str, learning_book: int) -> bool:
        """更新正在学习词书"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        with open(r"./static/user.pickle", "wb") as file:
            pickle.dump(self.users, file)
        return user.change_learning_book(learning_book)

    def change_group_word(self, user_id: str, group_word: int) -> bool:
        """改变单词组数"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        with open(r"./static/user.pickle", "wb") as file:
            pickle.dump(self.users, file)
        return user.change_group_word(group_word)

    def chang_def_learned(self, user_id: str, def_learned: int) -> bool:
        """改变单词熟练度定义"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        with open(r"./static/user.pickle", "wb") as file:
            pickle.dump(self.users, file)
        return user.chang_def_learned(def_learned)

    def get_all_user(self) -> List[User]:
        """获取所有用户"""
        return self.users

    def get_def_learned(self, user_id: str) -> int | None:
        """获取用户熟练度定义"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        return user.def_learned

    def get_learning_book_from_user_id(self, user_id: str) -> int | None:
        """获取用户已学词书"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        return user.learning_book

    def update_user(self, user: User, nickname: str, group_word: int, def_learned: int) -> bool:
        """更新用户信息"""
        # # 检查用户名是否已存在
        # if any(u.username == username for u in self.users if u.user_id != user.user_id):
        #     return False
        user.nickname = nickname
        user.group_word = group_word
        user.def_learned = def_learned
        # 更新用户列表
        with open(r"./static/user.pickle", "wb") as file:
            pickle.dump(self.users, file)
        return True
