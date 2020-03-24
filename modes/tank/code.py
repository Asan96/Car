from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5 import QtWidgets, QtGui
from ui.tankWindow import Ui_tankWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import keyword
import sys


class LexerPython(QsciLexerPython):
    def __init__(self, parent):
        QsciLexerPython.__init__(self, parent)
        self.setFont(QtGui.QFont('Consolas', 16))  # 设置默认字体
        self.setColor(QColor(0, 0, 0))  # 设置默认的字体颜色
        self.setPaper(QColor(255, 255, 255))  # 设置底色
        self.setColor(QColor("#B0171F"), QsciLexerPython.Keyword)

        self.setColor(QColor("#008000"), QsciLexerPython.Comment)  # 文档注释 /**开头的颜色
        self.setColor(QColor("#008000"), QsciLexerPython.Comment)  # 块注释 的颜色
        self.setColor(QColor("#007f7f"), QsciLexerPython.Number)  # 数字 的颜色
        self.setColor(QColor("#ff00ff"), QsciLexerPython.DoubleQuotedString)  # 双引号字符串的颜色
        self.setColor(QColor("#ff00ff"), QsciLexerPython.SingleQuotedString)  # 单引号字符的颜色
        self.setColor(QColor("#191970"), QsciLexerPython.Operator)
        self.setColor(QColor("#0000FF"), QsciLexerPython.UnclosedString)  # 未完成输入的字符串的颜色


class CodeWidget(QsciScintilla):

    def __init__(self):
        super().__init__()

        self.setEolMode(self.SC_EOL_LF)    # 以\n换行
        self.setWrapMode(self.WrapWord)    # 自动换行。self.WrapWord是父类QsciScintilla的
        self.setAutoCompletionSource(self.AcsAll)  # 自动补全。对于所有Ascii字符
        self.setAutoCompletionCaseSensitivity(False)  # 自动补全大小写敏感
        self.setAutoCompletionThreshold(1)  # 输入多少个字符才弹出补全提示
        self.setFolding(True)  # 代码可折叠
        self.setTabWidth(4)  # 设置缩进长度
        self.setIndentationGuides(True)  # 设置缩进参考线
        self.setAutoIndent(True)  # 设置自动缩进
        self.setCaretLineVisible(True)
        self.lexer = LexerPython(self)  # 语法高亮显示
        self.setLexer(self.lexer)
        self.setCaretLineVisible(True)  # 是否高亮显示光标所在行
        self.setCaretLineBackgroundColor(QtGui.QColor(250, 244, 217))  # 光标所在行的底色
        self.setIndentationsUseTabs(True)  # 设置使用Tabs缩进
        self.setFont(QtGui.QFont('Consolas', 20))  # 设置默认字体
        self.setMarginType(0, self.NumberMargin)    # 0~4。第0个左边栏显示行号
        self.setMarginLineNumbers(4, True)  # 我也不知道
        self.setMarginsBackgroundColor(QtGui.QColor(120, 220, 180))  # 边栏背景颜色
        self.setMarginWidth(0, 30)  # 边栏宽度
        self.setAutoIndent(True)  # 换行后自动缩进
        self.setUtf8(True)  # 支持中文字符
        self.__api = QsciAPIs(self.lexer)
        for kw in keyword.kwlist:
            self.__api.add(kw)
        self.__api.prepare()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mode_dilog = CodeWidget()
    mode_dilog.show()
    sys.exit(app.exec_())