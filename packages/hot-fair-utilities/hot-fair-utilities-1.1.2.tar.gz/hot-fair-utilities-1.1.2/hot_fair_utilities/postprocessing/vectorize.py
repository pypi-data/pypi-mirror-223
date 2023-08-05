# Standard library imports
from glob import glob
from pathlib import Path

# Third party imports
import geopandas as gpd
import numpy as np
import rasterio as rio
from rasterio.features import shapes
from rasterio.merge import merge
from shapely.geometry import Polygon, shape
from tqdm import tqdm

TOLERANCE = 0.5
AREA_THRESHOLD = 0.1
MAX_RATIO = 10
MIN_AREA = 3  # sqm


def vectorize(input_path: str, output_path: str) -> None:
    """Polygonize raster tiles from the input path.

    Note that as input, we are expecting GeoTIF images with EPSG:3857 as
    CRS here. CRS of the resulting GeoJSON file will be EPSG:4326.

    Args:
        input_path: Path of the directory where the TIF files are stored.
        output_path: Path of the output file.

    Example::

        vectorize("data/masks_v2/4", "labels.geojson")
    """
    base_path = Path(output_path).parents[0]
    base_path.mkdir(exist_ok=True, parents=True)

    raster_paths = glob(f"{input_path}/*.tif")
    with rio.open(raster_paths[0]) as src:
        kwargs = src.meta.copy()

    rasters = [rio.open(path) for path in raster_paths]
    mosaic, output = merge(rasters)

    # Close raster files after merging
    for raster in rasters:
        raster.close()

    polygons = [shape(s) for s, _ in shapes(mosaic, transform=output)]

    areas = [poly.area for poly in polygons]
    max_area, median_area = np.max(areas), np.median(areas)
    polygons = [
        Polygon(poly.exterior.coords)
        for poly in polygons
        if poly.area != max_area
        and poly.area / median_area > AREA_THRESHOLD
        and poly.area > MIN_AREA
    ]

    gs = gpd.GeoSeries(polygons, crs=kwargs["crs"]).simplify(TOLERANCE)
    gs = remove_overlapping_polygons(gs)
    if gs.empty:
        raise ValueError("No Features Found")
    gs.to_crs("EPSG:4326").to_file(output_path)


def remove_overlapping_polygons(gs: gpd.GeoSeries) -> gpd.GeoSeries:
    to_remove = set()
    gs_sindex = gs.sindex

    for i, p in tqdm(gs.items()):
        possible_matches_index = list(gs_sindex.intersection(p.bounds))
        possible_matches = gs.iloc[possible_matches_index]
        precise_matches = possible_matches[possible_matches.overlaps(p)]

        for j, q in precise_matches.items():
            if i != j:
                ratio = max(p.area, q.area) / min(p.area, q.area)
                if ratio > MAX_RATIO:
                    to_remove.add(i if p.area < q.area else j)

    return gs.drop(list(to_remove))
