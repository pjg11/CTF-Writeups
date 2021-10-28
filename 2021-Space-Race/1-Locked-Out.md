![](images/1-header.png)
# TEASER: Locked out
### beginner | cloud | 50 points
<br/>

## Challenge Information
After a relaxing space walk, you realize that you have been locked out of your spaceship by the spaceship's AI. Thankfully, you remember that you prepared for this eventuality by storing access keys in an external storage.
<br/><br />

## Sub-Challenges
### [25 points] Obtaining external access keys
Open the external storage and see if there's something useful in there.

### Solution

The link to the external storage leads to `https://external-spaceship-storage-b38e8c6.s3-eu-west-1.amazonaws.com`, an AWS S3 bucket.

![](images/1-external-storage.png)

There is an item called `external-spaceship-storage.txt`. The file can be downloaded by typing the filename in the URL, i.e., `https://external-spaceship-storage-b38e8c6.s3-eu-west-1.amazonaws.com/external-spaceship-storage.txt`.

The contents are as follows:

```
AKIAQD6AU4VDTDJRGXRE
+BAPTBu9QFX6TVSpjerFoIJiJJr1D+c210ZyKdqv
CTF{6c2c45330a85b126f551}
```

The last line is the flag for the first sub-challenge, and the rest of the information will be useful for the next sub-challenge.

Flag: `CTF{6c2c45330a85b126f551}`
<br/><br /> 


### [25 points] Checking your internal storage
You have managed to get keys. See if you can get inside and check the internal spaceship storage.

### Solution
This part took me FOREVER to figure out due to the fact that I had absolutely no clue how AWS S3 buckets work. Looking through some cloud challenges from other CTFs and the AWS docs, I figured that remaining information from `external-spaceship-storage.txt` is what helps to complete this challenge. 

```markdown
AKIAQD6AU4VDTDJRGXRE - AWS Access Key ID
+BAPTBu9QFX6TVSpjerFoIJiJJr1D+c210ZyKdqv - AWS Secret Access Key
```

From the AWS Documentation:
> AWS requires different types of security credentials depending on how you access AWS. For example, you need a user name and password to sign in to the AWS Management Console and you need access keys to make programmatic calls to AWS or to use the AWS Command Line Interface or AWS Tools for PowerShell.

So the AWS Access Key ID and Secret Access Key are credentials for an AWS account. This can be configured in the AWS CLI (Command Line Interface) to view buckets and items within those buckets associated with the account. The steps to install AWS CLI for your system can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).

Once installed, we configure AWS CLI with these credentials. Using `--profile` helps to distinguish between different credentials.
```bash
$ aws configure --profile=locked-out
AWS Access Key ID [None]: AKIAQD6AU4VDTDJRGXRE
AWS Secret Access Key [None]: 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
Default region name [None]: eu-west-1
Default output format [None]: 
```

Listing all buckets reveals an internal storage bucket, which contains a keys text file.
```bash
$ aws s3 ls --profile=locked-out
2021-06-24 19:36:05 external-spaceship-storage-b38e8c6
2021-06-24 19:35:27 internal-spaceship-storage-fdde98f
$ aws s3 ls internal-spaceship-storage-fdde98f --profile=locked-out
2021-06-24 19:35:33 25 spaceship-keys
```

Downloading and viewing the file reveals the flag for this sub challenge
```bash
$ aws s3 cp s3://internal-spaceship-storage-fdde98f/spaceship-keys . --profile=locked-out
download: s3://internal-spaceshipstoragefdde98f/spaceship-keys to ./spaceship-keys
$ cat spaceship-keys 
CTF{4ababede5580d9a22a2a}
```

Flag: `CTF{4ababede5580d9a22a2a}`
<br/><br />


