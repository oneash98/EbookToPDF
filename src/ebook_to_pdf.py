from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIntValidator
from pynput.mouse import Listener
import mss
import pyautogui


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("EBook To PDF")
        self.setFixedSize(480, 320)

############################################위젯##############################################
        # 제목
        self.label_title = QLabel('Ebook To PDf')
        font_label_title = self.label_title.font()
        font_label_title.setPointSize(26)
        self.label_title.setFont(font_label_title)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        
        # 좌표
        self.coord1 = {'x': 0, 'y': 0}
        self.label_coord1Text = QLabel('좌측 상단 좌표   ==>')
        self.label_coord1 = QLabel('({x}, {y})'.format(x = self.coord1['x'], y = self.coord1['y']))
        self.btn_coord1 = QPushButton('좌표 위치 설정')

        self.coord2 = {'x': 0, 'y': 0}
        self.label_coord2Text = QLabel('우측 하단 좌표   ==>')
        self.label_coord2 = QLabel('({x}, {y})'.format(x = self.coord2['x'], y = self.coord2['y']))
        self.btn_coord2 = QPushButton('좌표 위치 설정')

        # 페이지 수
        self.label_numPage = QLabel('총 페이지 수')
        self.input_numPage = QLineEdit()
        self.input_numPage.setPlaceholderText('총 페이지 수 입력')
        self.input_numPage.setValidator(QIntValidator())

        # 파일명
        self.label_filename = QLabel('파일명')
        self.input_filename = QLineEdit()
        self.input_filename.setPlaceholderText('파일명 입력')


        # 캡처 속도 조절
        self.label_captureSpeed = QLabel('캡쳐 속도: 0.1초')
        self.slider_captureSpeed = QSlider(Qt.Orientation.Horizontal)

        # 캡처 시작 버튼
        self.btn_captureStart = QPushButton('캡처 시작')



############################################레이아웃##############################################

        # Layout
        layout = QVBoxLayout()

        # 제목 layout
        layout_title = QVBoxLayout()
        layout_title.setContentsMargins(0, 0, 0, 20)

        # 메인 layout
        layout_main = QVBoxLayout()

        # 메인 layout 내부 layouts
        layout_coord1 = QHBoxLayout()
        layout_coord2 = QHBoxLayout()
        layout_numPage = QHBoxLayout()
        layout_filename = QHBoxLayout()
        layout_captureSpeed = QHBoxLayout()


        # Layout 설정
        layout.addLayout(layout_title)
        layout_title.addWidget(self.label_title)

        layout.addLayout(layout_main)

        layout_main.addLayout(layout_coord1)
        layout_coord1.addWidget(self.label_coord1Text)
        layout_coord1.addWidget(self.label_coord1)
        layout_coord1.addWidget(self.btn_coord1)

        layout_main.addLayout(layout_coord2)
        layout_coord2.addWidget(self.label_coord2Text)
        layout_coord2.addWidget(self.label_coord2)
        layout_coord2.addWidget(self.btn_coord2)

        layout_main.addLayout(layout_numPage)
        layout_numPage.addWidget(self.label_numPage)
        layout_numPage.addWidget(self.input_numPage)

        layout_main.addLayout(layout_filename)
        layout_filename.addWidget(self.label_filename)
        layout_filename.addWidget(self.input_filename)

        layout_main.addLayout(layout_captureSpeed)
        layout_captureSpeed.addWidget(self.label_captureSpeed)
        layout_captureSpeed.addWidget(self.slider_captureSpeed)

        layout_main.addWidget(self.btn_captureStart)

        layout.addStretch()


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


############################################시그널##############################################
        self.btn_coord1.clicked.connect(self.set_coord1)
        self.btn_coord2.clicked.connect(self.set_coord2)
        self.btn_captureStart.clicked.connect(self.captureStart)



############################################함수##############################################
    def set_coord1(self):
        coord = get_coord()
        self.coord1 = coord
        self.label_coord1.setText('({x:.2f}, {y:.2f})'.format(x = self.coord1['x'], y = self.coord1['y']))
        
    def set_coord2(self):
        coord = get_coord()
        self.coord2 = coord
        self.label_coord2.setText('({x:.2f}, {y:.2f})'.format(x = self.coord2['x'], y = self.coord2['y']))

    def captureStart(self):
        top = self.coord1['y']
        left = self.coord1['x']
        width = self.coord2['x'] - self.coord1['x']
        height = self.coord2['y'] - self.coord1['y']

        pyautogui.click(left + width / 2, top + height / 2)

        for _ in range(2):
            with mss.mss() as sct:
                monitor = {"top": top, "left": left, "width": width, "height": height}
                output = "test.png"
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            pyautogui.press('down')


def get_coord():
    coord = {'x': None, 'y': None}
    def on_click(x, y, button, pressed):
        coord['x'] = x
        coord['y'] = y
        return False
    with Listener(on_click=on_click) as listener:
        listener.join()
    return coord

            


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()