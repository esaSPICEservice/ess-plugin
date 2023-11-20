import PyQt5.QtGui as QtGui
import PyQt5.QtCore  as QtCore
import PyQt5.QtWidgets as QtWidgets

import datetime

def epoch_seconds(isoc):
    epoch = datetime.datetime.fromisoformat(isoc)
    return epoch.timestamp()

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
    width: 3px;
 } 
"""

block_type_style_map = {
    'OBS': {
        'color': QtGui.QColor(255, 0, 0, 30)
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
    start: int
    end: int
    block_type: str

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
        self.origMax = self.maximum()
        self.oriMin = self.minimum()
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setStyleSheet(styleSheet)
        self.setMouseTracking(True)
        self.setPageStep(1)
        self.setMinimumSize(800, 40)
        self.installEventFilter(self)
        self.epoch = None
        self.max_epoch = None
        self.default_pen = QtGui.QPen(QtGui.QColor(200, 200, 200), 1, 
            QtCore.Qt.SolidLine)
        self.default_font = QtGui.QFont('Arial', 10, QtGui.QFont.Light)


    def add_block(self, block: TimelineBlock):
        self.epoch = min(self.epoch, block.start) if self.epoch else block.start
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

    def drawWidget(self, qp):

        qp.setFont(self.default_font)
        w = self.width()
        h = self.height()
        nb =  (self.maximum() - self.minimum())

        fStep = int(float(w) / nb)
        step = max(1,int(round(fStep)))

        qp.setPen(self.default_pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-50, h-50)
        
        metrics = qp.fontMetrics()
        fh = metrics.height()      
       
        if self.hover:
            val = self.style().sliderValueFromPosition(self.minimum(),self.maximum(),self.hoverPos.x(),self.width())
            if val != self.value() and self.epoch != None:
                    pos = self.style().sliderPositionFromValue(self.minimum(),self.maximum(),val,self.width())
                    fw = metrics.width("0")
                    if val > self.maximum()-(self.maximum()/2):
                        fw += metrics.width(str(val))
                        fw *= -1
                    pen2 = QtGui.QPen(QtGui.QColor(0,0,0,255), 2, QtCore.Qt.SolidLine)
                    qp.setPen(pen2)
                    qp.drawLine(pos,0, pos,h)
                    date_value = datetime.datetime.fromtimestamp(self.epoch + val).isoformat()
                    qp.drawText((pos)+fw, 0+fh, str(date_value)) 
        qp.setPen(self.default_pen)

        for block in self.blocks:
            self.drawBlock(qp, h, block)
        qp.setPen(self.default_pen)


    def drawBlock(self, qp, h, block):
        vertical_pad = 8
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
        if event.modifiers() == QtCore.Qt.AltModifier:
            self.PressPos = event.globalPos()
            self.MovePos = event.globalPos()
            self.press_slider_value = self.get_slider_value(self.PressPos.x())
        if event.button() == QtCore.Qt.LeftButton and event.modifiers() != QtCore.Qt.AltModifier:
            butts = QtCore.Qt.MouseButtons(QtCore.Qt.MidButton)
            nevent = QtGui.QMouseEvent(event.type(),QtCore.QPointF(event.pos()),QtCore.QPointF(event.globalPos()),QtCore.Qt.MidButton,butts,event.modifiers())
            value = self.get_slider_value(event.pos().x())
            date_value = datetime.datetime.fromtimestamp(self.epoch + value).isoformat()
            self.callback(date_value)
            super(Timeline, self).mousePressEvent(nevent)
        elif event.modifiers() != QtCore.Qt.AltModifier:
            super(Timeline, self).mousePressEvent(event)

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

    def mouseMoveEvent(self, event):
        if event.modifiers() == QtCore.Qt.AltModifier:
            if event.buttons() in [QtCore.Qt.MidButton,QtCore.Qt.LeftButton] :
                globalPos = event.globalPos()
                slider_value = self.get_slider_value(globalPos.x())
                diff_x = self.press_slider_value - slider_value
                newMin = self.minimum() + diff_x
                newMax = self.maximum() + diff_x
                self.setRange(newMin,newMax)
                self.repaint()
        else:
            return super(Timeline, self).mouseMoveEvent( event)
