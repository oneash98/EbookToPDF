from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIntValidator
from pynput.mouse import Listener
import mss
import pyautogui
import time
from datetime import datetime
import os
from pathlib import Path
import natsort
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("EBook To PDF")
        self.setFixedSize(480, 400)

############################################위젯##############################################
        # 제목
        self.label_title = QLabel('Ebook To PDF')
        font_label_title = self.label_title.font()
        font_label_title.setPointSize(26)
        self.label_title.setFont(font_label_title)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        
        # 좌표
        self.coord1 = {'x': 0.00, 'y': 0.00}
        self.label_coord1Text = QLabel('좌측 상단 좌표   ==>')
        self.label_coord1 = QLabel('({x:.2f}, {y:.2f})'.format(x = self.coord1['x'], y = self.coord1['y']))
        self.btn_coord1 = QPushButton('좌표 위치 설정')

        self.coord2 = {'x': 0.00, 'y': 0.00}
        self.label_coord2Text = QLabel('우측 하단 좌표   ==>')
        self.label_coord2 = QLabel('({x:.2f}, {y:.2f})'.format(x = self.coord2['x'], y = self.coord2['y']))
        self.btn_coord2 = QPushButton('좌표 위치 설정')

        # 페이지 수
        self.label_numPage = QLabel('총 페이지 수')
        self.input_numPage = QLineEdit()
        self.input_numPage.setPlaceholderText('페이지 수')
        self.input_numPage.setValidator(QIntValidator())

        # 넘기는 방향
        self.flipDir = 'right'
        self.label_flipDir = QLabel('넘기는 방향')
        self.combo_flipDir = QComboBox()
        self.combo_flipDir.addItems(['오른쪽', '아래'])

        # 분할 여부
        self.label_divide = QLabel('페이지 분할')
        self.combo_divide = QComboBox()
        self.combo_divide.addItems(['한 번에', '절반씩'])

        # 캡처 속도 조절
        self.captureSpeed = 0
        self.label_captureSpeedText = QLabel('캡쳐 속도:')
        self.label_captureSpeed = QLabel('{}'.format(self.captureSpeed))
        self.slider_captureSpeed = QSlider(Qt.Orientation.Horizontal)
        self.slider_captureSpeed.setRange(0, 100)
        self.slider_captureSpeed.setSingleStep(1)

        # 파일명
        self.label_filename = QLabel('파일명')
        self.input_filename = QLineEdit()
        self.input_filename.setPlaceholderText('파일명 입력')

        # 저장 경로
        self.label_saveDir = QLabel('저장 경로')
        self.saveDir = QLineEdit('~')
        self.saveDir.setReadOnly(True)
        self.btn_saveDir = QPushButton('저장 위치 선택')

        # 캡처 시작 버튼
        self.btn_captureStart = QPushButton('캡처 시작')

        # 초기화 버튼
        self.btn_init = QPushButton('설정 초기화')



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
        layout_page = QHBoxLayout()
        layout_captureSpeed = QHBoxLayout()
        layout_filename = QHBoxLayout()
        layout_savedir = QHBoxLayout()


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

        layout_main.addLayout(layout_page)
        layout_page.addWidget(self.label_numPage)
        layout_page.addWidget(self.input_numPage)
        layout_page.addWidget(self.label_flipDir)
        layout_page.addWidget(self.combo_flipDir)
        layout_page.addWidget(self.label_divide)
        layout_page.addWidget(self.combo_divide)

        layout_main.addLayout(layout_captureSpeed)
        layout_captureSpeed.addWidget(self.label_captureSpeedText)
        layout_captureSpeed.addWidget(self.label_captureSpeed)
        layout_captureSpeed.addWidget(self.slider_captureSpeed)

        layout_main.addLayout(layout_filename)
        layout_filename.addWidget(self.label_filename)
        layout_filename.addWidget(self.input_filename)

        layout_main.addLayout(layout_savedir)
        layout_savedir.addWidget(self.label_saveDir)
        layout_savedir.addWidget(self.saveDir)
        layout_savedir.addWidget(self.btn_saveDir)

        layout_main.addWidget(self.btn_captureStart)
        layout_main.addWidget(self.btn_init)

        layout.addStretch()


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


############################################시그널##############################################
        self.btn_coord1.clicked.connect(lambda: self.set_coord1())
        self.btn_coord2.clicked.connect(lambda: self.set_coord2())
        self.combo_flipDir.currentIndexChanged.connect(self.set_flipDir)
        self.slider_captureSpeed.valueChanged.connect(self.set_captureSpeed)
        self.btn_saveDir.clicked.connect(self.findDir)
        self.btn_captureStart.clicked.connect(self.captureStart)
        self.btn_init.clicked.connect(self.init_settings)



