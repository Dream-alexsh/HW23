import os

from flask import Flask, request, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(iter_query, cmd, val):
    res = map(lambda x: x.strip(), iter_query)
    if cmd == 'filter':
        res = filter(lambda x: val in x, res)
    if cmd == 'map':
        val = int(val)
        res = map(lambda x: x.split()[val], res)
    if cmd == 'unique':
        res = list(set(res))
    if cmd == 'sort':
        val = bool(val)
        res = sorted(res, reverse=val)
    if cmd == 'limit':
        val = int(val)
        res = list(res)[:val]
    return res


@app.route("/perform_query")
def perform_query():
    try:
        cmd1 = request.args["cmd1"]
        val1 = request.args["val1"]
        cmd2 = request.args["cmd2"]
        val2 = request.args["val2"]
        file_name = request.args["file_name"]
    except:
        return 'Bad query', 400

    path_file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_file):
        return abort(400)

    with open(path_file) as f:
        res = build_query(f, cmd1, val1)
        res = build_query(res, cmd2, val2)
        res = '\n'.join(res)

    return app.response_class(res, content_type="text/plain")


if __name__ == '__main__':
    app.run()


    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
