# PRTG API v2 — Schema Reference

Auto-generated from current PRTG server spec. Contains request/response body schemas.

## Contents

- [Sensors](#sensors)
- [Devices](#devices)
- [Channels](#channels)
- [Groups](#groups)
- [Probes](#probes)
- [Timeseries](#timeseries)
- [Objects](#objects)
- [Schemas](#schemas)
- [Accounts](#accounts)
- [Libraries](#libraries)
- [Lookups](#lookups)
- [Authentication](#authentication)
- [System](#system)

## Sensors

### `POST /experimental/devices/{id}/metascan` [E]

_Execute a meta-scan on a given device for a given sensor kind_

**Response `201`:**

_object (no properties documented)_

---

### `POST /experimental/devices/{id}/sensor` [E]

_Creates a new sensor in a device._

**Request Body:** object

**Response `201` (array item):**

_object (no properties documented)_

---

### `PATCH /experimental/sensor/{id}` [E]

_Edits a sensor._

**Request Body:** object

**Response `204`:** No content.

---

### `GET /experimental/sensors` [E]

_Returns a list of sensors._

**Response `200` (array item):**

_object (no properties documented)_

---

### `DELETE /experimental/sensors/{id}` [E]

_Deletes a sensor with all child channels._

**Response `204`:** No content.

---

### `GET /sensor-status-summary`

_Returns a summary of all sensor states._

**Response `200`:**

_object (no properties documented)_

---

### `GET /sensor-status-summary/{id}`

_Returns a summary of sensor states for a probe, group, or device._

**Response `200`:**

_object (no properties documented)_

---

### `GET /sensors` [D]

_Returns a list of all sensors that match a filter._

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /sensors/acknowledge`

_Acknowledges the alarms of all sensors that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /sensors/alarms` [D]

_Returns a list of sensors with alarms that match a filter._

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /sensors/pause`

_Pauses all sensors that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /sensors/resume`

_Resumes all sensors that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /sensors/scan`

_Triggers a scan of all sensors that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /sensors/{id}`

_Returns metrics and settings of a sensor._

**Response `200`:**

_object (no properties documented)_

---

### `POST /sensors/{id}/acknowledge`

_Acknowledges the alarm of a sensor._

**Request Body:** object

**Response `204`:** No content.

---

### `POST /sensors/{id}/clone` [D]

_Clones a sensors._

**Request Body:** object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `parent_id` | string | Yes | Enter the ID of the target device |
| `position` | string |  | The position of the sensor clone within the children of the target device, top, bottom (default) or a number |
| `name` | string |  | Enter the new name of the cloned sensor, else the old name gets prefixed with 'Clone of' |

**Response `204`:** No content.

---

### `GET /sensors/{id}/data`

_Returns the channel data for a specific sensor._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /sensors/{id}/overview` [D]

_Returns a sensor overview._

**Response `200`:**

_object (no properties documented)_

---

### `POST /sensors/{id}/pause`

_Pauses a sensor._

**Request Body:** object

**Response `204`:** No content.

---

### `POST /sensors/{id}/resume`

_Resumes a sensor._

**Response `204`:** No content.

---

### `POST /sensors/{id}/scan`

_Triggers a scan of a sensor._

**Response `204`:** No content.

---

## Devices

### `GET /devices` [D]

_Returns a list of devices._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /devices/icons`

_Returns a list of device icons._

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /devices/pause`

_Pauses all devices that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /devices/resume`

_Resumes all devices that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /devices/scan`

_Triggers a scan of all devices that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /devices/{id}`

_Returns the metrics and settings of a device._

**Response `200`:**

_object (no properties documented)_

---

### `PATCH /devices/{id}`

_Edits a device._

**Request Body:** object

**Response `204`:** No content.

---

### `POST /devices/{id}/clone` [D]

_Clones a device._

**Request Body:** object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `parent_id` | string | Yes | Enter the ID of the target group or probe |
| `position` | string |  | The position of the devices clone within the children of the target group, top, bottom (default) or a number |
| `name` | string |  | Enter the new name of the cloned device, else the old name gets prefixed with 'Clone of' |
| `host` | string | Yes | Enter the new host IP Address or DNS name for the device clone |
| `service_url` | string |  | Enter the new service URL for the device clone |

**Response `204`:** No content.

---

### `GET /devices/{id}/overview` [D]

_Get a device overview._

**Response `200`:**

_object (no properties documented)_

---

### `POST /devices/{id}/pause`

_Pauses a device._

**Request Body:** object

**Response `204`:** No content.

---

### `POST /devices/{id}/resume`

_Resumes a device._

**Response `204`:** No content.

---

### `POST /devices/{id}/scan`

_Triggers a scan of all sensors on a device._

**Response `204`:** No content.

---

### `GET /experimental/devices` [E]

_Returns a list of devices._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /experimental/devices/templates` [E]

_Returns a list of device templates._

**Response `200`:**

_object (no properties documented)_

---

### `DELETE /experimental/devices/{id}` [E]

_Deletes a device with all child sensors and channels._

**Response `204`:** No content.

---

### `POST /experimental/devices/{id}/autodiscovery` [E]

_Trigger autodiscovery for a given device_

**Request Body:** object

**Response `204`:** No content.

---

### `POST /experimental/groups/{id}/device` [E]

_Creates a new device in a group._

**Request Body:** object

**Response `201` (array item):**

_object (no properties documented)_

---

### `POST /experimental/probes/{id}/device` [E]

_Creates a new device on a probe._

**Request Body:** object

**Response `201` (array item):**

_object (no properties documented)_

---

## Channels

### `GET /channels` [D]

_Returns a list of channels._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /channels/data` [D]

_Get a list of the last measurements with references to the corresponding channels._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /channels/{id}`

_Returns the metrics and settings of a channel._

**Response `200`:**

_object (no properties documented)_

---

### `GET /channels/{id}/overview` [D]

_Get a channel overview._

**Response `200`:**

_object (no properties documented)_

---

### `GET /experimental/channels` [E]

_Returns a list of channels._

**Response `200` (array item):**

_object (no properties documented)_

---

## Groups

### `GET /experimental/groups` [E]

_Returns a list of groups._

**Response `200` (array item):**

_object (no properties documented)_

---

### `PATCH /experimental/groups/{id}` [E]

_Edits a group._

**Request Body:** object

**Response `204`:** No content.

---

### `DELETE /experimental/groups/{id}` [E]

_Deletes a group with all child groups and devices._

**Response `204`:** No content.

---

### `POST /experimental/groups/{id}/autodiscovery` [E]

_Trigger autodiscovery for a given group_

**Request Body:** object

**Response `204`:** No content.

---

### `POST /experimental/groups/{id}/group` [E]

_Creates a new group in a group._

**Request Body:** object

**Response `201` (array item):**

_object (no properties documented)_

---

### `POST /experimental/probes/{id}/group` [E]

_Creates a new group in a probe._

**Request Body:** object

**Response `201` (array item):**

_object (no properties documented)_

---

### `GET /groups` [D]

_Get a list of all groups that match a filter._

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /groups/pause`

_Pauses all groups that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /groups/resume`

_Resumes all groups that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /groups/scan`

_Triggers a scan of all groups that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /groups/{id}`

_Returns the metrics and settings of a group._

**Response `200`:**

_object (no properties documented)_

---

### `POST /groups/{id}/clone` [D]

_Clones a group._

**Request Body:** object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `parent_id` | string | Yes | Enter the ID of the target group or probe. |
| `position` | string |  | The position of the group clone within the children of the target group: top, bottom (default), or a number. |
| `name` | string |  | Enter the new name of the cloned group. If you do not define a name, the old name gets prefixed with 'Clone of' |

**Response `204`:** No content.

---

### `GET /groups/{id}/overview` [D]

_Get a group overview._

**Response `200`:**

_object (no properties documented)_

---

### `POST /groups/{id}/pause`

_Pauses a group._

**Request Body:** object

**Response `204`:** No content.

---

### `POST /groups/{id}/resume`

_Resumes a group._

**Response `204`:** No content.

---

### `POST /groups/{id}/scan`

_Triggers a scan of all sensors in a group._

**Response `204`:** No content.

---

## Probes

### `GET /experimental/probes` [E]

_Returns a list of probes._

**Response `200` (array item):**

_object (no properties documented)_

---

### `DELETE /experimental/probes/{id}` [E]

_Deletes a probe with all child groups and devices._

**Response `204`:** No content.

---

### `GET /probes` [D]

_Get a list of all probes that match a filter._

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /probes/pause`

_Pauses all probes that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /probes/resume`

_Resumes all probes that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /probes/scan`

_Triggers a scan of all probes that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /probes/{id}`

_Returns the metrics and settings of a probe._

**Response `200`:**

_object (no properties documented)_

---

### `GET /probes/{id}/info`

_Returns the network information of a probe._

**Response `200`:**

_object (no properties documented)_

---

### `GET /probes/{id}/overview` [D]

_Get a probe overview._

**Response `200`:**

_object (no properties documented)_

---

### `POST /probes/{id}/pause`

_Pauses a probe._

**Request Body:** object

**Response `204`:** No content.

---

### `POST /probes/{id}/resume`

_Resumes a probe._

**Response `204`:** No content.

---

### `POST /probes/{id}/scan`

_Triggers a scan of all sensors on a probe._

**Response `204`:** No content.

---

## Timeseries

### `GET /experimental/timeseries/{id}` [E] [D]

_Get time series data_

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /experimental/timeseries/{id}/{type}` [E]

_Returns time series data of a sensor for predefined time frames._

**Response `200` (array item):**

_object (no properties documented)_

---

## Objects

### `GET /experimental/objects` [E]

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /objects` [D]

_Get a list of all probes, groups, devices, and sensors that match a filter._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /objects/count`

_Returns a list of how many objects of each kind exist._

**Response `200`:**

_object (no properties documented)_

---

### `POST /objects/{id}/move`

_Move the position of any monitoring object within it's siblings or to a new parent._

**Request Body:** object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `parent` | string |  | The new parent where to move the object or 'null' |
| `position` | integer |  | The absolute position within the siblings or 'null'. |
| `position_preset` | enum: ['top', 'up', 'down', 'bottom', 'None'] |  | position_preset movement commands or 'null'   * `top` - move to the first place   * `bottom` - move to the end   * `up` - move one place ... |

**Response `204`:** No content.

---

### `GET /schemas/{kind}` [D]

_Returns a OAS schema to use in other endpoints._

**Response `200`:**

_object (no properties documented)_

---

### `GET /setting-lookups/{name}` [D]

_Returns possible setting lookup values._

**Response `200`:**

_object (no properties documented)_

---

## Schemas

### `GET /experimental/schemas/{id}/get` [E]

_Returns OAS schema for use in `GET` endpoints for a specific object._

**Response `200`:**

_object (no properties documented)_

---

### `GET /experimental/schemas/{id}/patch` [E]

_Returns an OAS schema for use in `PATCH` endpoints for a specific object._

**Response `200`:**

_object (no properties documented)_

---

### `GET /experimental/schemas/{parent}` [E]

_Returns a list of all object kinds that you can create on a given parent object._

**Response `200` (array item):**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `creatable` | boolean |  | True if the schema is creatable other check the hints. |
| `hints` | array of enum: ['CredentialsMissing', 'ProbeIsDisconnected', 'SensorNeedsLocalProbe', 'SensorNeedsLocalProbeDevice', 'SensorNeedsProbeDevice', 'MissingCredentialGroup'] |  | Hints why the specific schema is not creatable. |
| `kind` | string |  | The schema kind. |
| `name` | string |  | The name of the schema. |
| `href` | string |  | The URL to the schema for POST requests. |
| `description` | string |  | Describes the purpose of the the monitoring object. |
| `help` | string |  | Provides additional helpful information. |
| `Manual` | string |  | A link to the manuals page where you can find more information. |

---

### `GET /experimental/schemas/{parent}/post` [E]

_Returns an OAS schema for use in `POST` endpoints._

**Response `200`:**

_object (no properties documented)_

---

## Accounts

### `GET /experimental/usergroups` [E]

_Returns a list of user groups._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /experimental/usergroups/{id}` [E]

_Returns the settings of a usergroup._

**Response `200`:**

_object (no properties documented)_

---

### `GET /experimental/users` [E]

_Returns a list of users._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /experimental/users/{id}` [E]

_Returns the metrics and settings of a user._

**Response `200`:**

_object (no properties documented)_

---

### `GET /usergroups` [D]

_Get a list of all user groups that match a filter._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /usergroups/{id}` [D]

_Return information about a user group._

**Response `200`:**

_object (no properties documented)_

---

### `GET /users` [D]

_Returns a list of all user accounts._

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /users/api-keys/find`

_Returns details of an API key._

**Request Body:** object

**Response `200`:**

_object (no properties documented)_

---

### `PATCH /users/api-keys/{id}`

_Edits an API key._

**Request Body:** object

**Response `204`:** No content.

---

### `DELETE /users/api-keys/{id}`

_Deletes an API key._

**Response `204`:** No content.

---

### `POST /users/pause`

_Pauses all user accounts that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /users/request-password`

_Triggers the password reset process for a user account._

**Request Body:** object

**Response `204`:** No content.

---

### `POST /users/reset-password`

_Set a new password for a user account with the token from the password reset process._

**Request Body:** object

**Response `204`:** No content.

---

### `POST /users/resume`

_Resumes all user accounts that match a filter._

**Request Body:** object

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /users/{id}` [D]

_Returns information about a user account._

**Response `200`:**

_object (no properties documented)_

---

### `GET /users/{id}/api-keys`

_Returns a list of API keys that belong to a user account._

**Response `200` (array item):**

_object (no properties documented)_

---

### `POST /users/{id}/api-keys`

_Creates a new API key._

**Request Body:** object

**Response `200`:**

_object (no properties documented)_

---

### `POST /users/{id}/pause`

_Pauses a user account._

**Response `204`:** No content.

---

### `POST /users/{id}/resume`

_Resumes a user account._

**Response `204`:** No content.

---

## Libraries

### `GET /libraries` [D]

_Returns a list of all libraries that match a filter._

**Response `200` (array item):**

_object (no properties documented)_

---

## Lookups

### `GET /lookup-definitions` [D]

_Returns a list of lookups definitions._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /lookup-definitions/{id}` [D]

_Returns a lookup definition._

**Response `200`:**

_object (no properties documented)_

---

## Authentication

### `GET /session`

_Renews an active user session._

**Response `200`:**

_object (no properties documented)_

---

### `POST /session`

_Creates a new user session._

**Request Body:** object

**Response `200`:**

_object (no properties documented)_

---

### `DELETE /session`

_Ends an active user session._

**Response `204`:** No content.

---

## System

### `GET /autodiscoveries`

_Returns a list of all running auto-discoveries._

**Response `200` (array item):**

_object (no properties documented)_

---

### `GET /experimental/feature-toggles` [E] [D]

_Returns a list of all enabled feature-toggles._

**Response `200` (array item):**

_string (no properties documented)_

---

### `GET /experimental/license` [E]

_Returns PRTG license information._

**Response `200`:**

_object (no properties documented)_

---

### `GET /health`

_Returns the status of the PRTG application server._

**Response `204`:** No content.

---

### `GET /settings/public`

_Returns a list of settings that are available for unauthenticated users._

**Response `200`:**

_object (no properties documented)_

---

### `GET /version`

_Returns information on the PRTG version and appserver version._

**Response `200`:**

_object (no properties documented)_

---
