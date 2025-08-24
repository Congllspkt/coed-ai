# AWS IAM (Identity and Access Management)

AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. With IAM, you manage who is authenticated (signed in) and authorized (has permissions) to use resources.

## What is AWS IAM?

IAM allows you to:
*   **Manage Users and their credentials:** Create IAM users, manage their passwords, access keys, and MFA devices.
*   **Organize Users into Groups:** Assign permissions to a group, and all users in that group inherit those permissions.
*   **Define Permissions with Policies:** Specify what actions users, groups, or roles can perform on which AWS resources.
*   **Grant Temporary Permissions with Roles:** Delegate permissions to users or AWS services that need to access resources temporarily, without sharing long-term credentials.
*   **Enable Federation:** Allow users from an external identity system (like your corporate directory) to access AWS resources using their existing credentials.

## Core IAM Concepts

### 1. IAM Users

An IAM user represents a person or application that interacts with AWS.
*   **Root User:** The account owner, created when you first open an AWS account. It has unrestricted access and should *never* be used for daily tasks. Secure it with strong MFA.
*   **IAM User:** An entity you create in AWS to represent a person or application. It can have specific permissions.

### 2. IAM Groups

An IAM group is a collection of IAM users. You can attach an access policy to a group, and all users in the group automatically inherit the permissions specified in that policy. This simplifies managing permissions for multiple users.

### 3. IAM Roles

An IAM role is similar to an IAM user in that it is an AWS identity with permission policies that determine what the identity can do in AWS. However, a role is intended to be assumable by anyone who needs it, not associated with a specific person.
*   **Delegation:** Grant access to users, applications, or services that don't normally have access to your AWS resources.
*   **Cross-account access:** Allow users in one AWS account to access resources in another account.
*   **AWS Service Roles:** Allow AWS services (e.g., EC2, Lambda) to perform actions on your behalf (e.g., an EC2 instance accessing S3).

### 4. IAM Policies

Policies are the core of IAM. They are JSON documents that define permissions. Policies specify:
*   **Effect:** `Allow` or `Deny` (Deny always overrides Allow).
*   **Action:** The specific API calls or actions that can be performed (e.g., `s3:GetObject`, `ec2:RunInstances`).
*   **Resource:** The AWS resources on which the actions can be performed (e.g., `arn:aws:s3:::my-bucket/*`).
*   **Principal:** The identity that is allowed or denied access (not always present in identity-based policies).
*   **Condition (Optional):** Criteria that must be met for the policy to take effect (e.g., only from a specific IP address, or within a certain time frame).

**Types of Policies:**
*   **Identity-based policies:** Attached to IAM users, groups, or roles. They define what that identity can do.
*   **Resource-based policies:** Attached directly to an AWS resource (e.g., S3 bucket policies, SQS queue policies). They specify who has access to that resource and what actions they can perform.
*   **AWS Managed Policies:** Predefined policies created and managed by AWS (e.g., `AmazonS3ReadOnlyAccess`).
*   **Customer Managed Policies:** Policies you create and manage in your AWS account.
*   **Inline Policies:** Policies embedded directly into a single IAM user, group, or role. They are deleted if the identity is deleted.

### 5. Multi-Factor Authentication (MFA)

MFA adds an extra layer of security on top of your username and password. With MFA enabled, when a user signs in to an AWS website, they provide their credentials and then a response from their MFA device.

## IAM Best Practices

*   **Principle of Least Privilege:** Grant only the permissions required to perform a task.
*   **Lock away your AWS account root user credentials:** Do not use the root user for daily tasks.
*   **Enable MFA for all users:** Especially for the root user and privileged IAM users.
*   **Use IAM roles for applications and AWS services:** Never embed AWS credentials directly in your code.
*   **Use IAM groups to assign permissions to users:** This simplifies management.
*   **Regularly review your IAM policies:** Ensure they are still appropriate.
*   **Remove unused credentials:** Delete unused IAM users, roles, and access keys.
*   **Monitor activity in AWS CloudTrail:** Log and continuously monitor activity in your AWS account.

---

## IAM Examples (with Input/Output)

These examples will primarily use the AWS CLI for demonstration, as it provides clear input/output.

### Example 1: Creating an IAM User with Console and Programmatic Access, and adding to a Group

Let's create an IAM user named `dev-user-01` who can log in to the AWS Management Console and also has programmatic access (via access keys). We'll also create a `Developers` group and add the user to it.

#### Step 1: Create an IAM User

**Input (AWS CLI):**

```bash
# Create the user
aws iam create-user --user-name dev-user-01

# Create a login profile (password for console access)
# IMPORTANT: Replace 'MySecurePassword123!' with a strong, unique password.
# For production, consider using --password-reset-required
aws iam create-login-profile --user-name dev-user-01 --password 'MySecurePassword123!' --no-password-reset-required

# Create access keys (for programmatic access)
aws iam create-access-key --user-name dev-user-01
```

