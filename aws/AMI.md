# AMI (Amazon Machine Image) in AWS

An Amazon Machine Image (AMI) is a special type of virtual appliance image that is used to create a virtual machine within the Amazon Elastic Compute Cloud (EC2). It serves as a fundamental building block for deploying EC2 instances.

Think of an AMI as a **template** for your EC2 instances. It contains all the information required to launch an instance, including:

1.  **A template for the root volume:** This includes the operating system (OS), application server, and applications.
2.  **Launch permissions:** These control which AWS accounts can use the AMI to launch instances.
3.  **Block device mapping:** This specifies the volumes to attach to the instance when it's launched, including the root volume and any additional data volumes, and how they are mounted.

## Why Use AMIs? (Benefits and Use Cases)

*   **Consistency:** All instances launched from the same AMI will be identical, ensuring a consistent environment across your fleet.
*   **Faster Deployment:** Instead of installing the OS, applications, and configurations every time you launch an instance, you use a pre-built AMI, significantly speeding up the launch process.
*   **Scalability:** When your application needs to scale, you can quickly launch multiple identical instances from a well-tested AMI.
*   **Disaster Recovery/Backup:** You can create AMIs of your running instances, effectively backing up their state. In case of failure, you can launch new instances from these AMIs.
*   **Customization:** You can create custom AMIs tailored to your specific application requirements, pre-installing all necessary software, libraries, and configurations.
*   **Version Control:** AMIs can be versioned, allowing you to roll back to previous stable configurations if issues arise with a newer version.
*   **Security Baselines:** Establish and enforce security baselines by building AMIs with specific hardening, patches, and security agents pre-installed.

## Types of AMIs

1.  **AWS-Provided AMIs (Public AMIs):**
    *   Maintained by AWS.
    *   Include various operating systems like Amazon Linux, Ubuntu, Windows Server, Red Hat Enterprise Linux, SUSE Linux, etc.
    *   Free to use (you only pay for the EC2 instance).

2.  **AWS Marketplace AMIs:**
    *   Provided by third-party vendors.
    *   Often include pre-installed software, databases, or specialized tools (e.g., FortiGate firewall, WordPress stack).
    *   May incur additional software licensing costs on top of the EC2 instance cost.

3.  **Custom AMIs:**
    *   You create these from your own EC2 instances.
    *   They are private by default and only visible to your AWS account.
    *   Can be shared with specific AWS accounts or made public (though making AMIs public should be done with caution).

4.  **Shared AMIs:**
    *   Custom AMIs that have been explicitly shared by other AWS accounts.
    *   While useful, always exercise caution when using shared AMIs from unknown sources, as they could pose security risks.

## Creating a Custom AMI

A common use case is to configure an EC2 instance with all your desired software, settings, and data, and then create an AMI from it. This allows you to launch exact replicas of that instance in the future.

### Example 1: Creating an AMI from an Existing EC2 Instance (AWS Console)

**Input (Steps):**

1.  **Launch an EC2 Instance:** If you don't have one already, launch an EC2 instance (e.g., Amazon Linux 2023).
2.  **Configure the Instance:** Connect to the instance and install your desired software. For example, let's install Apache HTTP Server:
    ```bash
    sudo yum update -y
    sudo yum install -y httpd
    sudo systemctl start httpd
    sudo systemctl enable httpd
    echo "<h1>Hello from My Custom AMI!</h1>" | sudo tee /var/www/html/index.html
    ```
3.  **Go to EC2 Dashboard:** Navigate to the EC2 service in the AWS Management Console.
4.  **Select the Instance:** In the "Instances" section, select the running EC2 instance you just configured.
5.  **Create Image:** Click on "Actions" -> "Image and templates" -> "Create image".
6.  **Configure Image:**
    *   **Image name:** `MyWebServerAMI`
    *   **Image description:** `Custom AMI with Apache web server installed`
    *   **No reboot:** (Optional, but recommended for production to ensure data consistency. If you choose "No reboot", the instance might be briefly paused or experience I/O quiescence, which can still affect services). For this example, let's leave it unchecked (meaning it *will* reboot to ensure data integrity).
    *   **Instance volumes:** Review the attached volumes. You can add more or modify existing ones if needed.
    *   **Tags:** (Optional) Add tags like `Name: MyWebServerAMI`.
7.  **Create Image:** Click the "Create image" button.

**Output (Console & Observation):**

*   You will see a notification in the console that the image creation has started.
*   The status of your EC2 instance might briefly change to "pending" or "stopping" and then "running" again if you didn't select "No reboot".
*   Navigate to "AMIs" under "Images" in the left navigation pane. You will see your new AMI listed with a status of "pending" and then "available" once the creation process (which includes taking EBS snapshots) is complete. This usually takes a few minutes, depending on the size of the root volume.

    ```
    # Example AMI List Entry in Console
    Image ID        Name                Status      Platform details    Creation date       Public
    ami-0abcdef1234567890 MyWebServerAMI    available   Linux/UNIX          2023-10-27T10:30:00.000Z no
    ```

