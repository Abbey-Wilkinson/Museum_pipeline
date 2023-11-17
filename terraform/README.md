# Terraform

Definition of infrastructure required by the project.

## How Terraform works

- You define the **provider** of your cloud resources
- You `init` to tell Terraform to do the background things
- You define a set of resource in `.tf` files
- You provide all the details those resources need to be created
- You `apply` the plan to create them
- You `destory` to automatically remove them

## Required installations

- Terraform (`brew install terraform`)
- [AWS CLI] (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## Project resources

- Run on AWS
- **Postgres Database**
- Credentials
- Publicly available
- **Security group**