**Output (AWS CLI):**

```json
# Output from aws iam create-user
{
    "User": {
        "Path": "/",
        "UserName": "dev-user-01",
        "UserId": "AIDACKCKCKC7V6Q2C66",
        "Arn": "arn:aws:iam::123456789012:user/dev-user-01",
        "CreateDate": "2023-10-27T10:00:00Z"
    }
}

# Output from aws iam create-login-profile (no explicit output for success)
# (If error, it will show here)

# Output from aws iam create-access-key
{
    "AccessKey": {
        "UserName": "dev-user-01",
        "Status": "Active",
        "CreateDate": "2023-10-27T10:00:10Z",
        "SecretAccessKey": "YOUR_SUPER_SECRET_ACCESS_KEY_HERE", # <<< IMPORTANT: SAVE THIS!
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE" # <<< IMPORTANT: SAVE THIS!
    }
}
```
**Note:** The `SecretAccessKey` is only shown once. You *must* save it immediately. If you lose it, you'll need to create a new one.

#### Step 2: Create an IAM Group

**Input (AWS CLI):**

```bash
aws iam create-group --group-name Developers
```

**Output (AWS CLI):**

```json
{
    "Group": {
        "Path": "/",
        "GroupName": "Developers",
        "GroupId": "AGPA4M444444444444",
        "Arn": "arn:aws:iam::123456789012:group/Developers",
        "CreateDate": "2023-10-27T10:01:00Z"
    }
}
```

#### Step 3: Add the User to the Group

**Input (AWS CLI):**

```bash
aws iam add-user-to-group --group-name Developers --user-name dev-user-01
```

**Output (AWS CLI):**
(No explicit output for success, just an empty response if successful)

```
# (empty output on success)
```

### Example 2: Creating a Customer Managed Policy for S3 Read-Only Access and Attaching it to a Group

Let's create a policy that allows read-only access to all S3 buckets and then attach it to our `Developers` group.

#### Step 1: Define the Policy Document (JSON)

Create a file named `s3-read-only-policy.json`:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": "*"
        }
    ]
}
```

#### Step 2: Create the Customer Managed Policy

**Input (AWS CLI):**

```bash
aws iam create-policy --policy-name S3ReadOnlyAccessCustom --policy-document file://s3-read-only-policy.json
```

**Output (AWS CLI):**

```json
{
    "Policy": {
        "PolicyName": "S3ReadOnlyAccessCustom",
        "PolicyId": "ANPAKKKKKKK56P56P56",
        "Arn": "arn:aws:iam::123456789012:policy/S3ReadOnlyAccessCustom",
        "Path": "/",
        "DefaultVersionId": "v1",
        "AttachmentCount": 0,
        "IsAttachable": true,
        "CreateDate": "2023-10-27T10:05:00Z",
        "UpdateDate": "2023-10-27T10:05:00Z"
    }
}
```
**Note:** Make sure to save the `Arn` of the policy.

#### Step 3: Attach the Policy to the Developers Group

**Input (AWS CLI):**

```bash
aws iam attach-group-policy --group-name Developers --policy-arn arn:aws:iam::123456789012:policy/S3ReadOnlyAccessCustom
```
*(Replace `arn:aws:iam::123456789012:policy/S3ReadOnlyAccessCustom` with the actual ARN from the previous step)*

**Output (AWS CLI):**
(No explicit output for success)

```
# (empty output on success)
```

Now, `dev-user-01` (and any other user in the `Developers` group) will have read-only access to all S3 buckets.

### Example 3: Creating an IAM Role for an EC2 Instance to Access S3

EC2 instances often need to interact with other AWS services. Instead of storing access keys directly on the instance, you attach an IAM role to it. This role grants temporary credentials to the instance.

#### Step 1: Define the Trust Policy for the Role

This policy specifies *who* can assume this role. For an EC2 instance, the principal is the EC2 service itself. Create a file named `ec2-trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### Step 2: Create the IAM Role

**Input (AWS CLI):**

```bash
aws iam create-role --role-name EC2S3ReadOnlyRole --assume-role-policy-document file://ec2-trust-policy.json
```

**Output (AWS CLI):**

```json
{
    "Role": {
        "Path": "/",
        "RoleName": "EC2S3ReadOnlyRole",
        "RoleId": "AROAQ3Q3Q3Q3Q3Q3Q3",
        "Arn": "arn:aws:iam::123456789012:role/EC2S3ReadOnlyRole",
        "CreateDate": "2023-10-27T10:15:00Z",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    }
}
```
**Note:** Save the `Arn` of the role.

#### Step 3: Attach a Permissions Policy to the Role

