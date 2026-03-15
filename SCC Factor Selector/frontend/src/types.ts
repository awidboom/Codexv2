export type WebFireResult = {
  activity?: string;
  ap42section?: number | string;
  applicability?: string;
  cas?: string;
  composite_test_rating?: number | string;
  condition?: string;
  control_1?: string;
  control_2?: string;
  control_3?: string;
  control_4?: string;
  control_5?: string;
  controlcode_1?: number | string;
  controlcode_2?: number | string;
  controlcode_3?: number | string;
  controlcode_4?: number | string;
  controlcode_5?: number | string;
  created?: string;
  data_category?: string;
  date_record_updated?: string;
  derivation?: string;
  eis_action_code?: string;
  eis_denominator_code?: string;
  eis_material_code?: number | string;
  eis_numerator_code?: string;
  factor?: number | string;
  factor_text?: string;
  factor_status?: string;
  factorid?: number | string;
  formula?: string;
  nei_pollutant_code?: string;
  notes?: string;
  references?: string;
  reference?: string;
  pollutant?: string;
  quality?: string;
  record_update_reason?: string;
  revoked_date?: string;
  scc?: number | string;
  scctext?: string;
  unit?: string;
  variable_definition?: string;
};

export type SearchResponse = {
  hits: number;
  results: WebFireResult[];
  snapshot_id: number;
  fetched_at: string;
};

export type SccSector = {
  name: string;
  sector_code: string;
};

export type Ap42Section = {
  value: string;
  label: string;
};

export type SccMatch = {
  code: string;
  short_name: string;
  level4: string;
};

export type CartItem = {
  scc: string;
  pollutants: string[];
};

export type SccCodeMatch = {
  code: string;
  level4: string;
  sector: string;
};