### Example 2: Creating an AMI (AWS CLI)

**Input (Command):**

First, ensure you have the AWS CLI installed and configured.
Let's assume your running EC2 instance ID is `i-0123456789abcdef0`.

```bash
aws ec2 create-image \
    --instance-id i-0123456789abcdef0 \
    --name "MyWebServerAMICLI" \
    --description "Custom AMI with Apache web server installed via CLI" \
    --no-reboot
```

*   `--instance-id`: The ID of the EC2 instance from which to create the AMI.
*   `--name`: A name for your new AMI.
*   `--description`: A brief description of the AMI.
*   `--no-reboot`: Specifies that the instance should not be rebooted during AMI creation. Use with caution, as it might lead to data inconsistencies if the instance is writing data. Removing this flag will cause the instance to reboot.

**Output (CLI - JSON):**

```json
{
    "ImageId": "ami-0abcdef1234567890",
    "Description": "Custom AMI with Apache web server installed via CLI",
    "BlockDeviceMappings": [
        {
            "DeviceName": "/dev/xvda",
            "Ebs": {
                "DeleteOnTermination": true,
                "SnapshotId": "snap-0fedcba9876543210",
                "VolumeSize": 8,
                "VolumeType": "gp2"
            }
        }
    ],
    "CreationDate": "2023-10-27T10:30:00.000Z",
    "ImageLocation": "123456789012/MyWebServerAMICLI",
    "ImageOwnerAlias": "amazon",
    "ImageType": "machine",
    "Name": "MyWebServerAMICLI",
    "OwnerId": "123456789012",
    "ProductCodes": [],
    "Public": false,
    "RootDeviceName": "/dev/xvda",
    "RunnerOn": "i-0123456789abcdef0",
    "State": "pending",
    "StateReason": {
        "Code": "pending",
        "Message": "ami-0abcdef1234567890 is pending"
    },
    "Tags": [],
    "VirtualizationType": "hvm"
}
```

You can then monitor the state of the AMI using:

```bash
aws ec2 describe-images --image-ids ami-0abcdef1234567890
```

The `State` will change from `pending` to `available` once the AMI is ready.

## Launching an Instance from an AMI

Once you have an AMI (either AWS-provided, Marketplace, or custom), you can use it to launch new EC2 instances.

### Example 1: Launching an Instance (AWS Console)

**Input (Steps):**

1.  **Go to EC2 Dashboard:** Navigate to the EC2 service in the AWS Management Console.
2.  **Launch Instances:** Click the "Launch instances" button.
3.  **Name and tags:** Give your instance a name, e.g., `WebServerInstance-1`.
4.  **Application and OS Images (AMI):**
    *   Under "My AMIs", select the `MyWebServerAMI` you created earlier (or choose an AWS AMI like Amazon Linux).
5.  **Instance type:** Select an appropriate instance type (e.g., `t2.micro` or `t3.micro`).
6.  **Key pair (login):** Choose an existing key pair or create a new one to connect to your instance.
7.  **Network settings:**
    *   Select your VPC and subnet.
    *   Create a new security group or select an existing one. Ensure it allows inbound HTTP (port 80) and SSH (port 22) traffic from your IP or anywhere (for testing).
8.  **Configure storage:** Review the default storage, which comes from the AMI.
9.  **Launch instance:** Click the "Launch instance" button.

**Output (Console & Observation):**

*   You'll see a success message and can navigate to the "Instances" section.
*   Your new instance (`WebServerInstance-1`) will appear, initially in a "pending" state, then transition to "running".
*   Once running, you can copy its Public IP address or Public DNS.
*   **Verification:** Open a web browser and navigate to the Public IP address of the new instance. You should see:
    ```
    Hello from My Custom AMI!
    ```

### Example 2: Launching an Instance (AWS CLI)

**Input (Command):**

Replace `ami-0abcdef1234567890` with your actual AMI ID, `your-key-pair-name` with your key pair, and `sg-0abcdef1234567890` with your security group ID (or name if using `--security-groups`).

```bash
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t2.micro \
    --count 1 \
    --key-name your-key-pair-name \
    --security-group-ids sg-0abcdef1234567890 \
    --subnet-id subnet-0fedcba9876543210 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WebServerInstance-CLI}]' \
    --associate-public-ip-address
```

*   `--image-id`: The ID of the AMI to use.
*   `--instance-type`: The type of instance to launch (e.g., `t2.micro`).
*   `--count`: The number of instances to launch.
*   `--key-name`: The name of the key pair for SSH access.
*   `--security-group-ids`: The ID(s) of the security group(s) to apply.
*   `--subnet-id`: The ID of the subnet where the instance will be launched.
*   `--tag-specifications`: To add tags to your instance.
*   `--associate-public-ip-address`: To assign a public IP address to the instance.

**Output (CLI - JSON):**

