import numpy

from orangewidget.settings import Setting
from oasys2.widget import gui as oasysgui
from oasys2.widget.util import congruence
from oasys2.canvas.util.canvas_util import add_widget_parameters_to_module

from syned.beamline.shape import Sphere, Paraboloid, ParabolicCylinder

from wofrysrw.beamline.optical_elements.mirrors.srw_paraboloid_mirror import SRWParaboloidMirror

from orangecontrib.srw.widgets.gui.ow_srw_mirror import OWSRWMirror

class OWSRWParaboloidMirror(OWSRWMirror):

    name = "Paraboloid Mirror"
    description = "SRW: Paraboloid Mirror"
    icon = "icons/paraboloid_mirror.png"
    priority = 5

    focal_length = Setting(1.0)
    at_infinity = Setting(0)
    is_cylinder = Setting(1)
    sagittal_radius  = Setting(1.e23)

    def __init__(self):
        super().__init__()

    def get_mirror_instance(self):
        return SRWParaboloidMirror(focal_length=self.focal_length,
                                   at_infinity=self.at_infinity,
                                   sagittal_radius=1.e23 if self.is_cylinder==1 else self.sagittal_radius)

    def draw_specific_box(self):
        super().draw_specific_box()

        oasysgui.lineEdit(self.mirror_box, self, "focal_length", "Focal Length [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.comboBox(self.mirror_box, self, "at_infinity", label="At Infinity",
                          items=["Source", "Image"], labelWidth=300,
                           sendSelectedValue=False, orientation="horizontal")
        oasysgui.comboBox(self.mirror_box, self, "is_cylinder", label="Cylindrical",
                          items=["No", "Yes"], labelWidth=300,
                          sendSelectedValue=False, orientation="horizontal", callback=self.set_cylindrical)

        self._radius_box_1 =  oasysgui.widgetBox(self.mirror_box, "", addSpace=False, orientation="horizontal", height=25)
        self._radius_box_2 =  oasysgui.widgetBox(self.mirror_box, "", addSpace=False, orientation="horizontal", height=25)

        oasysgui.lineEdit(self._radius_box_1, self, "sagittal_radius", "Sagittal Radius [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_cylindrical()

    def set_cylindrical(self):
        self._radius_box_1.setVisible(self.is_cylinder==0)
        self._radius_box_2.setVisible(self.is_cylinder==1)

    def receive_shape_specific_syned_data(self, optical_element):
        if not isinstance(optical_element.get_surface_shape(), Paraboloid):
            raise Exception("Syned Data not correct: Mirror Surface Shape is not a Paraboloid/Parabolic Cylinder")

        self.focal_length = 0.5*optical_element.get_surface_shape().get_parabola_parameter()
        self.at_infinity  = optical_element.get_surface_shape().get_at_infinity()
        self.is_cylinder = 1 if isinstance(optical_element.get_surface_shape(), ParabolicCylinder) else 0
        self.sagittal_radius = 1.e23 if self.is_cylinder == 1 else self.focal_length

        self.set_cylindrical()

    def check_data(self):
        super().check_data()

        congruence.checkStrictlyPositiveNumber(self.focal_length,  "Focal Length")
        if self.is_cylinder == 0: congruence.checkStrictlyPositiveNumber(self.sagittal_radius, "Sagittal Radius")

add_widget_parameters_to_module(__name__)