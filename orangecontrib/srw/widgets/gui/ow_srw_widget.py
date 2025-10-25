from oasys2.widget.widget import OWWidget

from orangewidget import gui
from orangewidget.settings import Setting

from AnyQt.QtWidgets import QApplication
from AnyQt.QtCore import QRect

from oasys2.widget.gui import ConfirmDialog
import oasys2.widget.gui as oasysgui

class SRWWidget(OWWidget, openclass=True):

    want_main_area=1

    is_automatic_run = Setting(True)

    error_id = 0
    warning_id = 0
    info_id = 0

    MAX_WIDTH = 1320
    MAX_HEIGHT = 720

    CONTROL_AREA_WIDTH = 405
    TABS_AREA_HEIGHT   = 615

    srw_live_propagation_mode = "Unknown"

    def __init__(self, show_general_option_box=True, show_automatic_box=True):
        super().__init__()

        geom = QApplication.primaryScreen().geometry()
        self.setGeometry(QRect(round(geom.width()*0.05),
                               round(geom.height()*0.05),
                               round(min(geom.width()*0.98, self.MAX_WIDTH)),
                               round(min(geom.height()*0.95, self.MAX_HEIGHT))))

        self.setMaximumHeight(self.geometry().height())
        self.setMaximumWidth(self.geometry().width())

        self.controlArea.setFixedWidth(self.CONTROL_AREA_WIDTH)

        self.general_options_box = oasysgui.widgetBox(self.controlArea, "General Options", addSpace=False, orientation="horizontal", width=self.CONTROL_AREA_WIDTH-5)
        self.general_options_box.setVisible(show_general_option_box)

        if show_automatic_box :
            gui.checkBox(self.general_options_box, self, 'is_automatic_run', 'Automatic Execution')

    def callResetSettings(self):
        if ConfirmDialog.confirmed(parent=self, message="Confirm Reset of the Fields?"):
            try:
                self._reset_settings()
            except:
                pass
