# AWS Elastic Container Registry (ECR)

## Introduction

AWS **Elastic Container Registry (ECR)** is a fully managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images. ECR is integrated with Amazon Elastic Container Service (ECS), Amazon Elastic Kubernetes Service (EKS), AWS Fargate, and AWS Lambda, simplifying your development to production workflow.

ECR eliminates the need to operate your own container repositories or worry about scaling the underlying infrastructure. It provides a secure, high-performance, and highly available solution for storing your container images, with support for private and public repositories.

### Why use ECR?

*   **Managed Service:** No servers to provision or manage. AWS handles the underlying infrastructure.
*   **Secure:** Integrated with AWS IAM for granular permissions, allows private repositories, and supports image scanning for vulnerabilities.
*   **Highly Available & Durable:** Images are stored in Amazon S3, providing high durability and availability.
*   **Scalable:** Automatically scales to meet your storage and throughput needs.
*   **Integrated:** Seamlessly works with other AWS services like ECS, EKS, Lambda, CodeBuild, and CodePipeline.
*   **Cost-Effective:** Pay only for the storage you use and data transfer.

## Core Concepts

1.  **Repository:** A logical grouping of Docker images. Each repository contains multiple versions (tags) of a specific container image.
2.  **Image:** A Docker container image stored within a repository. Images are immutable once pushed.
3.  **Tag:** A label attached to an image, typically used for versioning (e.g., `latest`, `v1.0`, `dev`). An image can have multiple tags.
4.  **Lifecycle Policy:** Rules that define how to manage images in a repository, such as automatically deleting old, unused, or untagged images to reduce costs and clutter.
5.  **Image Scanning:** An optional feature that helps identify software vulnerabilities in your container images. ECR uses Clair for this.

## How ECR Works

The typical workflow with ECR involves these steps:

1.  **Create a Repository:** Define a new repository in ECR where your images will be stored.
2.  **Authenticate Docker:** Get an authentication token from ECR to allow your Docker client to connect securely.
3.  **Build Docker Image:** Use your `Dockerfile` to build a Docker image locally.
4.  **Tag Docker Image:** Tag your local image with the ECR repository URI and a specific tag (e.g., `latest`).
5.  **Push Docker Image:** Push the tagged image from your local Docker client to the ECR repository.
6.  **Deploy Container:** Your deployment service (ECS, EKS, Lambda, etc.) can then pull the image from ECR to run your containers.

## Detailed Example: Pushing a Docker Image to ECR

Let's walk through an example of creating an ECR repository, building a simple Docker image, and pushing it to ECR.

### Prerequisites

Before you begin, ensure you have:

1.  **AWS Account:** With necessary permissions to manage ECR, IAM, and other services.
2.  **AWS CLI Configured:** The AWS Command Line Interface (CLI) installed and configured with your AWS credentials and a default region.
3.  **Docker Installed:** The Docker daemon and client running on your local machine.
4.  **A Sample Application (Optional):** For this example, we'll create a very simple NGINX-based web server.

### 1. Create a Sample Docker Application (Optional)

Create a directory named `my-nginx-app` and inside it, create the following files:

**`Dockerfile`**:

```dockerfile
# Use an official Nginx image as a base
FROM nginx:latest

# Remove the default Nginx index.html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy your custom index.html file to the Nginx web root
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80

# Command to run Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
```

**`nginx.conf`**:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

**`index.html`**:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My ECR App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
    <h1>Hello from My ECR Container!</h1>
    <p>This is a simple NGINX web server deployed via AWS ECR.</p>
</body>
</html>
```

### 2. Create an ECR Repository

First, you need a repository in ECR to store your Docker image.

**Input (AWS CLI):**

```bash
# Replace <YOUR_REGION> with your desired AWS region, e.g., us-east-1
aws ecr create-repository \
    --repository-name my-nginx-repo \
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability MUTABLE \
    --region <YOUR_REGION>
```

**Output (Example JSON from AWS CLI):**

```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:<YOUR_REGION>:<YOUR_ACCOUNT_ID>:repository/my-nginx-repo",
        "registryId": "<YOUR_ACCOUNT_ID>",
        "repositoryName": "my-nginx-repo",
        "repositoryUri": "<YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo",
        "createdAt": 1678886400.0,
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

