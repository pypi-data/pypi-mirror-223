import cmd
from 语言 import 分析器, 分词器

class 交互(cmd.Cmd):
    def __init__(self, ):
        super().__init__()
        self.prompt = '请：'

    def default(self, 行):
        print(分析器.按语法分词(分词器.分词(行)))


def 开始交互():
    交互().cmdloop("向您问好")

开始交互()