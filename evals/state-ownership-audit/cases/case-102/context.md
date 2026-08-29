# Context

A platform engineer, doing a general safety review before onboarding a new
device fleet type, asks:

> Both `ProvisioningService` and `DeviceManagementAPI` can write
> `devices.config`. Before we scale up device onboarding, I want a clear
> answer on who actually owns `Device.config` and whether there's any way
> both of these could stomp on each other's writes.

Files in this directory (`provisioning_service.py`,
`device_management_api.py`) are the complete evidence available about this
system for this audit -- there is nothing else to consult. Device status
values observed in this codebase: `pending`, `provisioning`, `active`,
`decommissioned`.
