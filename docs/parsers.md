Parsers are designed to take the incoming email notifications from carriers and parse them in to a machine readable JSON format which can then be passed to the circuit maintenance plugin API for storage and further processing. The challenge is that virtually every provider leverages their own maintenance notification format with very little uptake of industry standards, the [circuit-maintenance-parser](https://github.com/networktocode/circuit-maintenance-parser) python package was written to convert both standard based iCal notifications and non-standard HTML based notifications in to a well defined structure.

The high level process is simple, a parser leverages the  [circuit-maintenance-parser](https://github.com/networktocode/circuit-maintenance-parser) library to parse inbound notifications, passing them to the NetBox Circuit Maintenance plugin, the plugin then stores and optionally post-processes the notification (i.e. duplication detection, consolidated notifications).

The following parsers have been written and/or contributed by the community to assist in automating provider maintenance notifications:

- [AWS SNS & Lambda](parsers_sns_lambda.md)

- IMAP Netbox Script (Coming Soon)

- IMAP CRON Job (Coming Soon)