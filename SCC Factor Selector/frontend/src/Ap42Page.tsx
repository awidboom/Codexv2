import { useEffect, useMemo, useState } from 'react';
import FactorDetailModal from './FactorDetailModal';
import { exportAp42Selected, fetchAp42Sections, searchAp42Factors } from './api';
import { Ap42Section, WebFireResult } from './types';

export default function Ap42Page() {
  const [sections, setSections] = useState<Ap42Section[]>([]);
  const [section, setSection] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingSections, setLoadingSections] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState<WebFireResult[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [detailItem, setDetailItem] = useState<WebFireResult | null>(null);
  const [lastFetchedAt, setLastFetchedAt] = useState('');
  const [latestRecordUpdate, setLatestRecordUpdate] = useState('');
  const [pollutantFilter, setPollutantFilter] = useState('');
  const [selectedFactorIds, setSelectedFactorIds] = useState<Array<number | string>>([]);
  const [exportError, setExportError] = useState('');
  const [columnFilters, setColumnFilters] = useState({
    scc: '',
    pollutant: '',
    factor: '',
    unit: '',
    activity: '',
    quality: '',
    scctext: ''
  });

  useEffect(() => {
    setLoadingSections(true);
    fetchAp42Sections()
      .then(setSections)
      .catch(() => setSections([]))
      .finally(() => setLoadingSections(false));
  }, []);

  const getLatestRecordUpdate = (rows: WebFireResult[]) => {
    const candidates: Date[] = [];
    rows.forEach((row) => {
      const raw = (row.date_record_updated || row.created || '').toString().trim();
      if (!raw) {
        return;
      }
      const parsed = Date.parse(raw);
      if (!Number.isNaN(parsed)) {
        candidates.push(new Date(parsed));
      }
    });
    if (!candidates.length) {
      return '';
    }
    const latest = candidates.reduce((acc, current) => (current > acc ? current : acc));
    return latest.toISOString();
  };

  const onSearch = async () => {
    if (!section.trim()) {
      setError('Choose an AP-42 section before searching.');
      return;
    }
    setLoading(true);
    setError('');
    setHasSearched(true);
    try {
      const response = await searchAp42Factors(section);
      setResults(response.results);
      setLastFetchedAt(response.fetched_at);
      setLatestRecordUpdate(getLatestRecordUpdate(response.results));
      setSelectedFactorIds([]);
    } catch (err) {
      setError('Failed to load results.');
    } finally {
      setLoading(false);
    }
  };

  const filteredResults = useMemo(() => {
    if (!pollutantFilter.trim()) {
      return results;
    }
    const needle = pollutantFilter.trim().toLowerCase();
    return results.filter((item) => (item.pollutant || '').toLowerCase().includes(needle));
  }, [results, pollutantFilter]);

  const columnFilteredResults = useMemo(() => {
    const filters = {
      scc: columnFilters.scc.trim().toLowerCase(),
      pollutant: columnFilters.pollutant.trim().toLowerCase(),
      factor: columnFilters.factor.trim().toLowerCase(),
      unit: columnFilters.unit.trim().toLowerCase(),
      activity: columnFilters.activity.trim().toLowerCase(),
      quality: columnFilters.quality.trim().toLowerCase(),
      scctext: columnFilters.scctext.trim().toLowerCase()
    };

    return filteredResults.filter((item) => {
      if (filters.scc && !String(item.scc || '').toLowerCase().includes(filters.scc)) {
        return false;
      }
      if (
        filters.pollutant &&
        !String(item.pollutant || '').toLowerCase().includes(filters.pollutant)
      ) {
        return false;
      }
      const factorValue = item.factor_text ?? item.factor;
      if (filters.factor && !String(factorValue || '').toLowerCase().includes(filters.factor)) {
        return false;
      }
      if (filters.unit && !String(item.unit || '').toLowerCase().includes(filters.unit)) {
        return false;
      }
      if (filters.activity && !String(item.activity || '').toLowerCase().includes(filters.activity)) {
        return false;
      }
      if (filters.quality && !String(item.quality || '').toLowerCase().includes(filters.quality)) {
        return false;
      }
      if (filters.scctext && !String(item.scctext || '').toLowerCase().includes(filters.scctext)) {
        return false;
      }
      return true;
    });
  }, [filteredResults, columnFilters]);

  const toggleSelection = (id: number | string) => {
    setSelectedFactorIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const selectAllVisible = () => {
    const ids = columnFilteredResults
      .map((item) => item.factorid)
      .filter((value): value is number | string => value !== undefined && value !== null);
    setSelectedFactorIds(ids);
  };

  const clearSelection = () => {
    setSelectedFactorIds([]);
  };

  const exportSelected = async () => {
    if (!selectedFactorIds.length) {
      setExportError('Select at least one emission factor to export.');
      return;
    }
    setExportError('');
    try {
      const response = await exportAp42Selected(selectedFactorIds);
      const blob = await response.blob();
      const header = response.headers.get('content-disposition') || '';
      const match = header.match(/filename=([^;]+)/i);
      const filename = match ? match[1].replace(/\"/g, '') : 'webfire_ap42_export.csv';
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setExportError('Export failed. Try again.');
    }
  };

  const uniqueOptions = useMemo(() => {
    const values = {
      unit: new Set<string>(),
      activity: new Set<string>(),
      quality: new Set<string>(),
      pollutant: new Set<string>()
    };
    filteredResults.forEach((item) => {
      if (item.unit) values.unit.add(item.unit);
      if (item.activity) values.activity.add(item.activity);
      if (item.quality) values.quality.add(item.quality);
      if (item.pollutant) values.pollutant.add(item.pollutant);
    });
    return {
      unit: Array.from(values.unit).sort(),
      activity: Array.from(values.activity).sort(),
      quality: Array.from(values.quality).sort(),
      pollutant: Array.from(values.pollutant).sort()
    };
  }, [filteredResults]);

  return (
    <div className="page">
      <header className="hero">
        <div className="hero-content">
          <p className="eyebrow">Internal Emission Factor Tool</p>
          <h1>AP-42 Section Downloader</h1>
          <p className="lede">
            Filter WebFIRE emission factors by AP-42 section and export the matching records.
          </p>
          <a className="external-link" href="#/">
            Back to SCC Factor Selector
          </a>
        </div>
        <div className="card">
          <h2>AP-42 Section</h2>
          <label>
            Choose an AP-42 section
            <select
              value={section}
              onChange={(event) => setSection(event.target.value)}
              disabled={loadingSections}
            >
              <option value="">Choose section</option>
              {sections.map((item) => (
                <option key={item.value} value={item.value}>
                  {item.value} {item.label ? `- ${item.label}` : ''}
                </option>
              ))}
            </select>
          </label>
          <button onClick={onSearch} disabled={loading || !section.trim()}>
            {loading ? 'Searching...' : 'Search'}
          </button>
          {error ? <p className="error">{error}</p> : null}
        </div>
      </header>

      <section className="results">
        <div className="results-header">
          <h2>Results</h2>
          <button
            className="ghost export-button"
            onClick={exportSelected}
            disabled={!selectedFactorIds.length}
          >
            Export CSV
          </button>
        </div>
        {loading ? (
          <div className="progress">
            <div className="progress-bar" role="progressbar" aria-label="Loading AP-42 factors" />
            <span>Loading AP-42 factors...</span>
          </div>
        ) : null}
        <div className="meta-row">
          <span>
            WebFIRE accessed: {lastFetchedAt ? new Date(lastFetchedAt).toLocaleString() : '-'}
          </span>
          <span>
            Latest record update: {latestRecordUpdate ? new Date(latestRecordUpdate).toLocaleDateString() : '-'}
          </span>
          <span className="note">Revoked factors appear in red italics.</span>
        </div>
        <div className="pollutant-filter">
          <div>
            <label>
              Filter pollutants
              <input
                value={pollutantFilter}
                onChange={(event) => setPollutantFilter(event.target.value)}
                placeholder="Search pollutants"
              />
            </label>
          </div>
          <div className="pollutant-actions">
            <button
              className="ghost"
              onClick={selectAllVisible}
              disabled={!columnFilteredResults.length}
            >
              Select all
            </button>
            <button className="ghost" onClick={clearSelection} disabled={!selectedFactorIds.length}>
              Clear
            </button>
          </div>
        </div>
        {exportError ? <p className="error">{exportError}</p> : null}
        <div className="table">
          <div className="table-row table-head ap42-row">
            <span>Select</span>
            <span>SCC</span>
            <span>Pollutant</span>
            <span>Factor</span>
            <span>Unit</span>
            <span>Per Activity</span>
            <span>Quality</span>
            <span>SCC Text</span>
          </div>
          <div className="table-row table-filters ap42-row">
            <span></span>
            <span>
              <input
                value={columnFilters.scc}
                onChange={(event) => setColumnFilters({ ...columnFilters, scc: event.target.value })}
                placeholder="Filter SCC"
              />
            </span>
            <span>
              <input
                list="pollutant-list"
                value={columnFilters.pollutant}
                onChange={(event) =>
                  setColumnFilters({ ...columnFilters, pollutant: event.target.value })
                }
                placeholder="Filter pollutant"
              />
            </span>
            <span>
              <input
                value={columnFilters.factor}
                onChange={(event) => setColumnFilters({ ...columnFilters, factor: event.target.value })}
                placeholder="Filter factor"
              />
            </span>
            <span>
              <input
                list="unit-list"
                value={columnFilters.unit}
                onChange={(event) => setColumnFilters({ ...columnFilters, unit: event.target.value })}
                placeholder="Filter unit"
              />
            </span>
            <span>
              <input
                list="activity-list"
                value={columnFilters.activity}
                onChange={(event) =>
                  setColumnFilters({ ...columnFilters, activity: event.target.value })
                }
                placeholder="Filter activity"
              />
            </span>
            <span>
              <input
                list="quality-list"
                value={columnFilters.quality}
                onChange={(event) => setColumnFilters({ ...columnFilters, quality: event.target.value })}
                placeholder="Filter quality"
              />
            </span>
            <span>
              <input
                value={columnFilters.scctext}
                onChange={(event) =>
                  setColumnFilters({ ...columnFilters, scctext: event.target.value })
                }
                placeholder="Filter text"
              />
            </span>
          </div>
          <datalist id="pollutant-list">
            {uniqueOptions.pollutant.map((item) => (
              <option key={item} value={item} />
            ))}
          </datalist>
          <datalist id="unit-list">
            {uniqueOptions.unit.map((item) => (
              <option key={item} value={item} />
            ))}
          </datalist>
          <datalist id="activity-list">
            {uniqueOptions.activity.map((item) => (
              <option key={item} value={item} />
            ))}
          </datalist>
          <datalist id="quality-list">
            {uniqueOptions.quality.map((item) => (
              <option key={item} value={item} />
            ))}
          </datalist>
          {columnFilteredResults.map((item) => (
            <div
              key={`${item.factorid}-${item.pollutant}`}
              className={`table-row ap42-row${item.factor_status === 'Revoked' ? ' revoked' : ''}`}
            >
              <span>
                {item.factorid ? (
                  <input
                    type="checkbox"
                    checked={selectedFactorIds.includes(item.factorid)}
                    onChange={() => toggleSelection(item.factorid as number | string)}
                  />
                ) : null}
              </span>
              <span>{item.scc}</span>
              <span>{item.pollutant}</span>
              <span>
                <button className="link-button" type="button" onClick={() => setDetailItem(item)}>
                  {item.factor_text ?? item.factor}
                </button>
              </span>
              <span>{item.unit}</span>
              <span>{item.activity}</span>
              <span>{item.quality}</span>
              <span>{item.scctext}</span>
            </div>
          ))}
          {!columnFilteredResults.length && !loading ? (
            <div className={hasSearched ? 'error' : 'empty'}>
              {hasSearched
                ? 'WebFIRE does not contain any emissions factors for this AP-42 section.'
                : 'No results yet. Choose an AP-42 section to search.'}
            </div>
          ) : null}
        </div>
      </section>

      {detailItem ? (
        <FactorDetailModal detailItem={detailItem} onClose={() => setDetailItem(null)} />
      ) : null}
    </div>
  );
}
