# ZX-Ventures LA e-Stores Team Backend Challenge

## Context
We are opening a new beer subscription system. We already have an e-commerce platform, so our system will need to integrate with that, since all the customer, pricing and inventory information is already there. As we are still testing the business model, it is required that part of the system is operated manually. Other parts, that won't require frequent changes will be operated directly in the database, such as managing the clubs in which our customers can subscribe. The system will also receive new subscriptions from users that access our website page. Your task will be to implement any integration between front-end and third-party systems. The project was already started by another developer and the data model has been approved. You will take on the previous developer work and complete it.

## Requirements & Scope
The subscription system is modeled as a Serverless HTTP API, providing endpoints that will make its operation possible. Your task will be to implement the minimal features of the system by writing the missing functions that will act as endpoints. Among the required endpoints there are:
* **POST** `/club/{id}/subscribe/` - responsible for receiving new subscriptions to *ACTIVE* clubs stored in its database. A customer may not subscribe more than once per club. These subscriptions will come from the frontend and will have the following payload:
    ```JSON
    {
        "customer_id":"00000000-0000-0000-000-0000000000000"
    }
    ```
* **POST** `/subscription/{id}/status/` - responsible for subscription management to support subscription PAUSE, CANCEL and ACTIVATE actions. The frontend will send a payload the the following format:
    ```JSON
    {
        "status_id":1
    }
    ```
    *This method is already implemented and should not be modified.*
* **GET** `/subscription/eligible` - should return all eligible subscriptions for charging and dispatching orders. A subscriptions is eligible if it is currently in the *ACTIVE* state and in a club that is currently in either *ACTIVE* or *CLOSED* state. IT must return the payload with a list of eligible subscription ids, such as:
    ```JSON
    [
        "00000000-0000-0000-000-0000000000000",
        "00000000-0000-0000-000-0000000000001",
        "00000000-0000-0000-000-0000000000002",
        "00000000-0000-0000-000-0000000000003",
    ]
    ```
* **POST** `/subscription/{id}/charge/{request_id}` - Will act as a proxy. It will receive a subscription ID and it should send a *POST* request to our third-party e-commerce platform so it will generate the order, charge and dispatch it to our customer. The call to be sent to the e-commerce platform is as follows:

    **POST:** `https://emporiodev.com/la-estores-hiring-deploy/assessment/ecomm-mock/order/{request_id}`

    **PAYLOAD:**
    ```JSON
    {
        "customer_id":"00000000-0000-0000-000-0000000000000",
        "sku_id":1
    }
    ```
    **HEADERS:**
    ```JSON
    {
        "x-api-key":"your-repo-url",
        "x-api-secret":"the-password-provided-by-our-evaluation-platform"
    }
    ```
    This function should be idempotent, meaning that if it receives a charge request for a subscription that has already been charged this month, it should not call out the e-commerce platform. However, for the base scenario, idempotence is not a requirement and will be seen as extra feature.
## Delivery
You should receive an invite from our evaluation system. You will receive access to our platform in which you'll be able to deploy and run the preset test suite. You repository must remain public so the platform can build and deploy it.

**You must not fork this repo!** Clone it and set the remote to a repository in your git account so you can develop on top of it.

## Other considerations
* Our evaluation system will have access to the database deployed through your code. **Do not change the current entities** already in the repository. You can add entities and features as much as you like, just bear in mind that the automatic correction will manipulate the data within the database in order to run the test scenarios. Depending on the database constraints you set, the test cases might fail.
* In order to deploy your functions you'll have to complete the [functions.yml](./functions.yml) file. It follows the standards of the [Serverless Framework](https://serverless.com/framework/docs/providers/aws/guide/functions/) yml configuration file's *functions* section
* This repository uses [Alembic Migrations](https://alembic.sqlalchemy.org/en/latest/tutorial.html). It was developed with [PostgreSQL](https://www.postgresql.org/), but it should work with any database supported by Alembic. To run migrations, you'll need to copy the [model_config.json](./model_config.json) to a `<scope>_config.json` file and edit it with your database credentials. To run migrations, use the command `alembic -x scope=<scope> upgrade head`

## Evaluation
The evaluation is taken through two steps, the self-service step and the review step. You'll receive an invite to our evaluation platform, where you'll be able to run our preset tests. If your project manages to meet the minimum requirements for the position you've applied to, it will be evaluated by our engineering team. We will be looking for:

* Performance
* Testing
* Maintainability
* Separation of concerns
* Adherence to project standards
* Enhancements to the project
* Documentation

## Support:
Should you need any assistance, please reach out to your recruiter and ask to get in touch with us!
