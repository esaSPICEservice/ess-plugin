import typing
from PyQt5 import QtGui
import PyQt5.QtGui as QtGui
import PyQt5.QtCore  as QtCore
import PyQt5.QtWidgets as QtWidgets

import datetime
import math
from utils.time import epoch_seconds, from_epoch_seconds, nearest_previous_oclock_epoch



styleSheet = """

QSlider,QSlider:disabled,QSlider:focus     {  
                          background: qcolor(0,0,0,0);   }

QSlider:item:hover    {   background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #eaa553);
                          color: #000000;              }

QWidget:item:selected {   background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);      }

 QSlider::groove:horizontal {
 
    border: 1px solid #999999;
    background: qcolor(0,0,0,0);
 }
QSlider::handle:horizontal {
    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255,160,47, 141), stop:0.497175 rgba(255,160,47, 200), stop:0.497326 rgba(255,160,47, 200), stop:1 rgba(255,160,47, 147));
    width: 0px;
 } 
"""

block_type_style_map = {
    'OBS': {
        'color': QtGui.QColor(0, 0, 255, 35)
    },
    'SLEW': {
        'color': QtGui.QColor(128, 128, 0, 30)
    }
}

default_style = {
    'color': QtGui.QColor(0, 0, 255, 30)
}

def get_style(block_type):
    return block_type_style_map.get(block_type, default_style)

class TimelineBlock:

    def __init__(self, start_str, end_str, block_type):
        if start_str > end_str:
            raise RuntimeError('Block not valid: start after end')
        self.start = epoch_seconds(start_str)
        self.end = epoch_seconds(end_str)
        self.block_type = block_type

    def relative_start(self, epoch):
        return int(self.start - epoch)

    def relative_end(self, epoch):
        return int(self.end - epoch)


