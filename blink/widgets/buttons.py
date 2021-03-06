# Copyright (c) 2010 AG Projects. See LICENSE for details.
#

__all__ = ['ToolButton', 'ConferenceButton', 'StreamButton', 'SegmentButton', 'SingleSegment', 'LeftSegment', 'MiddleSegment', 'RightSegment', 'RecordButton', 'SwitchViewButton']

from PyQt4.QtCore import QTimer, pyqtSignal
from PyQt4.QtGui  import QAction, QIcon, QPushButton, QStyle, QStyleOptionToolButton, QStylePainter, QToolButton


class ToolButton(QToolButton):
    """A custom QToolButton that doesn't show a menu indicator arrow"""
    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionToolButton()
        self.initStyleOption(option)
        option.features &= ~QStyleOptionToolButton.HasMenu
        painter.drawComplexControl(QStyle.CC_ToolButton, option)


class ConferenceButton(ToolButton):
    makeConference  = pyqtSignal()
    breakConference = pyqtSignal()

    def __init__(self, parent=None):
        super(ConferenceButton, self).__init__(parent)
        self.make_conference_action = QAction(u'Conference all single sessions', self, triggered=self.makeConference.emit)
        self.break_conference_action = QAction(u'Break selected conference', self, triggered=self.breakConference.emit)
        self.toggled.connect(self._SH_Toggled)
        self.addAction(self.make_conference_action)

    def _SH_Toggled(self, checked):
        if checked:
            self.removeAction(self.make_conference_action)
            self.addAction(self.break_conference_action)
        else:
            self.removeAction(self.break_conference_action)
            self.addAction(self.make_conference_action)


class StreamButton(QToolButton):
    hidden = pyqtSignal()
    shown  = pyqtSignal()

    def __init__(self, parent=None):
        super(StreamButton, self).__init__(parent)
        self.default_icon = QIcon()
        self.alternate_icon = QIcon()
        self.clicked.connect(self._clicked)

    def _clicked(self):
        super(StreamButton, self).setIcon(self.default_icon)

    def _get_accepted(self):
        return not self.isChecked()

    def _set_accepted(self, accepted):
        super(StreamButton, self).setIcon(self.alternate_icon)
        self.setChecked(not accepted)

    accepted = property(_get_accepted, _set_accepted)
    del _get_accepted, _set_accepted

    def _get_active(self):
        return self.isEnabled()

    def _set_active(self, active):
        self.setEnabled(bool(active))

    active = property(_get_active, _set_active)
    del _get_active, _set_active

    @property
    def in_use(self):
        return self.isVisibleTo(self.parent())

    def setVisible(self, visible):
        super(StreamButton, self).setVisible(visible)
        signal = self.shown if visible else self.hidden
        signal.emit()

    def setIcon(self, icon):
        self.default_icon = icon
        self.alternate_icon = QIcon(icon)
        normal_sizes = icon.availableSizes(QIcon.Normal, QIcon.On)
        selected_sizes = icon.availableSizes(QIcon.Selected, QIcon.On)
        selected_additional_sizes = [size for size in selected_sizes if size not in normal_sizes]
        for size in normal_sizes + selected_additional_sizes:
            pixmap = icon.pixmap(size, QIcon.Selected, QIcon.On)
            self.alternate_icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        disabled_sizes = icon.availableSizes(QIcon.Disabled, QIcon.On)
        selected_additional_sizes = [size for size in selected_sizes if size not in disabled_sizes]
        for size in disabled_sizes + selected_additional_sizes:
            pixmap = icon.pixmap(size, QIcon.Selected, QIcon.On)
            self.alternate_icon.addPixmap(pixmap, QIcon.Disabled, QIcon.On)
        super(StreamButton, self).setIcon(icon)


class SegmentTypeMeta(type):
    def __repr__(cls):
        return cls.__name__

class SegmentType(object):
    __metaclass__ = SegmentTypeMeta
    style_sheet = ''