############################################함수##############################################
    def set_coord1(self, x = None, y = None):
        coord = {'x': x, 'y': y}
        if x == None and y == None:
            coord = get_coord()
        self.coord1 = coord
        self.label_coord1.setText('({x:.2f}, {y:.2f})'.format(x = coord['x'], y = coord['y']))
        
    def set_coord2(self, x = None, y = None):
        coord = {'x': x, 'y': y}
        if x == None and y == None:
            coord = get_coord()
        self.coord2 = coord
        self.label_coord2.setText('({x:.2f}, {y:.2f})'.format(x = coord['x'], y = coord['y']))

    def set_flipDir(self):
        text = self.combo_flipDir.currentText()
        if text == '오른쪽':
            self.flipDir = 'right'
        elif text == '아래':
            self.flipDir = 'down'
        
    def set_captureSpeed(self):
        self.captureSpeed = self.slider_captureSpeed.value() / 10
        self.label_captureSpeed.setText('{}'.format(self.captureSpeed))

    def findDir(self):
        dir = QFileDialog.getExistingDirectory()
        self.saveDir.setText(dir)
        

    def captureStart(self):
        # 페이지 수 미입력 시 경고   
        try:
            num_pages = int(self.input_numPage.text())
        except ValueError as e:
            return self.warning_numPage()

        top = self.coord1['y']
        left = self.coord1['x']
        width = self.coord2['x'] - self.coord1['x']
        height = self.coord2['y'] - self.coord1['y']

        # 캡처 위치 다시 클릭해주기
        pyautogui.click(left + width / 2, top + height / 2)

        # 경로 생성
        dir = Path(self.saveDir.text()) / 'capture_{}'.format(datetime.now().strftime("%y%m%d%H%M%S"))
        dir.mkdir()
        images_dir = dir / 'images'
        images_dir.mkdir()

        # 화면 캡처
        for i in range(num_pages):
            if self.combo_divide.currentText() == '한 번에':
                capture(top, left, width, height, images_dir)

            elif self.combo_divide.currentText() == '절반씩':
                capture(top, left, width / 2, height, images_dir) # 왼쪽 절반
                capture(top, left + width / 2, width / 2, height, images_dir) # 오른쪽 절반

            # 페이지 넘기기
            if i != num_pages - 1:
                pyautogui.press(self.flipDir)
                if self.captureSpeed != 0:
                    time.sleep(self.captureSpeed)

        # pdf 변환
        file_list = os.listdir(images_dir)
        file_list = natsort.natsorted(file_list)
        if '.DS_Store' in file_list:
            del file_list[0]

        images_list = []
        image_path = images_dir / file_list[0]
        image_buf = Image.open(image_path)
        cvt_rgb_0 = image_buf.convert('RGB')

        for file in file_list:
            image_path = images_dir / file
            image_buf = Image.open(image_path)
            cvt_rgb = image_buf.convert('RGB')
            images_list.append(cvt_rgb)
        del images_list[0]

        file_name = self.input_filename.text()
        if file_name == '':
            file_name = '무제'

        cvt_rgb_0.save(dir / (file_name + '.pdf'), save_all = True, append_images = images_list)

        # 변환 완료 창
        QMessageBox.information(self, '변환 완료', 'PDF 변환이 완료되었습니다.')



    # 페이지 수 입력 경고
    def warning_numPage(self):
        QMessageBox.warning(self, '페이지 수 확인 안됨', '총 페이지 수를 입력해주세요.')
    
    # 설정 초기화
    def init_settings(self):
        self.set_coord1(0, 0)
        self.set_coord2(0, 0)
        self.input_numPage.clear()
        self.combo_flipDir.setCurrentIndex(0)
        self.combo_divide.setCurrentIndex(0)
        self.slider_captureSpeed.setValue(0)
        self.input_filename.clear()
        self.saveDir.setText('~')


def get_coord():
    coord = {'x': None, 'y': None}
    def on_click(x, y, button, pressed):
        coord['x'] = x
        coord['y'] = y
        return False
    with Listener(on_click=on_click) as listener:
        listener.join()
    return coord

def make_filename(dir):
    # 파일명 현재 시간으로 설정.
    current_time = datetime.now().strftime("%y%m%d%H%M%S%f")
    file_ext = '.png'
    output = dir / (current_time + file_ext)

    # (혹시라도) 이미 파일명 존재할 경우
    uniq = 1
    while os.path.exists(output):
        output =  dir / (current_time + '({})'.format(uniq) + file_ext)
        uniq += 1

    return output

def capture(top, left, width, height, images_dir):
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        output = make_filename(images_dir)
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()