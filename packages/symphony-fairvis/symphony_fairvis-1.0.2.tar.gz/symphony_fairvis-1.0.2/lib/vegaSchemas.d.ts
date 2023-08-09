import type { VegaSpec, VegaLiteSpec } from 'svelte-vega';
export declare enum SchemaType {
    beeswarm = 0,
    strip = 1
}
export declare function getSchema(type: SchemaType, width: number): VegaSpec | VegaLiteSpec;
