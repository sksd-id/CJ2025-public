# Latent Kingdom

Category: Cloud<br>
Difficulty: Easy<br>
Author: aseng & kangwijen<br>

## Description

CloudServe is a PaaS platform startup that hosts a static marketing site on AWS. One day their site was attacked by an attacker. Your job is to reconstruct what happened end-to-end by answering 15 investigation questions.

## Questions

1. From where did the attacker first obtain sensitive info from the public site?
   Example answer: Admin.sql

2. When was the sensitive file first accessed? (Format: YYYY-MM-DD HH:MM:SS UTC)
   Example answer: 2025-01-01 00:00:00 UTC

3. What is the CloudFront request ID for the sensitive file access?
   Example answer: 1A2B3C4D5E6F7

4. Which IAM user does the leaked access key belong to?
   Example answer: Example-User

5. What is the access key ID of the compromised IAM user?
   Example answer: AKIA1A2B3C4D5E6F7G8H

6. What AWS region was used for the attack?
   Example answer: us-east-1

7. What was the first API call made using the stolen key?
   Example answer: aws:ExampleCall

8. When did the attacker first use the stolen credentials? (Format: YYYY-MM-DD HH:MM:SS UTC)
   Example answer: 2025-01-01 00:00:00 UTC

9. Which tool was used for AWS reconnaissance?
   Example answer: example-tool

10. What is the weak IAM policy statement?
    Example answer: IAMPolicyStatement

11. Which IAM user was created for privilege escalation?
    Example answer: Example-User

12. When did the attacker first access the created backdoor user? (Format: YYYY-MM-DD HH:MM:SS UTC)
    Example answer: 2025-01-01 00:00:00 UTC

13. What is the access key ID of the backdoor user?
    Example answer: AKIA1A2B3C4D5E6F7G8H

14. What is the source IP address when the backdoor user first accessed AWS?
    Example answer: 123.123.123.123

15. Which country is the attacker located in?
    Example answer: CountryName

## Writeup

### Overview

This challenge requires analyzing AWS CloudTrail logs and S3 server access logs to reconstruct an attack timeline. The attacker discovered a leaked `.env` file, used the credentials to perform reconnaissance, and then escalated privileges by creating a backdoor IAM user.

### Investigation Steps

#### Questions 1-3: Initial Foothold (.env File Access)

**Question 1: From where did the attacker first obtain sensitive info from the public site?**

Examine the S3 server access logs, look for GET requests to sensitive files. You'll find a log entry showing:
```
REST.GET.OBJECT .env "GET /.env HTTP/1.1" 200
```
**Answer:** `.env`

**Question 2: When was the sensitive file first accessed? (Format: YYYY-MM-DD HH:MM:SS UTC)**

In the same S3 access log entry (the one showing the sensitive file access), check the timestamp field. The log format shows:
```
[07/Dec/2025:05:22:12 +0000]
```
Convert this to the required format: `2025-12-07 05:22:12 UTC`

**Question 3: What is the CloudFront request ID for the sensitive file access?**

In the same S3 access log entry, look for the CloudFront request ID field. It appears in the log as:
```
46JVQE57VA61FVNS
```
**Answer:** `46JVQE57VA61FVNS`

#### Questions 4-6: Leaked Credentials Analysis

**Question 4: Which IAM user does the leaked access key belong to?**

Examine the CloudTrail logs (`event_history.csv`). Filter for events with the leaked access key. Look at the `User name` column for events where the attacker first uses the credentials. You'll see entries with:
```
User name: cloudserve
```
**Answer:** `cloudserve`

**Question 5: What is the access key ID of the compromised IAM user?**

In the CloudTrail logs, look at the `AWS access key` column for events where `User name` matches the compromised user identified in question 4. The access key ID is:
```
AKIA453N4QOMPG2YR45P
```
**Answer:** `AKIA453N4QOMPG2YR45P`

**Question 6: What AWS region was used for the attack?**

Check the `AWS region` column in CloudTrail logs for any event involving the `cloudserve` user. All malicious events show:
```
ap-southeast-1
```
**Answer:** `ap-southeast-1`

#### Questions 7-9: Initial Reconnaissance

**Question 7: What was the first API call made using the stolen key?**

Sort the CloudTrail logs by `Event time` in ascending order, filtering for `cloudserve` user events. The first API call will be:
```
Event source: sts.amazonaws.com
Event name: GetCallerIdentity
```
**Answer:** `sts:GetCallerIdentity` or `GetCallerIdentity`

**Question 8: When did the attacker first use the stolen credentials? (Format: YYYY-MM-DD HH:MM:SS UTC)**

From the same first `GetCallerIdentity` event, extract the `Event time`:
```
2025-12-07T05:27:08Z
```
Convert to the required format: `2025-12-07 05:27:08 UTC`

**Question 9: Which tool was used for AWS reconnaissance?**

Examine the `User agent` column in CloudTrail logs. You'll see a pattern of enumeration calls with:
```
aws-sdk-go-v2/1.3.2
```
This user agent, combined with the pattern of enumeration calls across multiple AWS services, indicates the use of [aws-enumerator](https://github.com/shabarkin/aws-enumerator), a popular AWS reconnaissance tool.

**Answer:** `aws-enumerator` or `aws_enumerator`

#### Questions 10-11: Privilege Escalation

**Question 10: What is the weak IAM policy statement?**

Examine the IAM policy JSON file, look for policy statements that allow IAM user management. You'll find a statement with:
```json
{
  "Sid": "ManageCloudServeUsers",
  ...
}
```
**Answer:** `ManageCloudServeUsers`

**Question 11: Which IAM user was created for privilege escalation?**

Search the CloudTrail logs for a new user appearing. Look for events where a different user name appears after the reconnaissance phase. You'll find an event with this user name:
```
User name: cloudserve-bot
```
**Answer:** `cloudserve-bot`

#### Questions 12-15: Backdoor Access

**Question 12: When did the attacker first access the created backdoor user? (Format: YYYY-MM-DD HH:MM:SS UTC)**

In CloudTrail logs, find the first event where `User name` is `cloudserve-bot`. Check the `Event time`:
```
2025-12-07T05:45:54Z
```
Convert to required format: `2025-12-07 05:45:54 UTC`

**Question 13: What is the access key ID of the backdoor user?**

From the same first `cloudserve-bot` event, check the `AWS access key` column:
```
AKIA453N4QOMJWZXIPOB
```
**Answer:** `AKIA453N4QOMJWZXIPOB`

**Question 14: What is the source IP address when the backdoor user first accessed AWS?**

From the first `cloudserve-bot` event, check the `Source IP address` column:
```
185.184.192.247
```
**Answer:** `185.184.192.247`

**Question 15: Which country is the attacker located in?**

Use IP geolocation services such as [ipinfo.io](https://ipinfo.io) to determine the country for IP address `185.184.192.247`. The IP geolocates to:
**Answer:** `Netherlands`