```json
{
    "Groups": [],
    "Instances": [
        {
            "AmiLaunchIndex": 0,
            "ImageId": "ami-0abcdef1234567890",
            "InstanceId": "i-0fedcba9876543210",
            "InstanceType": "t2.micro",
            "KernelId": null,
            "KeyName": "your-key-pair-name",
            "LaunchTime": "2023-10-27T11:00:00.000Z",
            "Monitoring": {
                "State": "disabled"
            },
            "Placement": {
                "AvailabilityZone": "us-east-1a",
                "GroupName": "",
                "Tenancy": "default"
            },
            "PlatformDetails": "Linux/UNIX",
            "PrivateDnsName": "ip-172-31-xx-xx.ec2.internal",
            "PrivateIpAddress": "172.31.xx.xx",
            "ProductCodes": [],
            "PublicDnsName": "ec2-3-xxx-xxx-xxx.compute-1.amazonaws.com",
            "PublicIpAddress": "3.xxx.xxx.xxx",
            "RootDeviceName": "/dev/xvda",
            "RootDeviceType": "ebs",
            "SecurityGroups": [
                {
                    "GroupName": "launch-wizard-1",
                    "GroupId": "sg-0abcdef1234567890"
                }
            ],
            "SourceDestCheck": true,
            "State": {
                "Code": 0,
                "Name": "pending"
            },
            "StateTransitionReason": "",
            "SubnetId": "subnet-0fedcba9876543210",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "WebServerInstance-CLI"
                }
            ],
            "VirtualizationType": "hvm"
        }
    ],
    "OwnerId": "123456789012",
    "ReservationId": "r-0123456789abcdef0"
}
```

You can then get the public IP and verify Apache:

```bash
# Get public IP
aws ec2 describe-instances --instance-ids i-0fedcba9876543210 --query "Reservations[0].Instances[0].PublicIpAddress" --output text

# Curl the IP (replace with actual IP)
curl http://3.xxx.xxx.xxx
```

Expected output for `curl`:
```
<h1>Hello from My Custom AMI!</h1>
```

## Managing AMIs

*   **Viewing AMIs:** In the EC2 console, go to "AMIs" under "Images". You can filter by "Owned by me", "Public images", or "Private images".
*   **Copying AMIs:** You can copy an AMI to a different AWS region. This is useful for multi-region deployments or disaster recovery strategies.
    ```bash
    aws ec2 copy-image \
        --source-image-id ami-0abcdef1234567890 \
        --source-region us-east-1 \
        --name "MyWebServerAMI-eu-west-1" \
        --description "Copied AMI to EU (Ireland) region" \
        --destination-region eu-west-1
    ```
*   **Modifying Permissions:** You can share your custom AMIs with other AWS accounts or make them public.
    ```bash
    # To share with another account (e.g., 987654321098)
    aws ec2 modify-image-attribute \
        --image-id ami-0abcdef1234567890 \
        --launch-permission "Add=[{UserId=987654321098}]"

    # To make public (use with extreme caution!)
    aws ec2 modify-image-attribute \
        --image-id ami-0abcdef1234567890 \
        --launch-permission "Add=[{Group=all}]"
    ```
*   **Deregistering AMIs:** When an AMI is no longer needed, you can deregister it. **Important:** Deregistering an AMI does *not* automatically delete the associated EBS snapshots. You must manually delete the snapshots to stop incurring storage costs.
    ```bash
    # Deregister the AMI
    aws ec2 deregister-image --image-id ami-0abcdef1234567890

    # List associated snapshots (you'll need to find the snapshot IDs from the AMI details)
    # This isn't directly linked by deregister-image, you need to know the snapshot from when it was created.
    # When you create an AMI, it tells you the snapshot ID.
    # To find snapshots associated with an AMI that was just deregistered,
    # you'd typically need to have recorded the snapshot ID when the AMI was created,
    # or you can infer them by creation date and volume size if you have a unique setup.
    # Assuming you knew the snapshot ID from the 'create-image' output:
    # aws ec2 delete-snapshot --snapshot-id snap-0fedcba9876543210
    ```

## Best Practices

*   **Keep AMIs Updated:** Regularly update your custom AMIs with the latest OS patches, security updates, and application versions. Consider using AWS EC2 Image Builder for automated AMI pipelines.
*   **Deregister Unused AMIs:** Clean up old or unused AMIs to prevent clutter. Remember to delete the underlying EBS snapshots as well to save costs.
*   **Tagging:** Use tags for better organization, cost allocation, and automation.
*   **Security:**
    *   Never share private AMIs with untrusted accounts.
    *   Be cautious when using public or shared AMIs.
    *   Ensure your AMIs adhere to your organization's security policies.
*   **Automation:** Automate AMI creation and testing processes using tools like AWS EC2 Image Builder, Packer, or custom scripts.
*   **Least Privilege:** When sharing AMIs, grant launch permissions only to necessary AWS accounts.

AMIs are a powerful feature of AWS EC2, enabling efficient, consistent, and scalable deployment of your applications. Understanding how to create, manage, and launch instances from them is fundamental to operating effectively in AWS.