from flask import Flask, render_template, send_file, send_from_directory

import recite
from recite import *
from flask import jsonify, request
import requests
app = Flask(__name__)
@app.route('/')
def index():
    return send_from_directory('static', 'download.html', mimetype='text/html')


# 创建用户控制器实例bud
user_controller = UserController()
word_controller = WordController()
progress_controller = recite.ProgressController()


@app.route('/users', methods=['POST'])
def add_user():
    """添加新用户"""
    data = request.json
    username = data.get('username')
    nickname = data.get('nickname')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
    try:
        new_user = user_controller.add_user(username, nickname, password)
        return jsonify(
            {"message": "用户创建成功", "user": {"id": new_user.user_id, "username": new_user.username}}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "服务器内部错误", "details": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
    try:
        user = user_controller.login(username, password)
        if user is None:
            return jsonify({"message": "用户或密码错误"}), 204
        else:
            return jsonify({"message": "登入成功", "user_id": user.user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/get_id_by_username', methods=['POST'])
def get_id_by_username():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"message": "请检查填入信息是否为空"}), 204
    try:
        user = user_controller.get_user_by_username(username)
        if user is not None:
            return jsonify({"user_id": user.user_id}), 201
        else:
            return jsonify({"message": "用户名错误"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    user_id = data.get('user_id')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if not user_id or not old_password or not new_password:
        return jsonify({"message": "请检查填入信息是否为空"}), 204
    try:
        user = user_controller.get_user_by_id(user_id)
        if user != None:
            if user.verify_password(old_password):
                user.update_password(old_password, new_password)
                return jsonify({"message": "更改成功"}), 201
            else:
                return jsonify(({"message": "密码错误"})), 204
        else:
            return jsonify({"message": "用户名错误"}), 204
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/del_user', methods=['POST'])
def del_user():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')
    if not user_id or not password:
        return jsonify({"message": "请检查填入信息是否为空"}), 204
    try:
        user = user_controller.get_user_by_id(user_id)
        if user != None:
            if user.verify_password(password):
                user_controller.del_user(user_id)
                return jsonify({"message": "用户已删除"}), 201
            else:
                return jsonify({"message": "密码错误"}), 204
        else:
            return jsonify({"message": "用户不存在"}), 204
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/change_learning_book', methods=['POST'])
def change_learning_book():
    data = request.json
    user_id = data.get('user_id')
    learning_book = data.get('learning_book')
    try:
        user_controller.change_learning_book(user_id, learning_book)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/change_group_word', methods=['POST'])
def change_group_word():
    data = request.json
    user_id = data.get('user_id')
    group_word = data.get('group_word')
    try:
        user_controller.change_group_word(user_id, group_word)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/chang_def_learned', methods=['POST'])
def chang_def_learned():
    data = request.json
    user_id = data.get('user_id')
    def_learned = data.get('def_learned')
    try:
        user_controller.chang_def_learned(user_id, def_learned)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_all_user', methods=['GET'])
def get_all_user():
    """获取所有用户"""
    users = user_controller.get_all_user()
    return jsonify({"users": [str(user) for user in users]}), 201


@app.route('/get_def_learned', methods=['POST'])
def get_def_learned():
    data = request.json
    user_id = data.get('user_id')
    try:
        user = user_controller.get_user_by_id(user_id)
        if user is None:
            return jsonify({"message": "用户不存在"}), 204
        user_id = user.user_id
        def_learned = user_controller.get_def_learned(user_id)
        if def_learned is not None:
            return jsonify({"def_learned": def_learned}), 201
        else:
            return jsonify({"message": "用户不存在"}), 204
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_learning_book', methods=['POST'])
def get_learning_book():
    data = request.json
    user_id = data.get('user_id')
    try:
        learning_book = user_controller.get_learning_book_from_user_id(user_id)
        if learning_book is not None:
            return jsonify({"learning_book": learning_book}), 201
        else:
            return jsonify({"message": "正在学习单词书为空"}), 204
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_user_message_by_id', methods=['POST'])
def get_user_message_by_id():
    data = request.json
    user_id = data.get('user_id')
    print(user_id)
    try:
        user = user_controller.get_user_by_id(user_id)
        if user is None:
            return jsonify({"message": "用户不存在"}), 204
        else:
            username = user.username
            nickname = user.nickname
            user_group_word = user.group_word
            user_def_learned = user.def_learned
            learn_num = progress_controller.get_learning_word_num(user_id)
            if learn_num is None:
                learn_num = 0
            learned_num = progress_controller.get_have_learned_word_num(user_id)
            if learned_num is None:
                learned_num = 0
            word_num = word_controller.get_all_word_number()
            if word_num is None:
                word_num = 0

            return jsonify(
                {"username": username, "nickname": nickname, "user_group_word": user_group_word,
                 "user_def_learned": user_def_learned,
                 "learn_num": learn_num, "learned_num": learned_num, "word_num": word_num}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/update_message', methods=['POST'])
def update_message():
    data = request.json
    user_id = data.get('user_id')
    nickname = data.get('nickname')
    group_word = data.get('group_word')
    def_learned = int(data.get('def_learned'))
    try:
        user = user_controller.get_user_by_id(user_id)
        if user is None:
            return jsonify({"message": "用户不存在"}), 204
        else:
            if not user_controller.update_user(user, nickname, group_word, def_learned):
                return jsonify({"message": "用户名已存在"}), 204
            return jsonify({"message": "信息更新成功"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


#word_book 部分API
@app.route('/get_word_by_id', methods=['POST'])
def get_word_by_id():
    data = request.json
    word_id = data.get('word_id')
    try:
        w = word_controller.get_word_by_id(word_id)
        if w == None:
            return jsonify({"message": "无此单词"}), 204
        else:
            return w.__str__(), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_learn_word', methods=['POST'])
def get_learn_word():
    data = request.json
    user_id = data.get('user_id')
    try:
        learn_word = progress_controller.get_learn_word(user_id)
        if learn_word == None:
            return jsonify({"message": "无此单词"}), 204
        else:
            return learn_word.__str__(), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_option', methods=['POST', 'GET'])
def get_option():
    # data = request.json
    try:
        option = word_controller.get_random_word().translations[0]['translation']
        option_en = word_controller.get_random_word().word
        if option is None:
            return jsonify({"message": "无此单词"}), 204
        else:
            res = jsonify({"option": option, "option_en": option_en})
            # print(res.data)
            return res, 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/update_word', methods=['POST'])
def update_word():
    data = request.json
    user_id = data.get('user_id')
    word_id = data.get('word_id')
    proficiency = data.get('proficiency')
    try:
        progress_controller.update_word(user_id, word_id, proficiency)
        return jsonify({"message": "单词更新成功"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/add_learned_word_to_have_learned', methods=['POST'])
def add_learned_word_to_have_learned():
    data = request.json
    user_id = data.get('user_id')
    word_id = data.get('word_id')
    try:
        progress_controller.add_word_to_have_learned(user_id, word_id)
        return jsonify({"message": "单词添加成功"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/back_have_learned_to_learning', methods=['POST'])
def back_have_learned_to_learning():
    data = request.json
    user_id = data.get('user_id')
    word_id = data.get('word_id')
    try:
        progress_controller.back_have_learned_to_learning(user_id, word_id)
        return jsonify({"message": "单词重新学习"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_word_progress', methods=['POST'])
def get_word_progress():
    data = request.json
    user_id = data.get('user_id')
    word_id = data.get('word_id')
    try:
        progress = progress_controller.get_learning_word_proficiency(user_id, word_id)
        if progress is None:
            return jsonify({"message": "无此单词"}), 204
        else:
            # print(progress)
            return jsonify({"proficiency": progress}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_reviews_word', methods=['POST'])
def get_reviews_word():
    data = request.json
    user_id = data.get('user_id')
    try:
        reviews_word = progress_controller.get_learned_word(user_id)
        if reviews_word is None:
            return jsonify({"message": "无此单词"}), 204
        else:
            print("reviews_word : " + reviews_word.__str__())
            return reviews_word.__str__(), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_learned_word_num', methods=['POST'])
def get_learned_word_num():
    data = request.json
    user_id = data.get('user_id')
    try:
        learned_word_num = progress_controller.get_learned_word_num(user_id)
        if learned_word_num == None:
            return jsonify({"message": "无此单词"}), 204
        else:
            return jsonify({"learned_word_num": learned_word_num}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/search_word', methods=['POST'])
def search_word():
    data = request.json
    word = data.get('word')
    try:
        word_info = recite.get_word_info(word)
        if word_info is None:
            return jsonify({"message": "无此单词"}), 204
        else:
            return jsonify({"word_info": word_info}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/get_openid', methods=['GET', 'POST'])
def get_openid():
    code = request.json.get('code')

    res = requests.get(
        url="https://api.weixin.qq.com/sns/jscode2session?appid=wxa09b33824d02b45f&secret"
            "=c431bd3ae77f9223b17efcd27f28c25f&grant_type=authorization_code&js_code=" + code
    )
    print(res.json())
    return jsonify(res.json()), res.status_code


@app.route('/check_update')
def check_update():
    # 指定本地 JSON 文件的路径
    ver = request.args.get("ver")
    apk_json = './resources/apk.json'
    wgt_json = './resources/wgt.json'
    # package_type: 1, // 0是整包升级（apk或者appstore或者安卓应用市场） 1是wgt升级

    with open(apk_json, 'r', encoding='utf-8') as file:
        apk_data = json.load(file)
    with open(wgt_json, 'r', encoding='utf-8') as file:
        wgt_data = json.load(file)

    if int(ver) >= apk_data['edition_number']:
        data = wgt_data
    else:
        data = apk_data

    # 返回 JSON 数据
    return jsonify(data)


@app.route('/apk')
def apk():
    ver = request.args.get("ver")
    if ver is None:
        return send_file('./resources/release' + '.apk', as_attachment=True)
    return send_file('./resources/release' + ver + '.apk', as_attachment=True)


@app.route('/wgt')
def wgt():
    ver = request.args.get("ver")
    return send_file('./resources/release' + ver + '.wgt', as_attachment=True)



if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

