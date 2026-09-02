import { useState } from 'react';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import BreadcrumbGroup from '@cloudscape-design/components/breadcrumb-group';
import Tabs from '@cloudscape-design/components/tabs';
import Table from '@cloudscape-design/components/table';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Button from '@cloudscape-design/components/button';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import List from '@cloudscape-design/components/list';

interface Member {
  name: string;
  email: string;
  role: 'owner' | 'editor' | 'viewer';
}

const MEMBERS: Member[] = [
  { name: 'Priya Nair', email: 'priya@example.com', role: 'owner' },
  { name: 'Sam Okafor', email: 'sam@example.com', role: 'editor' },
  { name: 'Jules Renard', email: 'jules@example.com', role: 'viewer' },
];

const ACTIVITY = [
  'Priya Nair updated the workspace plan to Team (2 hours ago)',
  'Sam Okafor invited jules@example.com (yesterday)',
  'Workspace created (14 days ago)',
];

// A single workspace's details -- name, owner, region, plan tier, created
// date, and status are the workspace's own general configuration facts:
// stable, read-mostly, and relevant no matter which tab a user is
// currently looking at (Members or Activity). Tabs organize the rest.
export const WorkspaceDetails = () => {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <ContentLayout
      header={
        <>
          <BreadcrumbGroup
            items={[
              { text: 'Workspaces', href: '/workspaces' },
              { text: 'eng-platform-prod', href: '#' },
            ]}
            ariaLabel="Breadcrumbs"
          />
          <Header
            variant="h1"
            actions={
              <SpaceBetween direction="horizontal" size="xs">
                <Button>Edit</Button>
                <Button>Delete</Button>
              </SpaceBetween>
            }
          >
            eng-platform-prod
          </Header>
        </>
      }
    >
      <Tabs
        activeTabId={activeTab}
        onChange={({ detail }) => setActiveTab(detail.activeTabId)}
        tabs={[
          {
            id: 'overview',
            label: 'Overview',
            content: (
              // General configuration -- name, owner, region, plan tier,
              // created date, status -- rendered here, one property per
              // column, one row per workspace (there is exactly one).
              <Table
                columnDefinitions={[
                  { id: 'name', header: 'Name', cell: () => 'eng-platform-prod' },
                  { id: 'owner', header: 'Owner', cell: () => 'Priya Nair' },
                  { id: 'region', header: 'Region', cell: () => 'us-east-1' },
                  { id: 'plan', header: 'Plan', cell: () => 'Team' },
                  { id: 'created', header: 'Created', cell: () => 'Jan 12, 2026' },
                  {
                    id: 'status',
                    header: 'Status',
                    cell: () => <StatusIndicator type="success">Active</StatusIndicator>,
                  },
                ]}
                items={[{}]}
                trackBy={() => 'workspace-overview-row'}
                ariaLabels={{ tableLabel: 'Workspace general configuration' }}
              />
            ),
          },
          {
            id: 'members',
            label: 'Members',
            content: (
              <Table<Member>
                columnDefinitions={[
                  { id: 'name', header: 'Name', cell: (m) => m.name, isRowHeader: true },
                  { id: 'email', header: 'Email', cell: (m) => m.email },
                  { id: 'role', header: 'Role', cell: (m) => m.role },
                ]}
                items={MEMBERS}
                trackBy="email"
                ariaLabels={{ tableLabel: 'Workspace members' }}
                empty="No members"
              />
            ),
          },
          {
            id: 'activity',
            label: 'Activity',
            content: (
              <List
                items={ACTIVITY}
                renderItem={(entry, index) => ({ id: `activity-${index}`, content: entry })}
              />
            ),
          },
        ]}
      />
    </ContentLayout>
  );
};
