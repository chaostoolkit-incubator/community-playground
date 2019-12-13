# Google Cloud Function: hour-in-range

This is intended to be used as a Google Cloud Function. Google Cloud Functions is a serverless execution environment for building and connecting cloud services, see this quickstart for all the steps required to write and deploy one in python [Quickstart Python Cloud Functions][1].

In this case the function accepts two parameters lower and upper which are treated as integer values that represent a lower bound and upper bound check for the current hour. If the hour is within those bounds the response from the function will be:

```javascript
{status: ok}
```

If the current hour is outside those bounds the response from the function will be:

```javascript
{status: ko}
```

## Deploying as a Google Cloud Function

Details on deploying Cloud functions can be seen here [Deploying Cloud Functions][2], but in summary if you are deplyoing from local files using the Gcloud command as follows:

```bash
gcloud functions deploy hour-in-range --runtime python37 --trigger-http
```

[1]: https://cloud.google.com/functions/docs/quickstart-python
[2]: https://cloud.google.com/functions/docs/deploying/
