"""Module containing the Data Store Product class."""
from __future__ import annotations

import re
from contextlib import contextmanager
from datetime import datetime
from functools import total_ordering
from typing import TYPE_CHECKING

from eumdac.request import get

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from typing import IO, Any, Optional

    if sys.version_info < (3, 9):
        from typing import Generator, Mapping, MutableMapping, Pattern, Sequence
    else:
        from collections.abc import Mapping, MutableMapping, Generator, Sequence
        from re import Pattern
    from eumdac.datastore import DataStore
    from eumdac.collection import Collection

from eumdac.errors import EumdacError, eumdac_raise_for_status
import eumdac.common


@total_ordering
class Product:
    """Product of a Collection in the Data Store

    Attributes:
        datastore: Reference to the Data Store
        download_url: URL to the download endpoint of the Data Store

    Arguments:
        collection_id: Data Store ID of the collection
        product_id: Data Store ID of the product
        datastore: Reference to the Data Store
    """

    _id: str
    datastore: DataStore
    collection: Collection
    _properties: Optional[Mapping[str, Any]] = None
    _geometry: Optional[Mapping[str, Any]] = None
    _entries: Optional[Sequence[str]] = None
    _extract_filename: Pattern[str] = re.compile(r'filename="(.*?)"')
    _extract_sensing_time: Pattern[str] = re.compile(
        r"(?P<start>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3,6})?)?"
        r"\d*Z?[\\/]+"
        r"(?P<end>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3,6})?)?"
    )
    _extract_ingestion_time: Pattern[str] = re.compile(
        r"(?P<updated>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3,6})?)?"
    )

    def __init__(self, collection_id: str, product_id: str, datastore: DataStore) -> None:
        self._id = product_id
        self.datastore = datastore
        self.collection = self.datastore.get_collection(collection_id)

    def __str__(self) -> str:
        return str(self._id)

    def __repr__(self) -> str:
        return f"{self.__class__}({self.collection._id}, {self._id})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and (self.collection._id, self._id) == (
            other.collection._id,
            other._id,
        )

    def __lt__(self, other: Product) -> bool:
        return (self.collection._id, self._id) < (other.collection._id, other._id)

    def __hash__(self) -> int:
        return hash(repr(self))

    def _ensure_properties(self) -> None:
        if self._properties is not None:
            return
        url = self.datastore.urls.get(
            "datastore",
            "download product metadata",
            vars={"collection_id": self.collection._id, "product_id": self._id},
        )
        auth = self.datastore.token.auth
        response = get(
            url,
            params={"format": "json"},
            auth=auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status(
            f"Product {self._id} not found in {self.collection._id}", response, ProductError
        )

        if "geometry" in response.json():
            geometry = response.json()["geometry"]
        else:
            geometry = None

        properties = response.json()["properties"]
        properties.pop("parentIdentifier")
        properties.pop("links", None)

        ## Fix product size by fetching it from the Browse endpoint
        url = self.datastore.urls.get(
            "datastore",
            "browse product",
            vars={"collection_id": self.collection._id, "product_id": self._id},
        )
        auth = self.datastore.token.auth
        response = get(
            url,
            params={"format": "json"},
            auth=auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status(
            f"Product {self._id} not found in {self.collection._id}", response, ProductError
        )
        browse_properties = response.json()["properties"]
        browse_size = browse_properties["productInformation"]["size"]
        properties["productInformation"]["size"] = browse_size

        ## Add MD5 and time of publication from the Browse endpoint
        if "md5" in browse_properties["extraInformation"]:
            properties.update({"md5": browse_properties["extraInformation"]["md5"]})
        else:
            properties.update({"md5": None})
        properties["updated"] = browse_properties["updated"]

        ## Add SIP entries from the Browse endpoint
        links = browse_properties["links"]

        self._geometry = geometry
        self._properties = properties
        self._entries = [link["title"] for link in links["sip-entries"]]

    @property
    def sensing_start(self) -> datetime or bool:  # type: ignore[valid-type]
        """Sensing start date"""
        self._ensure_properties()
        sensing_time = self._extract_sensing_time.search(  # type: ignore[union-attr]
            self._properties["date"]  # type: ignore[index]
        ).groupdict()
        sensing_start = sensing_time["start"]
        if sensing_start is None:
            return False
        else:
            return datetime.fromisoformat(sensing_start)

    @property
    def sensing_end(self) -> datetime or bool:  # type: ignore[valid-type]
        """Sensing end date"""
        self._ensure_properties()
        sensing_time = self._extract_sensing_time.search(  # type: ignore[union-attr]
            self._properties["date"]  # type: ignore[index]
        ).groupdict()
        sensing_end = sensing_time["end"]
        if sensing_end is None:
            return False
        else:
            return datetime.fromisoformat(sensing_end)

    @property
    def satellite(self) -> str:
        """Platform or Mission related to the product"""
        self._ensure_properties()
        satellites = [
            acquisition["platform"]["platformShortName"]
            for acquisition in self._properties["acquisitionInformation"]  # type: ignore[index]
        ]
        return ", ".join(satellites)

    @property
    def instrument(self) -> str:
        """Instrument related to the product"""
        self._ensure_properties()
        instruments = [
            acquisition["instrument"]["instrumentShortName"]
            for acquisition in self._properties["acquisitionInformation"]  # type: ignore[index]
        ]
        return ", ".join(instruments)

    @property
    def size(self) -> int:
        """Size of the product"""
        self._ensure_properties()
        return self._properties["productInformation"]["size"]  # type: ignore[index]

    @property
    def timeliness(self) -> int or bool:  # type: ignore[valid-type]
        """Timeliness of the product"""
        self._ensure_properties()
        if "timeliness" in self._properties["productInformation"]:  # type: ignore[index]
            return self._properties["productInformation"]["timeliness"]  # type: ignore[index]
        return False

    @property
    def md5(self) -> str or bool:  # type: ignore[valid-type]
        """MD5 checksum of the product SIP"""
        self._ensure_properties()
        if self._properties["md5"] is None:  # type: ignore[index]
            return False
        else:
            return self._properties["md5"]  # type: ignore[index]

    @property
    def ingested(self) -> datetime or bool:  # type: ignore[valid-type]
        """Date of publication"""
        self._ensure_properties()
        ingestion_time = self._extract_ingestion_time.search(  # type: ignore[union-attr]
            self._properties["updated"]  # type: ignore[index]
        ).groupdict()
        ingestion_time = ingestion_time["updated"]
        if ingestion_time is None:
            return False
        else:
            return datetime.fromisoformat(ingestion_time)

    @property
    def orbit_is_LEO(self) -> bool:
        """Is Orbit Type LEO?"""
        self._ensure_properties()
        if self._properties["acquisitionInformation"][0]["platform"]["orbitType"] == "LEO":  # type: ignore[index]
            return True
        return False

    @property
    def orbit_number(self) -> int or bool:  # type: ignore[valid-type]
        """Orbit Number of LEO product"""
        self._ensure_properties()
        if self._properties["acquisitionInformation"][0]["platform"]["orbitType"] == "LEO":  # type: ignore[index]
            if (
                "orbitNumber"
                in self._properties["acquisitionInformation"][0]["acquisitionParameters"]  # type: ignore[index]
            ):
                return self._properties["acquisitionInformation"][0]["acquisitionParameters"][  # type: ignore[index]
                    "orbitNumber"
                ]
        return False

    @property
    def orbit_direction(self) -> str or bool:  # type: ignore[valid-type]
        """Orbit Direction of LEO product"""
        self._ensure_properties()
        if self._properties["acquisitionInformation"][0]["platform"]["orbitType"] == "LEO":  # type: ignore[index]
            if (
                "orbitDirection"
                in self._properties["acquisitionInformation"][0]["acquisitionParameters"]  # type: ignore[index]
            ):
                return self._properties["acquisitionInformation"][0]["acquisitionParameters"][  # type: ignore[index]
                    "orbitDirection"
                ]
        return False

    @property
    def relative_orbit(self) -> int or bool:  # type: ignore[valid-type]
        """Relative Orbit Number of LEO product"""
        self._ensure_properties()
        if self._properties["acquisitionInformation"][0]["platform"]["orbitType"] == "LEO":  # type: ignore[index]
            if (
                "relOrbitStart"
                in self._properties["acquisitionInformation"][0]["acquisitionParameters"]  # type: ignore[index]
            ):
                return self._properties["acquisitionInformation"][0]["acquisitionParameters"][  # type: ignore[index]
                    "relOrbitStart"
                ]
        return False

    @property
    def cycle_number(self) -> int or bool:  # type: ignore[valid-type]
        """Cycle Number of LEO product"""
        self._ensure_properties()
        if self._properties["acquisitionInformation"][0]["platform"]["orbitType"] == "LEO":  # type: ignore[index]
            if (
                "cycleNumber"
                in self._properties["acquisitionInformation"][0]["acquisitionParameters"]  # type: ignore[index]
            ):
                return self._properties["acquisitionInformation"][0]["acquisitionParameters"][  # type: ignore[index]
                    "cycleNumber"
                ]
        return False

    @property
    def metadata(self) -> MutableMapping[str, Any]:
        """Product metadata"""
        self._ensure_properties()
        return {
            "geometry": self._geometry.copy(),  # type: ignore[union-attr]
            "properties": self._properties.copy(),  # type: ignore[union-attr]
        }

    @property
    def entries(self) -> Sequence[str] or bool:  # type: ignore[valid-type]
        """Files inside the product"""
        self._ensure_properties()
        if self._entries is None:
            return False
        else:
            return tuple(self._entries)  # type: ignore[arg-type]

    @property
    def url(self) -> str:
        """URL of the product"""
        auth = str(self.datastore.token.access_token)
        url = self.datastore.urls.get(
            "datastore",
            "download product",
            vars={"collection_id": self.collection._id, "product_id": self._id},
        )
        download_url = str(url) + "?access_token=" + auth
        return download_url

    @contextmanager
    def open(self, entry: Optional[str] = None) -> Generator[IO[bytes], None, None]:
        """Opens a stream to download the product content.

        Note:
            A Data Store product refers to a zip archive containing the data.

        Arguments:
            entry (optional): specific file inside the product
        """
        url = self.datastore.urls.get(
            "datastore",
            "download product",
            vars={"collection_id": self.collection._id, "product_id": self._id},
        )
        auth = self.datastore.token.auth
        params = None
        if entry is not None:
            url += "/entry"
            params = {"name": entry}
        with get(
            url,
            auth=auth,
            params=params,
            stream=True,
            headers=eumdac.common.headers,
        ) as response:
            eumdac_raise_for_status(
                f"Could not download Product {self._id} of Collection {self.collection._id}",
                response,
                ProductError,
            )
            match = self._extract_filename.search(response.headers["Content-Disposition"])
            filename = match.group(1)  # type: ignore[union-attr]
            response.raw.name = filename
            response.raw.decode_content = True
            yield response.raw


class ProductError(EumdacError):
    """Errors related to products"""
