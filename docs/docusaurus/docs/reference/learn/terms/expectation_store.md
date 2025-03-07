---
title: "Expectation Store"
---

import TechnicalTag from '@site/docs/reference/learn/term_tags/_tag.mdx';

An Expectation Store is a connector to store and retrieve information about collections of verifiable assertions about data.

Expectation Stores allow you to store and retrieve <TechnicalTag relative="../" tag="expectation_suite" text="Expectation Suites" />.  These Stores can be accessed and configured through the <TechnicalTag relative="../" tag="data_context" text="Data Context" />, but entries are added to them when you save an Expectation Suite (typically through a convenience method available from your Data Context).  A configured Expectation Store is required in order to work with Great Expectations.  A local configuration for an Expectation Store will be added automatically to `great_expectations.yml` when you initialize your Data Context for the first time.

Generally speaking, while working with Great Expectations to <TechnicalTag relative="../" tag="validation" text="Validate" /> data you will not need to interact with an Expectation Store directly outside configuring the <TechnicalTag relative="../" tag="store" text="Store" />.  Instead, your Data Context will use an Expectation Store to store and retrieve Expectation Suites behind the scenes, and the objects you will directly work with will be those suites.

## Relationship to other objects

Expectation Stores can be used to store and retrieve Expectation Suites.  This means that Expectation Stores may also come into play when working with <TechnicalTag relative="../" tag="checkpoint" text="Checkpoints" /> and <TechnicalTag relative="../" tag="validator" text="Validators" />, which can take Expectation Suites as input (rather than having a set Expectation Suite pre-defined in their configuration).

## Use cases

When you initialize your Data Context for the first time, a configuration for a local Expectation Store will automatically be added to `great_expectations.yml`. You may change this configuration to work with different environments. 

- For more information on configuring an Expectation Store for a specific environment, see [Configure Expectation Stores](/docs/oss/guides/setup/configuring_metadata_stores/configure_expectation_stores).

Most workflows for creating Expectations automatically bundle them into an Expectation Suite.  When you save the resultant Expectation Suite, your Data Context will use an Expectation Store to do so.  Likewise, to edit an existing Expectation Suite, you will use your Data Context to retrieve it through an Expectation Store.  This process is available through a convenience method in the Data Context, so you will not have to directly instantiate and interact with the Expectation Store.

When Validating Data it is possible to have Checkpoints configured to require an Expectation Suite as a parameter, or to have an Expectation Suite pre-defined in the Checkpoint's configuration.  In either case, your Expectation Store will be used behind the scenes to retrieve the Expectation Suite in question (unless you are providing an Expectation Suite that still exists in memory from the Create Expectations step).

## Access

You will not typically need direct access to your Expectation Store.  Instead, your Data Context will use your Expectation Store behind the scenes when storing or retrieving Expectation Suites.  Most of your direct interaction with the Expectation Store will take place during Setup, if you have need to configure your Expectation Store beyond the default that is provided when you initialize your Data Context.  The rest of the time you will most likely use convenience methods in your Data Context to retrieve Expectation Suites, and the `save_expectation_suite` method of a Validator to save newly created Expectation Suites.  Both of these methods will make use of your Expectation Store behind the scenes.

## Configure

To configure an Expectation Store, see [Configure Expectation Stores](/docs/oss/guides/setup/configuring_metadata_stores/configure_expectation_stores).