We can attach the AWS Managed Policy `AmazonS3ReadOnlyAccess` to this role.

**Input (AWS CLI):**

```bash
aws iam attach-role-policy --role-name EC2S3ReadOnlyRole --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

**Output (AWS CLI):**
(No explicit output for success)

```
# (empty output on success)
```

#### Step 4: Create an Instance Profile (Optional, but good practice for EC2)

An instance profile is a container for an IAM role that you can use to pass role information to an EC2 instance.

**Input (AWS CLI):**

```bash
aws iam create-instance-profile --instance-profile-name EC2S3ReadOnlyProfile
aws iam add-role-to-instance-profile --instance-profile-name EC2S3ReadOnlyProfile --role-name EC2S3ReadOnlyRole
```

**Output (AWS CLI):**

```json
# Output from aws iam create-instance-profile
{
    "InstanceProfile": {
        "Path": "/",
        "InstanceProfileName": "EC2S3ReadOnlyProfile",
        "InstanceProfileId": "AIPAQ3Q3Q3Q3Q3Q3Q3",
        "Arn": "arn:aws:iam::123456789012:instance-profile/EC2S3ReadOnlyProfile",
        "CreateDate": "2023-10-27T10:20:00Z",
        "Roles": []
    }
}

# Output from aws iam add-role-to-instance-profile
# (empty output on success)
```

#### Step 5: Launch an EC2 Instance with this Role (Example)

When launching an EC2 instance, you would specify the `InstanceProfileName`.

**Input (AWS CLI - Example):**

```bash
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t2.micro \
    --count 1 \
    --iam-instance-profile Name=EC2S3ReadOnlyProfile \
    --key-name my-ec2-key \
    --security-group-ids sg-0123456789abcdef0 \
    --subnet-id subnet-0123456789abcdef0
```

**Output (AWS CLI - truncated for brevity):**

```json
{
    "Groups": [],
    "Instances": [
        {
            "AmiLaunchIndex": 0,
            "ImageId": "ami-0abcdef1234567890",
            "InstanceId": "i-0abcdef1234567890",
            "InstanceType": "t2.micro",
            "KeyName": "my-ec2-key",
            "LaunchTime": "2023-10-27T10:25:00.000Z",
            "Monitoring": {
                "State": "disabled"
            },
            "PrivateIpAddress": "172.31.X.X",
            "PublicIpAddress": "52.X.X.X",
            "State": {
                "Code": 0,
                "Name": "pending"
            },
            "IamInstanceProfile": {
                "Arn": "arn:aws:iam::123456789012:instance-profile/EC2S3ReadOnlyProfile",
                "Id": "AIPAQ3Q3Q3Q3Q3Q3Q3"
            },
            ...
        }
    ],
    "OwnerId": "123456789012",
    "ReservationId": "r-0abcdef1234567890"
}
```

Any applications running on this EC2 instance can now implicitly assume the `EC2S3ReadOnlyRole` and perform S3 read-only operations without explicit credentials.

### Example 4: Testing Permissions with `aws sts get-caller-identity` and S3 Access

Let's assume you've configured your AWS CLI with `dev-user-01`'s access keys from Example 1. `dev-user-01` is in the `Developers` group, which has `S3ReadOnlyAccessCustom` policy attached.

#### Step 1: Verify the Current IAM Identity

**Input (AWS CLI):**

```bash
aws sts get-caller-identity
```

**Output (AWS CLI):**

```json
{
    "UserId": "AIDACKCKCKC7V6Q2C66:dev-user-01",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/dev-user-01"
}
```
This confirms you are operating as `dev-user-01`.

#### Step 2: Test S3 Read Access

Assume there's an S3 bucket named `my-test-bucket-12345`.

**Input (AWS CLI):**

```bash
aws s3 ls s3://my-test-bucket-12345
```

**Output (AWS CLI - if bucket exists and user has read access):**

```
                           PRE folder1/
2023-01-01 10:30:00          100 file1.txt
2023-01-01 10:35:00          200 file2.txt
```
This shows the user can list objects in the bucket due to the `s3:List*` permission.

#### Step 3: Test S3 Write Access (Expected to Fail)

Since `dev-user-01` only has read-only access, any write operation should be denied.

**Input (AWS CLI):**

```bash
echo "This is a test file." > test.txt
aws s3 cp test.txt s3://my-test-bucket-12345/test.txt
```

**Output (AWS CLI - expected denial):**

```
upload failed: ./test.txt to s3://my-test-bucket-12345/test.txt An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
```
This demonstrates the `Deny` effect for actions not covered by the `Allow` in the policy, adhering to the principle of least privilege.

---

This detailed overview and examples should provide a solid understanding of AWS IAM and how to use its core features. Remember to always follow IAM best practices for a secure AWS environment.