import type ColumnTable from 'arquero/dist/types/table/column-table';
export declare function getUniqueValuesForStringColumnForFamiliarity(split: boolean, familiarityColumn: string, columnName: string, table: ColumnTable): string[];
export declare function getSplitTable(columnValue: string, familiarityColumn: string, column: string, table: ColumnTable): ColumnTable;
export declare function getSplitTables(columnValue: string, familiarityColumn: string, column: string, tables: ColumnTable[]): ColumnTable[];
