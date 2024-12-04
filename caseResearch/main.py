import datetime

class task:
    def __init__(self,num,task_text,countdown,importance):
        self.num = num
        self.task_text = task_text
        self.countdown = countdown
        self.importance = importance
    # 重载打印时对象返回的形式
    def __str__(self):
        return f"  NO.{self.num}  {self.task_text}   剩余 {self.countdown} 天"


def priority(list):
    sort = sorted(list,key=lambda l:(l.countdown,l.num,-l.importance))
    for i,l in enumerate(sort,start=1):
        l.num = i
    return sort

# 输入并进行验证
def enter(task_index):
    task_text = input("请输入待办事项>>>")
    # 验证截止日期是否正确
    while True:
        try:
            ddl_Ori = input("请输入截止日期>>>")
            ddl = datetime.datetime.strptime(ddl_Ori, '%Y-%m-%d')
            # 不会计算今天，所以加上一天
            countdown = ddl - datetime.datetime.now() + datetime.timedelta(days = 1)
            if countdown.days < 0:
                print("日期输入错误！")
                continue
            break
        except ValueError:
            print("日期格式输入错误！例：2024-03-11")

    importance =int(input("请输入重要程度（1-10,10为最重要）>>>"))
    if importance not in range(1,11):
        raise ValueError(print("输入错误，只能输入在1-10以内的数字！"))

    # 初始化输入的新任务
    new_task = task(task_index,task_text,countdown.days,importance)
    return new_task

# 查看所有任务
def view(list):
    print("-------TODO--List-------")
    if not list:
        print("暂无待办事项。")
    else:
        for i in list:
            print(i)
    print("------------------------")

if __name__ == "__main__":
    list = []
    task_index = 0

    while True:
        print("1. 添加待办事项")
        print("2. 查看待办事项")
        print("3. 删除待办事项")
        print("4. 退出")
        choice = input("请输入你的选择: ")

        if choice == '1':
            new_task = enter(task_index)
            list.append(new_task)
            print("添加成功！")
        elif choice == '2':
            sort = priority(list)
            view(sort)
            task_index = task_index + 1
        elif choice == '3':
            try:
                num = int(input("请输入要删除的任务序号: "))
                del list[num+1]
                print("恭喜你，又完成了一个！")
            except ValueError:
                print("输入错误，请输入任务对应的序号！")
        elif choice == '4':
            print("期待下一次见面>_<!")
            break
        else:
            print("输入错误，请重新输入！")
