"""
This is a class that offers a set of functions to work with meteorological data
in ecsv or grib(2) format.

Created by Pere Munar-Adrover
email: pere.munaradrover@gmail.com
Further developed and mainted by
Mykhailo Dalchenko (mykhailo.dalchenko@unige.ch) and
Georgios Voutsinas (georgios.voutsinas@unige.ch)
"""

import os
import logging
import json

import astropy.units as u
from astropy.table import Table, vstack
import numpy as np
from scipy.interpolate import interp1d

from molecularprofiles.utils.grib_utils import get_grib_file_data, extend_grib_data
from molecularprofiles.utils.constants import (
    DENSITY_SCALE_HEIGHT,
    N0_AIR,
    STD_GRAVITATIONAL_ACCELERATION,
    STD_AIR_DENSITY,
)

from molecularprofiles.utils.humidity import (
    compressibility,
    density_moist_air,
    molar_fraction_water_vapor,
    partial_pressure_water_vapor,
)
from molecularprofiles.utils.rayleigh import Rayleigh

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
log_config_file = f"{ROOTDIR}/utils/mdps_log.conf"
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MolecularProfile:
    """
    This class provides a series of functions to analyze the quality of the data for both
    CTA-North and CTA-South.

    Methods within this class:

    get_data:                   it retrieves the data from the input file. If the input file
                                is a grib file and there is no file in the working directory
                                with the same name but with .txt extension the program extracts
                                the data from the grib file through the grib_utils program. If
                                there is such a txt file, it reads it directly
    write_corsika:              prints the data into a txt file which format is compliant with the input card
                                for the CORSIKA air shower simulation software
    create_mdp:                 creates an altitude profile of the molecular number density
    rayleigh_extinction:        creates a file, in format to be directly fed to simtel simulation, with the
                                extinction per altitude bin for wavelengths from 200 to 1000 nm
    """

    def __init__(self, data_file):
        """
        Constructor

        :param data_file: txt file containing the data (string)
        """

        self.data_file = data_file

    # =============================================================================================================
    # Private functions
    # =============================================================================================================
    def _interpolate_cubic(self, x_param, y_param, new_x_param):
        func = interp1d(x_param, y_param, kind="cubic", fill_value="extrapolate")
        return func(new_x_param)

    def _interpolate_param_to_h(self, param, height):
        logger.error("Not implemented")
        raise NotImplementedError
        # interpolated_param = []
        # group_mjd = self.dataframe.groupby("MJD")

        # logger.info("Computing the extrapolation of the values of density:")
        # logger.info("(This is to make it easier to compare ECMWF and GDAS, or any other")
        # logger.info("weather model)")

        # for mjd in self.dataframe.MJD.unique():
        #     h_at_mjd = group_mjd.get_group(mjd)["h"].tolist()
        #     param_at_mjd = group_mjd.get_group(mjd)[param].tolist()
        #     func = interp1d(h_at_mjd, param_at_mjd, kind="cubic", fill_value="extrapolate")

        #     if isinstance(height, int) or isinstance(height, float):
        #         interpolated_param.append(np.float(func(height)))
        #     else:
        #         interpolated_param.append(func(height))
        # interpolated_param = np.array(interpolated_param)
        # if isinstance(height, float) or isinstance(height, int):
        #     interpolated_param = np.array(interpolated_param)
        #     return interpolated_param
        # else:
        #     interpolated_param_avgs = compute_averages_std(interpolated_param)
        #     return (
        #         interpolated_param,
        #         interpolated_param_avgs[0],
        #         interpolated_param_avgs[1],
        #         interpolated_param_avgs[2],
        #         interpolated_param_avgs[3],
        #     )

    def _compute_mass_density(self, air="moist", co2_concentration=415):
        """
        Computes regular and exponential mass density of air.

        Adds to data the following columns:
        - 'Xw': molar fraction of water vapor (0 if air is dry)
        - 'Compressibility'
        - 'Mass Density'
        - 'Exponential Mass Density'

        Parameters
        ----------
        air : str
            Type of air, can be 'moist' or 'dry'
        co2_concentration : float
            CO2 volume concentration in ppmv
        """

        if air == "moist":
            self.data["Xw"] = molar_fraction_water_vapor(
                self.data["Pressure"], self.data["Temperature"], self.data["Relative humidity"]
            )
        elif air == "dry":
            self.data["Xw"] = 0.0
        else:
            raise ValueError("Wrong air condition. It must be 'moist' or 'dry'.")

        self.data["Compressibility"] = compressibility(
            self.data["Pressure"], self.data["Temperature"], self.data["Xw"]
        )
        self.data["Mass Density"] = density_moist_air(
            self.data["Pressure"],
            self.data["Temperature"],
            self.data["Compressibility"],
            self.data["Xw"],
            co2_concentration,
        )
        self.data["Exponential Mass Density"] = (
            self.data["Mass Density"] / STD_AIR_DENSITY
        ).decompose() * np.exp((self.data["Altitude"] / DENSITY_SCALE_HEIGHT).decompose())

    # =============================================================================================================
    # Main get data function
    # =============================================================================================================
    def get_data(self):
        """
        Reads ECMWF or GDAS data in ecsv or grib(2) format
        and computes statistical description of the data
        """
        file_ext = os.path.splitext(self.data_file)[1]
        if file_ext == ".grib" or file_ext == ".grib2":
            self.data = get_grib_file_data(self.data_file)
            self.data = extend_grib_data(self.data)
        elif file_ext == ".ecsv":
            self.data = Table.read(self.data_file, format="ascii.ecsv")
        else:
            raise NotImplementedError(
                f"Only grib (1,2) and ecsv formats are supported at the moment. Requested format: {file_ext}"
            )
        self.stat_columns = [
            "Pressure",
            "Altitude",
            "Density",
            "Temperature",
            "Wind Speed",
            "Wind Direction",
            "Relative humidity",
            "Exponential Density",
        ]
        self.stat_data = self.data[self.stat_columns].group_by("Pressure")
        self.stat_description = {
            "avg": self.stat_data.groups.aggregate(np.mean),
            "std": self.stat_data.groups.aggregate(np.std),
            "mad": self.stat_data.groups.aggregate(lambda x: np.mean(np.absolute(x - np.mean(x)))),
            "p2p_max": self.stat_data.groups.aggregate(lambda x: np.max(x) - np.mean(x)),
            "p2p_min": self.stat_data.groups.aggregate(lambda x: np.mean(x) - np.min(x)),
        }

    def _refractive_index(self, P, T, RH, wavelength, C):
        """Wrapper for Rayleigh.calculate_n()."""
        rayleigh = Rayleigh(wavelength, C, P, T, RH)
        return rayleigh.refractive_index

    # =======================================================================================================
    # printing functions:
    # =======================================================================================================

    def write_corsika(self, outfile, co2_concentration, upper_atmosphere=None):
        """
        Write an output file in the style of a CORSIKA atmospheric configuration file:

        alt (km)     rho (g/cm^3)   thick (g/cm^2)   (n-1)
        """

        height = np.arange(0.0, 46000.0, 1000) * u.m
        temperature = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Temperature"],
                height,
            )
            * self.stat_description["avg"]["Temperature"].unit
        )
        relative_humidity = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Relative humidity"],
                height,
            )
            * self.stat_description["avg"]["Relative humidity"].unit
        )
        pressure = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Pressure"],
                height,
            )
            * self.stat_description["avg"]["Pressure"].unit
        )
        thickness = pressure / STD_GRAVITATIONAL_ACCELERATION
        density = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Density"],
                height,
            )
            * self.stat_description["avg"]["Density"].unit
            / N0_AIR
        )
        rel_water_vapor_pressure = (
            partial_pressure_water_vapor(temperature, relative_humidity) / pressure
        ).decompose()
        rel_refractive_index = (
            self._refractive_index(
                pressure, temperature, relative_humidity, 350.0 * u.nm, co2_concentration
            )
            - 1.0
        )

        corsika_input_table = Table()
        tables = []

        for i in np.arange(len(height)):
            outdict = {
                "height": height[i].to(u.km),
                "rho": density[i].to(u.g / u.cm**3),
                "thick": thickness[i].decompose().to(u.g / u.cm**2),
                "nm1": rel_refractive_index[i],
                "T": temperature[i],
                "p": pressure[i],
                "pw/p": rel_water_vapor_pressure[i],
            }
            tables.append(outdict)
        # Merge ECMWF profile with upper atmospheric profile
        if upper_atmosphere:
            upper_atmosphere_table = Table.read(upper_atmosphere, format="ascii.ecsv")
            tables.append(upper_atmosphere_table)
        corsika_input_table = vstack(tables)
        corsika_input_table.write(outfile, overwrite=True)

    def create_mdp(self, mdp_file):
        """
        Write an output file with the molecular number density per height
        """

        heights = (
            np.arange(0.0, 27000.0, 1000) * u.m
        )  # FIXME: The hardcoded value 27 reflects the current ceiling of GDAS data (26km a.s.l.). Shouldn't be hardcoded and in general the binning and limits should be considered.
        number_density = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Density"],
                heights,
            )
            * self.stat_description["avg"]["Density"].unit
        )
        t = Table([heights, number_density], names=["height", "number density"])
        t.write(mdp_file, overwrite=True)

    def rayleigh_extinction(self, rayleigh_extinction_file, co2_concentration):
        """
        Calculates the integral optical depth due to Rayleigh scattering
        per altitude bins as a function of wavelength.
        The optical depth (AOD) for an altitude h over the observatory will be given by
        the integral of the monochromatic volume coefficient beta, with integration limits
        h_obs up to h.

        Returns:
        --------
            Ecsv file with integral optical depth per height bin per wavelength bin. The data model is the same with MODTRAN files.
        """

        # For now we work for La Palma site. We will most probably have to find an average
        # altitude for each site. h_obs should become an attribute of observatory class.
        height_obs = 2158
        height = (
            np.array(
                [
                    height_obs,
                    2258,
                    2358,
                    2458,
                    2658,
                    2858,
                    3158,
                    3658,
                    4158,
                    4500,
                    5000,
                    5500,
                    6000,
                    7000,
                    8000,
                    9000,
                    10000,
                    11000,
                    12000,
                    13000,
                    14000,
                    15000,
                    16000,
                    18000,
                    20000,
                    22000,
                    24000,
                    26000,
                ]
            )
            * u.m
        )
        # and here's the big question, still unanswered. What do we do with the altitudes that DAS values do not exist?
        # , 28.000, 30.000, 32.500, 35.000, 37.500, 40.000, 45.000, 50.000, 60.000, 70.000, 80.000, 100.000 ]
        bin_widths = np.diff(height)
        bin_centers = (height[:-1] + height[1:]) / 2

        temperature = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Temperature"],
                bin_centers,
            )
            * self.stat_description["avg"]["Temperature"].unit
        )
        relative_humidity = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Relative humidity"],
                bin_centers,
            )
            * self.stat_description["avg"]["Relative humidity"].unit
        )
        pressure = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Pressure"],
                bin_centers,
            )
            * self.stat_description["avg"]["Pressure"].unit
        )
        wavelength_range = np.arange(200, 1001, 1) * u.nm

        # Here is a schoolkid's, homemade numerical integration. Though it gives reasonable results.
        rayleigh_extinction_table = Table()
        tables = []
        for wavelength in wavelength_range:
            aod = 0
            l = []
            optical_depth = []
            l.append(wavelength)
            file_line = []
            file_line.append(wavelength.to_value())
            for P, T, RH, dh in zip(pressure, temperature, relative_humidity, bin_widths):
                rayleigh = Rayleigh(wavelength, co2_concentration, P, T, RH)
                beta = rayleigh.beta
                aod += dh * beta
                optical_depth.append(aod.to_value())
            optical_depth_column = np.array([optical_depth])
            height_column = np.array([height])
            extinction_per_wavelength = Table(
                [l, height_column, optical_depth_column],
                names=("wavelength", "altitude", "AOD"),
                units=(u.nm, u.m, u.dimensionless_unscaled),
            )
            tables.append(extinction_per_wavelength)
        rayleigh_extinction_table = vstack(tables)
        rayleigh_extinction_table.write(rayleigh_extinction_file, overwrite=True)
        return rayleigh_extinction_file