**Important:** Note the `repositoryUri`. You will need this for tagging and pushing your Docker image. It follows the format: `<YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo`.

### 3. Authenticate Docker to ECR

Your Docker client needs credentials to push and pull images from your ECR repository. ECR provides a temporary authentication token.

**Input (AWS CLI):**

```bash
# Replace <YOUR_REGION> with your AWS region
aws ecr get-login-password --region <YOUR_REGION> | docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com
```

**Output (Example):**

```
Login Succeeded
```

### 4. Build Your Docker Image

Navigate to your `my-nginx-app` directory (where your `Dockerfile` is) and build your Docker image.

**Input (Bash):**

```bash
cd my-nginx-app
docker build -t my-nginx-app .
```

**Output (Example - truncated):**

```
[+] Building 4.7s (9/9) FINISHED
 => [internal] load build definition from Dockerfile                                                                        0.0s
 => => transferring dockerfile: 260B                                                                                          0.0s
 => [internal] load .dockerignore                                                                                           0.0s
 => => transferring context: 2B                                                                                               0.0s
 => [internal] load metadata for docker.io/library/nginx:latest                                                             2.1s
 => [1/5] FROM docker.io/library/nginx:latest@sha256:d8295982f6e9b4662d55986dd240c034b2203ed48e3e4cf6b889390232df6355      0.0s
 => [internal] load build context                                                                                           0.0s
 => => transferring context: 110B                                                                                             0.0s
 => [2/5] RUN rm /etc/nginx/conf.d/default.conf                                                                            0.3s
 => [3/5] COPY nginx.conf /etc/nginx/conf.d/default.conf                                                                   0.0s
 => [4/5] COPY index.html /usr/share/nginx/html/index.html                                                                  0.0s
 => [5/5] EXPOSE 80                                                                                                         0.0s
 => exporting to image                                                                                                      0.0s
 => => exporting layers                                                                                                     0.0s
 => => writing image sha256:f1234567890abcdef1234567890abcdef1234567890abcdef1234567890abc                                   0.0s
 => => naming to docker.io/library/my-nginx-app
```

You can verify the image is built locally:

**Input (Bash):**

```bash
docker images my-nginx-app
```

**Output (Example):**

```
REPOSITORY       TAG       IMAGE ID       CREATED         SIZE
my-nginx-app     latest    f1234567890a   5 seconds ago   142MB
```

### 5. Tag Your Docker Image for ECR

Before pushing, you need to tag your local image with the full ECR repository URI.

**Input (Bash):**

```bash
# Replace <YOUR_ACCOUNT_ID> and <YOUR_REGION>
docker tag my-nginx-app:latest <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo:latest
```

**Output:** No explicit output, but you can verify the new tag:

```bash
docker images
```

**Output (Example):**

```
REPOSITORY                                                 TAG       IMAGE ID       CREATED         SIZE
my-nginx-app                                               latest    f1234567890a   3 minutes ago   142MB
<YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo   latest    f1234567890a   3 minutes ago   142MB
```

### 6. Push Your Docker Image to ECR

Now push the tagged image to your ECR repository.

**Input (Bash):**

```bash
# Replace <YOUR_ACCOUNT_ID> and <YOUR_REGION>
docker push <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo:latest
```

**Output (Example - truncated):**

```
The push refers to repository [<YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo]
1a2b3c4d5e6f: Pushed
... (multiple layers pushed) ...
latest: digest: sha256:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abc size: 528
```

### 7. Verify the Image in ECR

You can verify that the image has been successfully pushed to ECR using the AWS CLI or the AWS Management Console.

**Input (AWS CLI):**

```bash
# Replace <YOUR_REGION>
aws ecr describe-images \
    --repository-name my-nginx-repo \
    --region <YOUR_REGION>
```

**Output (Example JSON):**

