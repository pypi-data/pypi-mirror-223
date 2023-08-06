# Symphony Summary Widget

A component that displays an overview of the provided dataset table.
To configure it, pass a list of `SummaryElement`.
One `SummaryElement` is defined as:

```
export interface SummaryElement {
    name: string;
    data: number | ChartData;
}
```

`ChartData` is defined as:

```
export interface ChartData {
    spec: VegaLiteSpec;
    data: Record<string, unknown>;
}
```
