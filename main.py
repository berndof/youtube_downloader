import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QComboBox
from pytube import YouTube
import datetime

class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.inputField = QLineEdit(self)
        layout.addWidget(self.inputField)

        self.checkFormatsBtn = QPushButton('Check Formats', self)
        self.checkFormatsBtn.clicked.connect(self.checkFormats)
        layout.addWidget(self.checkFormatsBtn)
        
        self.qualityOptions = QComboBox(self)
        layout.addWidget(self.qualityOptions)
        
        self.downloadBtn = QPushButton('Download', self)
        self.downloadBtn.clicked.connect(self.startDownload)
        layout.addWidget(self.downloadBtn)
        
        self.setLayout(layout)
        self.show()
        
    def startDownload(self):
        link = self.inputField.text()
        youtubeObject = YouTube(link)
        selectedOption = self.qualityOptions.currentText()
        formatData = selectedOption.split(",")[0].split(":")[1].strip()
        stream = youtubeObject.streams.filter(res=formatData).first()
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "." + stream.subtype
        stream.download(filename=filename)
        
    def checkFormats(self):
        link = self.inputField.text()
        youtubeObject = YouTube(link)
        self.fillQualityOptions(youtubeObject)
        
    def fillQualityOptions(self, youtubeObject):
        self.qualityOptions.clear()
        streams = youtubeObject.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        for i, stream in enumerate(streams):
            self.qualityOptions.addItem(f"Resolution: {stream.resolution}, Type: {stream.mime_type}, FPS: {stream.fps}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloaderApp()
    sys.exit(app.exec_())