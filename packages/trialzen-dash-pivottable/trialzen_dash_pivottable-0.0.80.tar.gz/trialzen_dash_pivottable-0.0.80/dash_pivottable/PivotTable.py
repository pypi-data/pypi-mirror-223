# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PivotTable(Component):
    """A PivotTable component.
Pivot tables are useful for interactive presentation of
summary statistics computed for data contained in another table.

This function provides a convenient Dash interface
to the `react-pivottable` component, which makes it easy to embed
pivot tables into Dash for R applications.

Within React, the interactive component provided by `react-pivottable`
is `PivotTableUI`, but output rendering is delegated to the non-interactive
`PivotTable` component, which accepts a subset of its properties.
`PivotTable` in turn delegates to a specific renderer component, such as
the default `TableRenderer`, which accepts a subset of the same properties.
Finally, most renderers will create non-React PivotData objects to handle
the actual computations, which also accept a subset of the same properties
as the rest of the stack.

The arguments for this function correspond to properties of the component;
a full list is provided below.

`react-pivottable` was developed by Nicolas Kruchten; source
for this component is available from https://github.com/plotly/react-pivottable.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- data (list; optional): data to be summarized
- hiddenAttributes (list; optional): contains attribute names to omit from the UI
- extraAttributes (dict; optional): contains attribute names to add to the UI, useful when aggregation is done in the backend
e.g. { "Test": { 'a': 1, 'b': 1, 'c': 1 }, "Test2": {'x': 1, 'y': 1} }
where 1 stands for the count of the value (but it's optional to provide the true row count with backend aggregation)
- hiddenFromAggregators (list; optional): contains attribute names to omit from the aggregator arguments dropdowns
- hiddenFromDragDrop (list; optional): contains attribute names to omit from the drag'n'drop portion of the UI
- menuLimit (number; default 500): maximum number of values to list in the double-click menu
- unusedOrientationCutoff (number; default 85): If the attributes' names' combined length in characters exceeds this
value then the unused attributes area will be shown vertically to the
left of the UI instead of horizontally above it. 0 therefore means
'always vertical', and Infinity means 'always horizontal'.
- cols (list; optional): Which columns are currently in the column area
- colOrder (string; optional): the order in which column data is provided to the renderer, must be one
of "key_a_to_z", "value_a_to_z", "value_z_to_a", ordering by value
orders by column total
- rows (list; optional): Which rows is currently inside the row area.
- rowOrder (string; optional): the order in which row data is provided to the renderer, must be one
of "key_a_to_z", "value_a_to_z", "value_z_to_a", ordering by value
orders by row total
- aggregatorName (string; optional): Which aggregator is currently selected. E.g. Count, Sum, Average, etc.
- vals (list; optional): Vals for the aggregator.
- valueFilter (dict; optional): Value filter for each attribute name.
- rendererName (string; optional): Which renderer is currently selected. E.g. Table, Line Chart, Scatter
Chart, etc.
- listedAggregators (list; default ['Value']): Optional list of aggregators
- listedAggregationValues (list; optional): Optional list of aggregators values
- listedRenderers (list; optional): Optional list of renderer
- showUI (boolean; default True): If disabled, the entire pivot configuration UI is hidden
- plotlyOptions (dict; default {width: 100, height: 100}): to change plot options, e.g. the size of the graph {with:100, height:300}
- tableOptions (dict; optional): to change the table renderer options e.g
    {
    "rowTotals": true,
    "colTotals": true,
    "colTotalValues": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6},
    "rowTotalValues": {Female: 7, Male: 8},
    "grandTotalValue": 99,
    }"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, hiddenAttributes=Component.UNDEFINED, extraAttributes=Component.UNDEFINED, hiddenFromAggregators=Component.UNDEFINED, hiddenFromDragDrop=Component.UNDEFINED, menuLimit=Component.UNDEFINED, unusedOrientationCutoff=Component.UNDEFINED, cols=Component.UNDEFINED, colOrder=Component.UNDEFINED, rows=Component.UNDEFINED, rowOrder=Component.UNDEFINED, aggregatorName=Component.UNDEFINED, vals=Component.UNDEFINED, valueFilter=Component.UNDEFINED, rendererName=Component.UNDEFINED, listedAggregators=Component.UNDEFINED, listedAggregationValues=Component.UNDEFINED, listedRenderers=Component.UNDEFINED, showUI=Component.UNDEFINED, plotlyOptions=Component.UNDEFINED, tableOptions=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'hiddenAttributes', 'extraAttributes', 'hiddenFromAggregators', 'hiddenFromDragDrop', 'menuLimit', 'unusedOrientationCutoff', 'cols', 'colOrder', 'rows', 'rowOrder', 'aggregatorName', 'vals', 'valueFilter', 'rendererName', 'listedAggregators', 'listedAggregationValues', 'listedRenderers', 'showUI', 'plotlyOptions', 'tableOptions']
        self._type = 'PivotTable'
        self._namespace = 'dash_pivottable'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'hiddenAttributes', 'extraAttributes', 'hiddenFromAggregators', 'hiddenFromDragDrop', 'menuLimit', 'unusedOrientationCutoff', 'cols', 'colOrder', 'rows', 'rowOrder', 'aggregatorName', 'vals', 'valueFilter', 'rendererName', 'listedAggregators', 'listedAggregationValues', 'listedRenderers', 'showUI', 'plotlyOptions', 'tableOptions']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(PivotTable, self).__init__(**args)