```json
{
    "imageDetails": [
        {
            "registryId": "<YOUR_ACCOUNT_ID>",
            "repositoryName": "my-nginx-repo",
            "imageDigest": "sha256:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abc",
            "imageTags": [
                "latest"
            ],
            "imageSizeInBytes": 149345789,
            "imagePushedAt": 1678886500.0,
            "imageScanStatus": {
                "status": "COMPLETE"
            },
            "imageScanFindingsSummary": {
                "findingSeverityCounts": {
                    "CRITICAL": 0,
                    "HIGH": 0,
                    "MEDIUM": 0,
                    "LOW": 0,
                    "UNDEFINED": 0,
                    "INFORMATIONAL": 0
                }
            }
        }
    ]
}
```

You can also navigate to the ECR service in the AWS Management Console, select your region, and find `my-nginx-repo`. You should see `latest` tag listed with details.

### 8. Pull the Docker Image from ECR (Optional)

To simulate a deployment, you can pull the image from ECR to another machine or a clean local environment.

**Input (Bash):**

```bash
# First, remove the local image to ensure you're pulling from ECR
docker rmi <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo:latest
docker rmi my-nginx-app:latest # And the original local tag

# Authenticate again if needed (or if on a different machine)
aws ecr get-login-password --region <YOUR_REGION> | docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com

# Then pull
docker pull <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo:latest
```

**Output (Example):**

```
Using default tag: latest
latest: Pulling from my-nginx-repo
... (pulling layers) ...
Digest: sha256:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abc
Status: Downloaded newer image for <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo:latest
<YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo:latest
```

### 9. Clean Up (Delete Repository)

To avoid incurring charges for stored images, delete the repository when you no longer need it.

**Input (AWS CLI):**

```bash
# Replace <YOUR_REGION>
aws ecr delete-repository \
    --repository-name my-nginx-repo \
    --force \
    --region <YOUR_REGION>
```

**Output (Example JSON):**

```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:<YOUR_REGION>:<YOUR_ACCOUNT_ID>:repository/my-nginx-repo",
        "registryId": "<YOUR_ACCOUNT_ID>",
        "repositoryName": "my-nginx-repo",
        "repositoryUri": "<YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/my-nginx-repo",
        "createdAt": 1678886400.0,
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

## Integration with Other AWS Services

ECR seamlessly integrates with various AWS services to facilitate container-based workflows:

*   **Amazon ECS/EKS/Fargate:** Directly pull images from ECR for deploying and running your containerized applications.
*   **AWS Lambda:** Use container images stored in ECR for Lambda functions, allowing larger dependencies and custom runtimes.
*   **AWS CodeBuild:** Build your Docker images and push them directly to ECR as part of your CI/CD pipeline.
*   **AWS CodePipeline:** Orchestrate your entire release process, including building images with CodeBuild, storing them in ECR, and deploying them to ECS/EKS.
*   **AWS Identity and Access Management (IAM):** Control who can access your repositories and what actions they can perform (e.g., push, pull, delete).
*   **Amazon VPC Endpoints:** Access ECR privately from your VPC without traversing the public internet.

## Best Practices

*   **IAM Policies:** Implement least privilege. Grant specific IAM users or roles only the necessary permissions (e.g., `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer` for pulling; `ecr:PutImage`, `ecr:InitiateLayerUpload` for pushing).
*   **Lifecycle Policies:** Configure lifecycle policies to automatically clean up old, untagged, or vulnerable images, saving storage costs and keeping repositories tidy.
*   **Image Scanning:** Enable image scanning on push to automatically detect software vulnerabilities in your images.
*   **Tagging Strategy:** Use clear and consistent tagging conventions (e.g., semantic versioning like `v1.0.0`, `feature-branch-name`, or Git commit SHAs).
*   **VPC Endpoints:** For applications running within a VPC, use ECR VPC endpoints to enhance security and reduce data transfer costs by keeping traffic within the AWS network.
*   **Cross-Account/Cross-Region Access:** If needed, configure repository policies to allow access from other AWS accounts or replicate images across regions for disaster recovery or global deployments.
*   **Security Best Practices:** Regularly update your base images, minimize image size, and avoid storing sensitive information directly in images.

## Conclusion

AWS ECR is a fundamental service for anyone building and deploying containerized applications on AWS. It simplifies the management of Docker images, providing a secure, scalable, and highly available registry that integrates seamlessly with the broader AWS ecosystem. By leveraging ECR, developers can focus on writing code rather than managing infrastructure for their container images, accelerating their journey from development to production.