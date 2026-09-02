import { useState } from 'react';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Form from '@cloudscape-design/components/form';
import Container from '@cloudscape-design/components/container';
import SpaceBetween from '@cloudscape-design/components/space-between';
import FormField from '@cloudscape-design/components/form-field';
import Input from '@cloudscape-design/components/input';
import Textarea from '@cloudscape-design/components/textarea';
import Select, { SelectProps } from '@cloudscape-design/components/select';
import Checkbox from '@cloudscape-design/components/checkbox';
import Button from '@cloudscape-design/components/button';

const REGION_OPTIONS: SelectProps.Option[] = [
  { label: 'us-east-1', value: 'us-east-1' },
  { label: 'us-west-2', value: 'us-west-2' },
];
const INSTANCE_TYPE_OPTIONS: SelectProps.Option[] = [
  { label: 'm5.large', value: 'm5.large' },
  { label: 'm5.xlarge', value: 'm5.xlarge' },
];
const VPC_OPTIONS: SelectProps.Option[] = [{ label: 'vpc-primary', value: 'vpc-primary' }];
const SUBNET_OPTIONS: SelectProps.Option[] = [{ label: 'subnet-a', value: 'subnet-a' }];
const SECURITY_GROUP_OPTIONS: SelectProps.Option[] = [{ label: 'sg-default', value: 'sg-default' }];
const VOLUME_TYPE_OPTIONS: SelectProps.Option[] = [
  { label: 'gp3', value: 'gp3' },
  { label: 'io2', value: 'io2' },
];

const createEnvironment = (payload: Record<string, unknown>) => {
  console.log('creating environment', payload);
};

