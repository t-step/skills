import { useState } from 'react';
import Header from '@cloudscape-design/components/header';
import Table from '@cloudscape-design/components/table';
import Button from '@cloudscape-design/components/button';
import Modal from '@cloudscape-design/components/modal';
import KeyValuePairs from '@cloudscape-design/components/key-value-pairs';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Box from '@cloudscape-design/components/box';

interface QuotaRequest {
  id: string;
  quotaName: string;
  currentValue: number;
  requestedValue: number;
  region: string;
  requester: string;
  submittedAt: string;
  status: 'pending' | 'approved' | 'denied';
}

const REQUESTS: QuotaRequest[] = [
  {
    id: 'req-1',
    quotaName: 'Concurrent inference endpoints',
    currentValue: 20,
    requestedValue: 50,
    region: 'us-east-1',
    requester: 'priya@example.com',
    submittedAt: '2026-08-28',
    status: 'pending',
  },
  {
    id: 'req-2',
    quotaName: 'GPU instances per account',
    currentValue: 8,
    requestedValue: 16,
    region: 'us-west-2',
    requester: 'sam@example.com',
    submittedAt: '2026-08-20',
    status: 'approved',
  },
  {
    id: 'req-3',
    quotaName: 'Model registry entries',
    currentValue: 100,
    requestedValue: 250,
    region: 'eu-west-1',
    requester: 'jules@example.com',
    submittedAt: '2026-08-15',
    status: 'denied',
  },
];

const statusType = (s: QuotaRequest['status']) =>
  s === 'approved' ? 'success' : s === 'pending' ? 'in-progress' : 'error';

// Quota Requests: a log of quota-increase requests filed against this
// account. Selecting a row opens a modal with the request's full detail
// (current/requested value, region, requester, submission date, status)
// and, for pending requests, a single action to withdraw the request.
// Nothing else in the app links to an individual request; there is no
// per-request route.
export const QuotaRequests = () => {
  const [openRequest, setOpenRequest] = useState<QuotaRequest | undefined>();

  return (
    <>
      <Table
        variant="full-page"
        items={REQUESTS}
        trackBy="id"
        resizableColumns
        ariaLabels={{ tableLabel: 'Quota requests' }}
        header={
          <Header variant="h1" counter={`(${REQUESTS.length})`}>
            Quota requests
          </Header>
        }
        columnDefinitions={[
          { id: 'quotaName', header: 'Quota', isRowHeader: true, minWidth: 220, cell: (r) => r.quotaName },
          { id: 'region', header: 'Region', minWidth: 120, cell: (r) => r.region },
          {
            id: 'status',
            header: 'Status',
            minWidth: 130,
            cell: (r) => <StatusIndicator type={statusType(r.status)}>{r.status}</StatusIndicator>,
          },
          { id: 'submittedAt', header: 'Submitted', minWidth: 130, cell: (r) => r.submittedAt },
          {
            id: 'actions',
            header: 'Actions',
            minWidth: 110,
            cell: (r) => (
              <Button variant="inline-link" onClick={() => setOpenRequest(r)}>
                View
              </Button>
            ),
          },
        ]}
        empty="No quota requests"
      />

      {openRequest && (
        <Modal
          visible
          header={openRequest.quotaName}
          onDismiss={() => setOpenRequest(undefined)}
          closeAriaLabel="Close"
          footer={
            <Box float="right">
              <SpaceBetween direction="horizontal" size="xs">
                {openRequest.status === 'pending' && <Button>Withdraw request</Button>}
                <Button variant="primary" onClick={() => setOpenRequest(undefined)}>
                  Close
                </Button>
              </SpaceBetween>
            </Box>
          }
        >
          <KeyValuePairs
            columns={2}
            items={[
              { label: 'Current value', value: openRequest.currentValue },
              { label: 'Requested value', value: openRequest.requestedValue },
              { label: 'Region', value: openRequest.region },
              { label: 'Requester', value: openRequest.requester },
              { label: 'Submitted', value: openRequest.submittedAt },
              { label: 'Status', value: <StatusIndicator type={statusType(openRequest.status)}>{openRequest.status}</StatusIndicator> },
            ]}
          />
        </Modal>
      )}
    </>
  );
};
