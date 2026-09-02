import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Cards from '@cloudscape-design/components/cards';
import Badge from '@cloudscape-design/components/badge';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import Link from '@cloudscape-design/components/link';

interface Workspace {
  id: string;
  name: string;
  colorTag: 'blue' | 'green' | 'grey' | 'red';
  status: 'active' | 'archived';
  lastOpened: string;
}

const WORKSPACES: Workspace[] = [
  { id: 'ws-1', name: 'eng-platform-prod', colorTag: 'blue', status: 'active', lastOpened: '2 hours ago' },
  { id: 'ws-2', name: 'ml-experiments', colorTag: 'green', status: 'active', lastOpened: 'yesterday' },
  { id: 'ws-3', name: 'design-sandbox', colorTag: 'grey', status: 'active', lastOpened: '3 days ago' },
  { id: 'ws-4', name: 'q3-planning', colorTag: 'red', status: 'archived', lastOpened: '2 weeks ago' },
  { id: 'ws-5', name: 'onboarding-docs', colorTag: 'blue', status: 'active', lastOpened: '4 days ago' },
  { id: 'ws-6', name: 'support-triage', colorTag: 'green', status: 'active', lastOpened: '1 week ago' },
];

// Recent Workspaces: a personal "jump back in" shelf on the user's home
// page. Six workspaces the user has touched recently -- each identified
// by name and a color tag they picked (shown as a small colored badge),
// with a one-click link back in. There is no cross-workspace metric here
// to compare; the task is "recognize the one I want and reopen it."
export const RecentWorkspaces = () => (
  <ContentLayout
    header={
      <Header variant="h1" description="Jump back into a workspace you've recently opened.">
        Recent workspaces
      </Header>
    }
  >
    <Cards
      items={WORKSPACES}
      trackBy="id"
      cardDefinition={{
        header: (item) => <Link href={`/workspaces/${item.id}`}>{item.name}</Link>,
        sections: [
          {
            id: 'tag',
            content: (item) => <Badge color={item.colorTag}>{item.colorTag}</Badge>,
          },
          {
            id: 'status',
            content: (item) => (
              <StatusIndicator type={item.status === 'active' ? 'success' : 'stopped'}>
                {item.status}
              </StatusIndicator>
            ),
          },
          {
            id: 'lastOpened',
            header: 'Last opened',
            content: (item) => item.lastOpened,
          },
        ],
      }}
      cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 2 }, { minWidth: 900, cards: 3 }]}
      empty="No recent workspaces"
    />
  </ContentLayout>
);
