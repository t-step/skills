import { useState } from 'react';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Table from '@cloudscape-design/components/table';
import CollectionPreferences from '@cloudscape-design/components/collection-preferences';
import Pagination from '@cloudscape-design/components/pagination';
import TextFilter from '@cloudscape-design/components/text-filter';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import Button from '@cloudscape-design/components/button';
import { useCollection } from '@cloudscape-design/collection-hooks';

interface FleetNode {
  id: string;
  status: 'in-service' | 'draining' | 'unhealthy';
  region: string;
  instanceType: string;
  cpuUtilization: number;
  memoryUtilization: number;
  launchedAt: string;
}

const NODES: FleetNode[] = Array.from({ length: 24 }, (_, i) => ({
  id: `fleet-node-${String(i + 1).padStart(3, '0')}`,
  status: i % 11 === 0 ? 'unhealthy' : i % 5 === 0 ? 'draining' : 'in-service',
  region: ['us-east-1', 'us-west-2', 'eu-west-1'][i % 3],
  instanceType: ['m6i.xlarge', 'm6i.2xlarge', 'c6i.xlarge'][i % 3],
  cpuUtilization: 20 + ((i * 7) % 70),
  memoryUtilization: 15 + ((i * 11) % 75),
  launchedAt: new Date(Date.now() - i * 86_400_000).toISOString(),
}));

const statusType = (s: FleetNode['status']) =>
  s === 'in-service' ? 'success' : s === 'draining' ? 'in-progress' : 'error';

// Fleet Nodes: the operator's canonical inventory of every compute node
// backing the inference fleet. This page has one job -- list every node,
// its health, and its utilization, so an operator can scan for unhealthy
// or over/under-utilized capacity. Nothing on the page besides the table.
export const FleetNodes = () => {
  const [preferences, setPreferences] = useState({
    pageSize: 10,
    wrapLines: false,
  });

  const { items, collectionProps, filterProps, paginationProps } = useCollection<FleetNode>(NODES, {
    filtering: {
      empty: 'No fleet nodes',
      noMatch: 'No matching fleet nodes',
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
        <Header variant="h1" counter={`(${NODES.length})`}>
          Fleet nodes
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
          tableLabel: 'Fleet nodes',
        }}
        columnDefinitions={[
          {
            id: 'id',
            header: 'Node ID',
            isRowHeader: true,
            minWidth: 170,
            cell: (item) => item.id,
            sortingField: 'id',
          },
          {
            id: 'status',
            header: 'Status',
            minWidth: 130,
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
            id: 'instanceType',
            header: 'Instance type',
            minWidth: 140,
            cell: (item) => item.instanceType,
            sortingField: 'instanceType',
          },
          {
            id: 'cpu',
            header: 'CPU utilization',
            minWidth: 140,
            cell: (item) => `${item.cpuUtilization}%`,
            sortingField: 'cpuUtilization',
          },
          {
            id: 'memory',
            header: 'Memory utilization',
            minWidth: 150,
            cell: (item) => `${item.memoryUtilization}%`,
            sortingField: 'memoryUtilization',
          },
          {
            id: 'launchedAt',
            header: 'Launched',
            minWidth: 170,
            cell: (item) => new Date(item.launchedAt).toLocaleString(),
            sortingField: 'launchedAt',
          },
          {
            id: 'actions',
            header: 'Actions',
            minWidth: 110,
            cell: () => (
              <Button variant="inline-link" iconName="external">
                Console
              </Button>
            ),
          },
        ]}
        filter={
          <TextFilter
            {...filterProps}
            filteringPlaceholder="Find fleet node"
            filteringAriaLabel="Filter fleet nodes"
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
                { value: 10, label: '10 nodes' },
                { value: 20, label: '20 nodes' },
              ],
            }}
            wrapLinesPreference={{
              label: 'Wrap lines',
              description: 'Wrap long values instead of truncating.',
            }}
          />
        }
        empty="No fleet nodes"
      />
    </ContentLayout>
  );
};