export const CreateEnvironment = () => {
  // General
  const [envName, setEnvName] = useState('');
  const [description, setDescription] = useState('');
  const [region, setRegion] = useState<SelectProps.Option | null>(REGION_OPTIONS[0]);

  // Compute
  const [instanceType, setInstanceType] = useState<SelectProps.Option | null>(INSTANCE_TYPE_OPTIONS[0]);
  const [instanceCount, setInstanceCount] = useState('2');
  const [autoScalingMin, setAutoScalingMin] = useState('1');
  const [autoScalingMax, setAutoScalingMax] = useState('4');

  // Networking
  const [vpc, setVpc] = useState<SelectProps.Option | null>(VPC_OPTIONS[0]);
  const [subnet, setSubnet] = useState<SelectProps.Option | null>(SUBNET_OPTIONS[0]);
  const [securityGroup, setSecurityGroup] = useState<SelectProps.Option | null>(SECURITY_GROUP_OPTIONS[0]);
  const [publicIp, setPublicIp] = useState(false);

  // Storage
  const [volumeType, setVolumeType] = useState<SelectProps.Option | null>(VOLUME_TYPE_OPTIONS[0]);
  const [volumeSize, setVolumeSize] = useState('100');
  const [encryptVolume, setEncryptVolume] = useState(true);

  // Monitoring
  const [detailedMonitoring, setDetailedMonitoring] = useState(false);
  const [logRetentionDays, setLogRetentionDays] = useState('30');
  const [alertEmail, setAlertEmail] = useState('');

  // Tags
  const [ownerTag, setOwnerTag] = useState('');
  const [costCenterTag, setCostCenterTag] = useState('');
  const [environmentTag, setEnvironmentTag] = useState('');

  const handleSubmit = () => {
    createEnvironment({
      envName,
      description,
      region,
      instanceType,
      instanceCount,
      autoScalingMin,
      autoScalingMax,
      vpc,
      subnet,
      securityGroup,
      publicIp,
      volumeType,
      volumeSize,
      encryptVolume,
      detailedMonitoring,
      logRetentionDays,
      alertEmail,
      ownerTag,
      costCenterTag,
      environmentTag,
    });
  };

  return (
    <ContentLayout header={<Header variant="h1">Create environment</Header>}>
      <form onSubmit={(e) => e.preventDefault()}>
        <Form
          actions={
            <SpaceBetween direction="horizontal" size="xs">
              <Button formAction="none" variant="link">
                Cancel
              </Button>
              <Button formAction="submit" variant="primary" onClick={handleSubmit}>
                Create environment
              </Button>
            </SpaceBetween>
          }
        >
          <SpaceBetween size="l">
            <Container header={<Header variant="h2">General</Header>}>
              <SpaceBetween size="l">
                <FormField label="Environment name">
                  <Input value={envName} onChange={({ detail }) => setEnvName(detail.value)} />
                </FormField>
                <FormField label="Description">
                  <Textarea value={description} onChange={({ detail }) => setDescription(detail.value)} />
                </FormField>
                <FormField label="Region">
                  <Select
                    selectedOption={region}
                    onChange={({ detail }) => setRegion(detail.selectedOption)}
                    options={REGION_OPTIONS}
                  />
                </FormField>
              </SpaceBetween>
            </Container>

            <Container header={<Header variant="h2">Compute</Header>}>
              <SpaceBetween size="l">
                <FormField label="Instance type">
                  <Select
                    selectedOption={instanceType}
                    onChange={({ detail }) => setInstanceType(detail.selectedOption)}
                    options={INSTANCE_TYPE_OPTIONS}
                  />
                </FormField>
                <FormField label="Instance count">
                  <Input value={instanceCount} onChange={({ detail }) => setInstanceCount(detail.value)} type="number" />
                </FormField>
                <FormField label="Auto-scaling minimum">
                  <Input value={autoScalingMin} onChange={({ detail }) => setAutoScalingMin(detail.value)} type="number" />
                </FormField>
                <FormField label="Auto-scaling maximum">
                  <Input value={autoScalingMax} onChange={({ detail }) => setAutoScalingMax(detail.value)} type="number" />
                </FormField>
              </SpaceBetween>
            </Container>

            <Container header={<Header variant="h2">Networking</Header>}>
              <SpaceBetween size="l">
                <FormField label="VPC">
                  <Select
                    selectedOption={vpc}
                    onChange={({ detail }) => setVpc(detail.selectedOption)}
                    options={VPC_OPTIONS}
                  />
                </FormField>
                <FormField label="Subnet">
                  <Select
                    selectedOption={subnet}
                    onChange={({ detail }) => setSubnet(detail.selectedOption)}
                    options={SUBNET_OPTIONS}
                  />
                </FormField>
                <FormField label="Security group">
                  <Select
                    selectedOption={securityGroup}
                    onChange={({ detail }) => setSecurityGroup(detail.selectedOption)}
                    options={SECURITY_GROUP_OPTIONS}
                  />
                </FormField>
                <Checkbox checked={publicIp} onChange={({ detail }) => setPublicIp(detail.checked)}>
                  Assign a public IP address
                </Checkbox>
              </SpaceBetween>
            </Container>

            <Container header={<Header variant="h2">Storage</Header>}>
              <SpaceBetween size="l">
                <FormField label="Volume type">
                  <Select
                    selectedOption={volumeType}
                    onChange={({ detail }) => setVolumeType(detail.selectedOption)}
                    options={VOLUME_TYPE_OPTIONS}
                  />
                </FormField>
                <FormField label="Volume size (GB)">
                  <Input value={volumeSize} onChange={({ detail }) => setVolumeSize(detail.value)} type="number" />
                </FormField>
                <Checkbox checked={encryptVolume} onChange={({ detail }) => setEncryptVolume(detail.checked)}>
                  Encrypt volume
                </Checkbox>
              </SpaceBetween>
            </Container>

            <Container header={<Header variant="h2">Monitoring</Header>}>
              <SpaceBetween size="l">
                <Checkbox checked={detailedMonitoring} onChange={({ detail }) => setDetailedMonitoring(detail.checked)}>
                  Enable detailed monitoring
                </Checkbox>
                <FormField label="Log retention (days)">
                  <Input value={logRetentionDays} onChange={({ detail }) => setLogRetentionDays(detail.value)} type="number" />
                </FormField>
                <FormField label="Alert email">
                  <Input value={alertEmail} onChange={({ detail }) => setAlertEmail(detail.value)} type="email" />
                </FormField>
              </SpaceBetween>
            </Container>

            <Container header={<Header variant="h2">Tags</Header>}>
              <SpaceBetween size="l">
                <FormField label="Owner">
                  <Input value={ownerTag} onChange={({ detail }) => setOwnerTag(detail.value)} />
                </FormField>
                <FormField label="Cost center">
                  <Input value={costCenterTag} onChange={({ detail }) => setCostCenterTag(detail.value)} />
                </FormField>
                <FormField label="Environment tag">
                  <Input value={environmentTag} onChange={({ detail }) => setEnvironmentTag(detail.value)} />
                </FormField>
              </SpaceBetween>
            </Container>
          </SpaceBetween>
        </Form>
      </form>
    </ContentLayout>
  );
};
