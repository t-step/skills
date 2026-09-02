import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Cards from '@cloudscape-design/components/cards';
import TextFilter from '@cloudscape-design/components/text-filter';
import Pagination from '@cloudscape-design/components/pagination';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import { useCollection } from '@cloudscape-design/collection-hooks';

interface MessageQueue {
  id: string;
  name: string;
  status: 'healthy' | 'backlogged';
  region: 'us-east-1' | 'us-west-2';
  messagesPerSecond: number;
  oldestMessageAgeSec: number;
}

const QUEUES: MessageQueue[] = Array.from({ length: 24 }, (_, i) => ({
  id: `queue-${String(i + 1).padStart(2, '0')}`,
  name: `orders-${['ingest', 'fulfillment', 'billing', 'notifications'][i % 4]}-${String(i + 1).padStart(2, '0')}`,
  status: i % 5 === 0 ? 'backlogged' : 'healthy',
  region: i % 2 === 0 ? 'us-east-1' : 'us-west-2',
  messagesPerSecond: 5 + ((i * 13) % 400),
  oldestMessageAgeSec: i % 5 === 0 ? 300 + ((i * 41) % 1800) : ((i * 7) % 20),
}));

const statusType = (s: MessageQueue['status']) => (s === 'healthy' ? 'success' : 'warning');

// Message Queues: every queue in the account, side by side, so an
// operator can compare throughput and backlog age across all of them at
// once to decide which need scaling attention right now. Operators can
// search by queue name, or narrow the list down to a specific status or
// region while triaging.
export const MessageQueues = () => {
  const { items, collectionProps, filterProps, paginationProps } = useCollection<MessageQueue>(QUEUES, {
    filtering: {
      empty: 'No message queues',
      noMatch: 'No matching message queues',
    },
    pagination: { pageSize: 12 },
    sorting: {},
  });

  return (
    <ContentLayout
      header={
        <Header
          variant="h1"
          counter={`(${QUEUES.length})`}
          description="Compare message throughput and backlog age across queues to decide which need scaling attention."
        >
          Message queues
        </Header>
      }
    >
      <Cards
        {...collectionProps}
        items={items}
        trackBy="id"
        ariaLabels={{
          cardsLabel: 'Message queues',
        }}
        cardDefinition={{
          header: (item) => item.name,
          sections: [
            {
              id: 'status',
              header: 'Status',
              content: (item) => <StatusIndicator type={statusType(item.status)}>{item.status}</StatusIndicator>,
            },
            {
              id: 'region',
              header: 'Region',
              content: (item) => item.region,
            },
            {
              id: 'messagesPerSecond',
              header: 'Throughput (msg/s)',
              content: (item) => item.messagesPerSecond,
            },
            {
              id: 'oldestMessageAgeSec',
              header: 'Oldest message age (s)',
              content: (item) => item.oldestMessageAgeSec,
            },
          ],
        }}
        cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 2 }, { minWidth: 992, cards: 3 }]}
        filter={
          <TextFilter
            {...filterProps}
            filteringPlaceholder="Find message queue"
            filteringAriaLabel="Filter message queues"
          />
        }
        pagination={<Pagination {...paginationProps} />}
        empty="No message queues"
      />
    </ContentLayout>
  );
};
