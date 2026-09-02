import { useState } from 'react';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Table from '@cloudscape-design/components/table';
import Button from '@cloudscape-design/components/button';
import Pagination from '@cloudscape-design/components/pagination';
import TextFilter from '@cloudscape-design/components/text-filter';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import SpaceBetween from '@cloudscape-design/components/space-between';
import { useCollection } from '@cloudscape-design/collection-hooks';

interface SecurityGroup {
  id: string;
  name: string;
  vpcId: string;
  inboundRules: number;
  outboundRules: number;
  status: 'active' | 'unused';
  createdAt: string;
}

const GROUPS: SecurityGroup[] = Array.from({ length: 28 }, (_, i) => ({
  id: `sg-${String(i + 1).padStart(4, '0')}`,
  name: `${['web', 'db', 'cache', 'bastion'][i % 4]}-sg-${String(i + 1).padStart(2, '0')}`,
  vpcId: `vpc-${String((i % 3) + 1).padStart(4, '0')}`,
  inboundRules: (i * 3) % 12,
  outboundRules: (i * 2) % 8,
  status: i % 6 === 0 ? 'unused' : 'active',
  createdAt: new Date(Date.now() - i * 172_800_000).toISOString(),
}));

const statusType = (s: SecurityGroup['status']) => (s === 'active' ? 'success' : 'stopped');

// Security Groups: the operator's canonical inventory of every security
// group in this account. This page has one job -- list every group, its
// VPC, rule counts, and status, and let an operator pick a batch of
// unused groups and delete them in one action. Nothing on the page
// besides the table.
export const SecurityGroups = () => {
  const [checkedIds, setCheckedIds] = useState<Set<string>>(new Set());

  const { items, collectionProps, filterProps, paginationProps } = useCollection<SecurityGroup>(GROUPS, {
    filtering: {
      empty: 'No security groups',
      noMatch: 'No matching security groups',
    },
    pagination: { pageSize: 10 },
    sorting: {
      defaultState: {
        sortingColumn: { sortingField: 'name' },
      },
    },
  });

  const toggleOne = (id: string, checked: boolean) => {
    setCheckedIds((prev) => {
      const next = new Set(prev);
      if (checked) {
        next.add(id);
      } else {
        next.delete(id);
      }
      return next;
    });
  };

  const toggleAllOnPage = (checked: boolean) => {
    setCheckedIds((prev) => {
      const next = new Set(prev);
      for (const item of items) {
        if (checked) {
          next.add(item.id);
        } else {
          next.delete(item.id);
        }
      }
      return next;
    });
  };

  const allOnPageChecked = items.length > 0 && items.every((item) => checkedIds.has(item.id));

  return (
    <ContentLayout
      header={
        <Header
          variant="h1"
          counter={`(${GROUPS.length})`}
          actions={
            <SpaceBetween direction="horizontal" size="xs">
              <Button disabled={checkedIds.size === 0}>{`Delete selected (${checkedIds.size})`}</Button>
            </SpaceBetween>
          }
        >
          Security groups
        </Header>
      }
    >
      <Table
        {...collectionProps}
        variant="container"
        items={items}
        resizableColumns
        stickyHeader
        trackBy="id"
        ariaLabels={{
          tableLabel: 'Security groups',
        }}
        columnDefinitions={[
          {
            id: 'select',
            header: (
              <input
                type="checkbox"
                aria-label="Select all security groups on this page"
                checked={allOnPageChecked}
                onChange={(e) => toggleAllOnPage(e.target.checked)}
              />
            ),
            minWidth: 40,
            cell: (item) => (
              <input
                type="checkbox"
                aria-label={`Select ${item.name}`}
                checked={checkedIds.has(item.id)}
                onChange={(e) => toggleOne(item.id, e.target.checked)}
              />
            ),
          },
          {
            id: 'name',
            header: 'Name',
            isRowHeader: true,
            minWidth: 150,
            cell: (item) => item.name,
            sortingField: 'name',
          },
          {
            id: 'vpcId',
            header: 'VPC',
            minWidth: 120,
            cell: (item) => item.vpcId,
            sortingField: 'vpcId',
          },
          {
            id: 'inboundRules',
            header: 'Inbound rules',
            minWidth: 120,
            cell: (item) => item.inboundRules,
            sortingField: 'inboundRules',
          },
          {
            id: 'outboundRules',
            header: 'Outbound rules',
            minWidth: 130,
            cell: (item) => item.outboundRules,
            sortingField: 'outboundRules',
          },
          {
            id: 'status',
            header: 'Status',
            minWidth: 110,
            cell: (item) => <StatusIndicator type={statusType(item.status)}>{item.status}</StatusIndicator>,
            sortingField: 'status',
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
            filteringPlaceholder="Find security group"
            filteringAriaLabel="Filter security groups"
          />
        }
        pagination={<Pagination {...paginationProps} />}
        empty="No security groups"
      />
    </ContentLayout>
  );
};
