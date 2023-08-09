"""Calculate weights."""
import logging
import os
from typing import Any
from typing import Literal
from typing import Optional
from typing import Union

import geopandas as gpd
import pandas as pd

from gdptools.weights.calc_weight_engines import DaskWghtGenEngine
from gdptools.weights.calc_weight_engines import ParallelWghtGenEngine
from gdptools.weights.calc_weight_engines import SerialWghtGenEngine

logger = logging.getLogger(__name__)

WEIGHT_GEN_METHODS = Literal["serial", "parallel", "dask"]
""" Methods used in WeightGen class.

serial: Iterates through polygons to calculate weights.  Sufficient for most cases.
parallel: Chunks polygons and distributes to available processors.  Provides a
substantial speedup when there is a large number of polygons.

Raises:
    TypeError: If value is not one of "serial" or "parallel".

Returns:
    _type_: str
"""


class WeightGenP2P:
    """Class for weight calculation."""

    def __init__(
        self,
        *,
        target_poly: gpd.GeoDataFrame,
        target_poly_idx: str,
        source_poly: gpd.GeoDataFrame,
        source_poly_idx: str,
        method: WEIGHT_GEN_METHODS,
        weight_gen_crs: Any,
        output_file: Optional[Union[str, None]] = None,
        jobs: Optional[int] = -1,
        intersections: Optional[int] = False,
        verbose: Optional[bool] = False,
    ) -> None:
        """Weight generation class.

        The WeightGenP2P class is used to calculate weights between 2 polygonal
        GeoDataFrames.  The weights are returned as a pandas DataFrame and can be
        optionally save to a .csv file.  The DataFrame has the following columns:
        * target_id: The target polygon feature id
        * source_id: The source polygon feature id
        * weight: The calculated weight for the target/source pair. The weight
        represents the fractional area that the source polygon contributes to the
        target polygon.  If the source polygons are spatially continuous with no
        overlaps, suming the weights for a given target polygon should result in a
        value of 1.
        As long as the source polygon and targe polygons remain the same, the weights file
        can be saved and reused for future calculations, for example if the user wants
        a different variable or statistic and does not want to recalculate the weights.

        Args:
            target_poly (gpd.GeoDataFrame): Geodatafram consisting of a column with
                heading string of target_poly_idx, and a geometry column.
            target_poly_idx (str): String of the feature id that will be tagged in the
                resulting weights file.
            source_poly (gpd.GeoDataFrame):  Geodatafram consisting of a column with
                heading string of source_poly_idx, and a geometry column.
            source_poly_idx (str): String of the feature id that will be tagged
                in the resulting weights file.
            method (WEIGHT_GEN_METHODS): One of :data:`WEIGHT_GEN_METHODS`
            weight_gen_crs (Any): Any projection that can be used by
                pyproj.CRS.from_user_input
            output_file (Optional[Union[str, None]], optional): Sting of the
                /path/to/file or None if no output is desired. Defaults to None.
            jobs (Optional[int], optional): Optional, number of processors used in
                parallel or dask methods (dask uses dask bag). If set to default value
                (-1) jobs is defined as the number of processors available/2.
                In this case, because the data needs to be distributed amoung processors
                choosing half the processors available is a reasonable choice. Defaults
                to -1.
            intersections (Optional[bool], optional): _description_. Defaults to False.
            verbose (Optional[bool], optional): If True then extra output is printed.
                Defaults to False.

        Raises:
            TypeError: If one of the method arguments does not match
                :data:`WEIGHT_GEN_METHODS`

        """
        self.target_poly = target_poly.reset_index()
        self.target_poly_idx = target_poly_idx
        self.source_poly = source_poly.reset_index()
        self.source_poly_idx = source_poly_idx
        self.method = method
        if output_file is None:
            self.output_file = ""
        else:
            self.output_file = output_file
        self.weight_gen_crs = weight_gen_crs
        self.jobs = jobs
        self.calc_intersections = intersections
        self.verbose = verbose
        self._intersections: gpd.GeoDataFrame
        self.__calc_method: Union[
            SerialWghtGenEngine, ParallelWghtGenEngine, DaskWghtGenEngine
        ]
        if self.method == "serial":
            self.__calc_method = SerialWghtGenEngine()
            print("Using serial engine")
        elif self.method == "parallel":
            self.__calc_method = ParallelWghtGenEngine()
            print("Using parallel engine")
        elif self.method == "dask":
            self.__calc_method = DaskWghtGenEngine()
        else:
            raise TypeError(f"method: {self.method} not in [serial, parallel]")

        if jobs == -1:
            self.jobs = int(os.cpu_count() / 2)  # type: ignore
            if self.method in ["parallel", "dask"]:
                logger.info(" Getting jobs from os.cpu_count()")
        else:
            self.jobs = jobs
        if self.method in ["parallel", "dask"]:
            logger.info(f"  Parallel or Dask multiprocessing  using {self.jobs} jobs")
        self.verbose = verbose

    def calculate_weights(self) -> pd.DataFrame:
        """Calculate weights and return weights dataframe."""
        if self.calc_intersections:
            weights, self._intersections = self.__calc_method.calc_weights(
                target_poly=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                source_poly=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type="poly",
                wght_gen_crs=self.weight_gen_crs,
                filename=self.output_file,
                intersections=self.calc_intersections,
                jobs=self.jobs,
                verbose=self.verbose,
            )
        else:
            weights = self.__calc_method.calc_weights(
                target_poly=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                source_poly=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type="poly",
                wght_gen_crs=self.weight_gen_crs,
                filename=self.output_file,
                intersections=self.calc_intersections,
                jobs=self.jobs,
                verbose=self.verbose,
            )

        return weights

    def create_wght_df(self) -> pd.DataFrame:
        """Create dataframe from weight components."""
        wght_df = pd.DataFrame(
            {
                self.target_poly_idx: self.plist,
                self.source_poly_idx[0]: self.splist,
                "wght": self.wghtlist,
            }
        )
        wght_df = wght_df.astype(
            {"wght": float, self.target_poly_idx: str, self.source_poly_idx[0]: str}
        )
        return wght_df

    @property
    def intersections(self) -> gpd.GeoDataFrame:
        """Return intersections."""
        if self._intersections is None:
            print(
                "intersections not calculated, "
                "Run calculate_weights(intersectiosn=True)"
            )
        return self._intersections
