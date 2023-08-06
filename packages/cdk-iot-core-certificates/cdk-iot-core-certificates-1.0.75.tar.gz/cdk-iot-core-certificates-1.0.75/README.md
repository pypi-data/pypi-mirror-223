# CDK IoT Core Certificates

[![Source](https://img.shields.io/badge/Source-GitHub-blue?logo=github)](https://github.com/devops-at-home/cdk-iot-core-certificates)
[![Release](https://github.com/devops-at-home/cdk-iot-core-certificates/workflows/Release/badge.svg)](https://github.com/devops-at-home/cdk-iot-core-certificates/actions/workflows/release.yml)
[![GitHub](https://img.shields.io/github/license/devops-at-home/cdk-iot-core-certificates)](https://github.com/devops-at-home/cdk-iot-core-certificates/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/awscdk.io-cdk--iot--core--certificates-orange)](https://awscdk.io/packages/cdk-iot-core-certificates@0.0.4/#/)

[![npm package](https://img.shields.io/npm/v/cdk-iot-core-certificates?color=brightgreen)](https://www.npmjs.com/package/cdk-iot-core-certificates)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
[![npm downloads](https://img.shields.io/npm/dt/cdk-iot-core-certificates?label=npm&color=blueviolet)](https://www.npmjs.com/package/cdk-iot-core-certificates)

[AWS CDK](https://aws.amazon.com/cdk/) L3 construct for managing certificates for [AWS IoT Core](https://aws.amazon.com/iot-core/)

CloudFormation doesn't directly support creation of certificates for AWS IoT Core. This construct provides an easy interface for creating certificates through a [custom CloudFormation resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html). The private key is stored in [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html).

## Installation

This package has peer dependencies, which need to be installed along in the expected version.

For TypeScript/NodeJS, add these to your `dependencies` in `package.json`:

* cdk-iot-core-certificates

## Usage

```python
import { ThingWithCert } from 'cdk-iot-core-certificates';

// Creates new AWS IoT Thing called thingName
// Saves certs to /devices/thingName/certPem and /devices/thingName/privKey
// thingName and paramPrefix cannot start with '/'
const { thingArn, certId, certPem, privKey } = new ThingWithCert(this, 'ThingWithCert', {
    thingName: 'integrationTest',
    saveToParamStore: true,
    paramPrefix: 'devices',
});

new CfnOutput(this, 'Output-ThingArn', {
    value: thingArn,
});

new CfnOutput(this, 'Output-CertId', {
    value: certId,
});

new CfnOutput(this, 'Output-CertPem', {
    value: certPem,
});

new CfnOutput(this, 'Output-PrivKey', {
    value: privKey,
});
```
