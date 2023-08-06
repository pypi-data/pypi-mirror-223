# SymphonyDataMap

A rendered map where landmarks are colored by another variable.
To configure the map, the spec of this component is defined as follows:

```
@dataclass
class DataMapSpec(WidgetSpec):
    projection: str
    id_map: dict
    feature: str
    id_column: str
    map_url: str
```

The projection is a `vega-projection`, the `id_map` maps names to multiple `id` in a TopoJSON, the `feature` defines what column to color by, the `id_column` defines where names are to be found, and the `map_url` provides a link to the appropriate TopoJSON.
