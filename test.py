import unittest
import os
from user import User, UserController


class TestUserAndUserController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """在测试开始前清理或创建测试环境"""
        cls.user_controller = UserController()
        # 确保测试文件夹存在
        if not os.path.exists('./static'):
            os.makedirs('./static')
        # 清空用户数据文件
        with open('./static/user.pickle', 'wb') as file:
            file.truncate()

    def setUp(self):
        """每个测试用例前清理用户列表"""
        self.user_controller.users = []
        with open('./static/user.pickle', 'wb') as file:
            file.truncate()

    def test_add_user(self):
        """测试添加用户"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.nickname, 'Test Nickname')
        self.assertTrue(user.verify_password('password123'))

    def test_duplicate_username(self):
        """测试重复用户名"""
        self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        with self.assertRaises(ValueError):
            self.user_controller.add_user('testuser', 'Another Nickname', 'password456')

    def test_login_success(self):
        """测试登录成功"""
        self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        user = self.user_controller.login('testuser', 'password123')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    def test_login_failure(self):
        """测试登录失败"""
        self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        user = self.user_controller.login('testuser', 'wrongpassword')
        self.assertIsNone(user)

    def test_change_password(self):
        """测试修改密码"""
        self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        result = self.user_controller.change_password('testuser', 'password123', 'newpassword456')
        self.assertTrue(result)
        user = self.user_controller.login('testuser', 'newpassword456')
        self.assertIsNotNone(user)

    def test_delete_user(self):
        """测试删除用户"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        result = self.user_controller.del_user(user.user_id)
        self.assertTrue(result)
        self.assertIsNone(self.user_controller.get_user_by_id(user.user_id))

    def test_update_learned_book(self):
        """测试更新已学词书"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        result = self.user_controller.update_learned_book(user.user_id, 5)
        self.assertTrue(result)
        self.assertEqual(user.learned_book, 5)

    def test_change_learning_book(self):
        """测试更新正在学习词书"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        result = self.user_controller.change_learning_book(user.user_id, 3)
        self.assertTrue(result)
        self.assertEqual(user.learning_book, 3)

    def test_change_group_word(self):
        """测试改变单词组数"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        result = self.user_controller.change_group_word(user.user_id, 15)
        self.assertTrue(result)
        self.assertEqual(user.group_word, 15)

    def test_change_def_learned(self):
        """测试改变单词熟练度定义"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        result = self.user_controller.chang_def_learned(user.user_id, 7)
        self.assertTrue(result)
        self.assertEqual(user.def_learned, 7)

    def test_get_all_users(self):
        """测试获取所有用户"""
        self.user_controller.add_user('user1', 'Nickname1', 'password1')
        self.user_controller.add_user('user2', 'Nickname2', 'password2')
        users = self.user_controller.get_all_user()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, 'user1')
        self.assertEqual(users[1].username, 'user2')

import unittest
import os
import pickle
import time
from recite import ProgressController, LearnWord, Progress
from user import UserController, User
from word_book import WordController, Word


class TestProgressController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test environment before running tests"""
        cls.progress_controller = ProgressController()
        cls.user_controller = UserController()
        cls.word_controller = WordController()

        # Ensure test directories and files exist
        if not os.path.exists('./static'):
            os.makedirs('./static')
        with open('./static/progress.pickle', 'wb') as file:
            file.truncate()
        with open('./static/user.pickle', 'wb') as file:
            file.truncate()

    def setUp(self):
        """Reset data before each test"""
        self.progress_controller.progresses = []
        self.user_controller.users = []
        with open('./static/progress.pickle', 'wb') as file:
            file.truncate()
        with open('./static/user.pickle', 'wb') as file:
            file.truncate()

    def test_add_word_to_learning(self):
        """Test adding a word to the learning list"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        word = self.word_controller.add_word('testword', 'Test Definition')
        result = self.progress_controller.add_word_to_learning(user.user_id, word.word_id)
        self.assertTrue(result)
        self.assertEqual(len(self.progress_controller.get_learning_word(user.user_id)), 1)

    def test_update_word_proficiency(self):
        """Test updating word proficiency"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        word = self.word_controller.add_word('testword', 'Test Definition')
        self.progress_controller.add_word_to_learning(user.user_id, word.word_id)
        result = self.progress_controller.update_word(user.user_id, word.word_id, 5)
        self.assertTrue(result)
        proficiency = self.progress_controller.get_learning_word_proficiency(user.user_id, word.word_id)
        self.assertEqual(proficiency, 5)

    def test_add_word_from_learn_to_learned(self):
        """Test moving a word from learning to learned"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        word = self.word_controller.add_word('testword', 'Test Definition')
        self.progress_controller.add_word_to_learning(user.user_id, word.word_id)
        self.progress_controller.update_word(user.user_id, word.word_id, user.def_learned)
        learned_word_num = self.progress_controller.get_learned_word_num(user.user_id)
        self.assertEqual(learned_word_num, 1)

    def test_get_learn_word(self):
        """Test retrieving a word to learn"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        word = self.word_controller.add_word('testword', 'Test Definition')
        self.progress_controller.add_word_to_learning(user.user_id, word.word_id)
        learn_word = self.progress_controller.get_learn_word(user.user_id)
        self.assertEqual(learn_word.word_id, word.word_id)

    def test_if_in_learning_word(self):
        """Test checking if a word is in the learning list"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        word = self.word_controller.add_word('testword', 'Test Definition')
        self.progress_controller.add_word_to_learning(user.user_id, word.word_id)
        result = self.progress_controller.if_in_learning_word(user.user_id, word.word_id)
        self.assertTrue(result)

    def test_if_in_learned_word(self):
        """Test checking if a word is in the learned list"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        word = self.word_controller.add_word('testword', 'Test Definition')
        self.progress_controller.add_word_to_learning(user.user_id, word.word_id)
        self.progress_controller.update_word(user.user_id, word.word_id, user.def_learned)
        result = self.progress_controller.if_in_learned_word(user.user_id, word.word_id)
        self.assertTrue(result)

    def test_get_learned_word_num(self):
        """Test retrieving the number of learned words"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        word = self.word_controller.add_word('testword', 'Test Definition')
        self.progress_controller.add_word_to_learning(user.user_id, word.word_id)
        self.progress_controller.update_word(user.user_id, word.word_id, user.def_learned)
        learned_word_num = self.progress_controller.get_learned_word_num(user.user_id)
        self.assertEqual(learned_word_num, 1)

    def test_get_learning_word_num(self):
        """Test retrieving the number of learning words"""
        user = self.user_controller.add_user('testuser', 'Test Nickname', 'password123')
        word = self.word_controller.add_word('testword', 'Test Definition')
        self.progress_controller.add_word_to_learning(user.user_id, word.word_id)
        learning_word_num = self.progress_controller.get_learning_word_num(user.user_id)
        self.assertEqual(learning_word_num, 1)



if __name__ == '__main__':
    unittest.main()




