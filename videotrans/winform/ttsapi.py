from PySide6 import QtWidgets
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import Qt

from videotrans import tts
from videotrans.configure import config
from videotrans.util import tools


def open():
    class TestTTS(QThread):
        uito = Signal(str)

        def __init__(self, *, parent=None, text=None, language=None, rate="+0%", role=None):
            super().__init__(parent=parent)
            self.text = text
            self.language = language
            self.rate = rate
            self.role = role

        def run(self):
            try:
                tts.run(
                    queue_tts=[{"text": self.text, "role": self.role,
                                "filename": config.TEMP_HOME + "/testttsapi.mp3", "tts_type": tts.TTS_API}],
                    language=self.language,
                    play=True,
                    is_test=True
                )
                self.uito.emit("ok")
            except Exception as e:
                self.uito.emit(str(e))

    def feed(d):
        if d == "ok":
            QtWidgets.QMessageBox.information(winobj, "ok", "Test Ok")
        else:
            QtWidgets.QMessageBox.critical(winobj, config.transobj['anerror'], d)
        winobj.test.setText('测试api' if config.defaulelang == 'zh' else 'Test api')

    def test():
        url = winobj.api_url.text()
        extra = winobj.extra.text()
        role = winobj.voice_role.text().strip()

        config.params["ttsapi_url"] = url
        config.params["ttsapi_extra"] = extra
        config.params["ttsapi_voice_role"] = role

        task = TestTTS(parent=winobj,
                       text="你好啊我的朋友" if config.defaulelang == 'zh' else 'hello,my friend',
                       role=winobj.voice_role.text().strip().split(',')[0],
                       language="zh-cn" if config.defaulelang == 'zh' else 'en')
        winobj.test.setText('测试中请稍等...' if config.defaulelang == 'zh' else 'Testing...')
        task.uito.connect(feed)
        task.start()

    def save():
        url = winobj.api_url.text()
        extra = winobj.extra.text()
        role = winobj.voice_role.text().strip()

        config.params["ttsapi_url"] = url
        config.params["ttsapi_extra"] = extra
        config.params["ttsapi_voice_role"] = role
        config.getset_params(config.params)
        winobj.close()

    from videotrans.component import TtsapiForm
    winobj = config.child_forms.get('ttsapiw')
    if winobj is not None:
        winobj.show()
        winobj.raise_()
        winobj.activateWindow()
        return
    winobj = TtsapiForm()
    config.child_forms['ttsapiw'] = winobj
    if config.params["ttsapi_url"]:
        winobj.api_url.setText(config.params["ttsapi_url"])
    if config.params["ttsapi_voice_role"]:
        winobj.voice_role.setText(config.params["ttsapi_voice_role"])
    if config.params["ttsapi_extra"]:
        winobj.extra.setText(config.params["ttsapi_extra"])

    winobj.save.clicked.connect(save)
    winobj.test.clicked.connect(test)
    winobj.otherlink.clicked.connect(lambda: tools.open_url('https://github.com/kungful/openvoice-api'))
    winobj.otherlink.setCursor(Qt.PointingHandCursor)
    winobj.show()