import datetime
import mysql.connector

# 连接数据库
# 以下代码用于连接到MySQL数据库中的todo_list数据库
# 使用的主机是localhost，用户名为root，密码为123456
try:
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="todo_list"
    )
except mysql.connector.Error as err:
    print(f"Error: {err}")


class task:
    def __init__(self, task_num, task_text, countdown, importance):
        self.task_num = task_num
        self.task_text = task_text
        self.countdown = countdown
        self.importance = importance

# 本来想直接将排序后的结果保存在数据库中，但总是出现主键错误。
# 因为赋值时一定会出现两个值相等的情况，但主键是唯一的
# 结果：暂时无法从数据库层面解决，让一个变量等于从数据库中获得需要的结果，然后返回一个列表。
def priority():
    mycursor = mydatabase.cursor()
    mycursor.execute("SELECT task_text,countdown FROM todo_items ORDER BY countdown, importance DESC, task_num")
    results = mycursor.fetchall()
    mycursor.close()
    # 使用列表表达式！！！
    sort_res = [(i,row[0],row[1]) for i,row in enumerate(results,start=1)]
    return sort_res
# 输入并进行验证
def enter():
    # 得到数据库中最大的任务序号然后新建一个更大的来存储
    mycursor = mydatabase.cursor()
    mycursor.execute("SELECT MAX(task_num) FROM todo_items")
    max_num = mycursor.fetchone()[0]
    if max_num is None:
        task_num = 1
    else:
        task_num = max_num + 1
    mycursor.close()

    task_text = input("请输入待办事项>>>")
    # 验证截止日期是否正确
    while True:
        try:
            ddl_Ori = input("请输入截止日期>>>")
            ddl = datetime.datetime.strptime(ddl_Ori, '%Y-%m-%d')
            countdown = ddl - datetime.datetime.now() + datetime.timedelta(days = 1)
            if countdown.days < 0:
                print("日期输入错误！")
                continue
            break
        except ValueError:
            print("日期格式输入错误！例：2024-03-11")

    while True:
        try:
            importance = int(input("请输入重要程度（1 - 10,10为最重要）>>>"))
            importance = int(importance)
            if importance not in range(1, 11):
                raise ValueError
            else:
                break
        except ValueError:
            print("输入错误，请输入1 - 10以内的整数！")

    # 将用户输入添加到新任务里
    new_task = task(task_num, task_text, countdown.days, importance)
    return new_task


# 添加待办事项到数据库
def add_todo_item(item):
    mycursor = mydatabase.cursor()
    sql = "INSERT INTO todo_items (task_num, task_text, countdown, importance, due_date) VALUES (%s, %s, %s, %s, %s)"
    val = (item.task_num, item.task_text, item.countdown, item.importance,
           datetime.datetime.now() + datetime.timedelta(days=item.countdown))
    mycursor.execute(sql, val)
    mydatabase.commit()
    mycursor.close()


# 查看所有任务
def view(sort_list):
    print("-------TODO--List-------")
    if not sort_list:
        print("暂无待办事项。")
    else:
        for i in sort_list:
            print(f"  NO.{i[0]}  {i[1]}   剩余 {i[2]} 天")
    print("------------------------")

# 删除待办事项,因为重新进行了一次排序所以要倒回去
def delete_todo_item(sort_list,task_num):
    for tup in sort_list:
        if tup[0] == task_num:
            task_text = tup[1]
    mycursor = mydatabase.cursor()
    sql = "DELETE FROM todo_items WHERE task_text = %s"
    val = (task_text,)
    mycursor.execute(sql, val)
    mydatabase.commit()
    mycursor.close()


if __name__ == "__main__":
    while True:
        print("1. 添加待办事项")
        print("2. 查看待办事项")
        print("3. 删除待办事项")
        print("4. 退出")
        choice = input("请输入你的选择: ")

        if choice == '1':
            new_task = enter()
            add_todo_item(new_task)
            print("添加成功！")
        elif choice == '2':
            print("已按剩余天数和重要程度排序，请稍等...")
            view(priority())
        elif choice == '3':
            try:
                task_num = int(input("请输入要删除的任务序号: "))
                delete_todo_item(priority(),task_num)
                print("恭喜你，又完成了一个！")
            except ValueError:
                print("输入错误，请输入任务对应的序号！")
        elif choice == '4':
            print("期待下一次见面>_<!")
            break
        else:
            print("输入错误，请重新输入！")
