import time

from Utils.singleton import Singleton
from user import *
from word_book import *

word_controller = WordController()
user_controller = UserController()


class LearnWord:
    def __init__(self, word_id: int, proficiency: int, learn_time: List[float]):
        self.word_id = word_id
        self.proficiency = proficiency
        self.learn_time = learn_time

    def __str__(self):
        return f"{self.word_id} {self.proficiency} {self.learn_time}"


class Progress:
    def __init__(self, user_id: str, learned_word: List[LearnWord], learning_word: List[LearnWord],
                 have_learned: List[LearnWord]):
        self.user_id = user_id
        self.learned_word = learned_word
        self.learning_word = learning_word
        self.have_learned = have_learned

    def __str__(self):
        return f"{self.user_id} {self.learned_word} {self.learning_word} {self.have_learned}"


@Singleton
class ProgressController:
    def __init__(self):
        self.progresses: List[Progress] = []
        if os.path.exists(r"./static/progress.pickle"):
            if os.path.getsize(r"./static/progress.pickle") == 0:
                print("文件为空")
            else:
                with open(r"./static/progress.pickle", "rb") as file:
                    self.progresses = pickle.load(file)
                    print('progress ok')
        else:
            print("文件不存在")

    def get_learning_word_num(self, user_id: str):
        for progress in self.progresses:
            if progress.user_id == user_id:
                return len(progress.learning_word)
        return 0

    def get_learning_word(self, user_id: str):
        for progress in self.progresses:
            if progress.user_id == user_id:
                return progress.learning_word

    def get_learning_word_proficiency(self, user_id: str, learn_word_id: int):
        for progress in self.progresses:
            if progress.user_id == user_id:
                for word in progress.learning_word:
                    if word.word_id == learn_word_id:
                        return word.proficiency
        return 0

    def update_word(self, user_id: str, learn_word_id: int, proficiency: int):
        user = user_controller.get_user_by_id(user_id)
        user_def_learned = user.def_learned
        print(user_id)
        for progress in self.progresses:
            print('ok')
            if progress.user_id == user_id:
                print('find user')
                for word in progress.learning_word:
                    if word.word_id == learn_word_id:
                        print('find word')
                        print(proficiency)
                        word.proficiency = proficiency
                        if word.proficiency >= user_def_learned:
                            self.add_word_from_learn_to_learned(user_id, learn_word_id)
                            print('添加到已学单词')
                        with open(r"./static/progress.pickle",
                                  "wb") as file:
                            pickle.dump(self.progresses, file)
                        return True
        self.add_word_to_learning(user_id, learn_word_id)
        print('添加新单词')
        with open(r"./static/progress.pickle",
                  "wb") as file:
            pickle.dump(self.progresses, file)
        return True

    def get_learned_word_num(self, user_id: str):
        print(user_id)
        for progress in self.progresses:
            print(progress.user_id)
            if progress.user_id == user_id:
                print(progress.learned_word)
                print(len(progress.learned_word))
                return len(progress.learned_word)
        return 0

    def get_learned_word(self, user_id: str):
        user = user_controller.get_user_by_id(user_id)
        learned_word_list = []
        if self.get_learned_word_num(user_id) != 0:
            for progress in self.progresses:
                if progress.user_id == user_id:
                    for word in progress.learned_word:
                        learned_word = word_controller.get_word_by_id(word.word_id)
                        learned_word_list.append(learned_word)
        word = random.choice(learned_word_list)
        # print(word)
        return word

    def get_have_learned_word_num(self, user_id: str):
        for progress in self.progresses:
            if progress.user_id == user_id:
                return len(progress.have_learned)
        return 0

    def if_in_learning_word(self, user_id: str, learn_word_id: int):
        for progress in self.progresses:
            if progress.user_id == user_id:
                for word in progress.learning_word:
                    if word.word_id == learn_word_id:
                        return True
        return False

    def if_in_learned_word(self, user_id: str, learn_word_id: int):
        for progress in self.progresses:
            if progress.user_id == user_id:
                for word in progress.learned_word:
                    if word.word_id == learn_word_id:
                        return True
        return False

    def if_in_all(self, user_id: str, learn_word_id: int):
        for progress in self.progresses:
            if progress.user_id == user_id:
                for word in progress.have_learned:
                    if word.word_id == learn_word_id:
                        return True
                for word in progress.learned_word:
                    if word.word_id == learn_word_id:
                        return True
                for word in progress.learning_word:
                    if word.word_id == learn_word_id:
                        return True
        return False

    def get_learn_word_list(self, user_id: str):
        learn_word_list = []
        user = user_controller.get_user_by_id(user_id)
        if self.get_learning_word_num(user_id) != 0:
            print(self.get_learning_word(user_id))
            print(self.get_learning_word_num(user_id))
            for word in self.get_learning_word(user_id):
                learn_word = word_controller.get_word_by_id(word.word_id)
                learn_word_list.append(learn_word)

        return learn_word_list

    def get_learn_word(self, user_id: str):
        user = user_controller.get_user_by_id(user_id)
        learn_word_list = self.get_learn_word_list(user_id)
        if len(learn_word_list) == 0:
            word = word_controller.get_random_word()
            return word
        elif len(learn_word_list) <= 5:
            while len(learn_word_list) <= 5:
                word = word_controller.get_random_word()
                if not self.if_in_all(user_id, word.word_id):
                    learn_word_list.append(word)
            word = random.choice(learn_word_list)
            return word
        else:
            word = random.choice(learn_word_list)
            return word

    def add_word_to_learning(self, user_id: str, learn_word_id: int):
        for progress in self.progresses:
            if progress.user_id == user_id:
                current_time = time.time()
                timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime(current_time))
                new_learn_word = LearnWord(learn_word_id, 1, [current_time])
                progress.learning_word.append(new_learn_word)
                with open(r"./static/progress.pickle",
                          "wb") as file:
                    pickle.dump(self.progresses, file)
                print(f"Word added on: {timestamp}")  # 打印时间戳
                return True
        # 如果没有找到对应的用户，则创建新的 Progress 对象
        current_time = time.time()
        new_progress = Progress(user_id, [], [LearnWord(learn_word_id, 1, [current_time])], [])
        self.progresses.append(new_progress)
        with open(r"./static/progress.pickle",
                  "wb") as file:
            pickle.dump(self.progresses, file)

    def add_word_from_learn_to_learned(self, user_id: str, learn_word_id: int):
        user = user_controller.get_user_by_id(user_id)
        user_def_learned = user.def_learned
        for progress in self.progresses:
            if progress.user_id == user_id:
                for word in progress.learning_word:
                    if word.word_id == learn_word_id:
                        if word.proficiency >= user_def_learned:
                            print('添加到已学单词222')
                            progress.learned_word.append(word)
                            progress.learning_word.remove(word)
                            with open(r"./static/progress.pickle",
                                      "wb") as file:
                                pickle.dump(self.progresses, file)
                            return True
        return False

    def add_word_to_have_learned(self, user_id: str, learn_word_id: int):
        for progress in self.progresses:
            if progress.user_id == user_id:
                for word in progress.learned_word:
                    if word.word_id == learn_word_id:
                        progress.have_learned.append(word)
                        progress.learned_word.remove(word)
                        with open(r"./static/progress.pickle",
                                  "wb") as file:
                            pickle.dump(self.progresses, file)
                        return True
        return False

    def back_have_learned_to_learning(self, user_id: str, learn_word_id: int):
        for progress in self.progresses:
            if progress.user_id == user_id:
                for word in progress.have_learned:
                    if word.word_id == learn_word_id:
                        progress.learning_word.append(word)
                        progress.have_learned.remove(word)
                        with open(r"./static/progress.pickle",
                                  "wb") as file:
                            pickle.dump(self.progresses, file)
                        return True
        return False