class SingleSegment(SegmentType):
    style_sheet = """
                     QToolButton {
                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fafafa, stop:1 #bababa);
                         border-color: #545454;
                         border-radius: 4px;
                         border-width: 1px;
                         border-style: solid;
                     }
                     
                     QToolButton:pressed {
                         background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, stop:0 #dddddd, stop:1 #777777);
                         border-style: inset;
                     }
                  """

class LeftSegment(SegmentType):
    style_sheet = """
                     QToolButton {
                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fafafa, stop:1 #bababa);
                         border-color: #545454;
                         border-top-left-radius: 4px;
                         border-bottom-left-radius: 4px;
                         border-width: 1px;
                         border-style: solid;
                     }
                     
                     QToolButton:pressed {
                         background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, stop:0 #dddddd, stop:1 #777777);
                         border-style: inset;
                     }
                  """

class MiddleSegment(SegmentType):
    style_sheet = """
                     QToolButton {
                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fafafa, stop:1 #bababa);
                         border-color: #545454;
                         border-width: 1px;
                         border-left-width: 0px;
                         border-style: solid;
                     }
                     
                     QToolButton:pressed {
                         background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, stop:0 #dddddd, stop:1 #777777);
                         border-style: inset;
                     }
                  """

class RightSegment(SegmentType):
    style_sheet = """
                     QToolButton {
                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fafafa, stop:1 #bababa);
                         border-color: #545454;
                         border-top-right-radius: 4px;
                         border-bottom-right-radius: 4px;
                         border-width: 1px;
                         border-left-width: 0px;
                         border-style: solid;
                     }
                     
                     QToolButton:pressed {
                         background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, stop:0 #dddddd, stop:1 #777777);
                         border-style: inset;
                     }
                  """


class SegmentButton(QToolButton):
    SingleSegment = SingleSegment
    LeftSegment   = LeftSegment
    MiddleSegment = MiddleSegment
    RightSegment  = RightSegment

    hidden = pyqtSignal()
    shown  = pyqtSignal()

    def __init__(self, parent=None):
        super(SegmentButton, self).__init__(parent)
        self.type = SingleSegment

    def _get_type(self):
        return self.__dict__['type']

    def _set_type(self, value):
        if not issubclass(value, SegmentType):
            raise ValueError("Invalid type: %r" % value)
        self.__dict__['type'] = value
        self.setStyleSheet(value.style_sheet)

    type = property(_get_type, _set_type)
    del _get_type, _set_type

    def setVisible(self, visible):
        super(SegmentButton, self).setVisible(visible)
        signal = self.shown if visible else self.hidden
        signal.emit()


class RecordButton(SegmentButton):
    def __init__(self, parent=None):
        super(RecordButton, self).__init__(parent)
        self.timer_id = None
        self.toggled.connect(self._SH_Toggled)
        self.animation_icons = []
        self.animation_icon_index = 0

    def _get_animation_icon_index(self):
        return self.__dict__['animation_icon_index']

    def _set_animation_icon_index(self, index):
        self.__dict__['animation_icon_index'] = index
        self.update()

    animation_icon_index = property(_get_animation_icon_index, _set_animation_icon_index)
    del _get_animation_icon_index, _set_animation_icon_index

    def setIcon(self, icon):
        super(RecordButton, self).setIcon(icon)
        on_icon = QIcon(icon)
        off_icon = QIcon(icon)
        for size in off_icon.availableSizes(QIcon.Normal, QIcon.On):
            pixmap = off_icon.pixmap(size, QIcon.Normal, QIcon.Off)
            off_icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.animation_icons = [on_icon, off_icon]

    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionToolButton()
        self.initStyleOption(option)
        option.icon = self.animation_icons[self.animation_icon_index]
        painter.drawComplexControl(QStyle.CC_ToolButton, option)

    def timerEvent(self, event):
        self.animation_icon_index = (self.animation_icon_index+1) % len(self.animation_icons)

    def _SH_Toggled(self, checked):
        if checked:
            self.timer_id = self.startTimer(1000)
            self.animation_icon_index = 0
        else:
            self.killTimer(self.timer_id)
            self.timer_id = None


