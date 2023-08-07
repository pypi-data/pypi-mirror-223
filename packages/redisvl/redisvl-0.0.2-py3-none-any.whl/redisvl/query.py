import base64
from typing import Any, Dict, List, Optional

import numpy as np
from redis.commands.search.query import Query

from redisvl.utils.utils import TokenEscaper, array_to_buffer


class Filter:
    escaper = TokenEscaper()

    def __init__(self, field):
        self._field = field
        self._filters = []

    def __str__(self):
        base = "(" + self.to_string()
        if self._filters:
            base += "".join(self._filters)
        return base + ")"

    def __iadd__(self, other) -> "Filter":
        "intersection '+='"
        self._filters.append(f" {other.to_string()}")
        return self

    def __iand__(self, other) -> "Filter":
        "union '&='"
        self._filters.append(f" | {other.to_string()}")
        return self

    def __isub__(self, other) -> "Filter":
        "subtract '-='"
        self._filters.append(f" -{other.to_string()}")
        return self

    def __ixor__(self, other) -> "Filter":
        "With optional '^='"
        self._filters.append(f" ~{other.to_string()}")
        return self

    def to_string(self) -> str:
        raise NotImplementedError


class TagFilter(Filter):
    def __init__(self, field, tags: List[str]):
        super().__init__(field)
        self.tags = tags

    def to_string(self) -> str:
        """Converts the tag filter to a string.

        Returns:
            str: The tag filter as a string.
        """
        if not isinstance(self.tags, list):
            self.tags = [self.tags]
        return (
            "@"
            + self._field
            + ":{"
            + " | ".join([self.escaper.escape(tag) for tag in self.tags])
            + "}"
        )


class GeoFilter(Filter):
    GEO_UNITS = ["m", "km", "mi", "ft"]

    def __init__(self, field, longitude, latitude, radius, unit="km"):
        """Filter for Geo fields.

        Args:
            field (str): The field to filter on.
            longitude (float): The longitude.
            latitude (float): The latitude.
            radius (float): The radius.
            unit (str, optional): The unit of the radius. Defaults to "km".

        Raises:
            ValueError: If the unit is not one of ["m", "km", "mi", "ft"].

        Examples:
            >>> # looking for Chinese restaurants near San Francisco
            >>> # (within a 5km radius) would be
            >>> #
            >>> from redisvl.query import GeoFilter
            >>> gf = GeoFilter("location", -122.4194, 37.7749, 5)
        """
        super().__init__(field)
        self._longitude = longitude
        self._latitude = latitude
        self._radius = radius
        self._unit = self._set_unit(unit)

    def _set_unit(self, unit):
        if unit.lower() not in self.GEO_UNITS:
            raise ValueError(f"Unit must be one of {self.GEO_UNITS}")
        return unit.lower()

    def to_string(self) -> str:
        """Converts the geo filter to a string.

        Returns:
            str: The geo filter as a string.
        """
        return (
            "@"
            + self._field
            + ":["
            + str(self._longitude)
            + " "
            + str(self._latitude)
            + " "
            + str(self._radius)
            + " "
            + self._unit
            + "]"
        )


class NumericFilter(Filter):
    def __init__(self, field, minval, maxval, min_exclusive=False, max_exclusive=False):
        """Filter for Numeric fields.

        Args:
            field (str): The field to filter on.
            minval (int): The minimum value.
            maxval (int): The maximum value.
            min_exclusive (bool, optional): Whether the minimum value is exclusive. Defaults to False.
            max_exclusive (bool, optional): Whether the maximum value is exclusive. Defaults to False.
        """
        self.top = maxval if not max_exclusive else f"({maxval}"
        self.bottom = minval if not min_exclusive else f"({minval}"
        super().__init__(field)

    def to_string(self):
        return "@" + self._field + ":[" + str(self.bottom) + " " + str(self.top) + "]"


class TextFilter(Filter):
    def __init__(self, field, text: str):
        """Filter for Text fields.
        Args:
            field (str): The field to filter on.
            text (str): The text to filter on.
        """
        super().__init__(field)
        self.text = text

    def to_string(self) -> str:
        """Converts the filter to a string.

        Returns:
            str: The filter as a string.
        """
        return "@" + self._field + ":" + self.escaper.escape(self.text)


class BaseQuery:
    def __init__(
        self, return_fields: Optional[List[str]] = None, num_results: Optional[int] = 10
    ):
        self._return_fields = return_fields
        self._num_results = num_results

    @property
    def query(self):
        pass

    @property
    def params(self):
        pass


class VectorQuery(BaseQuery):
    dtypes = {
        "float32": np.float32,
        "float64": np.float64,
    }

    DISTANCE_ID = "vector_distance"

    def __init__(
        self,
        vector: List[float],
        vector_field_name: str,
        return_fields: List[str],
        hybrid_filter: Filter = None,
        dtype: str = "float32",
        num_results: Optional[int] = 10,
        return_score: bool = True,
    ):
        """Query for vector fields

        Args:
            vector (List[float]): The vector to query for.
            vector_field_name (str): The name of the vector field
            return_fields (List[str]): The fields to return.
            hybrid_filter (Filter, optional): A filter to apply to the query. Defaults to None.
            dtype (str, optional): The dtype of the vector. Defaults to "float32".
            num_results (Optional[int], optional): The number of results to return. Defaults to 10.
            return_score (bool, optional): Whether to return the score. Defaults to True.

        Raises:
            TypeError: If hybrid_filter is not of type redisvl.query.Filter

        """
        super().__init__(return_fields, num_results)
        self._vector = vector
        self._field = vector_field_name
        self._dtype = dtype.lower()
        if hybrid_filter:
            self.set_filter(hybrid_filter)
        else:
            self._filter = "*"

        if return_score:
            self._return_fields.append(self.DISTANCE_ID)

    def set_filter(self, hybrid_filter: Filter):
        """Set the filter for the query.

        Args:
            hybrid_filter (Filter): The filter to apply to the query.
        """
        if not isinstance(hybrid_filter, Filter):
            raise TypeError("hybrid_filter must be of type redisvl.query.Filter")
        self._filter = str(hybrid_filter)

    def get_filter(self) -> Filter:
        """Get the filter for the query.

        Returns:
            Filter: The filter for the query.
        """
        return self._filter

    def __str__(self):
        return " ".join([str(x) for x in self.query.get_args()])

    @property
    def query(self) -> Query:
        """Return a Redis-Py Query object representing the query.

        Returns:
            redis.commands.search.query.Query: The query object.
        """
        base_query = f"{self._filter}=>[KNN {self._num_results} @{self._field} $vector AS {self.DISTANCE_ID}]"
        query = (
            Query(base_query)
            .return_fields(*self._return_fields)
            .sort_by(self.DISTANCE_ID)
            .paging(0, self._num_results)
            .dialect(2)
        )
        return query

    @property
    def params(self) -> Dict[str, Any]:
        """Return the parameters for the query.

        Returns:
            Dict[str, Any]: The parameters for the query.
        """
        return {"vector": array_to_buffer(self._vector, dtype=self.dtypes[self._dtype])}
