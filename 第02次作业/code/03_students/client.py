import json
import urllib.parse
import urllib.request
import urllib.error

URL = "http://127.0.0.1:5000/"


def call_server(opt="", fields=None):
    url = URL
    if opt:
        url += "?" + urllib.parse.urlencode({"opt": opt})

    data = None
    if fields is not None:
        data = urllib.parse.urlencode(fields).encode("utf-8")

    req = urllib.request.Request(url, data=data)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return json.loads(error.read().decode("utf-8"))


def show_students():
    result = call_server()
    if result["msg"] != "OK":
        print("查询失败：", result["msg"])
        return

    rows = result["data"]
    print("\n学号\t姓名\t性别\t年龄")
    for row in rows:
        print(
            f'{row["No"]}\t{row["Name"]}\t'
            f'{row["Sex"]}\t{row["Age"]}'
        )
    print("记录总数：", len(rows))


def main():
    print("102402116 蔡靖熹")
    print("实践案例：Web学生管理程序")

    while True:
        print("\n0. 初始化学生表")
        print("1. 查看学生列表")
        print("2. 增加学生记录")
        print("3. 删除学生记录")
        print("4. 退出程序")

        choice = input("请选择（0—4）：").strip()

        if choice == "0":
            result = call_server("init")
            print("初始化结果：", result["msg"])

        elif choice == "1":
            show_students()

        elif choice == "2":
            fields = {
                "No": input("学号：").strip(),
                "Name": input("姓名：").strip(),
                "Sex": input("性别（男/女）：").strip(),
                "Age": input("年龄：").strip(),
            }
            result = call_server("insert", fields)
            print("增加结果：", result["msg"])

        elif choice == "3":
            no = input("要删除的学号：").strip()
            result = call_server("delete", {"No": no})
            print("删除结果：", result["msg"])

        elif choice == "4":
            print("程序已退出")
            break

        else:
            print("请输入0—4")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as error:
        print("连接服务器失败：", error.reason)
