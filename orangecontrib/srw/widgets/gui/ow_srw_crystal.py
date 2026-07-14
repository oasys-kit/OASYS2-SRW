import os

from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QMessageBox, QLabel, QSizePolicy
from AnyQt.QtGui import QPixmap
from PyQt6.QtWidgets import QGroupBox

import orangecanvas.resources as resources

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import MultiInput

from oasys2.widget import gui as oasysgui
from oasys2.widget.util import congruence
from oasys2.widget.util.exchange import DataExchangeObject

from syned.beamline.optical_elements.crystals.crystal import Crystal
from wofrysrw.beamline.optical_elements.crystals.srw_crystal import SRWCrystal

from orangecontrib.srw.widgets.gui.ow_srw_optical_element import OWSRWOpticalElement

class OWSRWCrystal(OWSRWOpticalElement):

    class Inputs:
        srw_data      = OWSRWOpticalElement.Inputs.srw_data
        trigger       = OWSRWOpticalElement.Inputs.trigger
        exchange_data = MultiInput("Exchange Data", DataExchangeObject, default=True, auto_summary=False)
        syned_data    = OWSRWOpticalElement.Inputs.syned_data

    which_energy         = Setting(0)
    energy               = Setting(8000.0)

    which_material      = Setting(0)
    material            = Setting('Si')
    miller_h            = Setting(1)
    miller_k            = Setting(1)
    miller_l            = Setting(1)

    d_spacing            = Setting(3.1355)
    asymmetry_angle      = Setting(0.0)
    thickness            = Setting(0.001)
    psi_0r               = Setting(-1.5127e-05)
    psi_0i               = Setting(3.4955e-07)
    psi_hr               = Setting(-7.9955e-06)
    psi_hi               = Setting(2.4361e-07)
    psi_hbr              = Setting(-7.0304e-06)
    psi_hbi              = Setting(2.1315e-07)
    diffraction_geometry = Setting(0)

    notes = Setting("")

    usage_path = os.path.join(resources.package_dirname("orangecontrib.srw.widgets.gui"), "misc", "crystal_usage.png")

    def __init__(self):
        super().__init__(azimuth_hor_vert=True)

        self.le_angle_radial.setEnabled(False)
        self.le_angle_radial_mrad.setEnabled(False)

    def draw_specific_box(self):

        tabs_crystal = oasysgui.tabWidget(self.tab_bas)

        tab_ene = oasysgui.createTabPage(tabs_crystal, "Crystal")
        tab_pro = oasysgui.createTabPage(tabs_crystal, "Polarizability")

        self.crystal_box_1 = oasysgui.widgetBox(tab_ene, "", addSpace=False, orientation="vertical")
        self.crystal_box_2 = oasysgui.widgetBox(tab_pro, "", addSpace=False, orientation="vertical")

        gui.comboBox(self.crystal_box_1, self, "which_energy", label="Photon Energy from",
                     items=["Wavefront", "User Defined"], labelWidth=250,
                     sendSelectedValue=False, orientation="horizontal",
                     callback=self.set_which_energy)

        self.energy_box_1 = oasysgui.widgetBox(self.crystal_box_1, "", addSpace=False, orientation="horizontal", height=25)
        self.energy_box_2 = oasysgui.widgetBox(self.crystal_box_1, "", addSpace=False, orientation="horizontal", height=25)

        oasysgui.lineEdit(self.energy_box_2, self, "energy", "Energy [eV]", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_which_energy()

        oasysgui.lineEdit(self.crystal_box_1, self, "asymmetry_angle", "Asymmetry Angle [rad]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.crystal_box_1, self, "thickness", "Crystal Thickness [m]", labelWidth=260, valueType=float, orientation="horizontal")

        gui.comboBox(self.crystal_box_1, self, "which_material", label="Material from",
                     items=["SRW", "User Defined"], labelWidth=250,
                     sendSelectedValue=False, orientation="horizontal",
                     callback=self.set_which_material)

        self.material_box_1 = oasysgui.widgetBox(self.crystal_box_1, "", addSpace=False, orientation="vertical", height=55)
        self.material_box_2 = oasysgui.widgetBox(self.crystal_box_1, "", addSpace=False, orientation="vertical", height=55)

        self.le_material = oasysgui.lineEdit(self.material_box_1, self, "material", "Material", labelWidth=260, valueType=str, orientation="horizontal")

        box_miller = oasysgui.widgetBox(self.material_box_1, "", orientation="horizontal")
        oasysgui.lineEdit(box_miller, self, "miller_h", tooltip="miller_h", label="Miller Indices [h k l]", addSpace=True, valueType=int, labelWidth=200, orientation="horizontal")
        oasysgui.lineEdit(box_miller, self, "miller_k", tooltip="miller_k", addSpace=True, valueType=int, orientation="horizontal")
        oasysgui.lineEdit(box_miller, self, "miller_l", tooltip="miller_l", addSpace=True, valueType=int, orientation="horizontal")

        self.le_d_spacing = oasysgui.lineEdit(self.crystal_box_1, self, "d_spacing", "d-spacing [Å]", labelWidth=260, valueType=float, orientation="horizontal")

        self.polarization_box = oasysgui.widgetBox(self.crystal_box_2, "Crystal Polarizability", addSpace=False, orientation="horizontal")

        polarization_box_l = oasysgui.widgetBox(self.polarization_box, "", addSpace=False, orientation="vertical", width=200)
        polarization_box_r = oasysgui.widgetBox(self.polarization_box, "", addSpace=False, orientation="vartical")

        gui.label(polarization_box_l, self, "               Real Part")
        oasysgui.lineEdit(polarization_box_l, self, "psi_0r" , "X0", labelWidth=50, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(polarization_box_l, self, "psi_hr" , "Xh \u03c3", labelWidth=50, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(polarization_box_l, self, "psi_hbr", "Xh \u03c0", labelWidth=50, valueType=float, orientation="horizontal")

        gui.label(polarization_box_r, self, "Imaginary Part")
        oasysgui.lineEdit(polarization_box_r, self, "psi_0i",  "", labelWidth=50, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(polarization_box_r, self, "psi_hi",  "", labelWidth=50, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(polarization_box_r, self, "psi_hbi", "", labelWidth=50, valueType=float, orientation="horizontal")

        self.notes_area = oasysgui.textArea(height=40, width=370)
        self.notes_area.setText(self.notes)

        self.crystal_box_2.layout().addWidget(self.notes_area)

        self.set_which_material()

        tab_usa = oasysgui.createTabPage(self.tabs_setting, "Use of the Widget")
        tab_usa.setStyleSheet("background-color: white;")

        usage_box = oasysgui.widgetBox(tab_usa, "", addSpace=True, orientation="horizontal")

        label = QLabel("")
        label.setAlignment(Qt.AlignCenter)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setPixmap(QPixmap(self.usage_path))

        usage_box.layout().addWidget(label)

    def set_which_energy(self):
        self.energy_box_1.setVisible(self.which_energy==0)
        self.energy_box_2.setVisible(self.which_energy==1)

    def set_which_material(self):
        self.material_box_1.setVisible(self.which_material==0)
        self.material_box_2.setVisible(self.which_material==1)

        self.le_d_spacing.setReadOnly(self.which_material==0)
        self.polarization_box.setEnabled(self.which_material==1)

        if self.which_material==0:
            self.notes = ""
            self.notes_area.clear()

    def set_additional_parameters(self, beamline_element, propagation_parameters, beamline):
        crystal = beamline.get_beamline_element_at(-1).get_optical_element()

        orientation_of_the_output_optical_axis_vector_x, \
        orientation_of_the_output_optical_axis_vector_y, \
        orientation_of_the_output_optical_axis_vector_z, \
        orientation_of_the_horizontal_base_vector_x    , \
        orientation_of_the_horizontal_base_vector_y     = crystal.get_output_orientation_vectors()

        self.oe_orientation_of_the_output_optical_axis_vector_x = round(orientation_of_the_output_optical_axis_vector_x, 8)
        self.oe_orientation_of_the_output_optical_axis_vector_y = round(orientation_of_the_output_optical_axis_vector_y, 8)
        self.oe_orientation_of_the_output_optical_axis_vector_z = round(orientation_of_the_output_optical_axis_vector_z, 8)
        self.oe_orientation_of_the_horizontal_base_vector_x     = round(orientation_of_the_horizontal_base_vector_x, 8)
        self.oe_orientation_of_the_horizontal_base_vector_y     = round(orientation_of_the_horizontal_base_vector_y, 8)

        super(OWSRWCrystal, self).set_additional_parameters(beamline_element, propagation_parameters, beamline)

    def get_optical_element(self):
        if self.which_energy == 0: energy = self.input_srw_data.get_srw_wavefront().get_photon_energy()
        else:                      energy = self.energy

        optical_element = SRWCrystal(orientation_of_reflection_plane = self.orientation_azimuthal,
                                     d_spacing                       = self.d_spacing,
                                     asymmetry_angle                 = self.asymmetry_angle,
                                     thickness                       = self.thickness,
                                     material                        = self.material if self.which_material==0 else None,
                                     miller_indices                  = [self.miller_h, self.miller_k, self.miller_l],
                                     psi_0r                          = self.psi_0r,
                                     psi_0i                          = self.psi_0i,
                                     psi_hr                          = self.psi_hr,
                                     psi_hi                          = self.psi_hi,
                                     psi_hbr                         = self.psi_hbr,
                                     psi_hbi                         = self.psi_hbi,
                                     energy                          = energy)
        self.angle_radial_mrad = optical_element.grazing_angle*1e3
        self.calculate_angle_radial_deg()

        if self.which_material == 0:
            self.d_spacing = round(optical_element.d_spacing, 5)
            self.psi_0r    = round(optical_element.psi_0r, 16)
            self.psi_0i    = round(optical_element.psi_0i, 16)
            self.psi_hr    = round(optical_element.psi_hr, 16)
            self.psi_hi    = round(optical_element.psi_hi, 16)
            self.psi_hbr   = round(optical_element.psi_hbr, 16)
            self.psi_hbi   = round(optical_element.psi_hbi, 16)

        return optical_element

    def receive_specific_syned_data(self, optical_element):
        if not optical_element is None:
            if isinstance(optical_element, Crystal):
                self.asymmetry_angle      = optical_element._asymmetry_angle,
                self.thickness            = optical_element._thickness,
                self.diffraction_geometry = optical_element._diffraction_geometry

                self.receive_shape_specific_syned_data(optical_element)
            else:
                raise Exception("Syned Data not correct: Optical Element is not a Crystal")
        else:
            raise Exception("Syned Data not correct: Empty Optical Element")

    def receive_shape_specific_syned_data(self, optical_element): raise NotImplementedError

    def check_data(self):
        super().check_data()

        congruence.checkStrictlyPositiveNumber(self.d_spacing, "d-spacing")

    @Inputs.exchange_data
    def set_exchange_data(self, index, exchange_data):
        self.acceptExchangeData(exchange_data)

    @Inputs.exchange_data.insert
    def insert_exchange_data(self, index, exchange_data):
        self.acceptExchangeData(exchange_data)

    @Inputs.exchange_data.remove
    def remove_exchange_data(self, index):
        pass

    def acceptExchangeData(self, exchangeData):
        if not exchangeData is None:
            try:
                if exchangeData.get_program_name() == "XRAYSERVER":
                    if exchangeData.get_widget_name() == "X0H":
                        self.notes = "Data from X-Ray Server: " + exchangeData.get_content("structure") + "(" + \
                                     str(exchangeData.get_content("h")) + "," + str(exchangeData.get_content("k")) + "," + str(exchangeData.get_content("l")) + ")" +  \
                                     " at " + str(round(exchangeData.get_content("energy")*1000, 4)) + " eV"
                        self.notes_area.setText(self.notes)

                        self.which_energy = 1
                        self.energy       = round(exchangeData.get_content("energy")*1000, 4)
                        self.set_which_energy()

                        self.which_material = 1
                        self.d_spacing = exchangeData.get_content("d_spacing")
                        self.psi_0r    = exchangeData.get_content("xr0")
                        self.psi_0i    = exchangeData.get_content("xi0")
                        self.psi_hr    = -1*exchangeData.get_content("xrh_s")
                        self.psi_hi    = exchangeData.get_content("xih_s")
                        self.psi_hbr   = -1*exchangeData.get_content("xrh_p")
                        self.psi_hbi   = exchangeData.get_content("xih_p")
                        self.set_which_material()

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e.args[0]), QMessageBox.Ok)

