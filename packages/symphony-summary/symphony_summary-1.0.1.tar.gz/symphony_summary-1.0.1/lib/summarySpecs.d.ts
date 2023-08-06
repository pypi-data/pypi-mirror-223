import type ColumnTable from 'arquero/dist/types/table/column-table';
import { QueryElement, SummaryElement } from '@apple/symphony-lib';
export declare function extractColumnElements(table: ColumnTable): SummaryElement[];
export declare function getQueryTree(table: ColumnTable): QueryElement;
