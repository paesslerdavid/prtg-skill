# PRTG API v2 — Endpoint Reference

Auto-generated from current PRTG server spec. 115 operations across 109 paths.

**Legend:** [D] = Deprecated, [E] = Experimental

## Contents

- [Sensors](#sensors) (21 endpoints)
- [Devices](#devices) (18 endpoints)
- [Channels](#channels) (5 endpoints)
- [Groups](#groups) (16 endpoints)
- [Probes](#probes) (12 endpoints)
- [Timeseries](#timeseries) (2 endpoints)
- [Objects](#objects) (6 endpoints)
- [Schemas](#schemas) (4 endpoints)
- [Accounts](#accounts) (19 endpoints)
- [Libraries](#libraries) (1 endpoints)
- [Lookups](#lookups) (2 endpoints)
- [Authentication](#authentication) (3 endpoints)
- [System](#system) (6 endpoints)

## Sensors

### `POST /experimental/devices/{id}/metascan` [E]

Execute a meta-scan on a given device for a given sensor kind

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to execute a new meta-scan. |
| `kind` | query | string | Yes | snmpdiskfree | Enter the kind of the sensor. |

**Responses:**

- `201`: Execute a new sensor meta-scan for an given device. — Metascan (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /experimental/devices/{id}/sensor` [E]

Creates a new sensor in a device.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to create a new sensor in. |
| `kindid` | query | string | Yes | ping | Enter the kind ID of the sensor. |

**Request body** (application/json): CreateRequestBody

**Responses:**

- `201`: A new sensor was created on the device. — array of SensorInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `PATCH /experimental/sensor/{id}` [E]

Edits a sensor.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to edit. |

**Request body** (application/json): SettingsRequestBody

**Responses:**

- `204`: The request was successful.
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/sensors` [E]

Returns a list of sensors.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested sensors.  You can ... |

**Responses:**

- `200`: The request was successful. — array of SensorInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `DELETE /experimental/sensors/{id}` [E]

Deletes a sensor with all child channels.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to delete. |

**Responses:**

- `204`: The sensor was deleted.
- `4XX`: 
- `5XX`: 

---

### `GET /sensor-status-summary`

Returns a summary of all sensor states.

**Responses:**

- `200`: The request was successful. — SensorStatusSummary (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /sensor-status-summary/{id}`

Returns a summary of sensor states for a probe, group, or device.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the object that you you want to get a sensor status summary of. |

**Responses:**

- `200`: The request was successful. — SensorStatusSummary (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /sensors` [D]

Returns a list of all sensors that match a filter.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |
| `include_all_channels` | query | boolean |  | False | Enter **true** to include all channels. Enter **false** to only include the primary channel and the Downtim... |

**Responses:**

- `200`: The request was successful. — array of SensorInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /sensors/acknowledge`

Acknowledges the alarms of all sensors that match a filter.

**Request body** (application/json): MultiAcknowledgeRequestBody

**Responses:**

- `200`: The request to acknowledge the alarms of all sensors that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /sensors/alarms` [D]

Returns a list of sensors with alarms that match a filter.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |
| `include_all_channels` | query | boolean |  | False | Enter **true** to include all channels. Enter **false** to only include the primary channel and the Downtim... |

**Responses:**

- `200`: The request was successful. — array of SensorInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /sensors/pause`

Pauses all sensors that match a filter.

**Request body** (application/json): MultiPauseRequestBody

**Responses:**

- `200`: The request to pause all sensors that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /sensors/resume`

Resumes all sensors that match a filter.

**Request body** (application/json): MultiResumeRequestBody

**Responses:**

- `200`: The request to resume all sensors that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /sensors/scan`

Triggers a scan of all sensors that match a filter.

**Request body** (application/json): MultiScanNowRequestBody

**Responses:**

- `200`: The request to scan all sensors that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /sensors/{id}`

Returns metrics and settings of a sensor.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to see the metrics and settings of. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about a sensor.    You can include add... |

**Responses:**

- `200`: The request was successful. — any (see schema)
- `4XX`: 

---

### `POST /sensors/{id}/acknowledge`

Acknowledges the alarm of a sensor.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to acknowledge the alarm of. |

**Request body** (application/json): AcknowledgeRequestBody

**Responses:**

- `204`: The sensor alarm was acknowledged.
- `4XX`: 
- `5XX`: 

---

### `POST /sensors/{id}/clone` [D]

Clones a sensors.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  |  |

**Request body** (application/json): object

**Responses:**

- `204`: The cloning process was successful.
- `4XX`: 
- `5XX`: 

---

### `GET /sensors/{id}/data`

Returns the channel data for a specific sensor.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to get channel data for. |
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of ChannelMeasurement (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /sensors/{id}/overview` [D]

Returns a sensor overview.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want an overview of. |

**Responses:**

- `200`: The request was successful. — SensorInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /sensors/{id}/pause`

Pauses a sensor.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to pause. |

**Request body** (application/json): PauseRequestBody

**Responses:**

- `204`: The sensor was paused.
- `4XX`: 
- `5XX`: 

---

### `POST /sensors/{id}/resume`

Resumes a sensor.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to resume. |

**Responses:**

- `204`: The sensor was resumed.
- `4XX`: 
- `5XX`: 

---

### `POST /sensors/{id}/scan`

Triggers a scan of a sensor.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to scan. |

**Responses:**

- `204`: The sensor was scanned.
- `4XX`: 
- `5XX`: 

---

## Devices

### `GET /devices` [D]

Returns a list of devices.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sensor_status_summary` | query | boolean |  | False | Define if you want to request a sensor status summary of each device. Enter **true** to request a sensor st... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of DeviceInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /devices/icons`

Returns a list of device icons.

**Responses:**

- `200`: The request was successful. — array of DeviceIcon (see schema)
- `4XX`: Client Errors — Error (see schema)
- `5XX`: 

---

### `POST /devices/pause`

Pauses all devices that match a filter.

**Request body** (application/json): MultiPauseRequestBody

**Responses:**

- `200`: The request to pause all devices that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /devices/resume`

Resumes all devices that match a filter.

**Request body** (application/json): MultiResumeRequestBody

**Responses:**

- `200`: The request to resume all devices that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /devices/scan`

Triggers a scan of all devices that match a filter.

**Request body** (application/json): MultiScanNowRequestBody

**Responses:**

- `200`: The request to scan all devices that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /devices/{id}`

Returns the metrics and settings of a device.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to see the metrics and settings of. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about a device.  You can include addit... |

**Responses:**

- `200`: The request was successful. — any (see schema)
- `4XX`: 

---

### `PATCH /devices/{id}`

Edits a device.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to edit. |

**Request body** (application/json): SettingsRequestBody

**Responses:**

- `204`: The request was successful.
- `4XX`: 
- `5XX`: 

---

### `POST /devices/{id}/clone` [D]

Clones a device.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  |  |

**Request body** (application/json): object

**Responses:**

- `204`: The cloning process was successful
- `4XX`: 
- `5XX`: 

---

### `GET /devices/{id}/overview` [D]

Get a device overview.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to get an overview of. |

**Responses:**

- `200`: The request was successful. — DeviceInfo (see schema)
- `4XX`: 

---

### `POST /devices/{id}/pause`

Pauses a device.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to pause. |

**Request body** (application/json): PauseRequestBody

**Responses:**

- `204`: The device was paused.
- `4XX`: 
- `5XX`: 

---

### `POST /devices/{id}/resume`

Resumes a device.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to resume. |

**Responses:**

- `204`: The device was resumed.
- `4XX`: 
- `5XX`: 

---

### `POST /devices/{id}/scan`

Triggers a scan of all sensors on a device.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to scan. |

**Responses:**

- `204`: The device was scanned.
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/devices` [E]

Returns a list of devices.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested devices.  You can ... |

**Responses:**

- `200`: The request was successful. — array of any (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/devices/templates` [E]

Returns a list of device templates.

**Responses:**

- `200`: The request was successful. — DeviceTemplates (see schema)
- `4XX`: 
- `5XX`: 

---

### `DELETE /experimental/devices/{id}` [E]

Deletes a device with all child sensors and channels.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to delete. |

**Responses:**

- `204`: The device was deleted.
- `4XX`: 
- `5XX`: 

---

### `POST /experimental/devices/{id}/autodiscovery` [E]

Trigger autodiscovery for a given device

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the device that you want to trigger autodiscovery for. |

**Request body** (application/json): TriggerAutoDiscoveryRequestBody

**Responses:**

- `204`: Auto discovery for an given device was triggered successfully.
- `4XX`: 
- `5XX`: 

---

### `POST /experimental/groups/{id}/device` [E]

Creates a new device in a group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to create a new device in. |

**Request body** (application/json): CreateRequestBody

**Responses:**

- `201`: A new device was created on the group. — array of DeviceInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /experimental/probes/{id}/device` [E]

Creates a new device on a probe.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to create a new device on. |

**Request body** (application/json): CreateRequestBody

**Responses:**

- `201`: A new device was created on the probe. — array of DeviceInfo (see schema)
- `4XX`: 
- `5XX`: 

---

## Channels

### `GET /channels` [D]

Returns a list of channels.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of ChannelInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /channels/data` [D]

Get a list of the last measurements with references to the corresponding channels.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of ChannelMeasurement (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /channels/{id}`

Returns the metrics and settings of a channel.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the channel that you want to see the metrics and settings of. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about a channel.  You can include addi... |

**Responses:**

- `200`: The request was successful. — any (see schema)
- `4XX`: 

---

### `GET /channels/{id}/overview` [D]

Get a channel overview.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the channel for which you want to get a channel overview. |

**Responses:**

- `200`: The request was successful. — ChannelInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/channels` [E]

Returns a list of channels.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested channels.  You can... |

**Responses:**

- `200`: The request was successful. — array of ChannelInfo (see schema)
- `4XX`: 
- `5XX`: 

---

## Groups

### `GET /experimental/groups` [E]

Returns a list of groups.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested groups.  You can i... |

**Responses:**

- `200`: The request was successful. — array of GroupInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `PATCH /experimental/groups/{id}` [E]

Edits a group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to edit. |

**Request body** (application/json): SettingsRequestBody

**Responses:**

- `204`: The request was successful.
- `4XX`: 
- `5XX`: 

---

### `DELETE /experimental/groups/{id}` [E]

Deletes a group with all child groups and devices.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to delete. |

**Responses:**

- `204`: The group was deleted.
- `4XX`: 
- `5XX`: 

---

### `POST /experimental/groups/{id}/autodiscovery` [E]

Trigger autodiscovery for a given group

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to trigger autodiscovery for. |

**Request body** (application/json): TriggerAutoDiscoveryRequestBody

**Responses:**

- `204`: Auto discovery for an given group was triggered successfully.
- `4XX`: 
- `5XX`: 

---

### `POST /experimental/groups/{id}/group` [E]

Creates a new group in a group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to create a new group in. |

**Request body** (application/json): CreateRequestBody

**Responses:**

- `201`: A new group was created on the group. — array of GroupInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /experimental/probes/{id}/group` [E]

Creates a new group in a probe.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to create a new group in. |

**Request body** (application/json): CreateRequestBody

**Responses:**

- `201`: A new group was created on the probe. — array of GroupInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /groups` [D]

Get a list of all groups that match a filter.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sensor_status_summary` | query | boolean |  | False | Define if you want to request a sensor status summary of each group. Enter **true** to request a sensor sta... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of GroupInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /groups/pause`

Pauses all groups that match a filter.

**Request body** (application/json): MultiPauseRequestBody

**Responses:**

- `200`: The request to pause all groups that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /groups/resume`

Resumes all groups that match a filter.

**Request body** (application/json): MultiResumeRequestBody

**Responses:**

- `200`: The request to resume all groups that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /groups/scan`

Triggers a scan of all groups that match a filter.

**Request body** (application/json): MultiScanNowRequestBody

**Responses:**

- `200`: The request to scan all groups that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /groups/{id}`

Returns the metrics and settings of a group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to see the metrics and settings of. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about a group.  You can include additi... |

**Responses:**

- `200`: The request was successful. — any (see schema)
- `4XX`: 

---

### `POST /groups/{id}/clone` [D]

Clones a group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to clone. |

**Request body** (application/json): object

**Responses:**

- `204`: The cloning process was successful
- `4XX`: 
- `5XX`: 

---

### `GET /groups/{id}/overview` [D]

Get a group overview.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group for which you want to get a group overview. |

**Responses:**

- `200`: The request was successful. — GroupInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /groups/{id}/pause`

Pauses a group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to pause. |

**Request body** (application/json): PauseRequestBody

**Responses:**

- `204`: The group was paused.
- `4XX`: 
- `5XX`: 

---

### `POST /groups/{id}/resume`

Resumes a group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to resume. |

**Responses:**

- `204`: The group was resumed.
- `4XX`: 
- `5XX`: 

---

### `POST /groups/{id}/scan`

Triggers a scan of all sensors in a group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the group that you want to scan. |

**Responses:**

- `204`: The group was scanned.
- `4XX`: 
- `5XX`: 

---

## Probes

### `GET /experimental/probes` [E]

Returns a list of probes.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested probes.  You can i... |

**Responses:**

- `200`: The request was successful. — array of ProbeInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `DELETE /experimental/probes/{id}` [E]

Deletes a probe with all child groups and devices.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to delete. |

**Responses:**

- `204`: The probe was deleted.
- `4XX`: 
- `5XX`: 

---

### `GET /probes` [D]

Get a list of all probes that match a filter.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sensor_status_summary` | query | boolean |  | False | Define if you want to request a sensor status summary of each probe. Enter **true** to request a sensor sta... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of ProbeInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /probes/pause`

Pauses all probes that match a filter.

**Request body** (application/json): MultiPauseRequestBody

**Responses:**

- `200`: The request to pause all probes that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /probes/resume`

Resumes all probes that match a filter.

**Request body** (application/json): MultiResumeRequestBody

**Responses:**

- `200`: The request to resume all probes that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /probes/scan`

Triggers a scan of all probes that match a filter.

**Request body** (application/json): MultiScanNowRequestBody

**Responses:**

- `200`: The request to resume all probes that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /probes/{id}`

Returns the metrics and settings of a probe.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to see the metrics and settings of. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about a probe.  You can include additi... |

**Responses:**

- `200`: The request was successful. — any (see schema)
- `4XX`: 

---

### `GET /probes/{id}/info`

Returns the network information of a probe.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to see the network information of. |

**Responses:**

- `200`: The request was successful. — ProbeNetworkInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /probes/{id}/overview` [D]

Get a probe overview.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to get an overview for. |

**Responses:**

- `200`: The request was successful. — ProbeInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /probes/{id}/pause`

Pauses a probe.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to pause. |

**Request body** (application/json): PauseRequestBody

**Responses:**

- `204`: The probe was paused.
- `4XX`: 
- `5XX`: 

---

### `POST /probes/{id}/resume`

Resumes a probe.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to resume. |

**Responses:**

- `204`: The probe was resumed.
- `4XX`: 
- `5XX`: 

---

### `POST /probes/{id}/scan`

Triggers a scan of all sensors on a probe.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the probe that you want to scan. |

**Responses:**

- `204`: The probe was scanned.
- `4XX`: 
- `5XX`: 

---

## Timeseries

### `GET /experimental/timeseries/{id}` [E] [D]

Get time series data

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor for which you want to get the time series data. |
| `channels` | query | array of string |  |  | Enter the comma separated IDs of the channels you want to include. If left empty all channels will be returned |
| `from` | query | string (date-time) | Yes |  | The starting point of the sample interval in the past as a timestamp in RFC3339 ("YYYY-MM-DDThh:mm:ssZ") fo... |
| `to` | query | string (date-time) |  |  | The ending point of the sample interval in the past as a time stamp in RFC3339 ("YYYY-MM-DDThh:mm:ssZ") for... |

**Responses:**

- `200`: The request was successful. — array of TimeseriesRow (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/timeseries/{id}/{type}` [E]

Returns time series data of a sensor for predefined time frames.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the sensor that you want to get the time series data for. |
| `type` | path | enum: ['live', 'short', 'medium', 'long'] | Yes | live | Select the dataset type:  * `live`: Returns data of the last four hours. * `short`: Returns data of the las... |
| `channels` | query | array of string |  |  | Enter a comma-separated list of channel IDs that you want to include (e.g. 3074.1, 3074.2) in the response.... |

**Responses:**

- `200`: The request was successful. — array of TimeseriesRow (see schema)
- `4XX`: 
- `5XX`: 

---

## Objects

### `GET /experimental/objects` [E]

Get a list of all probes, groups, devices, sensors and channels that match a filter.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested objects.  You can ... |

**Responses:**

- `200`: The request was successful. — array of any (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /objects` [D]

Get a list of all probes, groups, devices, and sensors that match a filter.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sensor_status_summary` | query | boolean |  | False | Define if you want to request a sensor status summary of all objects. Enter **true** to request a sensor st... |

**Responses:**

- `200`: The request was successful. — array of ObjectInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /objects/count`

Returns a list of how many objects of each kind exist.

**Responses:**

- `200`: The request was successful. — ObjectSummary (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /objects/{id}/move`

Move the position of any monitoring object within it's siblings or to a new parent.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the object that you want to move. |

**Request body** (application/json): object

**Responses:**

- `204`: The object was moved.
- `4XX`: 
- `5XX`: 

---

### `GET /schemas/{kind}` [D]

Returns a OAS schema to use in other endpoints.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `kind` | path | string | Yes |  | Enter the kind of schema you want. You can request a schema of a device, group, user, or a specific type of... |
| `purpose` | query | enum: ['create', 'update', 'read'] | Yes | read | Select the purpose to refine the schema for a specific use case:    * Use `read` for the schema of a `GET` ... |
| `parent` | query | string |  |  | Enter the object ID of the parent object where you want to create a new object to request the correct schem... |

**Responses:**

- `200`: The request was successful. — SchemaDefinition (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /setting-lookups/{name}` [D]

Returns possible setting lookup values.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `name` | path | string | Yes |  | Name of the lookup. |
| `id` | query | string |  |  | Enter ID of corresponding object of the setting lookup. |

**Responses:**

- `200`: The setting lookup result — SettingsLookupResult (see schema)
- `4XX`: 
- `5XX`: 

---

## Schemas

### `GET /experimental/schemas/{id}/get` [E]

Returns OAS schema for use in `GET` endpoints for a specific object.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | The object ID for which to retrieve the schema. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested objects.  You can ... |

**Responses:**

- `200`: The request was successful. — SchemaDefinition (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/schemas/{id}/patch` [E]

Returns an OAS schema for use in `PATCH` endpoints for a specific object.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | The object ID for which to retrieve the schema. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested objects.  You can ... |

**Responses:**

- `200`: The request was successful. — SchemaDefinition (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/schemas/{parent}` [E]

Returns a list of all object kinds that you can create on a given parent object.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `parent` | path | string | Yes |  | Enter the ID of the parent object. |
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |

**Responses:**

- `200`: The request was successful. — array of any (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/schemas/{parent}/post` [E]

Returns an OAS schema for use in `POST` endpoints.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `parent` | path | string | Yes |  | The object ID of the parent object where you want to create a new object. |
| `kind` | query | string | Yes |  | The kind of object you want to create (e.g., device, group, or in case of sensors e.g. ping). |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested objects.  You can ... |

**Responses:**

- `200`: The request was successful. — SchemaDefinition (see schema)
- `4XX`: 
- `5XX`: 

---

## Accounts

### `GET /experimental/usergroups` [E]

Returns a list of user groups.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use offset to define which results are returned. For example, if you enter 0 for offset and 100 for limit, ... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. The maximum number of objects is 3000. If you enter 0... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see <a href="../overview#filter" target="_blank... |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested users.  You can in... |

**Responses:**

- `200`: The request was successful. — array of any (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/usergroups/{id}` [E]

Returns the settings of a usergroup.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the usergroup that you want to see the settings of. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about a usergroup.  You can include ad... |

**Responses:**

- `200`: The request was successful. — any (see schema)
- `4XX`: 

---

### `GET /experimental/users` [E]

Returns a list of users.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use offset to define which results are returned. For example, if you enter 0 for offset and 100 for limit, ... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. The maximum number of objects is 3000. If you enter 0... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see <a href="../overview#filter" target="_blank... |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about the requested users.  You can in... |

**Responses:**

- `200`: The request was successful. — array of any (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/users/{id}` [E]

Returns the metrics and settings of a user.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the user that you want to see the metrics and settings of. |
| `include` | query | array of string |  |  | By default, this endpoint only returns the most relevant information about a user.  You can include additio... |

**Responses:**

- `200`: The request was successful. — any (see schema)
- `4XX`: 

---

### `GET /usergroups` [D]

Get a list of all user groups that match a filter.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of UserGroupInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /usergroups/{id}` [D]

Return information about a user group.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the user group that you want to get information for. |

**Responses:**

- `200`: The request was successful. — UserGroupInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /users` [D]

Returns a list of all user accounts.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of UserInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /users/api-keys/find`

Returns details of an API key.

**Request body** (application/json): FindAPIKeyRequestBody

**Responses:**

- `200`: The API key was found. — APIKeyInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `PATCH /users/api-keys/{id}`

Edits an API key.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the API key that you want to edit. |

**Request body** (application/json): ModifyAPIKeyRequestBody

**Responses:**

- `204`: The API key was edited.
- `4XX`: 
- `5XX`: 

---

### `DELETE /users/api-keys/{id}`

Deletes an API key.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the API key that you want to delete. |

**Responses:**

- `204`: The API key was deleted.
- `4XX`: 
- `5XX`: 

---

### `POST /users/pause`

Pauses all user accounts that match a filter.

**Request body** (application/json): MultiUserPauseRequest

**Responses:**

- `200`: The request to pause all user accounts that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /users/request-password`

Triggers the password reset process for a user account.

**Request body** (application/json): TriggerPasswordResetRequest

**Responses:**

- `204`: The request to trigger the password reset process was successful.
- `4XX`: Client Errors
- `5XX`: 

---

### `POST /users/reset-password`

Set a new password for a user account with the token from the password reset process.

**Request body** (application/json): ResetPasswordRequest

**Responses:**

- `204`: The password was changed.
- `400`: 
- `5XX`: 

---

### `POST /users/resume`

Resumes all user accounts that match a filter.

**Request body** (application/json): MultiResumeRequestBody

**Responses:**

- `200`: The request to resume all user accounts that match the filter was successful. See the response for possible error messages. — array of ActionResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /users/{id}` [D]

Returns information about a user account.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the user account for which you want to get information. |

**Responses:**

- `200`: The request was successful. — UserInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /users/{id}/api-keys`

Returns a list of API keys that belong to a user account.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the user that you want to get a list of API keys for. Enter "me" if you want a list of your... |

**Responses:**

- `200`: The request to list the API keys of the specified user was successful. — array of APIKeyInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /users/{id}/api-keys`

Creates a new API key.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the user that you want to create an API key for. Enter "me" if you want to create an API ke... |

**Request body** (application/json): CreateAPIKeyRequestBody

**Responses:**

- `200`: The API Key was created. — CreateAPIKeyResponse (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /users/{id}/pause`

Pauses a user account.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the user account that you want to pause. |

**Responses:**

- `204`: The user account was paused.
- `4XX`: 
- `5XX`: 

---

### `POST /users/{id}/resume`

Resumes a user account.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the user account that you want to resume. |

**Responses:**

- `204`: The user account was resumed.
- `4XX`: 
- `5XX`: 

---

## Libraries

### `GET /libraries` [D]

Returns a list of all libraries that match a filter.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of LibraryInfo (see schema)
- `4XX`: 
- `5XX`: 

---

## Lookups

### `GET /lookup-definitions` [D]

Returns a list of lookups definitions.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of LookupDefinition (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /lookup-definitions/{id}` [D]

Returns a lookup definition.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `id` | path | string | Yes |  | Enter the ID of the lookup definition that you want to request. |

**Responses:**

- `200`: The request was successful. — LookupDefinition (see schema)
- `4XX`: 
- `5XX`: 

---

## Authentication

### `GET /session`

Renews an active user session.

**Responses:**

- `200`: The request was successful. — RenewResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `POST /session`

Creates a new user session.

**Request body** (application/json): LoginRequest

**Responses:**

- `200`: The request was successful. — LoginResult (see schema)
- `4XX`: 
- `5XX`: 

---

### `DELETE /session`

Ends an active user session.

**Responses:**

- `204`: The user was logged out successfully.
- `4XX`: 
- `400`: 
- `5XX`: 

---

## System

### `GET /autodiscoveries`

Returns a list of all running auto-discoveries.

**Parameters:**

| Name | In | Type | Required | Default | Description |
|------|----|------|----------|---------|-------------|
| `offset` | query | integer |  | 0 | Use an offset to define which results the request returns. The index is a zero-based array, which means tha... |
| `limit` | query | integer |  | 100 | Enter the number of objects that the request returns. If you set the limit to 0 or do not enter a value, th... |
| `filter` | query | string |  |  | Define filters to filter the results. For more information, see the <a href="../overview#filter" target="_b... |
| `sort_by` | query | string |  |  | Enter a comma-separated list of settings that you want to use to sort the results. By default, the results ... |

**Responses:**

- `200`: The request was successful. — array of AutodiscoveryInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/feature-toggles` [E] [D]

Returns a list of all enabled feature-toggles.

**Responses:**

- `200`: The request was successful. — array of enum: ['EFeatureToggleSettingsV2'] (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /experimental/license` [E]

Returns PRTG license information.

**Responses:**

- `200`: The request was successful. — LicenseInfo (see schema)
- `4XX`: 
- `5XX`: 

---

### `GET /health`

Returns the status of the PRTG application server.

**Responses:**

- `204`: The PRTG application server is up and running and connected to the PRTG core server.
- `503`: The service is unavailable or the license is inactive. — Error (see schema)

---

### `GET /settings/public`

Returns a list of settings that are available for unauthenticated users.

**Responses:**

- `200`: The request was successful. — PublicSettings (see schema)

---

### `GET /version`

Returns information on the PRTG version and appserver version.

**Responses:**

- `200`: The request was successful. — Versions (see schema)
- `4XX`: 
- `5XX`: 

---
