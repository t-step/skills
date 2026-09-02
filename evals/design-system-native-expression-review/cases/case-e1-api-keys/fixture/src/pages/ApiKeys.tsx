import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Table from '@cloudscape-design/components/table';
import TextFilter from '@cloudscape-design/components/text-filter';
import Pagination from '@cloudscape-design/components/pagination';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import { useCollection } from '@cloudscape-design/collection-hooks';

interface ApiKey {
  id: string;
  name: string;
  environment: 'production' | 'staging';
  status: 'active' | 'revoked';
  createdAt: string;
}

const API_KEYS: ApiKey[] = Array.from({ length: 16 }, (_, i) => ({
  id: `key-${String(i + 1).padStart(2, '0')}`,
  name: `${['billing', 'search', 'ingest', 'reporting'][i % 4]}-key-${String(i + 1).padStart(2, '0')}`,
  environment: i % 2 === 0 ? 'production' : 'staging',
  status: i % 6 === 0 ? 'revoked' : 'active',
  createdAt: `2026-0${(i % 8) + 1}-${String((i % 27) + 1).padStart(2, '0')}`,
}));

const statusType = (s: ApiKey['status']) => (s === 'active' ? 'success' : 'stopped');

export const ApiKeys = () => {
  const { items, collectionProps, filterProps, paginationProps } = useCollection<ApiKey>(API_KEYS, {
    filtering: {
      empty: 'No API keys',
      noMatch: 'No matching API keys',
    },
    pagination: { pageSize: 10 },
    sorting: {},
  });

  return (
    <ContentLayout
      header={
        <Header variant="h1" counter={`(${API_KEYS.length})`} description="Manage API keys for this account.">
          API keys
        </Header>
      }
    >
      <Table
        {...collectionProps}
        items={items}
        trackBy="id"
        columnDefinitions={[
          {
            id: 'name',
            header: 'Name',
            cell: (item) => item.name,
            sortingField: 'name',
          },
          {
            id: 'environment',
            header: 'Environment',
            cell: (item) => item.environment,
          },
          {
            id: 'status',
            header: 'Status',
            cell: (item) => <StatusIndicator type={statusType(item.status)}>{item.status}</StatusIndicator>,
          },
          {
            id: 'createdAt',
            header: 'Created',
            cell: (item) => item.createdAt,
            sortingField: 'createdAt',
          },
        ]}
        filter={
          <TextFilter {...filterProps} filteringPlaceholder="Find API key" filteringAriaLabel="Filter API keys" />
        }
        pagination={<Pagination {...paginationProps} />}
        variant="borderless"
        empty="No API keys"
      />
    </ContentLayout>
  );
};
