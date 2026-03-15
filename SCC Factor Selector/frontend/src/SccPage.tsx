import { useEffect, useMemo, useRef, useState } from 'react';
import {
  exportBulk,
  fetchHierarchy,
  fetchSccCodeMatches,
  fetchSccMatches,
  fetchSectors,
  searchFactors
} from './api';
import FactorDetailModal from './FactorDetailModal';
import { CartItem, SccCodeMatch, SccMatch, SccSector, WebFireResult } from './types';

const defaultScc = '30302388';

export default function SccPage() {
  const [scc, setScc] = useState(defaultScc);
  const [rawQuery, setRawQuery] = useState('');
  const [rawMatches, setRawMatches] = useState<SccCodeMatch[]>([]);
  const [rawLoading, setRawLoading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState<WebFireResult[]>([]);
  const [sectors, setSectors] = useState<SccSector[]>([]);
  const [sector, setSector] = useState('');
  const [level1, setLevel1] = useState('');
  const [level2, setLevel2] = useState('');
  const [level3, setLevel3] = useState('');
  const [level4, setLevel4] = useState('');
  const [level1Options, setLevel1Options] = useState<string[]>([]);
  const [level2Options, setLevel2Options] = useState<string[]>([]);
  const [level3Options, setLevel3Options] = useState<string[]>([]);
  const [level4Options, setLevel4Options] = useState<string[]>([]);
  const [sccMatches, setSccMatches] = useState<SccMatch[]>([]);
  const [selectedMatch, setSelectedMatch] = useState('');
  const [matchFilter, setMatchFilter] = useState('');
  const [pollutantFilter, setPollutantFilter] = useState('');
  const [selectedPollutants, setSelectedPollutants] = useState<string[]>([]);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [cartError, setCartError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);
  const preserveSelectionRef = useRef(false);
  const [detailItem, setDetailItem] = useState<WebFireResult | null>(null);
  const [lastFetchedAt, setLastFetchedAt] = useState('');
  const [latestRecordUpdate, setLatestRecordUpdate] = useState('');
  const [columnFilters, setColumnFilters] = useState({
    scc: '',
    pollutant: '',
    factor: '',
    unit: '',
    activity: '',
    quality: '',
    scctext: ''
  });

  const clearRawSearch = () => {
    setRawQuery('');
    setRawMatches([]);
  };

  const clearLevelSearch = () => {
    setSector('');
    setLevel1('');
    setLevel2('');
    setLevel3('');
    setLevel4('');
    setLevel1Options([]);
    setLevel2Options([]);
    setLevel3Options([]);
    setLevel4Options([]);
    setSccMatches([]);
    setSelectedMatch('');
    setMatchFilter('');
  };

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
    setLoading(true);
    setError('');
    setHasSearched(true);
    clearRawSearch();
    try {
      const response = await searchFactors({ SCC: scc });
      setResults(response.results);
      setLastFetchedAt(response.fetched_at);
      setLatestRecordUpdate(getLatestRecordUpdate(response.results));
    } catch (err) {
      setError('Failed to load results.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSectors()
      .then(setSectors)
      .catch(() => setSectors([]));
  }, []);

  useEffect(() => {
    const query = rawQuery.trim();
    if (query.length < 2) {
      setRawMatches([]);
      return;
    }
    const timer = window.setTimeout(() => {
      setRawLoading(true);
      fetchSccCodeMatches(query)
        .then(setRawMatches)
        .catch(() => setRawMatches([]))
        .finally(() => setRawLoading(false));
    }, 300);
    return () => window.clearTimeout(timer);
  }, [rawQuery]);

  useEffect(() => {
    setLevel1('');
    setLevel2('');
    setLevel3('');
    setLevel4('');
    setLevel1Options([]);
    setLevel2Options([]);
    setLevel3Options([]);
    setLevel4Options([]);
    setSccMatches([]);
    setSelectedMatch('');
    if (!sector) {
      return;
    }
    fetchHierarchy({ level: 1, sector })
      .then(setLevel1Options)
      .catch(() => setLevel1Options([]));
  }, [sector]);

  useEffect(() => {
    setLevel2('');
    setLevel3('');
    setLevel4('');
    setLevel2Options([]);
    setLevel3Options([]);
    setLevel4Options([]);
    setSccMatches([]);
    setSelectedMatch('');
    if (!sector || !level1) {
      return;
    }
    fetchHierarchy({ level: 2, sector, level1 })
      .then(setLevel2Options)
      .catch(() => setLevel2Options([]));
  }, [sector, level1]);

  useEffect(() => {
    setLevel3('');
    setLevel4('');
    setLevel3Options([]);
    setLevel4Options([]);
    setSccMatches([]);
    setSelectedMatch('');
    if (!sector || !level1 || !level2) {
      return;
    }
    fetchHierarchy({ level: 3, sector, level1, level2 })
      .then(setLevel3Options)
      .catch(() => setLevel3Options([]));
  }, [sector, level1, level2]);

  useEffect(() => {
    setLevel4('');
    setLevel4Options([]);
    setSccMatches([]);
    setSelectedMatch('');
    if (!sector || !level1 || !level2 || !level3) {
      return;
    }
    fetchHierarchy({ level: 4, sector, level1, level2, level3 })
      .then(setLevel4Options)
      .catch(() => setLevel4Options([]));
  }, [sector, level1, level2, level3]);

  useEffect(() => {
    setSccMatches([]);
    setSelectedMatch('');
    setMatchFilter('');
    if (!sector || !level1 || !level2 || !level3 || !level4) {
      return;
    }
    fetchSccMatches({ sector, level1, level2, level3, level4 })
      .then(setSccMatches)
      .catch(() => setSccMatches([]));
  }, [sector, level1, level2, level3, level4]);

  useEffect(() => {
    if (!selectedMatch) {
      return;
    }
    clearRawSearch();
    setScc(selectedMatch);
  }, [selectedMatch]);

  useEffect(() => {
    if (preserveSelectionRef.current) {
      preserveSelectionRef.current = false;
      return;
    }
    setSelectedPollutants([]);
    setPollutantFilter('');
    setColumnFilters({
      scc: '',
      pollutant: '',
      factor: '',
      unit: '',
      activity: '',
      quality: '',
      scctext: ''
    });
  }, [results]);

  const filteredMatches = sccMatches.filter((item) =>
    matchFilter ? item.code.includes(matchFilter.trim()) : true
  );

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

  const visiblePollutants = useMemo(() => {
    const unique = new Set<string>();
    filteredResults.forEach((item) => {
      if (item.pollutant) {
        unique.add(item.pollutant);
      }
    });
    return Array.from(unique).sort((a, b) => a.localeCompare(b));
  }, [filteredResults]);

  const togglePollutant = (name: string) => {
    setSelectedPollutants((prev) =>
      prev.includes(name) ? prev.filter((item) => item !== name) : [...prev, name]
    );
  };

  const addToCart = () => {
    if (!scc.trim()) {
      setCartError('Enter an SCC code before adding to the cart.');
      return;
    }
    setCartError('');
    setCartItems((prev) => {
      const next = prev.filter((item) => item.scc !== scc.trim());
      next.push({ scc: scc.trim(), pollutants: selectedPollutants });
      return next;
    });
  };

  const loadCartItem = async (item: CartItem) => {
    setLoading(true);
    setError('');
    setHasSearched(true);
    try {
      clearRawSearch();
      preserveSelectionRef.current = true;
      const response = await searchFactors({ SCC: item.scc });
      setResults(response.results);
      setLastFetchedAt(response.fetched_at);
      setLatestRecordUpdate(getLatestRecordUpdate(response.results));
      setScc(item.scc);
      setSelectedPollutants(item.pollutants);
      setPollutantFilter('');
    } catch (err) {
      setError('Failed to load results.');
    } finally {
      setLoading(false);
    }
  };

  const removeFromCart = (code: string) => {
    setCartItems((prev) => prev.filter((item) => item.scc !== code));
  };

  const clearCart = () => {
    setCartItems([]);
  };

  const exportCart = async () => {
    if (!cartItems.length) {
      return;
    }
    setCartError('');
    try {
      const response = await exportBulk(cartItems);
      const blob = await response.blob();
      const header = response.headers.get('content-disposition') || '';
      const match = header.match(/filename=([^;]+)/i);
      const filename = match ? match[1].replace(/\"/g, '') : 'webfire_bulk_export.csv';
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setCartError('Bulk export failed. Try again.');
    }
  };

  return (
    <div className="page">
      <header className="hero">
        <div className="hero-content">
          <p className="eyebrow">Internal Emission Factor Tool</p>
          <h1>SCC Factor Selector</h1>
          <p className="lede">
            Search EPA WebFIRE emission factors with caching, history, and CSV export.
          </p>
          <a
            className="external-link"
            href="https://cfpub.epa.gov/webfire/SearchEmissionFactor/searchpage.cfm"
            target="_blank"
            rel="noreferrer"
          >
            Official US EPA WebFIRE Search
          </a>
          <a className="external-link" href="#/ap42">
            Web-Fire AP-42 Section Downloader
          </a>
          <section className="cart">
            <div className="results-header">
              <h2>Bulk Download List</h2>
              <div className="cart-actions">
                <button onClick={exportCart} disabled={!cartItems.length}>
                  Download CSV
                </button>
                <button className="ghost" onClick={clearCart} disabled={!cartItems.length}>
                  Clear list
                </button>
              </div>
            </div>
            {!cartItems.length ? (
              <div className="empty">No SCCs in the list yet.</div>
            ) : (
              <div className="cart-list">
                {cartItems.map((item) => (
                  <div key={item.scc} className="cart-row">
                    <div>
                      <button
                        className="link-button"
                        type="button"
                        onClick={() => loadCartItem(item)}
                      >
                        {item.scc}
                      </button>
                      <span>
                        {item.pollutants.length
                          ? `Pollutants: ${item.pollutants.join(', ')}`
                          : 'Pollutants: all'}
                      </span>
                    </div>
                    <button className="ghost" onClick={() => removeFromCart(item.scc)}>
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
        <div className="card">
          <div className="search-panels">
            <div className="panel">
              <h3>Raw SCC Code Search</h3>
              <label>
                SCC Code Search
                <input
                  value={rawQuery}
                  onChange={(e) => setRawQuery(e.target.value)}
                  placeholder="Type SCC code"
                />
              </label>
              <div className="suggestions">
                {rawLoading ? <div className="empty">Searching...</div> : null}
                {!rawLoading && rawQuery.trim().length >= 2 && !rawMatches.length ? (
                  <div className="empty">No matches found.</div>
                ) : null}
                {rawMatches.map((item) => (
                  <button
                    key={item.code}
                    type="button"
                    className="suggestion"
                    onClick={() => {
                      setScc(item.code);
                      clearLevelSearch();
                      clearRawSearch();
                    }}
                  >
                    <strong>{item.code}</strong>
                    <span>{item.level4 || item.sector || 'Uncategorized'}</span>
                  </button>
                ))}
              </div>
              <label>
                SCC Code
                <input value={scc} onChange={(e) => setScc(e.target.value)} placeholder="Enter SCC" />
              </label>
            </div>
            <div className="panel">
              <h3>SCC Sector & Levels</h3>
              <div className="filters">
                <label>
                  SCC Sector
                  <select value={sector} onChange={(e) => setSector(e.target.value)}>
                    <option value="">Choose sector</option>
                    {sectors.map((item) => (
                      <option key={item.name} value={item.name}>
                        {item.name}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  SCC Level 1
                  <select
                    value={level1}
                    onChange={(e) => setLevel1(e.target.value)}
                    disabled={!sector || !level1Options.length}
                  >
                    <option value="">Choose level 1</option>
                    {level1Options.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  SCC Level 2
                  <select
                    value={level2}
                    onChange={(e) => setLevel2(e.target.value)}
                    disabled={!level1 || !level2Options.length}
                  >
                    <option value="">Choose level 2</option>
                    {level2Options.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  SCC Level 3
                  <select
                    value={level3}
                    onChange={(e) => setLevel3(e.target.value)}
                    disabled={!level2 || !level3Options.length}
                  >
                    <option value="">Choose level 3</option>
                    {level3Options.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  SCC Level 4
                  <select
                    value={level4}
                    onChange={(e) => setLevel4(e.target.value)}
                    disabled={!level3 || !level4Options.length}
                  >
                    <option value="">Choose level 4</option>
                    {level4Options.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  SCC Code Matches
                  <input
                    value={matchFilter}
                    onChange={(e) => setMatchFilter(e.target.value)}
                    placeholder="Filter by partial SCC code"
                    disabled={!sccMatches.length}
                  />
                  <select
                    value={selectedMatch}
                    onChange={(e) => setSelectedMatch(e.target.value)}
                    disabled={!filteredMatches.length}
                  >
                    <option value="">Choose SCC code</option>
                    {filteredMatches.map((item) => (
                      <option key={item.code} value={item.code}>
                        {item.code} {item.level4 ? `- ${item.level4}` : ''}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            </div>
          </div>
          <div className="card-actions">
            <button onClick={addToCart} disabled={!scc.trim() || !filteredResults.length}>
              Add SCC with all pollutants to list
            </button>
            {cartError ? <p className="error">{cartError}</p> : null}
          </div>
          <button onClick={onSearch} disabled={loading || !scc.trim()}>
            {loading ? 'Searching...' : 'Search'}
          </button>
          {error ? <p className="error">{error}</p> : null}
        </div>
      </header>

      <section className="results">
        <div className="results-header">
          <h2>Results</h2>
          <a href={`/api/export?SCC=${encodeURIComponent(scc)}`} className="export">
            Export CSV
          </a>
        </div>
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
                onChange={(e) => setPollutantFilter(e.target.value)}
                placeholder="Search pollutants"
              />
            </label>
          </div>
          <div className="pollutant-actions">
            <button
              className="ghost"
              onClick={() => setSelectedPollutants(visiblePollutants)}
              disabled={!visiblePollutants.length}
            >
              Select all
            </button>
            <button className="ghost" onClick={() => setSelectedPollutants([])}>
              Clear
            </button>
            <button onClick={addToCart} disabled={!scc.trim() || !filteredResults.length}>
              Add SCC to list
            </button>
          </div>
        </div>
        <div className="table">
          <div className="table-row table-head">
            <span>Select</span>
            <span>SCC</span>
            <span>Pollutant</span>
            <span>Factor</span>
            <span>Unit</span>
            <span>Per Activity</span>
            <span>Quality</span>
            <span>SCC Text</span>
          </div>
          <div className="table-row table-filters">
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
              className={`table-row${item.factor_status === 'Revoked' ? ' revoked' : ''}`}
            >
              <span>
                <input
                  type="checkbox"
                  checked={item.pollutant ? selectedPollutants.includes(item.pollutant) : false}
                  onChange={() => item.pollutant && togglePollutant(item.pollutant)}
                />
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
                ? 'WebFIRE does not contain any emissions factors for this SCC.'
                : 'No results yet. Try searching by SCC.'}
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
