import { WebFireResult } from './types';

type FactorDetailModalProps = {
  detailItem: WebFireResult;
  onClose: () => void;
};

export default function FactorDetailModal({ detailItem, onClose }: FactorDetailModalProps) {
  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div className="modal" role="dialog" aria-modal="true" onClick={(event) => event.stopPropagation()}>
        <div className="modal-header">
          <h3>Emission Factor Details</h3>
          <button className="ghost" type="button" onClick={onClose}>
            Close
          </button>
        </div>
        <div className="detail-grid">
          <div>
            <span className="detail-label">SCC</span>
            <span>{detailItem.scc || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Pollutant</span>
            <span>{detailItem.pollutant || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Emission Factor</span>
            <span>{detailItem.factor_text ?? detailItem.factor ?? '-'}</span>
          </div>
          <div>
            <span className="detail-label">Unit</span>
            <span>{detailItem.unit || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Activity</span>
            <span>{detailItem.activity || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Quality</span>
            <span>{detailItem.quality || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Factor Status</span>
            <span>{detailItem.factor_status || '-'}</span>
          </div>
          <div>
            <span className="detail-label">NEI Code</span>
            <span>{detailItem.nei_pollutant_code || '-'}</span>
          </div>
          <div>
            <span className="detail-label">CAS</span>
            <span>{detailItem.cas || '-'}</span>
          </div>
          <div>
            <span className="detail-label">AP-42 Section</span>
            <span>{detailItem.ap42section ?? '-'}</span>
          </div>
          <div>
            <span className="detail-label">Formula</span>
            <span>{detailItem.formula || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Derivation</span>
            <span>{detailItem.derivation || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Applicability</span>
            <span>{detailItem.applicability || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Variable Definition</span>
            <span>{detailItem.variable_definition || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Notes</span>
            <span>{detailItem.notes || '-'}</span>
          </div>
          <div>
            <span className="detail-label">References</span>
            <span>{detailItem.references || detailItem.reference || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Controls</span>
            <span>
              {[
                detailItem.control_1,
                detailItem.control_2,
                detailItem.control_3,
                detailItem.control_4,
                detailItem.control_5
              ]
                .filter(Boolean)
                .join(', ') || '-'}
            </span>
          </div>
          <div>
            <span className="detail-label">SCC Text</span>
            <span>{detailItem.scctext || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Created</span>
            <span>{detailItem.created || '-'}</span>
          </div>
          <div>
            <span className="detail-label">Record Updated</span>
            <span>{detailItem.date_record_updated || '-'}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
