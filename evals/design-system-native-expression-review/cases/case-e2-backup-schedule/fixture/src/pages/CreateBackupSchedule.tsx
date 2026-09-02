import { useState } from 'react';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Form from '@cloudscape-design/components/form';
import Container from '@cloudscape-design/components/container';
import SpaceBetween from '@cloudscape-design/components/space-between';
import FormField from '@cloudscape-design/components/form-field';
import Input from '@cloudscape-design/components/input';
import Select, { SelectProps } from '@cloudscape-design/components/select';
import RadioGroup from '@cloudscape-design/components/radio-group';
import Button from '@cloudscape-design/components/button';

const FREQUENCY_OPTIONS: SelectProps.Option[] = [
  { label: 'Daily', value: 'daily' },
  { label: 'Weekly', value: 'weekly' },
  { label: 'Monthly', value: 'monthly' },
];

interface FormState {
  name: string;
  frequency: SelectProps.Option | null;
  retention: string;
}

const createBackupSchedule = (state: FormState) => {
  console.log('creating backup schedule', state);
};

export const CreateBackupSchedule = () => {
  const [name, setName] = useState('');
  const [frequency, setFrequency] = useState<SelectProps.Option | null>(FREQUENCY_OPTIONS[0]);
  const [retention, setRetention] = useState('latest');

  const handleSubmit = () => {
    createBackupSchedule({ name, frequency, retention });
  };

  return (
    <ContentLayout header={<Header variant="h1">Create backup schedule</Header>}>
      <form onSubmit={(e) => e.preventDefault()}>
        <Form
          actions={
            <SpaceBetween direction="horizontal" size="xs">
              <Button formAction="none" variant="link">
                Cancel
              </Button>
              <Button formAction="submit" variant="primary" onClick={handleSubmit}>
                Create schedule
              </Button>
            </SpaceBetween>
          }
        >
          <Container header={<Header variant="h2">Schedule details</Header>}>
            <SpaceBetween size="l">
              <FormField label="Schedule name">
                <Input value={name} onChange={({ detail }) => setName(detail.value)} placeholder="nightly-backup" />
              </FormField>
              <FormField label="Frequency">
                <Select
                  selectedOption={frequency}
                  onChange={({ detail }) => setFrequency(detail.selectedOption)}
                  options={FREQUENCY_OPTIONS}
                />
              </FormField>
              <FormField label="Retention policy">
                <RadioGroup
                  value={retention}
                  onChange={({ detail }) => setRetention(detail.value)}
                  items={[
                    { value: 'latest', label: 'Keep only the latest backup' },
                    { value: 'full', label: 'Keep full backup history' },
                  ]}
                />
              </FormField>
            </SpaceBetween>
          </Container>
        </Form>
      </form>
    </ContentLayout>
  );
};