class Timeline(QtWidgets.QSlider):

    def __init__(self, parent, callback, *args):
        super(Timeline, self).__init__(parent=parent,*args)
        self.parent = parent
        self.callback = callback
        self.blocks = []
        self.hover = False
        self.hoverPos = None
        self.PressPos = None
        self.MovePos = None
        self.time = False
        self.timePos = None
        self.timeStr = None
        self.origMax = self.maximum()
        self.oriMin = self.minimum()
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setStyleSheet(styleSheet)
        self.setMouseTracking(True)
        self.setPageStep(1)
        self.setMinimumSize(800, 50)
        self.installEventFilter(self)
        self.epoch = None
        self.max_epoch = None
        self.default_pen = QtGui.QPen(QtGui.QColor(200, 200, 200), 1, 
            QtCore.Qt.SolidLine)
        self.default_font = QtGui.QFont('Arial', 10, QtGui.QFont.Light)


    def add_block(self, block: TimelineBlock):
        nearest = nearest_previous_oclock_epoch(from_epoch_seconds(block.start))
        self.epoch = min(self.epoch, nearest) if self.epoch else nearest
        self.max_epoch = max(self.max_epoch, block.end) if self.max_epoch else block.end
        self.blocks.append(block)  
        self.setRange(0, int(self.max_epoch - self.epoch))

    def setRange(self,min,max,setOrig=True):
        if setOrig:
            self.origMax = max
            self.oriMin = min
        return super(Timeline, self).setRange( min, max)

    def setCached(self,cached):
        self.cachedFrames = cached

    def setMissing(self,missing):
        self.missingFrames = missing

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()        
        super(Timeline, self).paintEvent(event)

    def get_slider_value(self, x_pos):
        return self.style().sliderValueFromPosition(self.minimum(),self.maximum(), x_pos ,self.width())

    def get_major_ticks(self, timeline_seconds):

        scale = 3600
        if timeline_seconds < 3600:
            scale = 900
        if timeline_seconds <= 900:
            scale = 300

        major_ticks = []
        mark = math.ceil(self.minimum() / scale) * scale
        while mark < self.maximum():
            major_ticks.append(mark)
            mark += scale
        return major_ticks

    def every_nth(self, lst, nth):
        return lst[nth - 1::nth]

    def drawWidget(self, qp):

        if not self.epoch:
            return

        qp.setFont(self.default_font)
        w = self.width()
        h = self.height()
        nb =  (self.maximum() - self.minimum())

        qp.setPen(self.default_pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-50, h-50)
        
        metrics = qp.fontMetrics()
        fh = metrics.height()
        fw = metrics.width("0")
        ticks = self.get_major_ticks(nb)
        ticks = self.every_nth(ticks, len(ticks) // 30) if len(ticks) > 30 else ticks
        show = range(0,len(ticks),len(ticks) // 5) if len(ticks) > 5 else range(0,len(ticks))
        for index, tick in enumerate(ticks):
            pos = self.style().sliderPositionFromValue(self.minimum(),self.maximum(),tick,self.width())
            pen2 = QtGui.QPen(QtGui.QColor(128,128,128,255), 2, QtCore.Qt.SolidLine)
            qp.setPen(pen2)
            tick_height = h - 3
            if index in show:
                date_value = datetime.datetime.fromtimestamp(self.epoch + tick, tz=datetime.timezone.utc).isoformat()[:19]
                qp.drawText((pos)+fw, h - fh, str(date_value))
                tick_height = h - fh
            qp.drawLine(pos,tick_height, pos, h)

       
        if self.hover:
            val = self.style().sliderValueFromPosition(self.minimum(),self.maximum(),self.hoverPos.x(),self.width())
            if val != self.value() and self.epoch != None:
                pos = self.style().sliderPositionFromValue(self.minimum(),self.maximum(),val,self.width())
                if val > self.maximum()-(self.maximum()/2):
                    fw += metrics.width(str(val))
                    fw *= -1
                pen2 = QtGui.QPen(QtGui.QColor(0,0,0,255), 2, QtCore.Qt.SolidLine)
                qp.setPen(pen2)
                qp.drawLine(pos,0, pos,h)
                date_value = datetime.datetime.fromtimestamp(self.epoch + val, tz=datetime.timezone.utc).isoformat()
                qp.drawText((pos)+fw, 0+fh, str(date_value[:19]))

        if self.time:
            if self.epoch != None:
                pos = self.style().sliderPositionFromValue(self.minimum(),self.maximum(),self.timePos,self.width())
                pen2 = QtGui.QPen(QtGui.QColor(255,0,0,255), 2, QtCore.Qt.SolidLine)
                qp.setPen(pen2)
                qp.drawLine(pos,0, pos,h)
                qp.drawText((pos)+fw, 0+fh, self.timeStr) 

        qp.setPen(self.default_pen)

        for block in self.blocks:
            self.drawBlock(qp, h, block)

        qp.setPen(self.default_pen)


    def drawBlock(self, qp, h, block):
        vertical_pad = 14
        style = get_style(block.block_type)
        qp.setPen(style.get('color'))
        qp.setBrush(style.get('color'))
        rel_start = block.relative_start(self.epoch)
        rel_end = block.relative_end(self.epoch)

        pos = self.style().sliderPositionFromValue(self.minimum(),self.maximum(), rel_start, self.width())
        pos_end = self.style().sliderPositionFromValue(self.minimum(),self.maximum(), rel_end, self.width())
        if pos != pos_end :
            if pos < pos_end:
                qp.drawRect(pos, 0 + vertical_pad , (pos_end - pos), h - 2 * vertical_pad)
            else:
                qp.drawRect(pos, 0 + vertical_pad , (self.maximum() - pos), h - 2 * vertical_pad)



    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            if event.modifiers() != QtCore.Qt.AltModifier:
                value = self.get_slider_value(event.pos().x())
                date_value = datetime.datetime.fromtimestamp(self.epoch + value, tz=datetime.timezone.utc).isoformat()
                self.callback(date_value)
            else:
                self.press_slider_value = self.get_slider_value(event.pos().x())

    def mouseReleaseEvent(self, event):
        if event.modifiers() == QtCore.Qt.AltModifier:
            slider_value = self.get_slider_value(event.pos().x())
            diff_x = self.press_slider_value - slider_value
            newMin = self.minimum() + diff_x
            newMax = self.maximum() + diff_x
            self.setRange(newMin,newMax)
            self.repaint()

    def wheelEvent(self,event):
        delta_ratio = (self.maximum() - self.minimum()) / 500
        delta = int(event.pixelDelta().y() * delta_ratio)
        newMin = self.minimum() + delta
        newMax = self.maximum() - delta
        if newMin >= newMax:
            return
        self.setRange(newMin,newMax)
        self.repaint()

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.MouseMove:
            self.hover = True
            self.hoverPos = event.pos()
            self.repaint()
        elif event.type() == QtCore.QEvent.Leave:
            self.hover = False
            self.repaint()
        return super(Timeline, self).eventFilter( widget, event)


    def set_time(self, time_str):
        if self.epoch:
            self.time = True
            self.timeStr = time_str[:19]
            self.timePos = int(epoch_seconds(time_str) - self.epoch)
            self.repaint()

    def move_timeline(self, pos):
        delta_ratio = (self.maximum() - self.minimum()) / 10
        delta = int(pos * delta_ratio)
        newMin = self.minimum() + delta
        newMax = self.maximum() + delta
        if newMin >= newMax:
            return
        self.setRange(newMin,newMax)
        self.repaint()

    def zoom_timeline(self, pos):
        delta_ratio = (self.maximum() - self.minimum()) / 10
        delta = int(pos * delta_ratio)
        newMin = self.minimum() - delta
        newMax = self.maximum() + delta
        if newMin >= newMax:
            return
        self.setRange(newMin,newMax)
        self.repaint()

class TimelineControl(QtWidgets.QWidget):

    def __init__(self, parent, callback):
        super(TimelineControl, self).__init__(parent)
        self.parent = parent
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.timeline = Timeline(self, callback)
        self.layout().addWidget(self.create_buttonbar(self.timeline))
        self.layout().addWidget(self.timeline)
        

    def create_buttonbar(self, timeline):
        button_bar = QtWidgets.QWidget()
        button_bar.setLayout(QtWidgets.QHBoxLayout())
        button_bar.layout().setContentsMargins(0, 0, 0, 0)

        button = QtWidgets.QPushButton()
        button.setText('<')        
        button.clicked.connect(lambda: timeline.move_timeline(-1))
        button_bar.layout().addWidget(button)

        button = QtWidgets.QPushButton()
        button.setText('>')        
        button.clicked.connect(lambda: timeline.move_timeline(+1))
        button_bar.layout().addWidget(button)

        button = QtWidgets.QPushButton()
        button.setText('-')        
        button.clicked.connect(lambda: timeline.zoom_timeline(+2.5))
        button_bar.layout().addWidget(button)

        button = QtWidgets.QPushButton()
        button.setText('+')        
        button.clicked.connect(lambda: timeline.zoom_timeline(-2.5))
        button_bar.layout().addWidget(button)
        return button_bar

    def add_block(self, block):
        self.timeline.add_block(block)

    def set_time(self, time_str):
        self.timeline.set_time(time_str)

    def move_timeline(self, pos):
        self.timeline.move_timeline(pos)