# CloDeS3 API

## Attendance
To send an attendance value by some sensor, a POST/PUT HTTP message could be sent on `https://attendance-aggregator.mybluemix.net/attendance`.
example json:
```
{
    'source':source, 'attendance':aggregated_value
}
```
where `aggregated_value` is an integer, and `source` is a string such as `'laboratory-machine-agent-aggregator'`
Note: If you are posting from the same sensor, always use same string as source.

## Reservation

To send the reservation, a POST/PUT HTTP message could be sent on
`https://clodes3-airstatus.mybluemix.net/reservation`
example json:
```

```
<!--TODO Not my job -->

## Data fusion

To send the fused data, a POST/PUT HTTP message could be sent on
`https://clodes3-airstatus.mybluemix.net/DataFusionService`
example json:
```

```
<!--TODO Not my job -->
