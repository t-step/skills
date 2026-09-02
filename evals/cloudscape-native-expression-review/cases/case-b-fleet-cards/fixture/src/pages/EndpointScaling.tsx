import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Cards from '@cloudscape-design/components/cards';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import Button from '@cloudscape-design/components/button';
import Box from '@cloudscape-design/components/box';

interface InferenceEndpoint {
  id: string;
  region: string;
  status: 'healthy' | 'degraded' | 'overloaded';
  invocationsPerMin: number;
  latencyP99Ms: number;
  errorRatePct: number;
}

const ENDPOINTS: InferenceEndpoint[] = Array.from({ length: 22 }, (_, i) => ({
  id: `endpoint-${String(i + 1).padStart(2, '0')}`,
  region: ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1'][i % 4],
  status: i % 9 === 0 ? 'overloaded' : i % 4 === 0 ? 'degraded' : 'healthy',
  invocationsPerMin: 200 + ((i * 37) % 4000),
  latencyP99Ms: 80 + ((i * 23) % 900),
  errorRatePct: Number(((i % 7) * 0.35).toFixed(2)),
}));

const statusType = (s: InferenceEndpoint['status']) =>
  s === 'healthy' ? 'success' : s === 'degraded' ? 'warning' : 'error';

// Endpoint Scaling: every inference endpoint the on-call operator might
// need to scale right now. The whole point of this page is comparing
// invocation volume, p99 latency, and error rate side by side across all
// endpoints to decide which one(s) need a capacity change -- described
// explicitly in the page header below.
export const EndpointScaling = () => (
  <ContentLayout
    header={
      <Header
        variant="h1"
        counter={`(${ENDPOINTS.length})`}
        description="Compare request volume, latency, and error rate across endpoints to decide which ones need to scale."
      >
        Endpoint scaling
      </Header>
    }
  >
    <Cards
      items={ENDPOINTS}
      trackBy="id"
      cardDefinition={{
        header: (item) => item.id,
        sections: [
          {
            id: 'status',
            content: (item) => <StatusIndicator type={statusType(item.status)}>{item.status}</StatusIndicator>,
          },
          {
            id: 'region',
            header: 'Region',
            content: (item) => item.region,
          },
          {
            id: 'invocations',
            header: 'Invocations / min',
            content: (item) => item.invocationsPerMin.toLocaleString(),
          },
          {
            id: 'latency',
            header: 'p99 latency (ms)',
            content: (item) => item.latencyP99Ms,
          },
          {
            id: 'errorRate',
            header: 'Error rate',
            content: (item) => `${item.errorRatePct}%`,
          },
          {
            id: 'actions',
            content: (item) => (
              <Box float="right">
                <Button>Scale up</Button>
              </Box>
            ),
          },
        ],
      }}
      cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 2 }, { minWidth: 900, cards: 3 }]}
      empty="No endpoints"
    />
  </ContentLayout>
);
