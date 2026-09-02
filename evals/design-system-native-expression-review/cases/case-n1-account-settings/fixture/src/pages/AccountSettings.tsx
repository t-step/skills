import { useState } from 'react';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Container from '@cloudscape-design/components/container';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Checkbox from '@cloudscape-design/components/checkbox';

interface AccountSettingsState {
  requireTwoFactor: boolean;
  emailNotifications: boolean;
}

const updateAccountSetting = (key: keyof AccountSettingsState, value: boolean) => {
  fetch('/api/account/settings', {
    method: 'PATCH',
    body: JSON.stringify({ [key]: value }),
  });
};

export const AccountSettings = () => {
  const [requireTwoFactor, setRequireTwoFactor] = useState(false);
  const [emailNotifications, setEmailNotifications] = useState(true);

  return (
    <ContentLayout header={<Header variant="h1">Account settings</Header>}>
      <Container header={<Header variant="h2">Security and notifications</Header>}>
        <SpaceBetween size="l">
          <Checkbox
            checked={requireTwoFactor}
            onChange={({ detail }) => {
              setRequireTwoFactor(detail.checked);
              updateAccountSetting('requireTwoFactor', detail.checked);
            }}
          >
            Require two-factor authentication for sign-in
          </Checkbox>
          <Checkbox
            checked={emailNotifications}
            onChange={({ detail }) => {
              setEmailNotifications(detail.checked);
              updateAccountSetting('emailNotifications', detail.checked);
            }}
          >
            Send email notifications for account activity
          </Checkbox>
        </SpaceBetween>
      </Container>
    </ContentLayout>
  );
};
