import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Button from '@cloudscape-design/components/button';
import Table from '@cloudscape-design/components/table';
import Pagination from '@cloudscape-design/components/pagination';
import TextFilter from '@cloudscape-design/components/text-filter';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import { useCollection } from '@cloudscape-design/collection-hooks';

interface ApiKey {
  id: string;
  label: string;
  status: 'active' | 'revoked';
  createdAt: string;
}

const KEYS: ApiKey[] = [
  { id: 'sk-••••7f3a', label: 'CI pipeline', status: 'active', createdAt: '2026-02-11T09:00:00.000Z' },
  { id: 'sk-••••1c9d', label: 'Staging integration', status: 'active', createdAt: '2026-03-02T09:00:00.000Z' },
  { id: 'sk-••••44be', label: 'Local dev (thomas)', status: 'active', createdAt: '2026-04-18T09:00:00.000Z' },
  { id: 'sk-••••90aa', label: 'Legacy webhook relay', status: 'revoked', createdAt: '2025-11-05T09:00:00.000Z' },
  { id: 'sk-••••2e77', label: 'Analytics export job', status: 'active', createdAt: '2026-05-27T09:00:00.000Z' },
  { id: 'sk-••••b031', label: 'Partner sandbox', status: 'active', createdAt: '2026-06-14T09:00:00.000Z' },
  { id: 'sk-••••5d6c', label: 'One-off migration script', status: 'revoked', createdAt: '2026-01-09T09:00:00.000Z' },
  { id: 'sk-••••f812', label: 'Support tooling', status: 'active', createdAt: '2026-07-30T09:00:00.000Z' },
];

// API keys settings page: lets a service owner see and manage the small
// set of API keys their own integrations use, and create new ones. Keys
// are provisioned rarely (this account has created eight in its
// lifetime) -- this is a settings surface, not an operational fleet
// inventory.
export const ApiKeys = () => {
  const { items, collectionProps, filterProps, paginationProps } = useCollection<ApiKey>(KEYS, {
    filtering: {
      empty: 'No API keys',
      noMatch: 'No matching API keys',
    },
    pagination: { pageSize: 10 },
    sorting: {
      defaultState: {
        sortingColumn: { sortingField: 'createdAt' },
      },
    },
  });

  return (
    <ContentLayout
      header={
        <Header
          variant="h1"
          counter={`(${KEYS.length})`}
          description="Manage the API keys your integrations use to call this service. Revoke a key immediately if it may have been exposed."
          actions={<Button variant="primary">Create API key</Button>}
        >
          API keys
        </Header>
      }
    >
      <Table
        {...collectionProps}
        variant="container"
        items={items}
        resizableColumns
        trackBy="id"
        ariaLabels={{
          tableLabel: 'API keys',
        }}
        columnDefinitions={[
          {
            id: 'label',
            header: 'Label',
            isRowHeader: true,
            minWidth: 200,
            cell: (item) => item.label,
            sortingField: 'label',
          },
          {
            id: 'id',
            header: 'Key',
            minWidth: 140,
            cell: (item) => item.id,
          },
          {
            id: 'status',
            header: 'Status',
            minWidth: 110,
            cell: (item) => (
              <StatusIndicator type={item.status === 'active' ? 'success' : 'stopped'}>
                {item.status}
              </StatusIndicator>
            ),
            sortingField: 'status',
          },
          {
            id: 'createdAt',
            header: 'Created',
            minWidth: 170,
            cell: (item) => new Date(item.createdAt).toLocaleDateString(),
            sortingField: 'createdAt',
          },
        ]}
        filter={
          <TextFilter
            {...filterProps}
            filteringPlaceholder="Find API key"
            filteringAriaLabel="Filter API keys"
          />
        }
        pagination={<Pagination {...paginationProps} />}
        empty="No API keys"
      />
    </ContentLayout>
  );
};