class SwitchViewButton(QPushButton):
    ContactView = 0
    SessionView = 1

    viewChanged = pyqtSignal(int)

    button_text = {ContactView: u'Switch to Calls', SessionView: u'Switch to Contacts'}
    button_dnd_text = {ContactView: u'Drag here to add to a conference', SessionView: u'Drag here to go back to contacts'}

    dnd_style_sheet1 = """
                          QPushButton {
                              background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #d3ffdc);
                              border-color: #237523;
                              border-radius: 4px;
                              border-width: 2px;
                              border-style: solid;
                          }
                       """

    dnd_style_sheet2 = """
                          QPushButton {
                              background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #c2ffce);
                              border-color: #dc3169;
                              border-radius: 4px;
                              border-width: 2px;
                              border-style: solid;
                          }
                       """

    def __init__(self, parent=None):
        super(SwitchViewButton, self).__init__(parent)
        self.setAcceptDrops(True)
        self.__dict__['dnd_active'] = False
        self.view = self.ContactView
        self.original_height = 20 # used to restore button size after DND
        self.dnd_timer = QTimer(self)
        self.dnd_timer.setInterval(100)
        self.dnd_timer.timeout.connect(self._update_dnd)
        self.dnd_timer.phase = 0
        self.clicked.connect(self._change_view)

    def _get_view(self):
        return self.__dict__['view']

    def _set_view(self, value):
        if self.__dict__.get('view', None) == value:
            return
        if value not in (self.ContactView, self.SessionView):
            raise ValueError("invalid view value: %r" % value)
        self.__dict__['view'] = value
        if self.dnd_active:
            text = self.button_dnd_text[value]
        else:
            text = self.button_text[value]
        self.setText(text)
        self.viewChanged.emit(value)

    view = property(_get_view, _set_view)
    del _get_view, _set_view

    def _get_dnd_active(self):
        return self.__dict__['dnd_active']

    def _set_dnd_active(self, value):
        if self.__dict__.get('dnd_active', None) == value:
            return
        self.__dict__['dnd_active'] = value
        if value is True:
            self.dnd_timer.phase = 0
            self.original_height = self.height()
            self.setStyleSheet(self.dnd_style_sheet1)
            self.setText(self.button_dnd_text[self.view])
            self.setFixedHeight(40)
        else:
            self.setStyleSheet('')
            self.setText(self.button_text[self.view])
            self.setFixedHeight(self.original_height)

    dnd_active = property(_get_dnd_active, _set_dnd_active)
    del _get_dnd_active, _set_dnd_active

    def _change_view(self):
        self.view = self.ContactView if self.view is self.SessionView else self.SessionView

    def _update_dnd(self):
        self.dnd_timer.phase += 1
        if self.dnd_timer.phase == 11:
            self.dnd_timer.stop()
            self.click()
            self.setStyleSheet(self.dnd_style_sheet1)
        else:
            style_sheet = (self.dnd_style_sheet1, self.dnd_style_sheet2)[self.dnd_timer.phase % 2]
            self.setStyleSheet(style_sheet)

    def dragEnterEvent(self, event):
        if not self.dnd_active:
            event.ignore()
        elif event.mimeData().formats() == ['application/x-blink-contact-list']:
            event.accept()
            self._update_dnd()
            self.dnd_timer.start()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        if self.dnd_active:
           self.dnd_timer.stop()
           self.dnd_timer.phase = 0
           self.setStyleSheet(self.dnd_style_sheet1)
        super(SwitchViewButton, self).dragLeaveEvent(event)

    def dropEvent(self, event):
        if self.dnd_active:
           self.dnd_timer.stop()
           self.dnd_timer.phase = 0
           self.setStyleSheet(self.dnd_style_sheet1)
        event.ignore()


