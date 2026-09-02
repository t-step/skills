import { useParams } from 'react-router';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import BreadcrumbGroup from '@cloudscape-design/components/breadcrumb-group';
import Container from '@cloudscape-design/components/container';
import KeyValuePairs from '@cloudscape-design/components/key-value-pairs';
import Table from '@cloudscape-design/components/table';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Button from '@cloudscape-design/components/button';
import StatusIndicator from '@cloudscape-design/components/status-indicator';

const SANS = ['api.example.com', 'api-staging.example.com', '*.internal.example.com'];

const ATTACHED_RESOURCES = [
  { name: 'alb-public-prod', type: 'Application Load Balancer', region: 'us-east-1' },
  { name: 'alb-internal-prod', type: 'Application Load Balancer', region: 'us-east-1' },
];

const RENEWAL_HISTORY = [
  { date: '2026-03-01', outcome: 'Renewed automatically' },
  { date: '2025-03-01', outcome: 'Renewed automatically' },
  { date: '2024-03-02', outcome: 'Renewed manually (validation delay)' },
];

// A single certificate's full detail set: identity, every domain it
// covers, every resource it's attached to, and its renewal history --
// four related but distinct fact groups about one resource, each big
// enough (or independently useful enough) to be its own container.
export const CertificateDetails = () => {
  const { certId } = useParams();

  return (
    <ContentLayout
      header={
        <>
          <BreadcrumbGroup
            items={[
              { text: 'Certificates', href: '/certificates' },
              { text: 'api.example.com', href: '#' },
            ]}
            ariaLabel="Breadcrumbs"
          />
          <Header
            variant="h1"
            actions={
              <SpaceBetween direction="horizontal" size="xs">
                <Button>Renew</Button>
                <Button>Revoke</Button>
              </SpaceBetween>
            }
          >
            api.example.com ({certId})
          </Header>
        </>
      }
    >
      <SpaceBetween size="l">
        <Container header={<Header variant="h2">General configuration</Header>}>
          <KeyValuePairs
            columns={3}
            items={[
              { label: 'Status', value: <StatusIndicator type="success">Issued</StatusIndicator> },
              { label: 'Issued by', value: 'Amazon' },
              { label: 'Expires', value: '2027-03-01' },
            ]}
          />
        </Container>

        <Container header={<Header variant="h2" counter={`(${SANS.length})`}>Domains covered</Header>}>
          <Table
            columnDefinitions={[{ id: 'domain', header: 'Domain', cell: (d: string) => d, isRowHeader: true }]}
            items={SANS}
            trackBy={(d: string) => d}
            ariaLabels={{ tableLabel: 'Domains covered' }}
            variant="borderless"
          />
        </Container>

        <Container header={<Header variant="h2" counter={`(${ATTACHED_RESOURCES.length})`}>Attached resources</Header>}>
          <Table
            columnDefinitions={[
              { id: 'name', header: 'Name', cell: (r) => r.name, isRowHeader: true },
              { id: 'type', header: 'Type', cell: (r) => r.type },
              { id: 'region', header: 'Region', cell: (r) => r.region },
            ]}
            items={ATTACHED_RESOURCES}
            trackBy="name"
            ariaLabels={{ tableLabel: 'Attached resources' }}
            variant="borderless"
          />
        </Container>

        <Container header={<Header variant="h2">Renewal history</Header>}>
          <Table
            columnDefinitions={[
              { id: 'date', header: 'Date', cell: (r) => r.date, isRowHeader: true },
              { id: 'outcome', header: 'Outcome', cell: (r) => r.outcome },
            ]}
            items={RENEWAL_HISTORY}
            trackBy="date"
            ariaLabels={{ tableLabel: 'Renewal history' }}
            variant="borderless"
          />
        </Container>
      </SpaceBetween>
    </ContentLayout>
  );
};
