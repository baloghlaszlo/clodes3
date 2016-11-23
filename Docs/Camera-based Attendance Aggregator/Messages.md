Message descriptors
===================

This document details the message formats sent to specific topics. Each message is in BSON format

image.process
-------------

- `id`: An GUID generated in the REST api entry point. From that point forward, this must serve a key across multiple database instances.
- `timestamp`: The timestamp w
