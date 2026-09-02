import { useState } from 'react';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Button from '@cloudscape-design/components/button';
import Table from '@cloudscape-design/components/table';
import CollectionPreferences from '@cloudscape-design/components/collection-preferences';
import Pagination from '@cloudscape-design/components/pagination';
import TextFilter from '@cloudscape-design/components/text-filter';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import { useCollection } from '@cloudscape-design/collection-hooks';

interface Endpoint {
  id: string;
  status: 'in-service' | 'updating' | 'failed';
  region: string;
  model: string;
  requestsPerSecond: number;
  lastDeployed: string;
}

const ENDPOINTS: Endpoint[] = Array.from({ length: 26 }, (_, i) => ({
  id: `endpoint-${String(i + 1).padStart(3, '0')}`,
  status: i % 12 === 0 ? 'failed' : i % 6 === 0 ? 'updating' : 'in-service',
  region: ['us-east-1', 'us-west-2', 'eu-west-1'][i % 3],
  model: ['claude-sonnet', 'claude-haiku', 'claude-opus'][i % 3],
  requestsPerSecond: 5 + ((i * 13) % 400),
  lastDeployed: new Date(Date.now() - i * 43_200_000).toISOString(),
}));

const statusType = (s: Endpoint['status']) =>
  s === 'in-service' ? 'success' : s === 'updating' ? 'in-progress' : 'error';

export const Endpoints = () => {
  const [preferences, setPreferences] = useState({
    pageSize: 10,
    wrapLines: false,
  });

  const { items, collectionProps, filterProps, paginationProps } = useCollection<Endpoint>(ENDPOINTS, {
    filtering: {
      empty: 'No endpoints',
      noMatch: 'No matching endpoints',
    },
    pagination: { pageSize: preferences.pageSize },
    sorting: {
      defaultState: {
        sortingColumn: { sortingField: 'id' },
      },
    },
  });

  return (
    <ContentLayout
      header={
        <Header
          variant="h1"
          counter={`(${ENDPOINTS.length})`}
          description="Endpoints receiving traffic for model invocations across this account."
          actions={<Button variant="primary">Create endpoint</Button>}
        >
          Endpoints
        </Header>
      }
    >
      <Table
        {...collectionProps}
        variant="container"
        items={items}
        wrapLines={preferences.wrapLines}
        resizableColumns
        stickyHeader
        trackBy="id"
        ariaLabels={{
          tableLabel: 'Endpoints',
        }}
        columnDefinitions={[
          {
            id: 'id',
            header: 'Endpoint ID',
            isRowHeader: true,
            minWidth: 160,
            cell: (item) => item.id,
            sortingField: 'id',
          },
          {
            id: 'status',
            header: 'Status',
            minWidth: 120,
            cell: (item) => <StatusIndicator type={statusType(item.status)}>{item.status}</StatusIndicator>,
            sortingField: 'status',
          },
          {
            id: 'region',
            header: 'Region',
            minWidth: 120,
            cell: (item) => item.region,
            sortingField: 'region',
          },
          {
            id: 'model',
            header: 'Model',
            minWidth: 140,
            cell: (item) => item.model,
            sortingField: 'model',
          },
          {
            id: 'requestsPerSecond',
            header: 'Requests/sec',
            minWidth: 130,
            cell: (item) => item.requestsPerSecond,
            sortingField: 'requestsPerSecond',
          },
          {
            id: 'lastDeployed',
            header: 'Last deployed',
            minWidth: 170,
            cell: (item) => new Date(item.lastDeployed).toLocaleString(),
            sortingField: 'lastDeployed',
          },
        ]}
        filter={
          <TextFilter
            {...filterProps}
            filteringPlaceholder="Find endpoint"
            filteringAriaLabel="Filter endpoints"
          />
        }
        pagination={<Pagination {...paginationProps} />}
        preferences={
          <CollectionPreferences
            title="Preferences"
            confirmLabel="Confirm"
            cancelLabel="Cancel"
            preferences={preferences}
            onConfirm={({ detail }) =>
              setPreferences({
                pageSize: detail.pageSize ?? preferences.pageSize,
                wrapLines: Boolean(detail.wrapLines),
              })
            }
            pageSizePreference={{
              title: 'Page size',
              options: [
                { value: 10, label: '10 endpoints' },
                { value: 20, label: '20 endpoints' },
              ],
            }}
            wrapLinesPreference={{
              label: 'Wrap lines',
              description: 'Wrap long values instead of truncating.',
            }}
          />
        }
        empty="No endpoints"
      />
    </ContentLayout>
  );
};
