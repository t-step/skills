import { useNavigate } from 'react-router';
import Header from '@cloudscape-design/components/header';
import Table from '@cloudscape-design/components/table';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import Button from '@cloudscape-design/components/button';
import Pagination from '@cloudscape-design/components/pagination';
import TextFilter from '@cloudscape-design/components/text-filter';
import { useCollection } from '@cloudscape-design/collection-hooks';

interface Certificate {
  id: string;
  domain: string;
  status: 'issued' | 'expiring-soon' | 'expired';
  expiresAt: string;
  issuedBy: string;
}

const CERTIFICATES: Certificate[] = [
  { id: 'cert-1', domain: 'api.example.com', status: 'issued', expiresAt: '2027-03-01', issuedBy: 'Amazon' },
  { id: 'cert-2', domain: 'app.example.com', status: 'expiring-soon', expiresAt: '2026-09-20', issuedBy: 'Amazon' },
  { id: 'cert-3', domain: 'cdn.example.com', status: 'issued', expiresAt: '2027-01-15', issuedBy: 'Amazon' },
  { id: 'cert-4', domain: 'legacy.example.com', status: 'expired', expiresAt: '2026-06-01', issuedBy: 'DigiCert' },
];

const statusType = (s: Certificate['status']) =>
  s === 'issued' ? 'success' : s === 'expiring-soon' ? 'warning' : 'error';

// Certificates: the fleet of TLS certificates this account manages. Each
// certificate is a real, addressable, long-lived resource with its own
// lifecycle -- domains it covers, load balancers it's attached to, and a
// renewal history -- so "view details" navigates to that certificate's
// own full details page (CertificateDetails.tsx), not a modal or panel.
export const CertificatesTable = () => {
  const navigate = useNavigate();
  const { items, collectionProps, filterProps, paginationProps } = useCollection<Certificate>(CERTIFICATES, {
    filtering: { empty: 'No certificates', noMatch: 'No matching certificates' },
    pagination: { pageSize: 10 },
    sorting: { defaultState: { sortingColumn: { sortingField: 'expiresAt' } } },
  });

  return (
    <Table
      {...collectionProps}
      variant="full-page"
      items={items}
      resizableColumns
      stickyHeader
      trackBy="id"
      ariaLabels={{ tableLabel: 'Certificates' }}
      header={
        <Header variant="h1" counter={`(${CERTIFICATES.length})`}>
          Certificates
        </Header>
      }
      columnDefinitions={[
        { id: 'domain', header: 'Domain', isRowHeader: true, minWidth: 200, cell: (c) => c.domain, sortingField: 'domain' },
        {
          id: 'status',
          header: 'Status',
          minWidth: 140,
          cell: (c) => <StatusIndicator type={statusType(c.status)}>{c.status}</StatusIndicator>,
          sortingField: 'status',
        },
        { id: 'expiresAt', header: 'Expires', minWidth: 130, cell: (c) => c.expiresAt, sortingField: 'expiresAt' },
        { id: 'issuedBy', header: 'Issued by', minWidth: 130, cell: (c) => c.issuedBy },
        {
          id: 'actions',
          header: 'Actions',
          minWidth: 130,
          cell: (c) => (
            <Button variant="inline-link" onClick={() => navigate(`/certificates/${c.id}`)}>
              View details
            </Button>
          ),
        },
      ]}
      filter={<TextFilter {...filterProps} filteringAriaLabel="Filter certificates" filteringPlaceholder="Find certificate" />}
      pagination={<Pagination {...paginationProps} />}
      empty="No certificates"
    />
  );
};
