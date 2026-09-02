import { useState } from 'react';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Table from '@cloudscape-design/components/table';
import CollectionPreferences from '@cloudscape-design/components/collection-preferences';
import Pagination from '@cloudscape-design/components/pagination';
import TextFilter from '@cloudscape-design/components/text-filter';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import { useCollection } from '@cloudscape-design/collection-hooks';

interface StorageVolume {
  id: string;
  status: 'attached' | 'available' | 'error';
  sizeGb: number;
  throughputMbps: number;
  attachedInstance: string;
  createdAt: string;
}

const VOLUMES: StorageVolume[] = Array.from({ length: 28 }, (_, i) => ({
  id: `vol-${String(i + 1).padStart(4, '0')}`,
  status: i % 13 === 0 ? 'error' : i % 4 === 0 ? 'available' : 'attached',
  sizeGb: [100, 250, 500, 1000][i % 4],
  throughputMbps: 125 + ((i * 17) % 500),
  attachedInstance: i % 4 === 0 ? '-' : `instance-${String((i % 9) + 1).padStart(3, '0')}`,
  createdAt: new Date(Date.now() - i * 172_800_000).toISOString(),
}));

const statusType = (s: StorageVolume['status']) =>
  s === 'attached' ? 'success' : s === 'available' ? 'pending' : 'error';

// Storage Volumes: the operator's canonical inventory of every block
// storage volume provisioned in this account. This page has one job --
// list every volume, its status, size, throughput, and attachment, so an
// operator can audit capacity and find unattached or errored volumes.
// Nothing on the page besides the table.
export const StorageVolumes = () => {
  const [preferences, setPreferences] = useState({
    pageSize: 10,
    wrapLines: false,
  });

  const { items, collectionProps, filterProps, paginationProps } = useCollection<StorageVolume>(VOLUMES, {
    filtering: {
      empty: 'No storage volumes',
      noMatch: 'No matching storage volumes',
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
        <Header variant="h1" counter={`(${VOLUMES.length})`}>
          Storage volumes
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
          tableLabel: 'Storage volumes',
        }}
        columnDefinitions={[
          {
            id: 'id',
            header: 'Volume ID',
            isRowHeader: true,
            minWidth: 150,
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
            id: 'sizeGb',
            header: 'Size (GB)',
            minWidth: 110,
            cell: (item) => item.sizeGb,
            sortingField: 'sizeGb',
          },
          {
            id: 'throughputMbps',
            header: 'Throughput (MB/s)',
            minWidth: 150,
            cell: (item) => item.throughputMbps,
            sortingField: 'throughputMbps',
          },
          {
            id: 'attachedInstance',
            header: 'Attached instance',
            minWidth: 160,
            cell: (item) => item.attachedInstance,
            sortingField: 'attachedInstance',
          },
          {
            id: 'createdAt',
            header: 'Created',
            minWidth: 170,
            cell: (item) => new Date(item.createdAt).toLocaleString(),
            sortingField: 'createdAt',
          },
        ]}
        filter={
          <TextFilter
            {...filterProps}
            filteringPlaceholder="Find storage volume"
            filteringAriaLabel="Filter storage volumes"
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
                { value: 10, label: '10 volumes' },
                { value: 20, label: '20 volumes' },
              ],
            }}
            wrapLinesPreference={{
              label: 'Wrap lines',
              description: 'Wrap long values instead of truncating.',
            }}
          />
        }
        empty="No storage volumes"
      />
    </ContentLayout>
  );
};
